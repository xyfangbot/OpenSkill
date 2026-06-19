# Screen Capture Demo Skill

Create truthful demo proof artifacts from real runs: screenshots, GIFs, MP4/WebM recordings, and clean terminal-log GIFs.

This skill is useful for:

- Capturing GUI demos such as RViz, browser apps, desktop tools, or visualization windows.
- Turning real CLI output into clean GIFs for README previews.
- Replacing fake or illustrative demo media with reproducible captures.

## Skill Variant

- `skills/codex/screen-capture-demo`: Codex skill with reusable capture scripts.

## Requirements

- Python 3
- Pillow:

```bash
python3 -m pip install --user pillow
```

Optional but recommended on Linux/X11:

```bash
sudo apt-get install -y xdotool ffmpeg
```

`xdotool` is used for window discovery and activation. `ffmpeg` is used for MP4/WebM output.

## Install In Codex

From GitHub:

```text
$skill-installer install https://github.com/xyfangbot/openskill/tree/main/capture/screen-capture-demo/skills/codex/screen-capture-demo
```

Manual local install from this directory:

```bash
./scripts/install-codex.sh
```

Restart Codex after installation.

## Examples

Ask Codex:

```text
Use $screen-capture-demo to capture a real ROS2 RViz demo GIF for the README.
```

Or:

```text
Use $screen-capture-demo to turn the real ROS1 and ROS2 pub/sub outputs into clean terminal GIFs.
```

## Safety

- Do not label generated or mocked images as real screenshots.
- Prefer terminal-log GIFs for CLI behavior to avoid desktop popups.
- Inspect captures before committing so private windows, credentials, QR codes, or local paths are not visible.
