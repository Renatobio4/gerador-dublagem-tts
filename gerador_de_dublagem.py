#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gerador de Dublagem Automática a partir de Legendas e Vídeos
"""

import os
import argparse
import subprocess
import webvtt  # <-- CORRIGIDO AQUI
from io import StringIO
from kokoro import KPipeline
import soundfile as sf
import numpy as np
from pydub import AudioSegment  # <-- CORRIGIDO AQUI
from pydub.effects import speedup

def parse_time(time_str):
    """Converte o formato de tempo 'HH:MM:SS.mmm' da webvtt para segundos (float)."""
    try:
        parts = time_str.split(':')
        seconds_parts = parts[-1].split('.')
        h = int(parts[0]) if len(parts) == 3 else 0
        m = int(parts[-2]) if len(parts) >= 2 else 0
        s = int(seconds_parts[0])
        ms = int(seconds_parts[1])
        return h * 3600 + m * 60 + s + ms / 1000.0
    except (ValueError, IndexError):
        print(f"AVISO: Formato de tempo inesperado: '{time_str}'. Tratando como 0.0s.")
        return 0.0

def gerar_dublagem(caminho_legenda, caminho_saida_audio, lang_code, voz_str, max_aceleracao):
    """
    Função principal que orquestra a criação do áudio sincronizado.
    """
    print(f"\n-> Iniciando processo de geração de áudio para '{os.path.basename(caminho_legenda)}'...")
    
    try:
        with open(caminho_legenda, 'r', encoding='utf-8-sig') as f:
            conteudo = f.read()
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: Arquivo de legenda não encontrado em '{caminho_legenda}'")
        return False

    if not conteudo.strip().startswith('WEBVTT'):
        print("AVISO: Adicionando cabeçalho 'WEBVTT' para compatibilidade.")
        conteudo = "WEBVTT\n\n" + conteudo
    
    try:
        legendas = webvtt.read_buffer(StringIO(conteudo)) # <-- CORRIGIDO AQUI
    except Exception as e:
        print(f"ERRO CRÍTICO: Não foi possível analisar o arquivo VTT. Verifique o formato.")
        print(f"Detalhes do erro: {e}")
        return False
    
    try:
        print(f"Carregando o pipeline Kokoro para o idioma '{lang_code}'...")
        tts_engine = KPipeline(lang_code=lang_code)
        print("Pipeline Kokoro carregado.")
    except Exception as e:
        print(f"ERRO CRÍTICO: Falha ao carregar o pipeline Kokoro.")
        print(f"Detalhes do erro: {e}")
        return False

    faixa_completa = AudioSegment.empty()
    ultimo_tempo_final_segundos = 0.0
    arquivo_temp = f"temp_{os.path.basename(caminho_saida_audio)}.wav"
    total_legendas = len(legendas)
    sample_rate = 24000

    print(f"Processando {total_legendas} legendas com a voz '{voz_str}'...")

    for i, legenda in enumerate(legendas):
        tempo_inicio_segundos = parse_time(legenda.start)
        tempo_fim_segundos = parse_time(legenda.end)
        
        duracao_pausa_segundos = tempo_inicio_segundos - ultimo_tempo_final_segundos
        if duracao_pausa_segundos > 0.01:
            silencio = AudioSegment.silent(duration=duracao_pausa_segundos * 1000)
            faixa_completa += silencio

        texto_legenda = legenda.text.replace('\n', ' ').strip()
        
        if not texto_legenda:
            ultimo_tempo_final_segundos = tempo_fim_segundos
            continue
            
        try:
            generator = tts_engine(texto_legenda, voice=voz_str)
            audio_chunks = [audio for _, _, audio in generator]
            
            if not audio_chunks:
                segmento_fala = AudioSegment.empty()
            else:
                audio_completo_np = np.concatenate(audio_chunks)
                sf.write(arquivo_temp, audio_completo_np, sample_rate)
                segmento_fala = AudioSegment.from_wav(arquivo_temp)

            duracao_ideal_segundos = tempo_fim_segundos - tempo_inicio_segundos
            duracao_real_segundos = len(segmento_fala) / 1000.0

            if duracao_real_segundos > duracao_ideal_segundos and duracao_ideal_segundos > 0:
                taxa_aceleracao = duracao_real_segundos / duracao_ideal_segundos
                if taxa_aceleracao > max_aceleracao:
                    taxa_aceleracao = max_aceleracao
                segmento_fala = speedup(segmento_fala, playback_speed=taxa_aceleracao)
            
            faixa_completa += segmento_fala
        except Exception as e:
            print(f"AVISO: Falha ao converter texto: '{texto_legenda}'. Erro: {e}")
        
        ultimo_tempo_final_segundos = tempo_fim_segundos

    try:
        faixa_completa.export(caminho_saida_audio, format="mp3", bitrate="192k")
        print(f"-> Áudio intermediário salvo com sucesso em '{caminho_saida_audio}'")
        if os.path.exists(arquivo_temp):
            os.remove(arquivo_temp)
        return True
    except Exception as e:
        print(f"ERRO CRÍTICO ao exportar o áudio: {e}")
        if os.path.exists(arquivo_temp):
            os.remove(arquivo_temp)
        return False

def adicionar_audio_ao_video(caminho_video, caminho_audio, caminho_saida_video):
    """
    Usa o FFmpeg para adicionar uma faixa de áudio a um vídeo, mantendo a original.
    """
    print(f"\n-> Adicionando áudio '{os.path.basename(caminho_audio)}' como segunda faixa em '{os.path.basename(caminho_video)}'...")
    
    comando = [
        'ffmpeg',
        '-i', caminho_video,
        '-i', caminho_audio,
        '-map', '0:v:0',
        '-map', '0:a:0',
        '-map', '1:a:0',
        '-c:v', 'copy',
        '-c:a', 'copy',
        '-y',
        caminho_saida_video
    ]
    
    try:
        subprocess.run(comando, check=True, capture_output=True, text=True)
        print(f"SUCESSO! Vídeo final com dublagem salvo em: '{caminho_saida_video}'")
    except FileNotFoundError:
        print("ERRO CRÍTICO: FFmpeg não encontrado. Verifique se ele está instalado e no PATH do sistema.")
    except subprocess.CalledProcessError as e:
        print("ERRO CRÍTICO ao executar o comando FFmpeg:")
        print(e.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Gera uma dublagem a partir de uma legenda e opcionalmente a adiciona a um vídeo.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    # ... (o resto do arquivo __main__ continua o mesmo)
    parser.add_argument("arquivo_legenda", help="Caminho para o arquivo .vtt de entrada.")
    parser.add_argument("saida", help="Caminho para o arquivo de SAÍDA (.mp3 ou .mp4).")
    parser.add_argument("--video_entrada", help="[OPCIONAL] Caminho para o vídeo original (.mp4). Necessário se a saída for .mp4.")
    parser.add_argument("--lang", default='p', help="Código do idioma para o TTS. Padrão: 'p' (Português).")
    parser.add_argument("--voz", default='pf_dora', help="Nome da voz a ser usada. Padrão: 'pf_dora'.")
    parser.add_argument("--max_aceleracao", type=float, default=1.5, help="Fator máximo de aceleração. Padrão: 1.5.")
    
    args = parser.parse_args()

    if args.saida.lower().endswith('.mp3'):
        if args.video_entrada:
            print("AVISO: --video_entrada foi fornecido, mas a saída é .mp3. O vídeo será ignorado.")
        gerar_dublagem(args.arquivo_legenda, args.saida, args.lang, args.voz, args.max_aceleracao)
        
    elif args.saida.lower().endswith('.mp4'):
        if not args.video_entrada:
            print("ERRO: A saída é um .mp4, mas o argumento --video_entrada não foi fornecido.")
            exit()
        if not os.path.exists(args.video_entrada):
            print(f"ERRO: Vídeo de entrada não encontrado em '{args.video_entrada}'")
            exit()
            
        caminho_audio_temp = args.saida.replace('.mp4', '.dub_temp.mp3')
        
        sucesso_audio = gerar_dublagem(args.arquivo_legenda, caminho_audio_temp, args.lang, args.voz, args.max_aceleracao)
        
        if sucesso_audio:
            adicionar_audio_ao_video(args.video_entrada, caminho_audio_temp, args.saida)
            print(f"Removendo arquivo de áudio temporário: '{caminho_audio_temp}'")
            os.remove(caminho_audio_temp)
    else:
        print("ERRO: A extensão do arquivo de saída deve ser .mp3 ou .mp4.")