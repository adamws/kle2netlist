FROM kicad/kicad:9.0.3-full

ARG DEBIAN_FRONTEND=noninteractive

USER root

RUN apt-get update \
  && apt-get install -y curl jq python3-pip python3-venv
RUN curl --proto '=https' --tlsv1.2 -sSf \
  https://just.systems/install.sh | bash -s -- --to /usr/bin --tag 1.42.2
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN find / -type f -name "EXTERNALLY-MANAGED" -exec rm {} \;

USER kicad
