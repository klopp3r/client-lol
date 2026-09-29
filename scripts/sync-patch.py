#!/usr/bin/env python3
"""Синхронизирует fork.patch с копией, вшитой в workflow.

Воркфлоу применяет не файл fork.patch из репозитория, а base64, вшитый
в YAML: checkout тянет только upstream, отдельного репозитория с патчем
рядом нет. Из-за этого файл и встроенная копия расходились, и сборки
уходили с кодом, которого нет в патче. Этот скрипт вшивает актуальный
патч, а шаг в workflow сверяет их по sha256 и останавливает сборку при
расхождении.

Запуск: python3 scripts/sync-patch.py
"""

import argparse
import base64
import hashlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PATCH = ROOT / "fork.patch"
WORKFLOW = ROOT / ".github" / "workflows" / "build-apk.yml"

PATTERN = re.compile(r"echo '([A-Za-z0-9+/=]+)' \| base64 -d > fork\.patch")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="только проверить расхождение, ничего не менять")
    args = parser.parse_args()
    if not PATCH.is_file():
        print("нет fork.patch")
        return 1
    data = PATCH.read_bytes()
    text = WORKFLOW.read_text(encoding="utf-8")
    match = PATTERN.search(text)
    if not match:
        print("в workflow не найдено место для base64")
        return 1
    embedded = base64.b64decode(match.group(1)) if match.group(1) else b""
    if embedded == data:
        print("уже синхронно: %d байт, sha %s" % (len(data), hashlib.sha256(data).hexdigest()[:12]))
        return 0
    if args.check:
        print("расхождение: вшито %d байт (sha %s), в файле %d байт (sha %s)"
              % (len(embedded), hashlib.sha256(embedded).hexdigest()[:12],
                 len(data), hashlib.sha256(data).hexdigest()[:12]))
        return 2
    WORKFLOW.write_text(
        text[: match.start(1)] + base64.b64encode(data).decode("ascii") + text[match.end(1) :],
        encoding="utf-8",
    )
    print("вшит актуальный патч: %d байт, sha %s" % (len(data), hashlib.sha256(data).hexdigest()[:12]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
