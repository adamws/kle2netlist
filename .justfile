template_atmega32u4_v1 := "./atmega32u4_v1.kicad_pcb"
pcb_url := "https://raw.githubusercontent.com/ai03-2725/JP60/main/JP60.kicad_pcb"
kicad_svg_fix := semver_matches(`kicad-cli --version`, ">=9.0.0")

test:
  hatch run default:test

svg-mm-to-cm svg_file:
  sed -i -E 's/(width|height)="([0-9]*\.[0-9]*)mm"/\1="\2cm"/g' {{svg_file}}

# this was not required when using KiCad 8 but it has changed for KiCad 9:
svg-fix-area svg_file:
  inkscape --export-type="svg" --export-area-drawing -o {{svg_file}} {{svg_file}}

svg kicad_pcb:
  kicad-cli pcb export svg --exclude-drawing-sheet --page-size-mode 2 \
    -l F.Cu,B.Cu,F.Silkscreen,B.Silkscreen,Edge.Cuts \
    -o "{{without_extension(kicad_pcb)}}.svg" {{kicad_pcb}}

circuit_atmega32u4 revision:
  hatch run kicad:main \
      --layout tests/test_netlist_generation/empty.json \
      --switch-footprint "" \
      --stabilizer-footprint "" \
      --diode-footprint "" \
      --controller-circuit "atmega32u4;{{revision}}" \
      --extra-circuits "dummy_matrix;v1" \
      --netlist-output atmega32u4_{{revision}}.net \
      --pcb-output atmega32u4_{{revision}}.kicad_pcb \
      --force
  just templates-svgs atmega32u4_{{revision}}

circuit_usb revision:
  hatch run kicad:main \
      --layout tests/test_netlist_generation/empty.json \
      --switch-footprint "" \
      --stabilizer-footprint "" \
      --diode-footprint "" \
      --extra-circuits "usb;{{revision}}" \
      --netlist-output usb_{{revision}}.net \
      --pcb-output usb_{{revision}}.kicad_pcb \
      --force
  just templates-svgs usb_{{revision}}

# demonstrates how to combine controller circuit with extra circuits:
circuit_atmega32u4_with_usb revision_uc revision_usb offset_usb:
  hatch run kicad:main \
      --layout tests/test_netlist_generation/empty.json \
      --switch-footprint "" \
      --stabilizer-footprint "" \
      --diode-footprint "" \
      --controller-circuit "atmega32u4;{{revision_uc}}" \
      --extra-circuits "dummy_matrix;v1" \
      --extra-circuits "usb;{{revision_usb}};{{offset_usb}}" \
      --netlist-output atmega32u4_{{revision_uc}}_with_usb_{{revision_usb}}.net \
      --pcb-output atmega32u4_{{revision_uc}}_with_usb_{{revision_usb}}.kicad_pcb \
      --force
  just templates-svgs atmega32u4_{{revision_uc}}_with_usb_{{revision_usb}}

all-circuits:
  just circuit_atmega32u4 v1
  just circuit_atmega32u4 v2
  just circuit_usb minimal
  just circuit_usb udb_clone
  just circuit_atmega32u4_with_usb v1 minimal 24.4865,-5.8633

positions template:
  hatch run kicad:positions {{template}}

tracks template:
  hatch run kicad:tracks {{template}}

io_tracks template:
  hatch run kicad:io_tracks {{template}}

vias template:
  hatch run kicad:vias {{template}}

templates-svgs variant:
  just svg {{variant}}.kicad_pcb
  just svg-mm-to-cm {{variant}}.svg
  if {{kicad_svg_fix}} == "true"; then just svg-fix-area {{variant}}.svg; fi
  cp {{variant}}.svg ./kicad-templates/
  rm {{variant}}.svg
  firefox ./kicad-templates/{{variant}}.svg

# assumes git-lukaj configured, see:
# https://github.com/adamws/lukaj?tab=readme-ov-file#git-integration
template-diff circuit revision:
  git diff-svg ./kicad-templates/{{circuit}}_{{revision}}.svg
