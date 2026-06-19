#!/usr/bin/env python3
"""Capture real screen pixels as a screenshot, GIF, MP4, or WebM."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from PIL import Image, ImageGrab


def parse_region(value: str) -> tuple[int, int, int, int]:
    parts = [int(part.strip()) for part in value.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("region must look like X,Y,W,H")
    x, y, w, h = parts
    if w <= 0 or h <= 0:
        raise argparse.ArgumentTypeError("region width and height must be positive")
    return x, y, x + w, y + h


def xdotool_window_bbox(title: str) -> tuple[int, int, int, int] | None:
    try:
        ids = subprocess.check_output(["xdotool", "search", "--name", title], text=True).split()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    if not ids:
        return None

    window_id = ids[-1]
    subprocess.run(["xdotool", "windowactivate", "--sync", window_id], check=False)
    subprocess.run(["xdotool", "windowraise", window_id], check=False)
    time.sleep(0.35)

    try:
        geometry = subprocess.check_output(
            ["xdotool", "getwindowgeometry", "--shell", window_id],
            text=True,
        )
    except subprocess.CalledProcessError:
        return None

    data: dict[str, int] = {}
    for line in geometry.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key in {"X", "Y", "WIDTH", "HEIGHT"}:
            data[key] = int(value)
    if {"X", "Y", "WIDTH", "HEIGHT"} <= data.keys():
        return data["X"], data["Y"], data["X"] + data["WIDTH"], data["Y"] + data["HEIGHT"]
    return None


def grab_frame(bbox: tuple[int, int, int, int] | None) -> Image.Image:
    return ImageGrab.grab(bbox=bbox).convert("RGB")


def capture_frames(
    *,
    bbox: tuple[int, int, int, int] | None,
    duration: float,
    fps: int,
) -> list[Image.Image]:
    if duration <= 0:
        return [grab_frame(bbox)]

    frames: list[Image.Image] = []
    interval = 1.0 / fps
    start = time.monotonic()
    next_frame = start
    while True:
        now = time.monotonic()
        if now >= start + duration:
            break
        if now < next_frame:
            time.sleep(min(next_frame - now, 0.05))
            continue
        frames.append(grab_frame(bbox))
        next_frame += interval
    return frames or [grab_frame(bbox)]


def save_video(frames: list[Image.Image], output: Path, fps: int) -> None:
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        raise SystemExit("ffmpeg is required for mp4/webm output")

    with tempfile.TemporaryDirectory(prefix="capture-screen-") as tmp:
        tmp_path = Path(tmp)
        for idx, frame in enumerate(frames):
            frame.save(tmp_path / f"{idx:06d}.png")
        cmd = [
            "ffmpeg",
            "-y",
            "-framerate",
            str(fps),
            "-i",
            str(tmp_path / "%06d.png"),
        ]
        if output.suffix.lower() == ".webm":
            cmd += ["-c:v", "libvpx-vp9", "-b:v", "0", "-crf", "32"]
        else:
            cmd += ["-pix_fmt", "yuv420p"]
        cmd.append(str(output))
        subprocess.run(cmd, check=True)


def save_output(frames: list[Image.Image], output: Path, fps: int) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    suffix = output.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg"}:
        frames[0].save(output)
    elif suffix == ".gif":
        frame_ms = max(20, int(1000 / fps))
        frames[0].save(
            output,
            save_all=True,
            append_images=frames[1:],
            duration=frame_ms,
            loop=0,
            optimize=True,
        )
    elif suffix in {".mp4", ".webm"}:
        save_video(frames, output, fps)
    else:
        raise SystemExit("output extension must be .png, .jpg, .gif, .mp4, or .webm")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--duration", type=float, default=0.0, help="Seconds to capture; 0 means one screenshot.")
    parser.add_argument("--fps", type=int, default=8)
    parser.add_argument("--delay", type=float, default=0.0, help="Seconds to wait before capture.")
    parser.add_argument("--region", type=parse_region, help="Capture region as X,Y,W,H.")
    parser.add_argument("--window-title", help="Use xdotool to find and raise a matching window.")
    args = parser.parse_args()

    if args.fps <= 0:
        raise SystemExit("--fps must be positive")
    if args.delay > 0:
        time.sleep(args.delay)

    bbox = args.region
    if args.window_title and bbox is None:
        bbox = xdotool_window_bbox(args.window_title)
        if bbox is None:
            print(
                f"[capture_screen] warning: could not find window title {args.window_title!r}; capturing full screen",
                file=sys.stderr,
            )

    if sys.platform.startswith("linux") and not os.environ.get("DISPLAY"):
        raise SystemExit("DISPLAY is not set; screen capture needs a graphical session")

    frames = capture_frames(bbox=bbox, duration=max(0.0, args.duration), fps=args.fps)
    save_output(frames, args.output, args.fps)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
