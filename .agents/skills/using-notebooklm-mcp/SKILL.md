---
name: using-notebooklm-mcp
description: Manages NotebookLM notebooks, sources, and triggers content generation. Use when user mentions listing notebooks, querying sources, creating audio overviews, or generating study guides.
---

# Using NotebookLM MCP

This skill provides step-by-step instructions on how to use the NotebookLM Model Context Protocol (MCP) server to manage notebooks, upload sources, ask queries, and generate studio outputs.

## When to Use This Skill

- When listing, creating, renaming, or deleting NotebookLM notebooks.
- When adding, syncing, or deleting sources (text, URLs, Drive files) in a notebook.
- When querying notebooks and getting citation-backed answers.
- When triggering the creation of study aids (Audio, Video, Slides, Infographics, Quizzes, Flashcards, Mind Maps).

## Prerequisites

- NotebookLM MCP Server (`notebooklm-mcp.exe` and `notebooklm-mcp-auth.exe`).
- Valid cookies stored in `~/.notebooklm-mcp/auth.json`.

## Authentication & Re-authentication Workflow

If authentication is missing or expired:

1. **Quick Re-auth using `auth_helper.py`:**
   Run in the workspace terminal:
   ```powershell
   python auth_helper.py
   ```
   - Automatically inspects the clipboard for copied Google `cookie:` headers or reads `cookies.txt`.
   - Formats, validates, saves to `~/.notebooklm-mcp/auth.json`, and tests connection.
2. **If the user needs to provide cookies:**
   Ask the user to:
   - Open `https://notebooklm.google.com` (logged in) -> `F12` -> `Network` -> `F5`.
   - Click `batchexecute` -> Request Headers -> Copy value of `cookie:`.
   - Run `python auth_helper.py` or paste the value into `cookies.txt`.

## Workflow

### Step 1: Initialize Connection and List Notebooks
Call `notebook_list` to list all notebooks and retrieve their `notebook_id`s.

### Step 2: Query Notebooks
Call `notebook_query` with:
- `notebook_id`: The ID of the target notebook.
- `query`: The question to ask.

### Step 3: Add Sources
Call `notebook_add_url` or `notebook_add_text` to import new context.

### Step 4: Generate Studio Content
Call `audio_overview_create`, `video_overview_create`, `slide_deck_create`, `quiz_create`, or `infographic_create`.
- *Note:* Always pass `language: "es"` if working in Spanish.
- Poll `studio_status` until generation is complete.

## Validation

Verify execution by calling `notebook_list` and ensuring a `"status": "success"` response is returned with the correct list of notebooks.

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Authentication expired / 401 | Cookies in cache are invalid or expired | Run `python auth_helper.py` to re-authenticate with fresh cookies |
| English outputs generated | Default language is `en` | Set `language="es"` explicitly in studio creation tools |
| Request timeout | Google servers took too long | Set `timeout` parameter to a higher value (up to 120.0) |

## Resources

- `auth_helper.py` - CLI tool for fast clipboard/file cookie renewal.
- `notebooklm_mcp_guide.md` - Complete MCP setup guide.

