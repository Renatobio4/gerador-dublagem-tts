#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Processador em Lote para Geração de Dublagem (Versão com busca flexível)
"""

import os
import argparse
from gerador_de_dublagem import gerar_dublagem, adicionar_audio_ao_video

def processar_pasta(pasta_alvo, lang_code, voz_str, max_aceleracao, manter_audio):
    """
    Procura por pares de arquivos de vídeo e legenda em uma pasta.
    Esta versão é mais flexível: para cada .mp4, procura por um .vtt que comece com o mesmo nome.
    """
    print(f"-> Iniciando processamento em lote na pasta: '{pasta_alvo}'")
    
    try:
        arquivos_na_pasta = os.listdir(pasta_alvo)
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: A pasta '{pasta_alvo}' não foi encontrada.")
        return
    
    videos_mp4 = [f for f in arquivos_na_pasta if f.lower().endswith('.mp4')]
    
    if not videos_mp4:
        print("Nenhum arquivo de vídeo (.mp4) encontrado na pasta.")
        return

    print(f"Encontrados {len(videos_mp4)} vídeos. Procurando por legendas correspondentes...")
    
    pares_encontrados = []
    for video_arquivo in videos_mp4:
        nome_base_video = os.path.splitext(video_arquivo)[0]
        legenda_encontrada = None
        
        # Procura por um arquivo .vtt que COMECE com o nome base do vídeo
        for arquivo in arquivos_na_pasta:
            if arquivo.lower().endswith('.vtt') and os.path.splitext(arquivo)[0].startswith(nome_base_video):
                legenda_encontrada = arquivo
                break # Encontrou o primeiro, para aqui
        
        if legenda_encontrada:
            pares_encontrados.append((video_arquivo, legenda_encontrada))
            print(f"  - Par encontrado: '{video_arquivo}' -> '{legenda_encontrada}'")
        else:
            print(f"  - AVISO: Nenhuma legenda encontrada para o vídeo '{video_arquivo}'")

    if not pares_encontrados:
        print("Nenhum par de vídeo/legenda correspondente foi encontrado para processar.")
        return
    
    total_pares = len(pares_encontrados)
    print(f"\nIniciando processamento de {total_pares} pares.")

    for i, (video_arquivo, legenda_arquivo) in enumerate(sorted(pares_encontrados)):
        print(f"\n--- Processando Par {i+1}/{total_pares}: {os.path.splitext(video_arquivo)[0]} ---")
        
        nome_base = os.path.splitext(video_arquivo)[0]
        video_entrada = os.path.join(pasta_alvo, video_arquivo)
        legenda_entrada = os.path.join(pasta_alvo, legenda_arquivo)
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