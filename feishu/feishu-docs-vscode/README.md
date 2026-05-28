# Feishu Docs VSCode Skill

Connect Feishu/Lark cloud documents to a VSCode/Codex or Claude Code workspace as local Markdown plus a rendered article preview.

This repository intentionally ships two skill variants:

- `skills/codex/feishu-docs-vscode`: tuned for Codex, `$skill-installer`, and Codex sandbox/elevation behavior.
- `skills/claude-code/feishu-docs-vscode`: tuned for Claude Code, `.claude/skills`, and Claude Code `allowed-tools` frontmatter.

Both variants use the same workflow:

1. Authenticate with `lark-cli`.
2. Fetch a Feishu `docx` or `wiki` document as Markdown.
3. Save it into `feishu-docs/current.md`.
4. Render `feishu-docs/current.html`.
5. Serve a local preview at `http://127.0.0.1:4777`.
6. Optionally push local Markdown back to Feishu after an explicit confirmation.

## Requirements

- Node.js and npm
- `lark-cli`
- Feishu/Lark account with access to the target document

Install `lark-cli`:

```bash
npx @larksuite/cli@latest install
```

## Install In Codex

From a published GitHub repo:

```text
$skill-installer install https://github.com/<owner>/<repo>/tree/main/skills/codex/feishu-docs-vscode
```

Then restart Codex so the new skill is loaded.

Manual local install:

```bash
./scripts/install-codex.sh
```

## Install In Claude Code

Personal skill:

```bash
./scripts/install-claude-code.sh
```

Project skill:

```bash
mkdir -p .claude/skills
cp -R skills/claude-code/feishu-docs-vscode .claude/skills/
```

In Claude Code, invoke directly with:

```text
/feishu-docs-vscode
```

or ask naturally, for example:

```text
把这个飞书文档接入 VSCode 预览：https://example.feishu.cn/docx/...
```

## Suggested GitHub Layout

```text
feishu-docs-vscode-skill/
├── README.md
├── LICENSE
├── evals/
│   └── evals.json
├── scripts/
│   ├── install-claude-code.sh
│   └── install-codex.sh
└── skills/
    ├── claude-code/
    │   └── feishu-docs-vscode/
    │       ├── SKILL.md
    │       └── references/
    │           └── workflow.md
    └── codex/
        └── feishu-docs-vscode/
            ├── SKILL.md
            └── references/
                └── workflow.md
```

## Publish To GitHub

From this directory:

```bash
git init
git add .
git commit -m "Add Feishu docs VSCode skill"
git branch -M main
git remote add origin git@github.com:<owner>/<repo>.git
git push -u origin main
```

Or with GitHub CLI:

```bash
gh repo create <owner>/<repo> --private --source=. --remote=origin --push
```

Use a private repo first if the workflow is only for your own machine or team.

## Security Notes

- Do not commit Feishu credentials, local keychain material, temporary QR codes, synced private documents, or `node_modules`.
- Remote push uses `docs +update --command overwrite`; the workflow must preview the target and require explicit confirmation before writing back.
- Keep `lark-cli` credentials in the user's local environment, not inside this repository.
