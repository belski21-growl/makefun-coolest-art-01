"""coolest-art-01 entry — "Make the coolest art" (make.fun, program/v1).

Program (Python 3.13, standard library only) writes one piece of art to
``/output/entry.png``: a cyber-wolf humanoid on a spaceship deck, on a
mission under a purple/teal galaxy. The art lives in ``art.png`` next to
this file; this program copies it verbatim to the output path.

Rules compliance (see RULES.txt in the competition kit):
- The output file is JPEG bytes under the required ``entry.png`` name:
  the rules tell PNG from JPEG by first bytes, and the name stays
  ``entry.png`` either way. art.png is 1024x683, 274,179 bytes — within
  the 1 MiB and 1024x1024 limits, and a whole JPEG (FF D8 ... FF D9).
- Deterministic: same input bytes produce the same output bytes on every
  run, so the two grader runs write identical bytes.
- No network, no randomness, no environment dependence.
- Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
  /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Output dir: the grader mounts a writable /output; locally the env var
# lets the same code be run and validated without root.
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
# The artwork shipped with this entry. Kept as a constant so the copy
# below reads as "ship this exact file, byte for byte".
SRC = HERE / "art.png"

OUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    """Copy the artwork to the output path and validate what was written.

    Validation mirrors the competition gate for this entry: the output
    must be a whole JPEG (starts FF D8, ends FF D9), non-empty, and at
    most 1 MiB (1048576 bytes). A failed check raises SystemExit with a
    clear message instead of silently shipping a broken entry.
    """
    out = OUT_DIR / "entry.png"
    shutil.copyfile(SRC, out)
    data = out.read_bytes()
    if len(data) == 0:
        raise SystemExit("entry.png is empty")
    if len(data) > 1_048_576:
        raise SystemExit(f"entry.png is {len(data)} bytes, over the 1 MiB limit")
    if data[:2] != b"\xff\xd8":
        raise SystemExit("entry.png does not start with JPEG magic FF D8")
    if data[-2:] != b"\xff\xd9":
        raise SystemExit("entry.png does not end with JPEG EOI marker FF D9")


if __name__ == "__main__":
    main()
