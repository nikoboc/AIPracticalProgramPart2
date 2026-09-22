# AI Practical Skills Programme — Part 2 Curriculum

> 日本語版: [README.md](README.md)

This repository is used to build the **Part 2 curriculum of an AI practical skills programme**. The subject is **n8n**, a no-code workflow automation platform.

The goal is to **produce a new curriculum by reworking the existing lecture videos**.

## Current status

| Step | Status | Output |
|---|---|---|
| 1. Transcribe the existing videos | ✅ Done | `Transcripts/` |
| 2. Normalise inconsistent terminology | ✅ Done | `unify_terms.py`, `Transcripts/表記ゆれ統一表.md` |
| 3. Document what each video explains | ✅ Done | `第2部カリキュラム/既存動画/` |
| 4. Reconcile with current product specs | ✅ Done (researched 2026-09-21, verified against the live product 2026-09-22) | `第2部カリキュラム/最新仕様反映/` |
| 5. Structure and write the new curriculum | Not started | — |

## Layout

| Path | Contents |
|---|---|
| [`Transcripts/`](Transcripts/) | Transcripts of the existing videos (`.txt` / `.srt`) and the terminology table |
| [`第1部カリキュラム/`](第1部カリキュラム/) | Part 1 (AI fundamentals, 10 chapters). Assumed knowledge for Part 2 |
| [`第2部カリキュラム/既存動画/`](第2部カリキュラム/既存動画/) | What each existing video explains, **faithful to the transcripts**, with no corrections for current specs |
| [`第2部カリキュラム/最新仕様反映/`](第2部カリキュラム/最新仕様反映/) | The same material, **revised against the specs as of 2026-09-21** |
| `transcribe.py` | Transcription script |
| `unify_terms.py` | Bulk terminology normalisation script |

The curriculum files themselves are written in Japanese, as they are teaching material for Japanese-speaking learners.

## The existing videos (9 videos, about 1 hour 58 minutes)

The course builds a "pseudo ChatGPT" as a single workflow, adding one capability at a time. Each episode first lets learners experience a shortcoming, then adds the feature that removes it.

| # | Title | Length |
|---|---|---|
| 1 | Orientation | 03:24 |
| 2 | Basic operations | 09:25 |
| 3 | AI automation vs AI agents | 09:42 |
| 4 | Credentials | 12:01 |
| 5 | Memory and system messages | 08:12 |
| 6 | Tools and orchestration | 11:32 |
| 7 | APIs and HTTP requests | 20:42 |
| 8 | Sub-agents: concept and structure | 21:23 |
| 9 | A framework for building workflows | 20:54 |

## The biggest gap between the videos and current n8n

**The videos repeatedly stress that "n8n has no autosave, so press Save after every change". That operation no longer exists.**

- n8n 2.4 (13 January 2026) **introduced autosave and removed the Save button**.
- Every edit is autosaved as a **draft**. Going live is a separate action: the **Publish** button.

Every other discrepancy — Gateway credits, Data Tables reaching general availability, how API keys should be stored, the publish requirement for sub-workflows, and so on — is catalogued in
[`第2部カリキュラム/最新仕様反映/README.md`](第2部カリキュラム/最新仕様反映/README.md).

## Working notes

- `第2部カリキュラム/既存動画/` is a **faithful record of the transcripts**. Do not correct it against current specs.
- **n8n changes quickly.** Check [docs.n8n.io](https://docs.n8n.io) on the day, and record the date you checked along with the n8n version.
- See [CLAUDE.md](CLAUDE.md) for the full working guidance.
