import argparse
import subprocess
import os
import re
import sys
import xml.etree.ElementTree as ET

import PIL.Image
from jinja2 import Environment, FileSystemLoader

SVG_TEMPLATE_FRONT = "B.Cu,F.Cu,F.Silkscreen,Edge.Cuts"
SVG_TEMPLATE_BACK = "F.Cu,B.Cu,B.Silkscreen,Edge.Cuts"
DEFAULT_FRAME_COUNT = 72
DEFAULT_WIDTH = 900
DEFAULT_HEIGHT = 600

TEMPLATE_STR = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{{ title }}</title>
  <style>
    .svg-pair {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 2vw;
      width: 100%;
      max-width: 1200px;
      margin: 0 auto;
    }
    .svg-pair img {
      flex: 1 1 0;
      max-width: 45vw;
      height: auto;
      width: 100%;
      min-width: 0;
      object-fit: contain;
      display: block;
    }
    #controls { margin-top: 10px; }
    canvas { background: #fff; display: block; margin: 0 auto; }
    #buttonBar {
      text-align: center;
      margin-top: 10px;
    }
    #buttonBar button {
      margin: 0 10px;
      padding: 8px 20px;
      font-size: 1.2em;
      cursor: pointer;
      min-width: 100px;
      box-sizing: border-box;
    }
    #progress { display: block; text-align: center; margin-top: 10px; }
  </style>
</head>
<body>
  <h2 style="text-align:center;">{{ header }}</h2>
  <div class="svg-pair">
    <img src="svgs/front.svg" />
    <img src="svgs/back.svg" />
  </div>
  {% if render_rotation %}
  <div>
    <canvas id="animation" width="{{ width }}" height="{{ height }}"></canvas>
    <div id="buttonBar">
      <button id="rotateLeft" title="Rotate Left">&#8592;</button>
      <button id="playPause" title="Pause/Play">Pause</button>
      <button id="rotateRight" title="Rotate Right">&#8594;</button>
    </div>
  </div>
  <span id="progress"></span>
  <script>
    const FRAME_COUNT = {{ frame_count }};
    const FRAME_URL = i => `renders/frame_${i.toString().padStart(2, '0')}.png`;
    const canvas = document.getElementById('animation');
    const ctx = canvas.getContext('2d');
    const playPauseBtn = document.getElementById('playPause');
    const rotateLeftBtn = document.getElementById('rotateLeft');
    const rotateRightBtn = document.getElementById('rotateRight');
    const progress = document.getElementById('progress');
    let playing = true;
    let currentFrame = 0;
    const frames = new Array(FRAME_COUNT);
    let loadedCount = 0;
    const FRAME_DELAY = 60;

    function preloadFrames() {
      for (let i = 0; i < FRAME_COUNT; i++) {
        const img = new Image();
        img.onload = () => {
          loadedCount++;
          progress.textContent = `Loaded ${loadedCount}/${FRAME_COUNT}`;
          if (loadedCount === FRAME_COUNT) {
            progress.textContent = 'All frames loaded!';
            progress.style.display = 'none';
            drawFrame(currentFrame);
          }
        };
        img.onerror = () => {
          progress.textContent = `Error loading frame ${i}`;
        };
        img.src = FRAME_URL(i);
        frames[i] = img;
      }
    }
    function drawFrame(frame) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const img = frames[frame];
      if (img && img.complete) {
        const imgW = img.width || canvas.width;
        const imgH = img.height || canvas.height;
        const x = (canvas.width - imgW)/2;
        const y = (canvas.height - imgH)/2;
        ctx.drawImage(img, x, y, imgW, imgH);
      } else {
        ctx.fillStyle = "#555";
        ctx.font = "24px sans-serif";
        ctx.fillText("Loading...", canvas.width/2 - 60, canvas.height/2);
      }
    }
    let intervalId = null;
    function startAnimation() {
      if (intervalId) return;
      intervalId = setInterval(() => {
        if (playing && loadedCount === FRAME_COUNT) {
          currentFrame = (currentFrame + 1) % FRAME_COUNT;
          drawFrame(currentFrame);
        }
      }, FRAME_DELAY);
    }
    function stopAnimation() {
      if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
      }
    }
    playPauseBtn.addEventListener('click', () => {
      playing = !playing;
      playPauseBtn.textContent = playing ? 'Pause' : 'Play';
    });
    rotateLeftBtn.addEventListener('click', () => {
      playing = false;
      playPauseBtn.textContent = 'Play';
      currentFrame = (currentFrame + 1 + FRAME_COUNT) % FRAME_COUNT;
      drawFrame(currentFrame);
    });
    rotateRightBtn.addEventListener('click', () => {
      playing = false;
      playPauseBtn.textContent = 'Play';
      currentFrame = (currentFrame - 1) % FRAME_COUNT;
      drawFrame(currentFrame);
    });
    let isDragging = false, dragStartX = 0, frameStart = 0;
    canvas.addEventListener('mousedown', (e) => {
      isDragging = true;
      dragStartX = e.clientX;
      frameStart = currentFrame;
      playing = false;
      playPauseBtn.textContent = 'Play';
    });
    canvas.addEventListener('mousemove', (e) => {
      if (isDragging) {
        let dx = e.clientX - dragStartX;
        let frame = (frameStart - Math.round(dx / 5)) % FRAME_COUNT;
        if (frame < 0) frame += FRAME_COUNT;
        currentFrame = frame;
        drawFrame(currentFrame);
      }
    });
    canvas.addEventListener('mouseup', () => { isDragging = false; });
    canvas.addEventListener('mouseleave', () => { isDragging = false; });
    preloadFrames();
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) stopAnimation();
      else startAnimation();
    });
    const checkStart = setInterval(() => {
      if (loadedCount === FRAME_COUNT) {
        startAnimation();
        clearInterval(checkStart);
      }
    }, 100);
  </script>
  {% endif %}
</body>
</html>
"""

def run_kicad_svg(pcb_file, layers, output_file):
    cmd = [
        "kicad-cli", "pcb", "export", "svg",
        "--exclude-drawing-sheet",
        "--page-size-mode", "2",
        "-l", layers,
        "-o", output_file,
        pcb_file
    ]
    subprocess.run(cmd, check=True)

    # xml.etree.ElementTree expects the namespace for SVG
    SVG_NS = "http://www.w3.org/2000/svg"
    ET.register_namespace('', SVG_NS)
    tree = ET.parse(output_file)
    root = tree.getroot()
    desc = root.find(f".//{{{SVG_NS}}}desc")
    # Get width and height attributes
    svg_w = root.attrib.get("width","")
    svg_h = root.attrib.get("height","")
    # Add background rect after desc
    if desc is not None:
        parent = root
        children = list(parent)
        desc_index = children.index(desc)
        rect = ET.Element("rect", x="0", y="0", width=svg_w, height=svg_h, fill="#282A36")
        parent.insert(desc_index + 1, rect)
        tree.write(output_file, encoding="unicode")
    # Change mm to cm in width/height attributes (edit file as text)
    with open(output_file, "r") as f:
        content = f.read()
    content = re.sub(r'(width|height)="([0-9]*\.[0-9]*)mm"', r'\1="\2cm"', content)
    with open(output_file, "w") as f:
        f.write(content)


def run_rotation_renders(pcb_file, output_dir, width, height, frame_count):
    os.makedirs(output_dir, exist_ok=True)
    zoom = "0.9"
    side = "bottom"
    for i in range(frame_count):
        angle = int(i * 360 / frame_count)
        output_file = os.path.join(output_dir, f"frame_{i:02d}.png")
        cmd = [
            "kicad-cli", "pcb", "render",
            "--quality", "basic",
            "--width", str(width),
            "--height", str(height),
            "--side", side,
            "--rotate", f"'-45,0,{angle}'",
            "--light-top", "0",
            "--light-bottom", "0",
            "--light-side", "0",
            "--light-camera", "1",
            "--zoom", zoom,
            "-o", output_file,
            pcb_file
        ]
        print(f"Rendering frame {i} at angle {angle}°")
        subprocess.run(cmd, check=True)


def get_image_size(png_file):
    im = PIL.Image.open(png_file)
    return im.width, im.height


def main() -> None:
    parser = argparse.ArgumentParser(description="Render PCB preview page with KiCad CLI.")
    parser.add_argument("pcb_file", help="Path to .kicad_pcb file")
    parser.add_argument("output_dir", help="Output directory for generated files")
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH, help="Render width")
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT, help="Render height")
    parser.add_argument("--frame-count", type=int, default=DEFAULT_FRAME_COUNT, help="Number of rotation frames")
    parser.add_argument("--no-rotation-render", action="store_true", help="Disable rotation render")
    parser.add_argument("--header", default=None, help="Header text (defaults to PCB file name)")
    args = parser.parse_args()

    pcb_file = args.pcb_file
    output_dir = args.output_dir
    width = args.width
    height = args.height
    frame_count = args.frame_count
    render_rotation = not args.no_rotation_render
    header = args.header if args.header else os.path.basename(pcb_file)

    # Prepare output folders
    svgs_dir = os.path.join(output_dir, "svgs")
    os.makedirs(svgs_dir, exist_ok=True)
    renders_dir = os.path.join(output_dir, "renders")
    if render_rotation:
        os.makedirs(renders_dir, exist_ok=True)

    # Render SVGs
    print("Rendering front SVG...")
    run_kicad_svg(pcb_file, SVG_TEMPLATE_FRONT, os.path.join(svgs_dir, "front.svg"))
    print("Rendering back SVG...")
    run_kicad_svg(pcb_file, SVG_TEMPLATE_BACK, os.path.join(svgs_dir, "back.svg"))

    # Render rotation PNGs if enabled
    if render_rotation:
        print(f"Rendering {frame_count} rotation frames...")
        run_rotation_renders(pcb_file, renders_dir, width, height, frame_count)
        # Check PNG dimensions
        png_files = sorted([
            os.path.join(renders_dir, f)
            for f in os.listdir(renders_dir)
            if f.lower().endswith('.png')
        ])
        if not png_files:
            print(f"No PNG files found in {renders_dir}")
            sys.exit(1)
        ref_w, ref_h = get_image_size(png_files[0])
        for f in png_files:
            w, h = get_image_size(f)
            if w != ref_w or h != ref_h:
                print(f"Error: Not all PNG files have the same dimensions. {f}: {w}x{h}, expected {ref_w}x{ref_h}")
                sys.exit(1)
        width = ref_w
        height = ref_h

    # Render HTML
    env = Environment(loader=FileSystemLoader(os.getcwd()))
    template = env.from_string(TEMPLATE_STR)
    html = template.render(
        title="Board preview",
        header=header,
        width=width,
        height=height,
        frame_count=frame_count,
        render_rotation=render_rotation
    )
    out_html = os.path.join(output_dir, "index.html")
    with open(out_html, "w") as f:
        f.write(html)
    print(f"Wrote {out_html}")

if __name__ == "__main__":
    main()
