#!/usr/bin/env python3
"""文字起こしテキストの表記ゆれを統一表に従って一括変換する。
Normalise terminology in the transcripts according to the unification table.

統一表: Transcripts/表記ゆれ統一表.md
Table:  Transcripts/表記ゆれ統一表.md
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

# 既定の対象ディレクトリ
# Default target directory
DEFAULT_ROOT = Path(__file__).resolve().parent / "Transcripts"

# SRT の連番行とタイムコード行（置換対象から除外する）
# Index and timecode lines of an SRT file (excluded from replacement)
SRT_INDEX = re.compile(r"^\d+$")
SRT_TIMECODE = re.compile(r"^\d{2}:\d{2}:\d{2}[,.]\d{3}\s*-->")

# 和文文字クラス（前後スペース除去の判定に使う）
# Japanese character class (used to decide where to strip spaces)
JA = r"ぁ-んァ-ヶ一-龥々ー、。（）「」"

# 置換ルール: (正規表現, 置換後, ラベル)
# 長い語から先に並べること。短い語を先に置換すると長い語が壊れる。
# Replacement rules: (regex, replacement, label).
# Longer terms must come first; replacing a shorter term first breaks the longer one.
RULES = [
    # --- 1. 製品・サービス名 / Product and service names ---
    (r"チャットGPT|シャットGPT", "ChatGPT", "ChatGPT"),
    (r"オープンAI", "OpenAI", "OpenAI"),
    (r"オープンルーターチャットモデル", "OpenRouter Chat Model", "OpenRouter Chat Model"),
    (r"オープンルーター", "OpenRouter", "OpenRouter"),
    (r"Tabilly|Tabby\s*Lee|TABIRI|タビリー|タビリ", "Tavily", "Tavily"),
    (r"スラック", "Slack", "Slack"),
    (r"ジェミニ", "Gemini", "Gemini"),
    (r"クロード", "Claude", "Claude"),
    (r"ノーション", "Notion", "Notion"),
    (r"Pathmo", "PASMO", "PASMO"),
    # 小文字で書き起こされた固有名詞・略語の大文字化
    # Capitalise proper nouns and acronyms that were transcribed in lower case
    (r"\bgmail\b", "Gmail", "Gmail"),
    (r"\bwikipedia\b", "Wikipedia", "Wikipedia"),
    (r"\bjavascript\b", "JavaScript", "JavaScript"),
    (r"\bjson\b", "JSON", "JSON"),
    (r"\bapi\b", "API", "API"),
    (r"\bai\b", "AI", "AI"),
    (r"\bllm\b", "LLM", "LLM"),
    (r"\bprd\b", "PRD", "PRD"),
    (r"\burl\b", "URL", "URL"),
    (r"\bok\b", "OK", "OK"),
    (r"\bpost\b", "POST", "POST"),

    # --- 2. n8n の画面用語・ノード名 / n8n UI terms and node names ---
    (r"クレデンシャル", "Credential", "Credential"),
    (r"認知症情報", "認証情報", "認証情報（誤変換）"),
    (r"エクスキュージョン", "Executions", "Executions"),
    (r"データテーブルズ|データテーブル", "Data Tables", "Data Tables"),
    (r"バックトゥキャンパス|バックトゥキャンバス", "Back to canvas", "Back to canvas"),
    (r"キャンパス", "キャンバス", "キャンバス（誤変換）"),
    (r"クリエイトワークフロー", "Create Workflow", "Create Workflow"),
    (r"ゲットスタート", "Get started", "Get started"),
    (r"スタートフリー", "Start free", "Start free"),
    (r"\badd first step\b", "Add first step", "Add first step"),
    (r"オンチャットメッセージ", "On chat message", "On chat message"),
    (r"オープンチャット", "Open chat", "Open chat"),
    (r"キーズ", "Keys", "Keys"),
    (r"Your\s*API\s*キー", "Your API Key", "Your API Key"),
    (r"キーネーム", "Key Name", "Key Name"),
    (r"サインアップ", "Sign up", "Sign up"),
    (r"アドオプション", "Add Option", "Add Option"),
    (r"インポートフロムファイル", "Import from File", "Import from File"),
    (r"インポートカール", "Import cURL", "Import cURL"),
    (r"ペーストザ、?カール、?コマンド、?ヒア", "Paste the cURL command here", "Paste the cURL command here"),
    (r"オールデータ", "All Data", "All Data"),
    (r"シンプルメモリ", "Simple Memory", "Simple Memory"),
    (r"チャットモデル", "Chat Model", "Chat Model"),
    (r"ソースオフォープロンプト", "Source for Prompt (User Message)", "Source for Prompt"),
    (r"AIエージェントノード", "AI Agentノード", "AI Agentノード"),
    (r"セーブ", "Save", "Save"),

    # --- 3. 一般技術用語 / General technical terms ---
    (r"カール", "cURL", "cURL"),
    (r"メモリー", "メモリ", "メモリ"),
    (r"システムプロンプト", "システムメッセージ", "システムメッセージ"),
    (r"ウェブリサーチ", "Webリサーチ", "Webリサーチ"),
    (r"ドキュメンテーション", "ドキュメント", "ドキュメント"),

    # --- 4. 誤変換 / Mis-transcriptions ---
    (r"コリアが追加できた", "トリガーが追加できた", "トリガー（誤変換）"),
    (r"どれくらいパイワーを", "どれくらい会話を", "会話（誤変換）"),
    (r"API機", "APIキー", "APIキー（誤変換）"),
    (r"Tavily\s*AIで強化された", "Tavily、AIで強化された", "Tavily、AI（読点補い）"),
    (r"n8nでもとか", "n8nデモとか", "n8nデモ（誤変換）"),

    # --- 5. 英数字と和文の間の半角スペースを除去 / Strip spaces between ASCII and Japanese ---
    (r"(?<=[" + JA + r"])[ 　]+(?=[A-Za-z0-9])", "", "和文→英数字の空白除去"),
    (r"(?<=[A-Za-z0-9])[ 　]+(?=[" + JA + r"])", "", "英数字→和文の空白除去"),
]

# 文脈によって判断が要るため自動変換しない語（検出して報告するだけ）
# Terms left untouched because they need a human decision (reported only)
REVIEW = [
    (r"認証情報", "Credential（画面名）か「認証情報」（概念）かを文脈で判断"),
    (r"保存", "ボタン名なら Save、動作の説明なら「保存」"),
    (r"テンプレート", "画面名なら Templates、一般名詞なら「テンプレート」"),
    (r"(?<!Google )スプレッドシート", "初出なら Google スプレッドシート"),
]

COMPILED = [(re.compile(p), r, label) for p, r, label in RULES]
COMPILED_REVIEW = [(re.compile(p), note) for p, note in REVIEW]


def convert_line(line):
    """1行を変換し、(変換後の行, {ラベル: 件数}) を返す。
    Convert one line and return (converted line, {label: count})."""
    hits = {}
    for pattern, repl, label in COMPILED:
        line, n = pattern.subn(repl, line)
        if n:
            hits[label] = hits.get(label, 0) + n
    return line, hits


def convert_text(text, is_srt):
    """本文行だけを変換する。SRT の連番行とタイムコード行はそのまま残す。
    Convert body lines only; SRT index and timecode lines are left as they are."""
    out, hits = [], {}
    for line in text.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        eol = line[len(body):]
        if is_srt and (SRT_INDEX.match(body) or SRT_TIMECODE.match(body)):
            out.append(line)
            continue
        converted, line_hits = convert_line(body)
        out.append(converted + eol)
        for label, n in line_hits.items():
            hits[label] = hits.get(label, 0) + n
    return "".join(out), hits


def review_text(text):
    """要確認語を数える。変換はしない。
    Count terms needing review; nothing is converted."""
    return {note: len(pattern.findall(text))
            for pattern, note in COMPILED_REVIEW
            if pattern.search(text)}


def display_name(path):
    """Google ドライブ由来のファイル名は濁点が分解されているので NFC に戻して表示する。
    File names from Google Drive have decomposed voiced marks; show them normalised to NFC."""
    return unicodedata.normalize("NFC", path.name)


def collect(paths):
    """対象ファイルを列挙する。
    Enumerate the target files."""
    files = []
    for path in paths:
        if path.is_dir():
            files += sorted(p for p in path.rglob("*") if p.suffix in (".txt", ".srt"))
        elif path.suffix in (".txt", ".srt"):
            files.append(path)
    return files


def main():
    # Windows のコンソール（cp932）でも和文が化けないよう UTF-8 で出力する
    # Print as UTF-8 so Japanese survives a cp932 console on Windows
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="*", type=Path,
                        help="対象のファイルまたはディレクトリ / target files or directories")
    parser.add_argument("--write", action="store_true",
                        help="実際に書き換える（既定は変換結果を表示するだけ）/ apply the changes (default: dry run)")
    parser.add_argument("--review", action="store_true",
                        help="自動変換しない要確認語も一覧する / also list the terms that need review")
    args = parser.parse_args()

    files = collect(args.paths or [DEFAULT_ROOT])
    if not files:
        print("対象ファイルが見つかりません / no target files found", file=sys.stderr)
        return 1

    total, changed_files = {}, 0
    for path in files:
        text = path.read_text(encoding="utf-8")
        converted, hits = convert_text(text, path.suffix == ".srt")
        if converted == text:
            continue
        changed_files += 1
        print("\n" + display_name(path))
        for label, n in sorted(hits.items(), key=lambda kv: -kv[1]):
            print("  %4d  %s" % (n, label))
            total[label] = total.get(label, 0) + n
        if args.write:
            path.write_text(converted, encoding="utf-8")

    mode = "書き換え済み / written" if args.write else "ドライラン / dry run"
    print("\n=== %s: %d ファイル, %d 箇所 ===" % (mode, changed_files, sum(total.values())))
    for label, n in sorted(total.items(), key=lambda kv: -kv[1]):
        print("  %4d  %s" % (n, label))
    if not args.write:
        print("\n--write を付けると実際に書き換えます / rerun with --write to apply")

    if args.review:
        print("\n=== 要確認（自動変換していない）/ needs review (not converted) ===")
        for path in files:
            found = review_text(path.read_text(encoding="utf-8"))
            if found:
                print("\n" + display_name(path))
                for note, n in found.items():
                    print("  %4d  %s" % (n, note))
    return 0


if __name__ == "__main__":
    sys.exit(main())
