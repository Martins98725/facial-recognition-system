import cv2
import os
import face_recognition

DATASET_DIR = "dataset"
NUM_IMAGENS_PARA_SALVAR = 3

name = input("Digite o nome da pessoa (use letras ): ").strip()

if not name:
    print("[ERRO] Nome inválido. O programa será encerrado.")
    exit()

person_dir = os.path.join(DATASET_DIR, name)

os.makedirs(person_dir, exist_ok=True)
print(f"Pasta de cadastro criada em: {person_dir}")

video = cv2.VideoCapture(0)
img_count = 0

print("\n[ATENÇÃO] Posicione o rosto no centro do quadrado.")
print(f"Pressione 's' para salvar uma foto. Precisamos de {NUM_IMAGENS_PARA_SALVAR} fotos.")
print("Mude um pouco a posição e a expressão do rosto a cada foto (olhe para o lado, sorria, etc.).")
print("Pressione 'q' para cancelar e sair.")

while img_count < NUM_IMAGENS_PARA_SALVAR:
    ret, frame = video.read()
    if not ret:
        print("[ERRO] Não foi possível capturar imagem da câmera.")
        break

    locations = face_recognition.face_locations(frame)

    if len(locations) > 0:
        top, right, bottom, left = locations[0]

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    texto_info = f"Fotos salvas: {img_count}/{NUM_IMAGENS_PARA_SALVAR}"
    cv2.putText(frame, texto_info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Cadastro de Rosto", frame)
    key = cv2.waitKey(1)

    if key == ord("s"):

        if len(locations) == 1:
            img_count += 1
            image_path = os.path.join(person_dir, f"{name}.jpg")
            cv2.imwrite(image_path, frame)
            print(f"[OK] Foto {img_count} salva em: {image_path}")
            if img_count < NUM_IMAGENS_PARA_SALVAR:
                print("Ótimo! Agora mude a posição para a próxima foto.")
        elif len(locations) == 0:
            print("[AVISO] Nenhum rosto detectado! Posicione-se melhor.")
        else:
            print("[AVISO] Mais de um rosto detectado! Apenas uma pessoa por vez.")

    elif key == ord("q"):
        print("[INFO] Cadastro cancelado pelo usuário.")
        break

if img_count == NUM_IMAGENS_PARA_SALVAR:
    print(f"\n[SUCESSO] Cadastro de '{name}' concluído com {img_count} fotos!")

video.release()
cv2.destroyAllWindows()
