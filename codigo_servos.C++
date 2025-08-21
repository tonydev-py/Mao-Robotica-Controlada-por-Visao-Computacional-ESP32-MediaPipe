//Use esse código no Aarduino IDE

#include <Arduino.h>
#include <ESP32Servo.h>

// Definição dos servos
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;

// Pinos correspondentes
int pin1 = 23;
int pin2 = 22;
int pin3 = 21;
int pin4 = 19;
int pin5 = 18;

// Função equivalente ao Python
void rotateServo(Servo &servo, int angle) {
  servo.write(angle);  // Ângulo de 0 a 180
  delay(15);           // Pequeno delay
}

// Função abrir/fechar
void abrir_fechar(Servo &servo, int pin, int on_off) {
  if (on_off == 1) {
    rotateServo(servo, 0);     // Abrir
  } else if (on_off == 0 && pin != pin1 && pin != pin2) {
    rotateServo(servo, 140);   // Fechar padrão
  } else if (on_off == 0 && pin == pin1) {
    rotateServo(servo, 150);   // Fechar dedo especial 1
  } else if (on_off == 0 && pin == pin2) {
    rotateServo(servo, 180);   // Fechar dedo especial 2
  }
}

// Função para testes iniciais
void testeTodos() {
  rotateServo(servo1, 0);
  rotateServo(servo2, 0);
  rotateServo(servo3, 0);
  rotateServo(servo4, 0);
  rotateServo(servo5, 0);
  delay(1000);

  rotateServo(servo1, 150);
  delay(1000);
  rotateServo(servo1, 0);
  delay(1000);

  rotateServo(servo2, 130);
  delay(1000);
  rotateServo(servo2, 0);
  delay(1000);

  rotateServo(servo3, 130);
  delay(1000);
  rotateServo(servo3, 0);
  delay(1000);

  rotateServo(servo4, 130);
  delay(1000);
  rotateServo(servo4, 0);
  delay(1000);

  rotateServo(servo5, 130);
  delay(1000);
  rotateServo(servo5, 0);
  delay(2000);
}

void setup() {
  Serial.begin(115200); // Comunicação com o Python

  // Anexar os servos aos pinos
  servo1.attach(pin1);
  servo2.attach(pin2);
  servo3.attach(pin3);
  servo4.attach(pin4);
  servo5.attach(pin5);

  // Executa o teste inicial
  testeTodos();
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n'); // Lê até quebra de linha
    data.trim(); // Remove espaços extras

    int commaIndex = data.indexOf(',');
    if (commaIndex > 0) {
      int servoNum = data.substring(0, commaIndex).toInt();
      int estado = data.substring(commaIndex + 1).toInt();

      switch (servoNum) {
        case 1: abrir_fechar(servo1, pin1, estado); break;
        case 2: abrir_fechar(servo2, pin2, estado); break;
        case 3: abrir_fechar(servo3, pin3, estado); break;
        case 4: abrir_fechar(servo4, pin4, estado); break;
        case 5: abrir_fechar(servo5, pin5, estado); break;
      }
    }
  }
}
