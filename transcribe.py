"""動画を完全オフラインで文字起こしする (faster-whisper / CUDA)。

使い方:
    .venv/Scripts/python.exe transcribe.py                  # OriginalVideo 配下を全部
    .venv/Scripts/python.exe transcribe.py path/to/one.mp4  # 単体
"""
import os
import sys
import pathlib
import time

# nvidia の pip パッケージに入っている cuBLAS / cuDNN の DLL を先に登録する
_NVIDIA = pathlib.Path(sys.prefix) / "Lib" / "site-packages" / "nvidia"
for _p in _NVIDIA.glob("*/bin"):
    os.add_dll_directory(str(_p))

from faster_whisper import WhisperModel

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "OriginalVideo"
OUT = ROOT / "Transcripts"
MODEL = os.environ.get("WHISPER_MODEL", "large-v3")
EXTS = {".mp4", ".mkv", ".mov", ".avi", ".webm", ".m4a", ".mp3", ".wav"}

# 用語ヒント。faster-whisper では initial_prompt は condition_on_previous_text=False
# だと最初の30秒ウィンドウ後に捨てられる (transcribe.py の prompt_reset_since) ため、
# 毎ウィンドウ注入される hotwords 側に文章形式で入れる。
#
# 実測での重要な注意: 用語を詰め込むほど薄まって効かなくなる。19語のリストでは
# 誤変換が1件も直らず、1文+10語程度に絞ると直った。増やしたくなったら短く保つこと。
HOTWORDS = (
    "n8n のワークフロー構築講座です。n8n、織田信長、Wikipedia、Gmail、"
    "ノード、AIエージェント、Credential、Webhook、HTTPリクエスト を扱います。"
)

# hotwords で拾いきれなかった分の保険
FIXUPS = [
    ("NATN", "n8n"), ("NATO", "n8n"), ("ナットエン", "n8n"),
    ("エヌエイトエヌ", "n8n"), ("N8N", "n8n"), ("ネイトエン", "n8n"),
    ("小田信長", "織田信長"), ("小野信長", "織田信長"),
]


def fixup(text: str) -> str:
    for before, after in FIXUPS:
        text = text.replace(before, after)
    return text


def fmt_ts(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def transcribe(model: WhisperModel, path: pathlib.Path) -> None:
    rel = path.relative_to(SRC) if SRC in path.parents else pathlib.Path(path.name)
    dest = OUT / rel.parent
    dest.mkdir(parents=True, exist_ok=True)
    txt_path = dest / (path.stem + ".txt")
    srt_path = dest / (path.stem + ".srt")
    if txt_path.exists() and srt_path.exists():
        print(f"[skip] {rel}")
        return

    print(f"[run ] {rel}", flush=True)
    t0 = time.time()
    segments, info = model.transcribe(
        str(path),
        language="ja",
        beam_size=5,
        # VAD は無音区間の保護も兼ねる。切ると無音部で hotwords の文字列が
        # そのまま出力に混入することを確認済み。False にしないこと。
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500},
        condition_on_previous_text=False,  # 日本語のループ暴走を防ぐ
        hotwords=HOTWORDS,
    )

    lines, srt = [], []
    for i, seg in enumerate(segments, 1):
        text = fixup(seg.text.strip())
        lines.append(text)
        srt.append(f"{i}\n{fmt_ts(seg.start)} --> {fmt_ts(seg.end)}\n{text}\n")
        pct = min(seg.end / info.duration * 100, 100) if info.duration else 0
        print(f"\r       {pct:5.1f}%  {time.time() - t0:6.0f}s", end="", flush=True)

    txt_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    srt_path.write_text("\n".join(srt), encoding="utf-8")
    dur = time.time() - t0
    speed = info.duration / dur if dur else 0
    print(f"\r[done] {rel}  {info.duration/60:.1f}分 → {dur:.0f}秒 ({speed:.0f}x realtime)")


def main() -> None:
    args = [pathlib.Path(a) for a in sys.argv[1:]]
    files = args or sorted(p for p in SRC.rglob("*") if p.suffix.lower() in EXTS)
    if not files:
        sys.exit(f"動画が見つかりません: {SRC}")

    print(f"モデル {MODEL} を読み込み中 (初回のみダウンロード)…", flush=True)
    model = WhisperModel(MODEL, device="cuda", compute_type="float16")
    print(f"対象 {len(files)} ファイル\n")
    for f in files:
        transcribe(model, f)


if __name__ == "__main__":
    main()
