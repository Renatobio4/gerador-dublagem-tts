[English Version](README.en.md)

# Gerador de Dublagem Automática com Legendas e TTS

Este projeto automatiza a criação de uma faixa de áudio de dublagem a partir de um arquivo de legenda (`.vtt`). Utilizando o motor de Text-to-Speech (TTS) **Kokoro**, o script gera uma narração sincronizada que respeita os tempos e pausas da legenda original, tornando-o ideal para dublar vídeos educacionais, tutoriais e outros conteúdos.

## Funcionalidades Principais

-   **Sincronização Precisa:** O áudio gerado respeita os tempos de início, fim e as pausas da legenda original.
-   **Aceleração Dinâmica:** Se uma fala é muito longa para o tempo alocado na legenda, o script acelera o clipe de áudio de forma inteligente para que ele se encaixe perfeitamente.
-   **Motor TTS Offline de Alta Qualidade:** Utiliza o **Kokoro (PyTorch)**, que oferece vozes com som natural sem depender de serviços online.
-   **Processamento em Lote:** Inclui um script para processar automaticamente uma pasta inteira de vídeos e legendas.
-   **Suporte a Múltiplos Idiomas (via Kokoro-TTS):** Permite gerar áudio em diferentes idiomas, desde que o texto da legenda já esteja no idioma desejado.

---

## Agradecimentos e Créditos

Este projeto só é possível graças ao trabalho incrível de desenvolvedores de código aberto. Faço questão de dar o devido crédito às ferramentas essenciais utilizadas:

-   **[Kokoro-TTS]:** O coração deste projeto. Um motor TTS fantástico baseado em PyTorch.
-   **[Pydub]:** Uma biblioteca essencial e poderosa para a manipulação de áudio em Python.
-   **[webvtt-py]:** Uma biblioteca robusta para a análise de arquivos de legenda WebVTT.
-   **[FFmpeg]:** A ferramenta fundamental que serve de backend para `pydub` e para toda a manipulação de mídia.

---

## Instalação

Siga os passos abaixo para configurar o ambiente e executar o projeto.

### 1. Pré-requisitos do Sistema
-   **Python 3.8+**
-   **Git**
-   **FFmpeg:** Essencial para a manipulação de áudio.
    -   **No Linux (Ubuntu/Debian/Mint):** `sudo apt-get update && sudo apt-get install ffmpeg`
    -   **No macOS (usando [Homebrew](https://brew.sh/)):** `brew install ffmpeg`
    -   **No Windows:** Recomenda-se instalar via [Chocolatey].

### 2. Configuração do Projeto
1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/Renatobio4/gerador-dublagem-tts.git
    cd gerador-dublagem-tts
    ```
    *(Desenvolvedores que desejam contribuir devem primeiro criar um [Fork](https://docs.github.com/pt/pull-requests/collaborating-with-pull-requests/working-with-forks/about-forks) do projeto).*

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Crie o ambiente
    python3 -m venv .venv

    # Ative o ambiente (Linux/macOS)
    source .venv/bin/activate
    
    # Ative o ambiente (Windows)
    .\.venv\Scripts\activate
    ```

3.  **Instale as dependências Python:**
    Abaixo estão duas opções. **`uv` é a recomendada por ser mais rápida e moderna.**

    -   **Opção A (Recomendado): Usando `uv`**
        `uv` é um instalador de pacotes extremamente rápido, compatível com `pip`.
        ```bash
        # Instale o uv (só precisa fazer uma vez)
        pip install uv

        # Use o uv para instalar as dependências
        uv pip install -r requirements.txt
        ```

    -   **Opção B: Usando `pip` padrão**
        ```bash
        pip install -r requirements.txt
        ```

---

## Como Usar

> **Nota Importante:** Este script **não traduz** o texto. Ele sintetiza o texto *existente* na legenda em áudio. A legenda de entrada já deve estar no idioma da dublagem desejada.

O projeto oferece dois modos de uso: processar um único arquivo ou uma pasta inteira.

### Modo 1: Processar um Único Arquivo (`gerador_de_dublagem.py`)

**Uso:** `python3 gerador_de_dublagem.py [LEGENDA_ENTRADA] [ARQUIVO_SAIDA] --video_entrada [VIDEO_ENTRADA]`

```bash
# Exemplo completo: gera o áudio e adiciona ao vídeo
python3 gerador_de_dublagem.py "legenda.vtt" "video_final.mp4" --video_entrada "video_original.mp4"
```

### Modo 2: Processar Vários Vídeos em Lote (`processar_lote.py`)

**Uso:** `python3 processar_lote.py [PASTA_DE_VIDEOS]`

```bash
# Exemplo: processa todos os pares de vídeo/legenda na pasta "meus_videos"
python3 processar_lote.py "meus_videos/"
```

### Opções de Customização (para ambos os scripts)

Adicione estas flags ao final de qualquer comando para alterar o resultado:

-   `--lang [CODIGO]`: Altera o idioma do TTS. Ex: `a` (Inglês), `e` (Espanhol), `p` (Português).
-   `--voz [NOME_VOZ]`: Altera a voz usada. Consulte o [Voices.md do Kokoro](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md) para a lista completa.
-   `--max_aceleracao [NUMERO]`: Altera o fator máximo de aceleração (ex: `1.8`).

**Exemplo com customização (voz masculina em inglês):**
```bash
python3 processar_lote.py "videos_em_ingles/" --lang a --voz am_george
```
