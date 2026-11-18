#!/usr/bin/env python3
"""
Send an emotion code to the pendant over its Wi-Fi hotspot.

This is the last step of the real pipeline (Muse EEG + camera -> Jetson ->
pendant). It is also handy for testing the pendant without any EEG hardware.

  python3 send_code.py 1          # Happy
  python3 send_code.py 4          # Sad
  python3 send_code.py 99         # caregiver help
  python3 send_code.py --demo     # cycle through every emotion

The computer must be connected to the "Emotion_Pendant" Wi-Fi network.
"""
import sys
import time
import urllib.error
import urllib.request

PENDANT = "http://192.168.4.1"      # ESP32 soft-AP default address

CODES = {
    1: "Happy", 2: "Joy", 3: "Wink", 4: "Sad", 5: "Surprised", 6: "Dizzy",
    7: "Worried", 8: "Love", 9: "Angry", 10: "Silly", 11: "Excited",
    12: "Sick", 13: "Neutral", 99: "HELP",
}


def send_code(code: int, timeout: float = 5.0) -> str:
    with urllib.request.urlopen(f"{PENDANT}/code?value={code}", timeout=timeout) as r:
        return r.read().decode()


def main() -> None:
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == "--demo":
        codes = [c for c in CODES if c != 99]
    else:
        codes = [int(sys.argv[1])]

    for code in codes:
        try:
            reply = send_code(code)
            print(f"code {code:>2} ({CODES.get(code, '?')}) -> pendant says: {reply}")
        except (urllib.error.URLError, OSError) as e:
            print(f"could not reach pendant at {PENDANT}: {e}")
            sys.exit(2)
        if len(codes) > 1:
            time.sleep(2)


if __name__ == "__main__":
    main()
