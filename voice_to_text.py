#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import select
import tty
import termios
from vosk import Model, KaldiRecognizer

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")
SAMPLE_RATE = 16000
SILENCE_THRESHOLD = 15
GEOMETRY_FILE = os.path.expanduser("~/.config/voice-geometry")

def save_geometry():
    try:
        result = subprocess.run(
            ['xdotool', 'search', '--name', 'Voice to Text'],
            capture_output=True, text=True, timeout=2
        )
        window_id = result.stdout.strip().split('\n')[0]
        if window_id:
            geom = subprocess.run(
                ['xdotool', 'getwindowgeometry', '--shell', window_id],
                capture_output=True, text=True, timeout=2
            )
            lines = geom.stdout.strip().split('\n')
            width = next(l.split('=')[1] for l in lines if l.startswith('WIDTH'))
            height = next(l.split('=')[1] for l in lines if l.startswith('HEIGHT'))
            x = next(l.split('=')[1] for l in lines if l.startswith('X='))
            y = next(l.split('=')[1] for l in lines if l.startswith('Y='))
            os.makedirs(os.path.dirname(GEOMETRY_FILE), exist_ok=True)
            with open(GEOMETRY_FILE, 'w') as f:
                f.write(f"{width}x{height}+{x}+{y}")
    except Exception:
        pass

def main():
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model not found at {MODEL_PATH}")
        sys.exit(1)

    print("Ładowanie modelu...")
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)
    os.system('clear')

    print("Słucham... Naciśnij Ctrl+C aby zakończyć")
    print("SPACJA - włącz/wyłącz nasłuchiwanie")
    print("Stan: ZATRZYMANY - naciśnij SPACJĘ aby zacząć")
    print()

    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())
        proc = subprocess.Popen(
            ['arecord', '-f', 'S16_LE', '-r', str(SAMPLE_RATE), '-c', '1', '-q'],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )

        accumulated_text = ""
        silence_count = 0
        paused = True

        while True:
            if select.select([sys.stdin], [], [], 0)[0]:
                char = sys.stdin.read(1)
                if char == ' ':
                    paused = not paused
                    if paused:
                        if accumulated_text:
                            subprocess.run(['xclip', '-selection', 'clipboard'], input=accumulated_text.encode(), check=True)
                            print(f"\n⏸  ZATRZYMANY - skopiowano: {accumulated_text}")
                            accumulated_text = ""
                            silence_count = 0
                        else:
                            print("\n  ZATRZYMANY")
                    else:
                        print("\n▶  NASŁUCH - mów teraz")

            if not paused:
                data = proc.stdout.read(4000)
                if not data:
                    break

                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "").strip()
                    if text:
                        if accumulated_text:
                            accumulated_text += " " + text
                        else:
                            accumulated_text = text
                        silence_count = 0
                        print(f"Rozpoznano: {text}")
                    else:
                        silence_count += 1
                else:
                    partial = json.loads(recognizer.PartialResult())
                    partial_text = partial.get("partial", "").strip()
                    if partial_text:
                        silence_count = 0
                    else:
                        silence_count += 1

                if silence_count > SILENCE_THRESHOLD:
                    silence_count = 0
            else:
                proc.stdout.read(4000)

    except KeyboardInterrupt:
        print("\nZakończono")
        proc.terminate()
    finally:
        save_geometry()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

if __name__ == "__main__":
    main()
