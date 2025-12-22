#!/usr/bin/env python3
import sys

def make_payload(path: str = "payload.bin", selector: int | None = None) -> None:
    """
    Generate a payload for kDeviceNDibTemplate.

    - The template uses only {{BYTES:img:256}}.
    - We therefore need at least 256 bytes in the input.
    - If your harness uses data[0] as a template selector, pass `selector`
      and it will be prepended as the first byte. Then you must remember to
      call ApplyPdfTemplate(template, data+1, size-1) on the C++ side.
    """
    IMG_BYTES = 256

    # Simple deterministic pattern: 0,1,2,...,255
    img = bytes(range(IMG_BYTES))

    if selector is None:
        data = img
    else:
        if not (0 <= selector <= 255):
            raise ValueError("selector must be 0..255")
        data = bytes([selector]) + img

    with open(path, "wb") as f:
        f.write(data)

    print(f"Wrote {len(data)} bytes to {path}")

if __name__ == "__main__":
    # Usage:
    #   python3 make_payload.py          -> payload.bin (256 bytes)
    #   python3 make_payload.py 7        -> payload.bin (257 bytes, first=7)
    if len(sys.argv) > 1:
        sel = int(sys.argv[1])
        make_payload(selector=sel)
    else:
        make_payload()