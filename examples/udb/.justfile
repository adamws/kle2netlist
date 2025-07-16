id := `id -u $(whoami)`
output := "output/udb.kicad_pcb"

venv:
  #!/usr/bin/env bash
  rm -rf .env
  python -m venv --system-site-package .env
  . .env/bin/activate
  pip install -r requirements.txt -r dev-requirements.txt

preview:
  python render_page.py {{output}} output \
    --width 900 --height 600
  cp output/svgs/*.svg resources/
  firefox output/index.html

pcb:
  #!/usr/bin/env bash
  set -euxo pipefail
  . .env/bin/activate
  python generate.py -out output -f
  rm generate.erc generate.log generate_lib_sklib.py
  just preview

# assumes git-lukaj configured, see:
# https://github.com/adamws/lukaj?tab=readme-ov-file#git-integration
diff:
  git diff-svg ./resources/pcb.svg
