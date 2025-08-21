# 🤖 Mão Robótica Controlada por Visão Computacional (ESP32 + MediaPipe)

Este projeto integra **visão computacional com MediaPipe** e dois **ESP32** (um ESP32 comum e um ESP32-CAM) para controlar uma mão robótica com **5 servos motores** em tempo real, baseada nos movimentos dos dedos capturados pela câmera.

---

## 📌 Visão Geral

- O **ESP32-CAM** transmite imagens em tempo real da mão do usuário.  
- O código em **Python (`mão.py`)** processa os frames com o **MediaPipe Hands** e detecta os estados dos dedos (abertos ou fechados).  
- Os estados são enviados via **Serial** para um **ESP32 comum**, que aciona os **servos motores** correspondentes, controlando a abertura e fechamento de cada dedo da mão robótica.  

---

## 🛠️ Hardware Utilizado

- 1x **ESP32-CAM** (stream de vídeo da mão humana)  
- 1x **ESP32** (controle dos servos motores)  
- 5x **Servos motores SG90 / MG90S**  
- Protoboard e jumpers  
- Fonte de alimentação externa para os servos  

⚠️ **Importante:** os servos devem ter alimentação separada do ESP32 para evitar sobrecarga. Conectar os **GNDs em comum**.

---

 🎥 Funcionamento

A câmera do ESP32-CAM transmite o vídeo.

O Python detecta os pontos-chave da mão via MediaPipe Hands.

Para cada dedo, calcula-se se está ABERTO ou FECHADO.

O estado é enviado via serial para o ESP32.

O ESP32 movimenta os servos correspondentes, replicando o gesto em uma mão robótica.

📸 Demonstração
<img src="gif/Exemplo1.gif" alt="Demonstração" width="400">



## 💻 Software Necessário

### No computador:
- Python 3.9+  
- OpenCV  
- MediaPipe  
- PySerial


Instalação das dependências:  
```bash
pip install opencv-python mediapipe pyserial

