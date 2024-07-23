template_atmega32u4_au_v1 := "./atmega32u4_au_v1.kicad_pcb"

test:
  hatch run default:test

svg-mm-to-cm svg_file:
  sed -i -E 's/(width|height)="([0-9]*\.[0-9]*)mm"/\1="\2cm"/g' {{svg_file}}

svg kicad_pcb:
  kicad-cli pcb export svg --exclude-drawing-sheet --page-size-mode 2 \
    -l F.Cu,B.Cu,F.Silkscreen,B.Silkscreen,Edge.Cuts \
    -o "{{without_extension(kicad_pcb)}}.svg" {{kicad_pcb}}

circuits variant:
  hatch run kicad:circuits --variant {{variant}}
  just templates-svgs {{variant}}

positions:
  hatch run kicad:positions

templates-svgs variant:
  just svg atmega32u4_au_{{variant}}.kicad_pcb
  just svg-mm-to-cm atmega32u4_au_{{variant}}.svg
  cp atmega32u4_au_{{variant}}.svg ./kicad-templates/
  rm atmega32u4_au_{{variant}}.svg
  firefox ./kicad-templates/atmega32u4_au_{{variant}}.svg

