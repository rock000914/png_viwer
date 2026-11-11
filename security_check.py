#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""コミット前の整合性ガード。

`git add` 済みの変更に対して `git commit` したとき、`.githooks/pre-commit` から
呼び出される。悪意ある、あるいは誤って紛れ込んだ「実行系コード / 外部通信 /
秘密情報」を検出するとコミットを中断する。

有効化（初回のみ・クローン毎に必要）:
    git config core.hooksPath .githooks

このアプリが元から持つ正当なコード（re.compile, ctypes, Qt の dlg.exec(),
shell=False の subprocess.Popen など）は検出しないよう作ってある。
許可する通信先を増やしたい場合は ALLOWED_HOSTS に追加する。
"""
from __future__ import annotations

import re
import subprocess
import sys

# コンソールで日本語が化けても判定(OK/BLOCKED)が読めるよう UTF-8 に寄せ、
# 符号化エラーではクラッシュしないようにする。
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# 自己検査による誤検知を防ぐため、これらはスキャン対象から除外
SELF_EXCLUDE = {"security_check.py", ".githooks/pre-commit", "SECURITY.md"}

# ---- *.py 専用: 実行系コードのルール (正規表現, 説明) --------------------
# Qt の "xxx.exec()" は直前が "." なので bare exec 規則には当たらない。
PY_RULES = [
    (re.compile(r"(?<![\w.])\bexec\s*\("), "組み込み exec() の使用"),
    (re.compile(r"(?<![\w.])\beval\s*\("), "組み込み eval() の使用"),
    (re.compile(r"os\.system\s*\("), "os.system() の使用"),
    (re.compile(r"os\.popen\s*\("), "os.popen() の使用"),
    (re.compile(r"shell\s*=\s*True"), "shell=True (コマンド注入のリスク)"),
    (re.compile(r"pickle\.loads?\s*\("), "pickle デシリアライズ (RCEのリスク)"),
    (re.compile(r"marshal\.loads?\s*\("), "marshal ロード (実行コード混入のリスク)"),
    (re.compile(r"\b__import__\s*\("), "動的 __import__()"),
    (re.compile(r"\brunpy\."), "runpy による動的実行"),
    (re.compile(r"codecs\.decode"), "codecs.decode 難読化"),
    (re.compile(r"base64\.(b64decode|decodebytes)"), "base64 デコード (このアプリでは不要)"),
    (re.compile(r"getattr\s*\(\s*__builtins__"), "ビルトイン改変 (回避/エスケープ)"),
]

# *.py に出現してよい通信先ホスト。それ以外のホスト向けURLは弾く。
ALLOWED_HOSTS = {"civitai.com", "www.w3.org"}
URL_RE = re.compile(r"https?://([A-Za-z0-9._-]+)")

# ---- 全テキスト共通: 秘密情報のルール (正規表現, 説明) --------------------
SECRET_RULES = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "秘密鍵ブロック"),
    (re.compile(r"\bgh[pousr]_[0-9A-Za-z]{20,}\b"), "GitHub トークン"),
    (re.compile(r"\bgithub_pat_[0-9A-Za-z_]{20,}\b"), "GitHub 細粒度トークン"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS アクセスキー"),
    (re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,}\b"), "Slack トークン"),
    (
        re.compile(
            r"(?i)(api[_-]?key|secret|passwd|password|token)\s*[:=]\s*['\"][^'\"\s]{16,}['\"]"
        ),
        "長い機密値のリテラル代入 (本物の鍵の疑い)",
    ),
]


def _run(args):
    return subprocess.run(args, capture_output=True)


def _staged_files():
    out = _run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM", "-z"]
    )
    if out.returncode != 0:
        sys.stderr.write("[security_check] git diff を実行できません\n")
        sys.exit(1)
    return [f for f in out.stdout.decode("utf-8", "replace").split("\x00") if f]


def _staged_blob(path):
    out = _run(["git", "show", f":{path}"])
    if out.returncode != 0:
        return None
    return out.stdout


def check():
    findings = []
    for path in _staged_files():
        if path in SELF_EXCLUDE:
            continue
        raw = _staged_blob(path)
        if raw is None:
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue  # バイナリはスキップ
        is_py = path.endswith(".py")
        for lineno, line in enumerate(text.splitlines(), 1):
            if is_py:
                for rx, why in PY_RULES:
                    if rx.search(line):
                        findings.append((path, lineno, "実行系", why, line.strip()))
                for m in URL_RE.finditer(line):
                    host = m.group(1).lower()
                    if host not in ALLOWED_HOSTS:
                        findings.append(
                            (path, lineno, "外部通信", f"許可外ホスト: {host}", line.strip())
                        )
            for rx, why in SECRET_RULES:
                if rx.search(line):
                    findings.append((path, lineno, "機密情報", why, line.strip()))
    return findings


def main():
    findings = check()
    if not findings:
        print("[security_check] OK - 整合性ガード通過（問題なし）")
        return 0
    print(
        "[security_check] BLOCKED - コミット前に以下の項目を検出し、中断しました:\n",
        file=sys.stderr,
    )
    for path, lineno, cat, why, snippet in findings:
        print(
            f"  - {path}:{lineno}  [{cat}] {why}\n      {snippet[:100]}",
            file=sys.stderr,
        )
    print(
        "\n意図した変更なら該当行を取り除いてください。通信先が増えて正当な場合は\n"
        "security_check.py の ALLOWED_HOSTS に追加します。",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
