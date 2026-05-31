# Voice to Text — kontekst dla AI

## Stos technologiczny

- Python 3
- Vosk (biblioteka rozpoznawania mowy, wrapper nad Kaldi)
- subprocess: `arecord` (przechwytywanie audio z ALSA), `xclip` (kopiowanie do schowka X11)

## Uruchomienie

```bash
python3 voice_to_text.py
```

Brak testów, lintera i typechecka.

### Skrót klawiszowy (systemowy)

- **Ctrl+Shift+W** uruchamia `/home/krisus/.local/bin/voice`
- Skrypt otwiera `gnome-terminal` z tytułem "Voice to Text" i uruchamia `voice_to_text.py`
- Jeśli aplikacja już działa, aktywuje istniejące okno (przez `xdotool`)
- Logi: `/tmp/voice.log`

## Struktura

- `voice_to_text.py` — jedyny plik źródłowy, cała logika aplikacji
- `model/` — binarny model Vosk PL (Kaldi), nie edytować ręcznie
  - `am/` — model akustyczny (final.mdl)
  - `graph/` — grafy dekodowania (HCLr.fst, Gr.fst, word_boundary.int)
  - `ivector/` — ekstrakcja cech i-wektorowych
  - `conf/` — konfiguracja MFCC i parametrów dekodera

## Konwencje

- UI w języku polskim
- Brak komentarzy w kodzie
- Stałe konfiguracyjne na górze pliku (MODEL_PATH, SAMPLE_RATE, SILENCE_THRESHOLD)

## Znane ograniczenia

- Hardcoded ścieżka do modelu (względem lokalizacji skryptu)
- Brak konfiguracji użytkownika (np. wybór urządzenia audio, języka)
- Brak obsługi błędów dla brakujących zależności systemowych (arecord, xclip)
- `SILENCE_THRESHOLD` nie jest skalowalny (zależy od szybkości pętli, nie od czasu)
