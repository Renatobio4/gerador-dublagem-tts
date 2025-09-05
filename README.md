# Gerador de Dublagem Automática com Legendas e TTS

Este projeto automatiza a criação de uma faixa de áudio de dublagem a partir de um arquivo de legenda (`.vtt`). Utilizando o motor de Text-to-Speech (TTS) **Kokoro**, o script gera uma narração sincronizada que respeita os tempos e pausas da legenda original, tornando-o ideal para dublar vídeos educacionais, tutoriais e outros conteúdos.

O projeto inclui ferramentas tanto para processar um único arquivo quanto para automatizar a dublagem de uma pasta inteira de vídeos.

## Funcionalidades Principais

-   **Sincronização Precisa:** O áudio gerado respeita os tempos de início, fim e as pausas da legenda original.
-   **Aceleração Dinâmica:** Se uma fala é muito longa para o tempo alocado na legenda, o script acelera o clipe de áudio de forma inteligente para que ele se encaixe perfeitamente.
-   **Motor TTS Offline de Alta Qualidade:** Utiliza o **Kokoro (PyTorch)**, que oferece vozes com som natural sem depender de serviços online.
-   **Processamento em Lote:** Inclui um script para processar automaticamente uma pasta inteira de vídeos e legendas.
-   **Flexibilidade:** Permite a escolha de diferentes vozes e idiomas através de argumentos de linha de comando.
-   **Robusto:** Lida com arquivos VTT comuns que não possuem o cabeçalho `WEBVTT` obrigatório e possui busca flexível por legendas.

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

    -   **No Linux (Ubuntu/Debian/Mint):**
        ```bash
        sudo apt-get update && sudo apt-get install ffmpeg
        ```
    -   **No macOS (usando [Homebrew]):**
        ```bash
        brew install ffmpeg
        ```
    -   **No Windows:**
        Recomenda-se instalar via [Chocolatey] (`choco install ffmpeg`) ou baixar o executável do site oficial e adicionar ao PATH do sistema.

### 2. Configuração do Projeto
1.  **Clone este repositório:**
    ```bash
    git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
    cd SEU-REPOSITORIO
    ```
    *(Substitua `SEU-USUARIO` e `SEU-REPOSITORIO` pelo seu nome de usuário e nome do repositório no GitHub)*

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

O projeto oferece dois modos de uso: processar um único arquivo ou processar uma pasta inteira em lote.

### Modo 1: Processar um Único Arquivo (`gerador_de_dublagem.py`)

Use este script quando quiser dublar apenas um vídeo ou gerar apenas o arquivo de áudio.

**Exemplo 1: Gerar o vídeo final com dublagem (recomendado)**
Este comando cria o áudio e o adiciona diretamente ao vídeo em uma única etapa.

```bash
python3 gerador_de_dublagem.py "legenda.vtt" "video_final.mp4" --video_entrada "video_original.mp4"
```

**Exemplo 2: Gerar apenas o arquivo de áudio (`.mp3`)**
```bash
python3 gerador_de_dublagem.py "legenda.vtt" "audio_dublado.mp3"
```

### Modo 2: Processar Vários Vídeos em Lote (`processar_lote.py`)

Use este script para automatizar a dublagem de uma pasta inteira. Ele procura por pares de arquivos de vídeo e legenda e processa todos eles.

**Organização dos arquivos:**
O script é flexível. Para cada arquivo `video.mp4`, ele procurará por um arquivo `.vtt` que **comece com o mesmo nome**.

Exemplo de estrutura de pasta válida:
```
minha_pasta_de_videos/
├── aula01.mp4
├── aula01 Portuguese.vtt
├── aula02.mp4
├── aula02.vtt
├── introducao.mp4
└── introducao - Legenda PTBR.vtt
```

**Exemplo de comando:**
```bash
python3 processar_lote.py "caminho/para/minha_pasta_de_videos"
```
O script irá criar os arquivos `aula01_dublado.mp4`, `aula02_dublado.mp4`, etc., dentro da mesma pasta.

### Opções Comuns (para ambos os scripts)

Você pode customizar a voz e a velocidade em qualquer um dos scripts.

-   **Mudar a voz para masculina (`pm_juca`):**
    Adicione `--voz pm_juca` ao final do comando.
    ```bash
    python3 processar_lote.py "minha_pasta_de_videos" --voz pm_juca
    ```
-   **Ajustar a aceleração máxima:**
    Use `--max_aceleracao`. Um valor maior permite que a voz fique mais rápida.
    ```bash
    python3 gerador_de_dublagem.py "legenda.vtt" "video_final.mp4" --video_entrada "video_original.mp4" --max_aceleracao 2.0
    ```

---

## Etapa Manual Alternativa: Usando FFmpeg

Se você preferir gerar apenas os arquivos de áudio e combiná-los com o vídeo manualmente, pode usar estes comandos do FFmpeg.

**Para adicionar o áudio como uma SEGUNDA faixa (mantendo a original):**
```bash
ffmpeg -i "video_original.mp4" -i "audio_dublado.mp3" -map 0:v:0 -map 0:a:0 -map 1:a:0 -c:v copy -c:a copy "video_final_com_dublagem.mp4"
```

**Para SUBSTITUIR o áudio original pelo novo:**
```bash
ffmpeg -i "video_original.mp4" -i "audio_dublado.mp3" -map 0:v:0 -map 1:a:0 -c:v copy -c:a copy "video_final_dublado.mp4"
```
