import cv2
import mediapipe as mp
import serial
import time

# Serial com ESP32
esp = serial.Serial("COM5", 115200)  # troque COM5 pela porta certa
time.sleep(2)

# Dicionário para associar servo ao dedo
dedos = {
    "polegar": 1,
    "indicador": 2,
    "medio": 3,
    "anelar": 4,
    "minimo": 5
}

# Estados dos dedos
estado_dedos = {dedo: " " for dedo in dedos}

def abrir_fechar(dedo, estado):
    servo = dedos[dedo]
    cmd = f"{servo},{estado}\n"
    esp.write(cmd.encode())
    estado_dedos[dedo] = "ABERTO" if estado == 1 else "FECHADO"
    print(f"[ENVIO] {dedo.upper()} -> Servo {servo} -> Estado {estado}")

# Captura do vídeo (ESP32-CAM)
# Troque 192.165.1.103 pelo código url exibido no Monitor Serial (Arduino IDE) do ESP32CAM CameraWebview
url = "http:192.165.1.103:81/stream" 
cap = cv2.VideoCapture(url)

hands = mp.solutions.hands
Hands = hands.Hands(max_num_hands=1)
mpDwaw = mp.solutions.drawing_utils

while True:
    success, img = cap.read()
    if not success:
        continue

    frameRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = Hands.process(frameRGB)
    h, w, _ = img.shape
    pontos = []

    if results.multi_hand_landmarks:
        for points in results.multi_hand_landmarks:
            mpDwaw.draw_landmarks(img, points, hands.HAND_CONNECTIONS)
            for id, cord in enumerate(points.landmark):
                cx, cy = int(cord.x * w), int(cord.y * h)
                pontos.append((cx, cy))

        if pontos:
            # Distâncias entre articulações para detectar "aberto/fechado"
            distPolegar = abs(pontos[17][0] - pontos[4][0])
            distIndicador = pontos[5][1] - pontos[8][1]
            distMedio = pontos[9][1] - pontos[12][1]
            distAnelar = pontos[13][1] - pontos[16][1]
            distMinimo = pontos[17][1] - pontos[20][1]

            abrir_fechar("polegar", 0 if distPolegar < 80 else 1)
            abrir_fechar("indicador", 1 if distIndicador >= 1 else 0)
            abrir_fechar("medio", 1 if distMedio >= 1 else 0)
            abrir_fechar("anelar", 1 if distAnelar >= 1 else 0)
            abrir_fechar("minimo", 1 if distMinimo >= 1 else 0)

    # Exibir estados dos dedos no frame
    y = 30
    for dedo, estado in estado_dedos.items():
        cv2.putText(img, f"{dedo.upper()}: {estado}", (10, y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0) if estado=="ABERTO" else (0,0,255), 2)
        y += 30

    cv2.imshow("ESP32-CAM + MediaPipe + DEDOS", img)

    # Tecla 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
