import face_recognition
import cv2
import os
import numpy as np
import serial
import time

PASTA_DATASET = "dataset"
FATOR_REDIMENSIONAMENTO = 0.5
COOLDOWN_ABERTURA_SEGUNDOS = 10

PORTA_SERIAL_ARDUINO = 'COM3'
BAUD_RATE = 9600

print("[INFO] Lendo pessoas autorizadas a partir das pastas do dataset...")
try:

    PESSOAS_AUTORIZADAS = [
        d for d in os.listdir(PASTA_DATASET)
        if os.path.isdir(os.path.join(PASTA_DATASET, d))
    ]

    if not PESSOAS_AUTORIZADAS:
        print("[AVISO] Nenhuma pessoa encontrada na pasta 'dataset'. A tranca não abrirá para ninguém.")
    else:

        print(f"[INFO] Pessoas autorizadas encontradas: {', '.join(PESSOAS_AUTORIZADAS)}")

except FileNotFoundError:
    print(f"[ERRO] A pasta '{PASTA_DATASET}' não foi encontrada! Execute o script 'cadastrar_rosto.py' primeiro.")
    PESSOAS_AUTORIZADAS = []
