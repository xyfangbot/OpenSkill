---
name: screen-capture-demo
description: "Create truthful demo proof artifacts from real app or command runs: screenshots, screen recordings, GIFs, MP4/WebM videos, and clean terminal-log GIFs. Use when Codex is asked to record, screenshot, screen-capture, make a GIF/video, document a demo run, prove ROS/RViz/web/CLI behavior visually, or replace fake/illustrative images with real captures."
---

# Screen Capture Demo

## Core Rule

Produce proof from a real run. Do not invent screenshots, generate illustrative images, or label synthetic assets as real.

Use a terminal-log GIF for CLI/pub-sub/log demos when the important evidence is text output. Use a real screen capture for GUI demos such as RViz, browser UIs, desktop apps, or visual simulations.

## Workflow

1. Identify the proof target:
   - CLI behavior: commands, logs, topic echoes, test output.
   - GUI behavior: window pixels, animation, interaction, RViz/browser/app state.
2. Start from a clean scene:
   - Close popups and unrelated windows.
   - Prefer a fresh terminal or clean desktop/workspace.
   - Record the exact command used to create the artifact.
3. Capture real evidence:
   - For CLI output, run the command and render the captured stdout/stderr with `scripts/terminal_gif.py`.
   - For GUI output, run the real app and capture the screen/window with `scripts/capture_screen.py`.
4. Verify the artifact:
   - Open or inspect at least the first and final frame for GIFs.
   - Confirm no unrelated popups, editor windows, private data, or misleading overlays are visible.
   - Confirm the artifact path and source command are clear in the final response.

## Scripts

Use `scripts/terminal_gif.py` for text-mode proof:

```bash
python3 scripts/terminal_gif.py \
  --output docs/assets/demo/pubsub.gif \
  --title "ROS pub/sub demo" \
  --log-output /tmp/pubsub.log \
  -- bash -lc 'source install/setup.bash && ros2 launch demo pubsub.launch.py'
```

Use `scripts/capture_screen.py` for real pixels:

```bash
python3 scripts/capture_screen.py \
  --output docs/assets/demo/rviz.gif \
  --window-title 'RViz' \
  --duration 8 \
  --fps 8
```

Use `--region X,Y,W,H` when a title match is unreliable. Use `.png` for screenshots, `.gif` for short looping previews, and `.mp4`/`.webm` for longer recordings.

## Notes

Prefer GIFs under about 10 seconds for README previews. For longer evidence, produce MP4/WebM and optionally a short GIF excerpt.

When the capture is generated from real logs rather than direct pixels, say so plainly: "real command output rendered as a terminal GIF." This is still truthful proof and avoids desktop contamination.

Read `references/capture-workflow.md` when a task needs ROS/RViz, Docker/X11, or repeatable verification details.
