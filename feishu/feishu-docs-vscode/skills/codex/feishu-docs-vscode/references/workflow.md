# Feishu Docs VSCode Workflow

## Fetch Docx/Wiki As Markdown

```bash
lark-cli docs +fetch \
  --api-version v2 \
  --doc "<feishu_doc_url_or_token>" \
  --doc-format markdown \
  --format json
```

The Markdown content is in:

```text
data.document.content
```

## Fetch Drive-Native Markdown

```bash
lark-cli markdown +fetch \
  --file-token "<file_token>" \
  --output "feishu-docs/current.md" \
  --overwrite
```

## Recommended Workspace Files

Create a minimal Node workspace with:

```text
package.json
feishu.config.json
scripts/feishu-sync.mjs
scripts/feishu-render.mjs
scripts/feishu-serve.mjs
scripts/feishu-push.mjs
.vscode/tasks.json
feishu-docs/current.md
```

Use scripts with these package commands:

```json
{
  "scripts": {
    "feishu:sync": "node scripts/feishu-sync.mjs",
    "feishu:render": "node scripts/feishu-render.mjs",
    "feishu:pull": "npm run feishu:sync && npm run feishu:render",
    "feishu:push": "node scripts/feishu-push.mjs",
    "feishu:serve": "node scripts/feishu-serve.mjs --sync-on-start"
  },
  "dependencies": {
    "marked": "^18.0.4"
  }
}
```

`feishu.config.json`:

```json
{
  "defaultDoc": "current",
  "docs": {
    "current": {
      "url": "<feishu_doc_url>",
      "markdownPath": "feishu-docs/current.md",
      "htmlPath": "feishu-docs/current.html"
    }
  }
}
```

## Pull

Pull should:

1. Read `feishu.config.json`.
2. Run `lark-cli docs +fetch --api-version v2 --doc-format markdown --format json`.
3. Save content to `feishu-docs/current.md`.
4. Write `feishu-docs/manifest.json` with title, source URL, document ID, revision ID, and sync time.
5. Render HTML from Markdown using `marked`.

## Serve

Serve should:

1. Start an HTTP server on `127.0.0.1:4777`.
2. Return the rendered HTML at `/`.
3. Expose `POST /sync` to pull and render latest remote content.
4. Include a visible `同步` button in the page that calls `/sync`.

## Push

Push should be safe by default:

1. Fetch the remote document first and display URL, title, revision ID, local file path, and local/remote line counts.
2. Without `--yes`, make no remote changes.
3. With `--yes`, run `lark-cli docs +update --api-version v2 --command overwrite --doc-format markdown --revision-id <remote_revision> --content @feishu-docs/current.md`.
4. After push, run pull again to verify the new revision and local content.

## Remote Editing Commands

Use Docx update commands for cloud docs:

```bash
lark-cli docs +update \
  --api-version v2 \
  --doc "<feishu_doc_url_or_token>" \
  --command append \
  --doc-format markdown \
  --content @local-change.md
```

Use Drive Markdown overwrite only for Drive-native `.md` files:

```bash
lark-cli markdown +overwrite \
  --file-token "<file_token>" \
  --file "feishu-docs/current.md"
```
