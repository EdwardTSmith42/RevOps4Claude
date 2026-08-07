# Gotchas — read before your first page edit

These are the failure modes that actually happened. They cost real rework.

## 1. Images last — the API strips uploaded media (the big one)

Editing a Confluence page through the Atlassian MCP by fetching
`contentFormat: "html"` and re-sending the body **does not preserve a
user-uploaded image**. The media node isn't round-tripped, so the update
silently deletes the embedded picture. Confirmed by checking both the html and
the **adf** fetch afterward (adf always shows real media as `"type":"media"` /
`"mediaSingle"` nodes) — zero media, only text placeholder panels remained.

Rules:
- Do **all** programmatic body edits FIRST. Have the human drag in every image
  **last**. After images are in, do not touch the body again.
- While building, leave clear text placeholders ("📸 drag the EPIC graphic here")
  where images go, and tell the manager to fill them from an exemplar page (media
  can't be copied page-to-page via the API either).
- If the manager already added an image and you must keep editing: warn them it
  will be stripped. Recovery is easy — the image usually remains a **page
  attachment** (editor → Insert → Files → Attached, re-place it) or lives in
  **Page History**; no re-upload needed.
- To authoritatively check whether a page currently has a real image, fetch
  `contentFormat: "adf"` and look for `"type":"media"`/`"mediaSingle"`/`"mediaGroup"`.

## 2. Edit surgically — never full-body from your own copy

Once a page exists (and especially once anyone has edited it manually), every
change must **fetch the live page and replace only the target section/table/
region**, preserving the rest byte-for-byte. Regenerating the whole body from
your own authored copy will silently drop the manager's manual edits and images.
Delegating a bounded edit to a subagent ("fetch live, swap only this table for
this exact HTML, preserve everything else, confirm images intact") keeps the big
body out of your context and makes the change auditable.

## 3. HTML+ syntax that works

`updateConfluencePage`/`createConfluencePage` with `contentFormat: "html"` accept
Confluence HTML+ (data-type nodes, not CSS classes). Reliable patterns:
- Panels: `<div data-type="panel-info|panel-note|panel-warning|panel-success|panel-error"><p>…</p></div>`
- Task list: `<ul data-type="task-list"><li data-type="task-item"><input type="checkbox"/> text</li></ul>` (items are inline-only)
- Collapsible: `<details><summary>Title</summary><p>…</p></details>` (great for reference-library entries)
- Two-column: `<section data-type="layout-two-equal"><div data-type="column">…</div><div data-type="column">…</div></section>`
- Tables round-trip fine; use `data-layout="wide"` for the weekly grids.
Constraints: panels can't contain tables/expands; list items can't contain
headings/tables/panels; don't nest a table inside a table. Invalid nesting is
rejected with a descriptive error — retry.

## 4. Large tool results

`getConfluencePage` on a big page can exceed the inline limit and get saved to a
file. Don't try to read that file linearly — have a subagent extract just what
you need (a section, the jargon table) and return it.

## 5. Page = source of truth once the manager edits

After the manager makes manual time/timezone/name corrections, **your notes are
stale**. Before sending invites or doing a review, re-read the live page and work
from it — do not send invites from remembered times.

## 6. Connector notes

- The Atlassian MCP emits a harmless HTTP+SSE deprecation notice on every call;
  ignore it (or relay once).
- M365/Outlook and other connectors occasionally drop and reconnect mid-session;
  if a tool "isn't available," re-load it via ToolSearch before concluding it's gone.
- `find_available_time` may report the organizer's calendar time zone as **UTC**;
  convert deliberately (see calendar reference) — a wrong conversion here is the
  classic source of "the times were all wrong."
