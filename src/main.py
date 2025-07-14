import face_recognition
import cv2
import os
import numpy as np
import serial
import time


PASTA_DATASET = "dataset" #
FATOR_REDIMENSIONAMENTO = 0.5 #
COOLDOWN_ABERTURA_SEGUNDOS = 10 #
PORTA_SERIAL_ARDUINO = 'COM3' #
BAUD_RATE = 9600 #
TOLERANCIA = 0.6



print("[INFO] Lendo pessoas autorizadas e carregando encodings...")
encodings_conhecidos = []
nomes_conhecidos = []
arduino = None
ultimo_acesso_liberado = 0

try:
    PESSOAS_AUTORIZADAS = [d for d in os.listdir(PASTA_DATASET) if os.path.isdir(os.path.join(PASTA_DATASET, d))] #

    if not PESSOAS_AUTORIZADAS:
        print("[AVISO] Nenhuma pessoa encontrada na pasta 'dataset'.") #
    else:
        print(f"[INFO] Pessoas autorizadas encontradas: {', '.join(PESSOAS_AUTORIZADAS)}") #
        for nome_pessoa in PESSOAS_AUTORIZADAS:
            caminho_pessoa = os.path.join(PASTA_DATASET, nome_pessoa)
            for nome_arquivo in os.listdir(caminho_pessoa):
                caminho_imagem = os.path.join(caminho_pessoa, nome_arquivo)
                imagem = face_recognition.load_image_file(caminho_imagem)
                lista_encodings = face_recognition.face_encodings(imagem)
                
                if len(lista_encodings) > 0:
                    encodings_conhecidos.append(lista_encodings[0])
                    nomes_conhecidos.append(nome_pessoa)
                else:
                    print(f"[AVISO] Nenhum rosto encontrado em {nome_arquivo}, pulando.")

except FileNotFoundError:
    print(f"[ERRO] A pasta '{PASTA_DATASET}' não foi encontrada! Execute o script 'registerFace.py' primeiro.") #
    PESSOAS_AUTORIZADAS = [] #



try:
    arduino = serial.Serial(PORTA_SERIAL_ARDUINO, BAUD_RATE, timeout=1)
    time.sleep(2) 
    print(f"[INFO] Conexão com Arduino na porta {PORTA_SERIAL_ARDUINO} estabelecida.")
except serial.SerialException:
    print(f"[AVISO] Não foi possível conectar ao Arduino na porta {PORTA_SERIAL_ARDUINO}. O script rodará sem acionar a tranca.")
    arduino = None



print("[INFO] Iniciando a webcam... Pressione 'q' para sair.")
video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    if not ret:
        break

    
    frame_pequeno = cv2.resize(frame, (0, 0), fx=FATOR_REDIMENSIONAMENTO, fy=FATOR_REDIMENSIONAMENTO)
    rgb_frame_pequeno = cv2.cvtColor(frame_pequeno, cv2.COLOR_BGR2RGB)

    
    locais_rosto = face_recognition.face_locations(rgb_frame_pequeno)
    encodings_rosto_frame = face_recognition.face_encodings(rgb_frame_pequeno, locais_rosto)

    for local_rosto, encoding_rosto in zip(locais_rosto, encodings_rosto_frame):
        matches = face_recognition.compare_faces(encodings_conhecidos, encoding_rosto, tolerance=TOLERANCIA)
        nome = "Desconhecido"
        cor_caixa = (0, 0, 255)

        distancias_rosto = face_recognition.face_distance(encodings_conhecidos, encoding_rosto)
        if len(distancias_rosto) > 0:
            melhor_match_index = np.argmin(distancias_rosto)
            if matches[melhor_match_index]:
                nome = nomes_conhecidos[melhor_match_index]
                
                
                if nome in PESSOAS_AUTORIZADAS:
                    cor_caixa = (0, 255, 0) 
                    
                   
                    if (time.time() - ultimo_acesso_liberado) > COOLDOWN_ABERTURA_SEGUNDOS:
                        if arduino and arduino.is_open:
                            print(f"[ACESSO LIBERADO] Abrindo para {nome}.")
                            arduino.write(b'A') 
                        ultimo_acesso_liberado = time.time()

        
        top, right, bottom, left = local_rosto
        top = int(top / FATOR_REDIMENSIONAMENTO)
        right = int(right / FATOR_REDIMENSIONAMENTO)
        bottom = int(bottom / FATOR_REDIMENSIONAMENTO)
        left = int(left / FATOR_REDIMENSIONAMENTO)

        cv2.rectangle(frame, (left, top), (right, bottom), cor_caixa, 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), cor_caixa, cv2.FILLED)
        cv2.putText(frame, nome, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

    cv2.imshow('Sistema de Reconhecimento Facial', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


print("[INFO] Encerrando o programa.")
video.release()
cv2.destroyAllWindows()
if arduino and arduino.is_open:
    arduino.close()