# OpenSkill

OpenSkill is a public collection of reusable AI-agent skills.

## Layout

```text
<capability>/<skill-name>/
```

Current skills:

- `feishu/feishu-docs-vscode`: Sync Feishu/Lark cloud documents into VSCode as Markdown with rendered preview and guarded push-back.

## Install

Codex skills can be installed from a GitHub directory URL:

```text
$skill-installer install https://github.com/<account>/OpenSkill/tree/main/feishu/feishu-docs-vscode/skills/codex/feishu-docs-vscode
```

Claude Code skills can be copied into `~/.claude/skills/` or project `.claude/skills/`:

```bash
cp -R feishu/feishu-docs-vscode/skills/claude-code/feishu-docs-vscode ~/.claude/skills/
```

## Safety

This repository must not contain credentials, synced private documents, generated previews, QR codes, or local machine paths.
