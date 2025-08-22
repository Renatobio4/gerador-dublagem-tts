#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gerador de Dublagem a partir de Arquivos de Legenda VTT

Este script converte o texto de um arquivo de legenda (.vtt) em uma faixa de áudio
sincronizada, utilizando o motor de Text-to-Speech (TTS) Kokoro.

Funcionalidades:
- Lê arquivos de legenda no formato WebVTT.
- Corrige automaticamente arquivos VTT que não possuem o cabeçalho "WEBVTT".
- Utiliza o motor de TTS Kokoro (PyTorch) para gerar áudio de alta qualidade offline.
- Insere pausas de silêncio para corresponder ao tempo entre as legendas.
- Acelera dinamicamente os clipes de áudio que excedem a duração da legenda para
  garantir uma sincronização precisa com o tempo do vídeo original.
- Exporta o resultado final como um único arquivo MP3.
"""

import os
import argparse
import webvtt
from io import StringIO
from kokoro import KPipeline
import soundfile as sf
import numpy as np
from pydub import AudioSegment
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
        print(f"AVISO: Formato de tempo inesperado encontrado: '{time_str}'. Tratando como 0.0s.")
        return 0.0

def gerar_dublagem(caminho_legenda, caminho_saida, lang_code, voz_str, max_aceleracao):
    """
    Função principal que orquestra a criação do áudio sincronizado.
    Acelera clipes de fala que excedem a duração da legenda para garantir a sincronia.
    """
    print("-> Iniciando processo de geração de dublagem...")
    
    # --- Passo 1: Leitura e validação do arquivo de legenda ---
    print(f"Lendo arquivo de legenda: '{caminho_legenda}'")
    try:
        with open(caminho_legenda, 'r', encoding='utf-8-sig') as f: # utf-8-sig lida com BOM
            conteudo = f.read()
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: Arquivo de legenda não encontrado em '{caminho_legenda}'")
        return

    # Garante que o conteúdo VTT é válido, adicionando o cabeçalho se necessário.
    if not conteudo.strip().startswith('WEBVTT'):
        print("AVISO: O arquivo não começava com 'WEBVTT'. Adicionando cabeçalho para compatibilidade.")
        conteudo = "WEBVTT\n\n" + conteudo
    
    try:
        legendas = webvtt.read_buffer(StringIO(conteudo))
    except Exception as e:
        print(f"ERRO CRÍTICO: Não foi possível analisar o arquivo VTT. Verifique o formato.")
        print(f"Detalhes do erro: {e}")
        return
    
    # --- Passo 2: Carregamento do motor de TTS ---
    try:
        print(f"Carregando o pipeline Kokoro para o idioma '{lang_code}' (pode demorar na 1ª vez)...")
        tts_engine = KPipeline(lang_code=lang_code)
        print("Pipeline Kokoro carregado com sucesso.")
    except Exception as e:
        print(f"ERRO CRÍTICO: Falha ao carregar o pipeline Kokoro. Verifique a instalação das dependências (torch, kokoro).")
        print(f"Detalhes do erro: {e}")
        return

    # --- Passo 3: Processamento e montagem do áudio ---
    faixa_completa = AudioSegment.empty()
    ultimo_tempo_final_segundos = 0.0
    arquivo_temp = "temp_audio_segmento.wav"
    total_legendas = len(legendas)
    sample_rate = 24000 # Taxa de amostragem padrão do Kokoro

    print(f"\n-> Processando {total_legendas} legendas com a voz '{voz_str}' e aceleração máxima de {max_aceleracao}x...")

    for i, legenda in enumerate(legendas):
        tempo_inicio_segundos = parse_time(legenda.start)
        tempo_fim_segundos = parse_time(legenda.end)
        
        # Insere a pausa de silêncio entre a legenda anterior e a atual
        duracao_pausa_segundos = tempo_inicio_segundos - ultimo_tempo_final_segundos
        if duracao_pausa_segundos > 0.01: # Adiciona silêncio apenas se for significativo
            silencio = AudioSegment.silent(duration=duracao_pausa_segundos * 1000)
            faixa_completa += silencio

        texto_legenda = legenda.text.replace('\n', ' ').strip()
        
        if not texto_legenda: # Pula legendas vazias
            ultimo_tempo_final_segundos = tempo_fim_segundos
            continue
            
        try:
            # Gera os pedaços de áudio com Kokoro
            generator = tts_engine(texto_legenda, voice=voz_str)
            audio_chunks = [audio for _, _, audio in generator]
            
            if not audio_chunks:
                segmento_fala = AudioSegment.empty()
            else:
                audio_completo_np = np.concatenate(audio_chunks)
                sf.write(arquivo_temp, audio_completo_np, sample_rate)
                segmento_fala = AudioSegment.from_wav(arquivo_temp)

            # LÓGICA DE ACELERAÇÃO DINÂMICA
            duracao_ideal_segundos = tempo_fim_segundos - tempo_inicio_segundos
            duracao_real_segundos = len(segmento_fala) / 1000.0

            if duracao_real_segundos > duracao_ideal_segundos and duracao_ideal_segundos > 0:
                taxa_aceleracao = duracao_real_segundos / duracao_ideal_segundos
                
                # Limita a aceleração para não distorcer demais o áudio
                if taxa_aceleracao > max_aceleracao:
                    print(f"  - AVISO: Aceleração necessária ({taxa_aceleracao:.2f}x) excede o limite de {max_aceleracao}x. Limitando.")
                    taxa_aceleracao = max_aceleracao
                
                print(f"  - Processado {i+1}/{total_legendas}: Acelerando em {taxa_aceleracao:.2f}x...")
                segmento_fala = speedup(segmento_fala, playback_speed=taxa_aceleracao)
            else:
                 print(f"  - Processado {i+1}/{total_legendas}: '{texto_legenda[:40]}...'")
            
            faixa_completa += segmento_fala
            
        except Exception as e:
            print(f"AVISO: Falha ao converter o texto: '{texto_legenda}'. Erro: {e}")
        
        # O relógio agora é sempre o tempo final da legenda, pois forçamos o áudio a caber
        ultimo_tempo_final_segundos = tempo_fim_segundos

    # --- Passo 4: Exportação do arquivo final ---
    print("\n-> Montagem final completa. Exportando o arquivo de áudio...")
    try:
        faixa_completa.export(caminho_saida, format="mp3", bitrate="192k")
        duracao_final_min = len(faixa_completa) / 60000
        print(f"SUCESSO! Áudio sincronizado salvo em '{caminho_saida}'")
        print(f"Duração final do áudio: {duracao_final_min:.2f} minutos.")
    except Exception as e:
        print(f"ERRO CRÍTICO ao exportar o arquivo final: {e}")
        
    # Limpa o arquivo temporário
    if os.path.exists(arquivo_temp):
        os.remove(arquivo_temp)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Gera uma dublagem em áudio a partir de um arquivo de legenda VTT, sincronizando o tempo.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("arquivo_legenda", help="Caminho para o arquivo .vtt de entrada.")
    parser.add_argument("arquivo_audio", help="Caminho para o arquivo .mp3 de saída.")
    parser.add_argument(
        "--lang", 
        default='p', 
        help="Código do idioma. Padrão: 'p' (Português).\n"
             "Outras opções: 'a' (Inglês Americano), 'e' (Espanhol), 'f' (Francês), etc."
    )
    parser.add_argument(
        "--voz", 
        default='pf_dora', 
        help="Nome da voz a ser usada. Padrão: 'pf_dora'.\n"
             "Vozes em português: 'pf_dora' (feminina), 'pm_juca' (masculina)."
    )
    parser.add_argument(
        "--max_aceleracao", 
        type=float, 
        default=1.5, 
        help="Fator máximo de aceleração para falas longas (ex: 1.5 para 50%% mais rápido).\n"
             "Valores mais altos podem distorcer o áudio. Padrão: 1.5."
    )
    
    args = parser.parse_args()
    
    gerar_dublagem(args.arquivo_legenda, args.arquivo_audio, args.lang, args.voz, args.max_aceleracao)