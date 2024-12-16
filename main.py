import numpy as np
import os
from assets.imageFunction import imageProcess
os.system("cls")
caminho_pasta = 'data/'
# Lista para armazenar os nomes dos arquivos
lista_arquivos = []
# Varrer a pasta e obter os nomes dos arquivos
for nome_arquivo in os.listdir(caminho_pasta):
    caminho_completo = os.path.join(caminho_pasta, nome_arquivo)
    # Verificar se é um arquivo (não um diretório)
    if os.path.isfile(caminho_completo):
        lista_arquivos.append(caminho_pasta+nome_arquivo)
#função imageProcess(arquivo) é chamada para cada imagem
for arquivo in lista_arquivos:
    print(f"Arquivo Detectado: {arquivo}")
    print("Iniciando Processamento....")
    imageProcess(arquivo)
