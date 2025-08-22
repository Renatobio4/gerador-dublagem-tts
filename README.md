# Gerador de Dublagem Automática com Legendas e TTS

Este projeto automatiza a criação de uma faixa de áudio de dublagem a partir de um arquivo de legenda (`.vtt`). Utilizando o motor de Text-to-Speech (TTS) **Kokoro**, o script gera uma narração sincronizada que respeita os tempos e pausas da legenda original, tornando-o ideal para dublar vídeos educacionais, tutoriais e outros conteúdos.

## Funcionalidades Principais

-   **Sincronização Precisa:** O áudio gerado respeita os tempos de início, fim e as pausas da legenda original.
-   **Aceleração Dinâmica:** Se uma fala é muito longa para o tempo alocado na legenda, o script acelera o clipe de áudio de forma inteligente para que ele se encaixe perfeitamente, garantindo que a duração final seja idêntica à do vídeo.
-   **Motor TTS Offline de Alta Qualidade:** Utiliza o **Kokoro (PyTorch)**, que oferece vozes com som natural sem depender de serviços online.
-   **Flexibilidade:** Permite a escolha de diferentes vozes e idiomas através de argumentos de linha de comando.
-   **Robusto:** Lida com arquivos VTT comuns que não possuem o cabeçalho `WEBVTT` obrigatório.

---

## Agradecimentos e Créditos

Este projeto só é possível graças ao trabalho incrível de desenvolvedores de código aberto. Faço questão de dar o devido crédito às ferramentas essenciais utilizadas:

-   **[Kokoro-TTS]** O coração deste projeto. Um motor TTS fantástico baseado em PyTorch.
-   **[Pydub]** Uma biblioteca essencial e poderosa para a manipulação de áudio em Python.
-   **[webvtt-py]** Uma biblioteca robusta para a análise de arquivos de legenda WebVTT.
-   **[FFmpeg]** A ferramenta fundamental que serve de backend para `pydub` e para toda a manipulação de mídia.

---

## Instalação

Siga os passos abaixo para configurar o ambiente e executar o projeto.

### 1. Pré-requisitos do Sistema
-   **Python 3.8+**
-   **Git**
-   **FFmpeg:** Essencial para a manipulação de áudio.

    -   **No Linux (Ubuntu/Debian/Mint):**
        ```bash
        sudo apt-get update && sudo apt-get install ffmpeg
        ```
    -   **No macOS (usando [Homebrew](https://brew.sh/)):**
        ```bash
        brew install ffmpeg
        ```
    -   **No Windows:**
        Recomenda-se instalar via [Chocolatey](https://chocolatey.org/) (`choco install ffmpeg`) ou baixar o executável do site oficial e adicionar ao PATH do sistema.

### 2. Configuração do Projeto
1.  **Clone este repositório:**


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
    ```bash
    pip install -r requirements.txt
    ```

---

## Como Usar

O script é executado via linha de comando. A estrutura básica é:

```bash
python3 gerador_de_dublagem.py "caminho/para/legenda.vtt" "caminho/para/saida.mp3" [OPÇÕES]
```

### Exemplos de Uso

**1. Gerar dublagem com voz feminina em português (padrão):**
```bash
python3 gerador_de_dublagem.py "minha_legenda.vtt" "audio_dublado_fem.mp3"
```

**2. Gerar dublagem com voz masculina em português:**
A voz masculina em PT-BR se chama `pm_juca`.
```bash
python3 gerador_de_dublagem.py "minha_legenda.vtt" "audio_dublado_masc.mp3" --voz pm_juca
```

**3. Aumentar a aceleração para vídeos muito rápidos:**
Se o locutor original fala muito rápido, pode ser necessário permitir uma aceleração mais agressiva.
```bash
python3 gerador_de_dublagem.py "legenda_rapida.vtt" "audio_muito_rapido.mp3" --max_aceleracao 2.0
```

---

## Etapa Final: Adicionando o Áudio ao Vídeo

Após gerar o arquivo `.mp3`, utilize o **FFmpeg** para combiná-lo com seu arquivo de vídeo.

**Para adicionar o áudio como uma SEGUNDA faixa (mantendo a original):**
```bash
ffmpeg -i "video_original.mp4" -i "audio_dublado_fem.mp3" -map 0:v:0 -map 0:a:0 -map 1:a:0 -c:v copy -c:a copy "video_final_com_dublagem.mp4"
```

**Para SUBSTITUIR o áudio original pelo novo:**
```bash
ffmpeg -i "video_original.mp4" -i "audio_dublado_fem.mp3" -map 0:v:0 -map 1:a:0 -c:v copy -c:a copy "video_final_dublado.mp4"
```
