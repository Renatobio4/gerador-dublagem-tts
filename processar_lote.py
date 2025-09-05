#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Processador em Lote para Geração de Dublagem

Este script automatiza o processo de dublagem para múltiplos arquivos. Ele varre
uma pasta em busca de pares de arquivos de vídeo (.mp4) e legenda (.vtt) com nomes
correspondentes e executa o fluxo de geração de áudio e adição ao vídeo para cada par.
"""

import os
import argparse
# Importa as funções que criamos no nosso outro script
from gerador_de_dublagem import gerar_dublagem, adicionar_audio_ao_video

def processar_pasta(pasta_alvo, lang_code, voz_str, max_aceleracao, manter_audio):
    """
    Procura por pares de arquivos de vídeo (.mp4) e legenda (.vtt) em uma pasta
    e executa o processo de dublagem para cada par encontrado.
    """
    print(f"-> Iniciando processamento em lote na pasta: '{pasta_alvo}'")
    
    try:
        arquivos_na_pasta = os.listdir(pasta_alvo)
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: A pasta '{pasta_alvo}' não foi encontrada.")
        return
    
    videos = {os.path.splitext(f)[0]: f for f in arquivos_na_pasta if f.lower().endswith('.mp4')}
    legendas = {os.path.splitext(f)[0]: f for f in arquivos_na_pasta if f.lower().endswith('.vtt')}
    
    # Encontra os nomes de base que existem em ambos os dicionários
    nomes_em_comum = set(videos.keys()) & set(legendas.keys())
    
    if not nomes_em_comum:
        print("Nenhum par de vídeo (.mp4) e legenda (.vtt) com nomes correspondentes foi encontrado.")
        return

    print(f"Encontrados {len(nomes_em_comum)} pares de arquivos para processar.")
    
    contador = 0
    for nome_base in sorted(list(nomes_em_comum)):
        contador += 1
        print(f"\n--- Processando Par {contador}/{len(nomes_em_comum)}: {nome_base} ---")
        
        video_entrada = os.path.join(pasta_alvo, videos[nome_base])
        legenda_entrada = os.path.join(pasta_alvo, legendas[nome_base])
        audio_temporario = os.path.join(pasta_alvo, f"{nome_base}.dub_temp.mp3")
        video_saida = os.path.join(pasta_alvo, f"{nome_base}_dublado.mp4")
        
        sucesso_audio = gerar_dublagem(legenda_entrada, audio_temporario, lang_code, voz_str, max_aceleracao)
        
        if sucesso_audio:
            adicionar_audio_ao_video(video_entrada, audio_temporario, video_saida)
            
            if not manter_audio:
                print(f"Removendo arquivo de áudio temporário: '{audio_temporario}'")
                os.remove(audio_temporario)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Processa uma pasta inteira, criando dublagens para todos os pares de vídeo/legenda.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("pasta", help="Caminho para a pasta contendo os arquivos .mp4 e .vtt.")
    parser.add_argument("--lang", default='p', help="Código do idioma para o TTS. Padrão: 'p' (Português).")
    parser.add_argument("--voz", default='pf_dora', help="Nome da voz a ser usada. Padrão: 'pf_dora'.")
    parser.add_argument("--max_aceleracao", type=float, default=1.5, help="Fator máximo de aceleração. Padrão: 1.5.")
    parser.add_argument("--manter_audio", action='store_true', help="Se definido, mantém os arquivos de áudio .mp3 intermediários.")
    
    args = parser.parse_args()
    
    processar_pasta(args.pasta, args.lang, args.voz, args.max_aceleracao, args.manter_audio)
