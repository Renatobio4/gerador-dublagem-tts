[Versão em Português](README.md)

# Automatic Dubbing Generator from Subtitles and TTS

This project automates the creation of a dubbed audio track from a subtitle file (`.vtt`). Using the **Kokoro** Text-to-Speech (TTS) engine, the script generates a synchronized narration that respects the original subtitle's timings and pauses, making it ideal for dubbing educational videos, tutorials, and other content.

## Key Features

-   **Precise Synchronization:** The generated audio respects the start times, end times, and pauses of the original subtitle file.
-   **Dynamic Speed-Up:** If a line of dialogue is too long for the time allocated in the subtitle, the script intelligently speeds up the audio clip to make it fit perfectly.
-   **High-Quality Offline TTS Engine:** Utilizes **Kokoro (PyTorch)**, which offers natural-sounding voices without relying on online services.
-   **Batch Processing:** Includes a script to automatically process an entire folder of videos and subtitles.
-   **Multi-Language Support (via Kokoro-TTS):** Allows generating audio in different languages, provided the subtitle text is already in the desired language.

---

## Acknowledgments and Credits

This project is only possible thanks to the incredible work of open-source developers. Full credit goes to the essential tools used:

-   **[Kokoro-TTS]:** The heart of this project. A fantastic PyTorch-based TTS engine.
-   **[Pydub]:** A powerful and essential library for audio manipulation in Python.
-   **[webvtt-py]:** A robust library for parsing WebVTT subtitle files.
-   **[FFmpeg]:** The fundamental tool that serves as the backend for `pydub` and all media manipulation.

---

## Installation

Follow the steps below to set up the environment and run the project.

### 1. System Prerequisites
-   **Python 3.8+**
-   **Git**
-   **FFmpeg:** Essential for audio manipulation.
    -   **On Linux (Ubuntu/Debian/Mint):** `sudo apt-get update && sudo apt-get install ffmpeg`
    -   **On macOS (using [Homebrew](https://brew.sh/)):** `brew install ffmpeg`
    -   **On Windows:** It is recommended to install via [Chocolatey]

### 2. Project Setup
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Renatobio4/gerador-dublagem-tts.git
    cd gerador-dublagem-tts
    ```
    *(Developers who wish to contribute should first [Fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/about-forks) the project).*

2.  **Create and activate a virtual environment:**
    ```bash
    # Create the environment
    python3 -m venv .venv

    # Activate (Linux/macOS)
    source .venv/bin/activate
    
    # Activate (Windows)
    .\.venv\Scripts\activate
    ```

3.  **Install Python dependencies:**
    Two options are provided below. **`uv` is recommended as it is faster and more modern.**

    -   **Option A (Recommended): Using `uv`**
        `uv` is an extremely fast package installer, compatible with `pip`.
        ```bash
        # Install uv (only needs to be done once)
        pip install uv

        # Use uv to install the dependencies
        uv pip install -r requirements.txt
        ```

    -   **Option B: Using standard `pip`**
        ```bash
        pip install -r requirements.txt
        ```

---

## How to Use

> **Important Note:** This script **does not translate** text. It synthesizes the *existing* text in the subtitle file into audio. The input subtitle must already be in the desired language for the dubbing.

The project offers two modes of operation: processing a single file or an entire folder.

### Mode 1: Process a Single File (`gerador_de_dublagem.py`)

**Usage:** `python3 gerador_de_dublagem.py [INPUT_SUBTITLE] [OUTPUT_FILE] --video_entrada [INPUT_VIDEO]`

```bash
# Full example: generates the audio and adds it to the video
python3 gerador_de_dublagem.py "subtitle.vtt" "final_video.mp4" --video_entrada "original_video.mp4"
```

### Mode 2: Process Multiple Videos in Batch (`processar_lote.py`)

**Usage:** `python3 processar_lote.py [VIDEOS_FOLDER]`

```bash
# Example: processes all video/subtitle pairs in the "my_videos" folder
python3 processar_lote.py "my_videos/"
```

### Customization Options (for both scripts)

Add these flags to the end of any command to customize the output:

-   `--lang [CODE]`: Changes the TTS language. E.g., `a` (American English), `e` (Spanish), `p` (Portuguese).
-   `--voz [VOICE_NAME]`: Changes the voice used. Refer to the [Kokoro Voices.md](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md) for a complete list.
-   `--max_aceleracao [NUMBER]`: Changes the maximum speed-up factor (e.g., `1.8`).

**Example with customization (American English male voice):**
```bash
python3 processar_lote.py "english_videos/" --lang a --voz am_george
```
