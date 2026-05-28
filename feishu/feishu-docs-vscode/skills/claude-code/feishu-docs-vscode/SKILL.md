---
name: feishu-docs-vscode
description: Use this skill whenever the user mentions Feishu/Lark cloud docs, 飞书云文档, docx/wiki links, Drive Markdown files, syncing a Feishu document into VSCode, previewing rendered Markdown articles, or asks Claude Code to read, sync, preview, edit, push, or build a VSCode workflow around Feishu docs. Prefer doing the workflow directly and only ask the user for Feishu authorization, a missing document link, or missing permissions.
allowed-tools: Bash, Read, Write, Edit, MultiEdit, Grep, Glob
---

# Feishu Docs VSCode

Use this skill to connect Feishu cloud documents to a Claude Code/VSCode workspace as local Markdown plus a rendered article preview.

## Claude Code Behavior

- Act first. Ask the user only when a browser/Feishu authorization step, a document link, or remote document permission is missing.
- Use `lark-cli` as the source of truth for Feishu/Lark access.
- Treat Feishu `docx` and `wiki` URLs as cloud docs and fetch them with `docs +fetch --api-version v2`.
- Treat Drive-native `.md` files as Markdown files and fetch them with `markdown +fetch`.
- Never print app secrets, access tokens, refresh tokens, or keychain material.
- Confirm before overwriting or large-scale editing a remote Feishu document.
- If this skill is installed as a project skill, keep generated preview files inside the project rather than under the skill directory.

## Workflow

Read [references/workflow.md](references/workflow.md) when the workspace does not already have a Feishu preview setup, when auth is broken, or when the user asks for local-to-remote push.

If the workspace already has these scripts, prefer using them:

```bash
npm run feishu:pull
npm run feishu:serve
npm run feishu:push
npm run feishu:push -- --yes
```

The default preview URL is:

```text
http://127.0.0.1:4777
```

VSCode users can open it with `Simple Browser: Show`, or open `feishu-docs/current.md` with `Markdown: Open Preview to the Side`.

## Auth

Check:

```bash
lark-cli auth status
```

If `lark-cli` is missing:

```bash
npx @larksuite/cli@latest install
```

Initialize and log in:

```bash
lark-cli config init --new
lark-cli auth login --recommend
```

When `auth login` prints a verification URL, show it to the user exactly as printed. If it asks for a QR code, generate and display it:

```bash
lark-cli auth qrcode "<verification_url>" --output tmp/feishu-auth-qr.png --size 320
```

## Invocation

The direct command name comes from the skill directory:

```text
/feishu-docs-vscode
```

The skill should also trigger naturally when the user provides a Feishu document URL and asks to sync, preview, or edit it.
