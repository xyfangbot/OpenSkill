# Capture Workflow Reference

## Realness Contract

State what was actually captured:

- "real window capture" for screen pixels from a running app.
- "real command output rendered as a terminal GIF" for CLI logs.
- "recorded MP4 converted to GIF" only when that is the actual pipeline.

Never describe generated or mocked media as real captures.

## CLI And Pub/Sub Demos

For command-line evidence, prefer `terminal_gif.py`:

1. Run the real command.
2. Capture combined stdout/stderr.
3. Save the raw log with `--log-output`.
4. Render the log into a terminal-style GIF.
5. Inspect the final GIF frame for contamination, truncation, and useful evidence.

This avoids accidental desktop popups while preserving real runtime output.

## GUI, RViz, Browser, And Desktop Demos

For visual evidence, prefer `capture_screen.py`:

1. Start the app and wait until the visual state is meaningful.
2. Use `--window-title` if the platform can find the target window.
3. Use `--region X,Y,W,H` if window discovery is unreliable.
4. Keep the capture short and focused.
5. Open the output and inspect at least the first and final frame.

On Linux/X11, install or use existing dependencies when needed:

```bash
python3 -m pip install --user pillow
sudo apt-get install -y xdotool ffmpeg
```

For Docker/X11 GUI captures, verify `DISPLAY`, `/tmp/.X11-unix`, and `xhost` access before recording.

## Artifact Hygiene

- Put generated demo assets under an obvious path such as `docs/assets/demo/`.
- Keep raw logs in `/tmp` or a clearly named temporary folder unless the user wants them committed.
- Do not commit large video files unless the user explicitly wants them in the repository.
- Prefer README GIF previews plus scripts that can regenerate them.
