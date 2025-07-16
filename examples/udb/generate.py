import logging
import shutil
from pathlib import Path
from textwrap import dedent
from typing import List, Tuple

import pcbnew
import skidl

from kle2netlist.netlist import connect_interfaces, generate_netlist, generate_pcb
from kle2netlist.pcb_kicad import apply_template
from kle2netlist.skidl import set_skidl_search_path
from kle2netlist.utilities import get_circuit_revision

logger = logging.getLogger(__name__)


def build_edge(
    board: pcbnew.BOARD,
    width: float,
    height: float,
    *,
    position: Tuple[float, float] = (0, 0),
) -> None:
    """Draws rounded rectangle with 2mm fillets"""
    fillet = pcbnew.FromMM(2)
    corners = [
        pcbnew.VECTOR2I_MM(position[0], position[1]),
        pcbnew.VECTOR2I_MM(position[0] + width, position[1]),
        pcbnew.VECTOR2I_MM(position[0] + width, position[1] + height),
        pcbnew.VECTOR2I_MM(position[0], position[1] + height),
    ]

    def _add_line(start: pcbnew.VECTOR2I, end: pcbnew.VECTOR2I) -> None:
        segment = pcbnew.PCB_SHAPE(board)
        segment.SetShape(pcbnew.SHAPE_T_SEGMENT)
        segment.SetLayer(pcbnew.Edge_Cuts)
        segment.SetStart(start)
        segment.SetEnd(end)
        segment.SetWidth(pcbnew.FromMM(0.2))
        board.Add(segment)

    def _add_arc(start: pcbnew.VECTOR2I, center: pcbnew.VECTOR2I) -> None:
        arc = pcbnew.PCB_SHAPE(board)
        arc.SetShape(pcbnew.SHAPE_T_ARC)
        arc.SetLayer(pcbnew.Edge_Cuts)
        arc.SetStart(start)
        arc.SetCenter(center)
        angle = pcbnew.EDA_ANGLE(90, pcbnew.DEGREES_T)
        arc.SetArcAngleAndEnd(angle, False)
        arc.SetWidth(pcbnew.FromMM(0.2))
        board.Add(arc)

    r_x_offset = pcbnew.VECTOR2I(fillet, 0)
    r_y_offset = pcbnew.VECTOR2I(0, fillet)

    # top left - top right
    _add_line(corners[0] + r_x_offset, corners[1] - r_x_offset)
    # top right - bottom right
    _add_line(corners[1] + r_y_offset, corners[2] - r_y_offset)
    # bottom right - bottom left
    _add_line(corners[2] - r_x_offset, corners[3] + r_x_offset)
    # bottom left - top left
    _add_line(corners[3] - r_y_offset, corners[0] + r_y_offset)
    # top left
    _add_arc(corners[0] + r_y_offset, corners[0] + r_y_offset + r_x_offset)
    # top right
    _add_arc(corners[1] - r_x_offset, corners[1] - r_x_offset + r_y_offset)
    # bottom right
    _add_arc(corners[2] - r_y_offset, corners[2] - r_y_offset - r_x_offset)
    # bottom left
    _add_arc(corners[3] + r_x_offset, corners[3] + r_x_offset - r_y_offset)


def get_footprint(board: pcbnew.BOARD, reference: str) -> pcbnew.FOOTPRINT:
    footprint = board.FindFootprintByReference(reference)
    if footprint is None:
        msg = f"Cannot find footprint {reference}"
        raise RuntimeError(msg)
    return footprint


def place_mounting_holes(board: pcbnew.BOARD) -> None:
    # in order, clockwise, starting from top left:
    holes = ["H1", "H2", "H3", "H4"]
    # 2mm from the edges
    positions = [
        (2, 2),
        (16, 2),
        (16, 14.5),
        (2, 14.5),
    ]

    for hole_ref, position_mm in zip(holes, positions):
        hole_footprint = get_footprint(board, hole_ref)
        position = pcbnew.VECTOR2I_MM(*position_mm)
        hole_footprint.SetPosition(position)
        for p in hole_footprint.Pads():
            p.SetSizeX(pcbnew.FromMM(3.5))
        # since we are here, hide value text for mounting holes
        value_field = hole_footprint.GetFieldByName("Value")
        value_field.SetVisible(False)
        # ... and that user.comment which really annoys me
        drawings = hole_footprint.GraphicalItems()
        for d in drawings:
            if d.GetLayer() == pcbnew.Cmts_User:
                hole_footprint.RemoveNative(d)

    # on real UDB board, NPTH holes have pads only elements side (bottom in our case)
    # doesn't really matter but replicate this to match original aesthetics:
    npth_holes = ["H2", "H3", "H4"]
    for hole_ref in npth_holes:
        hole_footprint = get_footprint(board, hole_ref)
        for p in hole_footprint.Pads():
            layerset = p.GetLayerSet()
            new_set = layerset.RemoveLayer(pcbnew.F_Cu)
            new_set = layerset.RemoveLayer(pcbnew.F_Mask)
            p.SetLayerSet(new_set)


def place_jst_connector(board: pcbnew.BOARD) -> None:
    jst = get_footprint(board, "J2")
    position = jst.GetPosition()
    jst.Flip(position, False)
    jst.SetOrientationDegrees(180)
    jst.SetPosition(pcbnew.VECTOR2I_MM(9, 13.4))


def add_ground_fill(
    board: pcbnew.BOARD,
    width: float,
    height: float,
    *,
    position: Tuple[float, float] = (0, 0),
    layer: int = pcbnew.F_Cu,
) -> pcbnew.ZONE:
    corners = [
        pcbnew.VECTOR2I_MM(position[0], position[1]),
        pcbnew.VECTOR2I_MM(position[0] + width, position[1]),
        pcbnew.VECTOR2I_MM(position[0] + width, position[1] + height),
        pcbnew.VECTOR2I_MM(position[0], position[1] + height),
    ]

    zone = pcbnew.ZONE(board)

    polygon = pcbnew.VECTOR_VECTOR2I()
    for c in corners:
        polygon.append(c)
    zone.AddPolygon(polygon)
    zone.SetLayer(layer)
    gnd_netcode = board.GetNetcodeFromNetname("GND")
    zone.SetNetCode(gnd_netcode)
    zone.SetFillFlag(gnd_netcode, True)
    zone.SetLocalClearance(pcbnew.FromMM(0.2))
    zone.SetThermalReliefGap(pcbnew.FromMM(0.2))
    zone.SetThermalReliefSpokeWidth(pcbnew.FromMM(0.5))
    zone.SetPadConnection(pcbnew.ZONE_CONNECTION_THT_THERMAL)
    zone.SetMinThickness(pcbnew.FromMM(0.15))
    zone.SetZoneName("GND_ZONE")
    board.Add(zone)
    return zone


def fill_zones(board: pcbnew.BOARD, zones: List[pcbnew.ZONE]) -> None:
    filler = pcbnew.ZONE_FILLER(board)
    _zones = pcbnew.ZONES()
    for z in zones:
        print(f"append {z=}")
        _zones.append(z)
    print(f"{zones=}")
    filler.Fill(_zones)


def hide_reference(footprint: pcbnew.FOOTPRINT) -> None:
    if reference := footprint.Reference():
        reference.SetVisible(False)


def hide_labels(board: pcbnew.BOARD) -> None:
    # there is no good space for clean labels with required 1mm height
    for f in board.GetFootprints():
        hide_reference(f)


def remove_silkscreen_outlines_from_connectors(board: pcbnew.BOARD) -> None:
    # on the filght footprint modification, remove silkscreen outlines
    usb = get_footprint(board, "J1")
    jst = get_footprint(board, "J2")
    for f in [usb, jst]:
        drawings = f.GraphicalItems()
        for d in drawings:
            if d.Type() == pcbnew.PCB_SHAPE_T and d.GetLayer() in [
                pcbnew.F_SilkS,
                pcbnew.B_SilkS,
            ]:
                f.RemoveNative(d)


def add_3d_models(board: pcbnew.BOARD) -> None:
    # just for 3d preview, not really required
    usb_3dmodel = pcbnew.FP_3DMODEL()
    usb_3dmodel.m_Filename = "${KIPRJMOD}/../3dmodels/HRO-TYPE-C-31-M-12.step"
    usb_3dmodel.m_Rotation = pcbnew.VECTOR3D(-90, 0, 0)
    usb_3dmodel.m_Offset = pcbnew.VECTOR3D(-4.5, -3.7, 0)
    usb_3dmodel.m_Show = True
    usb = get_footprint(board, "J1")
    usb.Add3DModel(usb_3dmodel)

    jst_3dmodel = pcbnew.FP_3DMODEL()
    jst_3dmodel.m_Filename = "${KIPRJMOD}/../3dmodels/SM04B-SRSS-TB.step"
    jst_3dmodel.m_Rotation = pcbnew.VECTOR3D(-90, 0, 0)
    jst_3dmodel.m_Offset = pcbnew.VECTOR3D(0, 1.4, -0.3)
    jst_3dmodel.m_Show = True
    jst = get_footprint(board, "J2")
    jst.Add3DModel(jst_3dmodel)


def finish_board(pcb_path):
    board = pcbnew.LoadBoard(pcb_path)
    build_edge(board, 18, 16.5)
    place_mounting_holes(board)
    place_jst_connector(board)

    z1 = add_ground_fill(board, 20, 18.5, position=(-1, -1), layer=pcbnew.F_Cu)
    z2 = add_ground_fill(board, 22, 20.5, position=(-2, -2), layer=pcbnew.B_Cu)
    fill_zones(board, [z1, z2])

    hide_labels(board)
    remove_silkscreen_outlines_from_connectors(board)

    add_3d_models(board)

    pcbnew.Refresh()
    pcbnew.SaveBoard(pcb_path, board)


@skidl.subcircuit
def udb_not_templated_extras() -> skidl.Interface:
    """Things which are not part of usb template but are needed to
    recreate UDB board
    """
    vcc = skidl.Net.fetch("VCC")
    gnd = skidl.Net.fetch("GND")

    jst = skidl.Part(
        "Connector_Generic",
        "Conn_01x04",
        footprint="Connector_JST:JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal",
    )

    vcc += jst[1]
    gnd += jst[4]

    hole_pth = skidl.Part(
        "Mechanical",
        "MountingHole_Pad",
        footprint="MountingHole:MountingHole_2.2mm_M2_Pad_TopBottom",
    )

    gnd += hole_pth

    for _ in range(0, 3):
        # non-plated mounting holes
        skidl.Part(
            "Mechanical",
            "MountingHole",
            footprint="MountingHole:MountingHole_2.2mm_M2",
        )

    # note: footprints used for mounting holes have correct 2.2 hole size
    # but too large pad size - 4.4mm instead of 3.5mm, this will be
    # updated later when placing

    return skidl.Interface(
        usb_io_dm=jst[2],
        usb_io_dp=jst[3],
    )


def custom_design_rules(dru_file):
    # fmt: off
    rules = """\
    (version 1)
    (rule "Clearance zone to board-edge"
      (constraint edge_clearance (min 0.2mm))
      (condition "A.Type =='Zone' && A.Name =='GND_ZONE' "))
    (rule "Clearance mechanical pads to board-edge"
      (constraint edge_clearance (min 0.2mm))
      (condition "A.Pad_Type =='NPTH, mechanical' || A.memberOfFootprint('J2') || A.memberOfFootprint('H*') "))
    """
    # fmt: on
    with open(dru_file, "w") as f:
        f.write(dedent(rules))


def check_drc_report_clear(filepath: str) -> bool:
    required_checks = {
        "DRC violations": False,
        "unconnected pads": False,
        "Footprint errors": False,
    }

    try:
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                for check in required_checks:
                    if f"Found 0 {check}" in line:
                        required_checks[check] = True

        return all(required_checks.values())
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return False


def new_pcb(output_dir) -> bool:
    project_name = "udb"

    pcb_file = f"{output_dir}/{project_name}.kicad_pcb"
    netlist_file = f"{output_dir}/{project_name}.net"
    dsn_file = f"{output_dir}/{project_name}.dsn"
    dru_file = f"{output_dir}/{project_name}.kicad_dru"
    drc_path = f"{output_dir}/{project_name}-drc.log"

    custom_design_rules(dru_file)

    usb = "usb"
    usb_revision = "udb_clone"
    usb_position = "9,2.37,0"
    usb_extra_circuit = f"{usb};{usb_revision};{usb_position}"

    set_skidl_search_path()
    circuit = skidl.Circuit()
    with circuit:
        interfaces = []

        for extra_circuit in [usb_extra_circuit]:
            subcircuit, revision, _ = get_circuit_revision(extra_circuit)
            extra_interface = subcircuit.add(revision)
            interfaces.append(extra_interface)

        interfaces.append(udb_not_templated_extras())

        connect_interfaces(interfaces)
        circuit.merge_net_names()

    generate_netlist(circuit, netlist_file)

    libraries = ["/usr/share/kicad/footprints"]
    footprints = Path(f"{Path.home()}/.local/share/kicad/9.0/3rdparty/footprints")
    for path in footprints.iterdir():
        if path.is_dir():
            libraries.append(str(path))
    generate_pcb(circuit, pcb_file, extra_libraries=libraries)

    for c in [usb_extra_circuit]:
        template, revision, position = get_circuit_revision(c)
        offset = (position[0], position[1])
        angle = float(position[2])
        apply_template(
            pcb_file,
            template,
            revision,
            offset=offset,
            angle=angle,
            add_fanout_tracks=False,
        )

    finish_board(pcb_file)

    pcbnew.ExportSpecctraDSN(pcbnew.LoadBoard(pcb_file), dsn_file)
    pcbnew.WriteDRCReport(
        pcbnew.LoadBoard(pcb_file), drc_path, pcbnew.EDA_UNITS_MM, True
    )

    return check_drc_report_clear(drc_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="KiCad project generator")
    parser.add_argument("-out", required=True, help="Destination directory")
    parser.add_argument(
        "-f",
        "--force",
        required=False,
        action="store_true",
        help="Overwrite destination directory",
    )

    args = parser.parse_args()
    output_path = args.out
    output_dir = Path(output_path)
    force = args.force

    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s: %(message)s", datefmt="%H:%M:%S"
    )

    if output_dir.is_dir():
        if force:
            shutil.rmtree(output_dir)
        else:
            print(f"error: -out pointing to an existing directory: {output_dir}")
            exit(1)
    output_dir.mkdir(exist_ok=False, parents=True)

    status = new_pcb(output_dir)
    if status:
        print("PCB OK")
    else:
        print("PCB DRC violations")
        exit(1)
