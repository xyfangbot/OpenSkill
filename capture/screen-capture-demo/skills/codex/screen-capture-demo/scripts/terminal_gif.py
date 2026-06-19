#!/usr/bin/env python3
"""Render real command output or a log file into a terminal-style GIF."""

from __future__ import annotations

import argparse
import os
import re
import shlex
import subprocess
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")


def parse_size(value: str) -> tuple[int, int]:
    parts = value.lower().split("x")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("size must look like 1000x620")
    return int(parts[0]), int(parts[1])


def load_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf",
        "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def clean_text(text: str) -> str:
    text = ANSI_RE.sub("", text)
    return text.replace("\r\n", "\n").replace("\r", "\n")


def run_command(command: list[str], cwd: str | None, timeout: float | None) -> str:
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        raise SystemExit("missing command after --")

    proc = subprocess.Popen(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    try:
        output, _ = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        output, _ = proc.communicate()
        output += f"\n[terminal_gif] command timed out after {timeout:g}s\n"
    if proc.returncode not in (0, None):
        output += f"\n[terminal_gif] command exited with code {proc.returncode}\n"
    return output


def wrap_lines(text: str, columns: int) -> list[str]:
    lines: list[str] = []
    for raw in clean_text(text).splitlines():
        if raw == "":
            lines.append("")
            continue
        wrapped = textwrap.wrap(
            raw,
            width=columns,
            replace_whitespace=False,
            drop_whitespace=False,
            break_long_words=True,
            break_on_hyphens=False,
        )
        lines.extend(wrapped or [""])
    return lines or ["(no output)"]


def render_frame(
    visible_lines: list[str],
    *,
    title: str,
    size: tuple[int, int],
    font: ImageFont.ImageFont,
    font_size: int,
) -> Image.Image:
    width, height = size
    bg = (18, 20, 24)
    panel = (28, 31, 36)
    border = (65, 72, 82)
    title_fg = (225, 229, 235)
    text_fg = (224, 231, 241)
    dim_fg = (143, 151, 163)

    img = Image.new("RGB", size, bg)
    draw = ImageDraw.Draw(img)
    margin = 24
    radius = 10
    header_h = 46
    draw.rounded_rectangle(
        (margin, margin, width - margin, height - margin),
        radius=radius,
        fill=panel,
        outline=border,
        width=1,
    )
    draw.rectangle((margin, margin + header_h, width - margin, margin + header_h + 1), fill=border)

    circle_y = margin + 22
    for idx, color in enumerate(((248, 113, 113), (251, 191, 36), (52, 211, 153))):
        x = margin + 18 + idx * 18
        draw.ellipse((x, circle_y - 6, x + 12, circle_y + 6), fill=color)

    draw.text((margin + 88, margin + 13), title, font=font, fill=title_fg)

    line_h = int(font_size * 1.45)
    x = margin + 18
    y = margin + header_h + 18
    max_y = height - margin - 16
    for line in visible_lines:
        if y + line_h > max_y:
            break
        fill = dim_fg if line.startswith("[terminal_gif]") else text_fg
        draw.text((x, y), line, font=font, fill=fill)
        y += line_h
    return img


def make_gif(
    lines: list[str],
    output: Path,
    *,
    title: str,
    size: tuple[int, int],
    fps: int,
    font_size: int,
    line_step: int,
    hold: float,
) -> None:
    font = load_font(font_size)
    width, height = size
    margin = 24
    header_h = 46
    line_h = int(font_size * 1.45)
    max_visible = max(1, (height - margin * 2 - header_h - 34) // line_h)

    frames: list[Image.Image] = []
    total = len(lines)
    for end in range(min(line_step, total), total + line_step, line_step):
        end = min(end, total)
        start = max(0, end - max_visible)
        frames.append(render_frame(lines[start:end], title=title, size=size, font=font, font_size=font_size))
        if end == total:
            break

    hold_frames = max(1, int(fps * hold))
    frames.extend([frames[-1].copy() for _ in range(hold_frames)])

    output.parent.mkdir(parents=True, exist_ok=True)
    frame_ms = max(20, int(1000 / fps))
    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=frame_ms,
        loop=0,
        optimize=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="Output GIF path.")
    parser.add_argument("--input", type=Path, help="Existing log file to render.")
    parser.add_argument("--log-output", type=Path, help="Write captured raw command output here.")
    parser.add_argument("--title", default="Real command output", help="Terminal title shown in the GIF.")
    parser.add_argument("--size", type=parse_size, default=(1000, 620), help="Canvas size, e.g. 1000x620.")
    parser.add_argument("--fps", type=int, default=8)
    parser.add_argument("--font-size", type=int, default=20)
    parser.add_argument("--line-step", type=int, default=2)
    parser.add_argument("--hold", type=float, default=1.5, help="Seconds to hold the final frame.")
    parser.add_argument("--cwd", help="Working directory for command mode.")
    parser.add_argument("--timeout", type=float, help="Command timeout in seconds.")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Command to run after --.")
    args = parser.parse_args()

    if args.input:
        text = args.input.read_text(encoding="utf-8", errors="replace")
    elif args.command:
        text = run_command(args.command, args.cwd, args.timeout)
        if args.log_output:
            args.log_output.parent.mkdir(parents=True, exist_ok=True)
            quoted = " ".join(shlex.quote(part) for part in args.command if part != "--")
            args.log_output.write_text(f"$ {quoted}\n{text}", encoding="utf-8")
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        raise SystemExit("provide --input, stdin, or a command after --")

    columns = max(20, (args.size[0] - 84) // max(8, int(args.font_size * 0.62)))
    lines = wrap_lines(text, columns)
    make_gif(
        lines,
        args.output,
        title=args.title,
        size=args.size,
        fps=args.fps,
        font_size=args.font_size,
        line_step=max(1, args.line_step),
        hold=max(0.0, args.hold),
    )
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
