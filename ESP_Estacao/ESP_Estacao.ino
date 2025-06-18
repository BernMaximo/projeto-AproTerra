#include <HardwareSerial.h>

HardwareSerial LoRaSerial(1); // Usar UART1

void setup() {
  Serial.begin(115200);
  
  // Iniciar LoRa serial (pinos RX, TX invertidos)
  LoRaSerial.begin(115200, SERIAL_8N1, 16, 17); // RX=16, TX=17

  Serial.println("LoRa UART pronto.");
}

void loop() {
  float umidadeAr = 11.1;
  float umidadeSolo = 22.2;
  float temperatura = 33.3;
  float vento = 44.4;
  float chuva = 55.5;

  // Monta mensagem
  String mensagem = String(umidadeAr) + "," +
                    String(umidadeSolo) + "," +
                    String(temperatura) + "," +
                    String(vento) + "," +
                    String(chuva);

  // Envia mensagem para o LoRa UART
  LoRaSerial.println(mensagem);
  Serial.println("Enviado via LoRa: " + mensagem);

  delay(10000); // a cada 10 segundos
}
