template_atmega32u4_au_v1 := "./kicad-templates/atmega32u4-au-v1/atmega32u4-au-v1.kicad_pcb"

test:
  hatch run default:test

svg-mm-to-cm svg_file:
  sed -i -E 's/(width|height)="([0-9]*\.[0-9]*)mm"/\1="\2cm"/g' {{svg_file}}

svg kicad_pcb:
  kicad-cli pcb export svg --exclude-drawing-sheet --page-size-mode 2 \
    -l F.Cu,B.Cu,F.Silkscreen,B.Silkscreen,Edge.Cuts \
    -o "{{without_extension(kicad_pcb)}}.svg" {{kicad_pcb}}

circuits:
  hatch run kicad:circuits
  just svg atmega32u4_au_v1.kicad_pcb
  firefox atmega32u4_au_v1.svg

positions:
  hatch run kicad:positions

templates-svgs:
 just svg {{template_atmega32u4_au_v1}}
 just svg-mm-to-cm {{without_extension(template_atmega32u4_au_v1)}}.svg
 firefox {{without_extension(template_atmega32u4_au_v1)}}.svg

