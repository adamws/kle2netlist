output := "output/udb.kicad_pcb"

venv:
  #!/usr/bin/env bash
  rm -rf .env
  python -m venv --system-site-package .env
  . .env/bin/activate
  python -m pip install -r requirements.txt -r dev-requirements.txt

render:
  python render_page.py {{output}} output \
    --width 900 --height 600
  cp output/svgs/*.svg resources/

preview:
  firefox output/index.html

pcb:
  #!/usr/bin/env bash
  set -euxo pipefail
  . .env/bin/activate
  python generate.py -out output -f
  rm generate.erc generate.log generate_lib_sklib.py
  just render

# assumes git-lukaj configured, see:
# https://github.com/adamws/lukaj?tab=readme-ov-file#git-integration
diff:
  git diff-svg ./resources/pcb.svg

run-in-docker image:
  #!/usr/bin/env bash
  cd ../../
  docker run --rm -v $(pwd):$(pwd) -w $(pwd) \
    --user kicad {{image}} \
    bash -c "
      cd examples/udb
      python -m pip install -r requirements.txt -r dev-requirements.txt
      python generate.py -out output -f
      just render
    "
