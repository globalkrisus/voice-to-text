# Voice to Text

Rozpoznawanie mowy po polsku w czasie rzeczywistym z użyciem Vosk (Kaldi).

## Wymagania

- Python 3
- `vosk` (`pip install vosk`)
- `arecord` (ALSA utils)
- `xclip`

## Uruchomienie

```bash
python3 voice_to_text.py
```

## Obsługa

- **SPACJA** — włącz/wyłącz nasłuchiwanie (pauza kopiuje tekst do schowka)
- **Ctrl+C** — zakończenie programu

## Parametry

- `SAMPLE_RATE` = 16000 Hz
- `SILENCE_THRESHOLD` = 15 iteracji ciszy przed resetem

## Model

Katalog `model/` zawiera mały polski model Vosk (TDNN chain):

- WER: ~11-18% (zależnie od zbioru testowego)
- Format: Kaldi (am, graph, ivector, conf)

## Struktura

```
voice-to-text/
├── voice_to_text.py   # główny skrypt
└── model/             # model Vosk PL
    ├── am/            # model akustyczny
    ├── graph/         # grafy dekodowania (HCLr.fst, Gr.fst)
    ├── ivector/       # ekstrakcja i-wektorów
    └── conf/          # konfiguracja MFCC i dekodera
```
