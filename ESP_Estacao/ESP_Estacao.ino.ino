#include <HardwareSerial.h>
#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

HardwareSerial LoRaSerial(1);

// VENTO
int pinoVento = 34;

// PLUVIÔMETRO
#define PINO_PLUVIOMETRO 18
volatile int contagemPulsos = 0;
volatile unsigned long lastPulseTime = 0;
const unsigned long DEBOUNCE_INTERVAL = 30 * 1000; // 30 ms em micros
const float mlPorPulso = 13.2;

void IRAM_ATTR contarPulso() {
  unsigned long now = micros();
  if (now - lastPulseTime >= DEBOUNCE_INTERVAL) {
    contagemPulsos++;
    lastPulseTime = now;
  }
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  LoRaSerial.begin(115200, SERIAL_8N1, 16, 17);

  pinMode(PINO_PLUVIOMETRO, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PINO_PLUVIOMETRO),
                  contarPulso, FALLING);

  Serial.println("LoRa UART pronto.");
}

void loop() {
  int leituraADC = analogRead(pinoVento);
  float tensao = (leituraADC / 4095.0) * 3.3;
  float vento = tensao * 7.6;

  float umidadeAr = dht.readHumidity();
  float temperatura = dht.readTemperature();
  float umidadeSolo = 0.0;

  if (isnan(umidadeAr) || isnan(temperatura)) {
    Serial.println("Erro ao ler o DHT11");
    return;
  }

  noInterrupts();
  int pulsos = contagemPulsos;
  contagemPulsos = 0;
  interrupts();

  float chuva = pulsos * mlPorPulso;

  String mensagem = String(umidadeAr, 2) + "," +
                    String(umidadeSolo, 2) + "," +
                    String(temperatura, 2) + "," +
                    String(vento, 2) + "," +
                    String(chuva, 2);

  LoRaSerial.println(mensagem);
  
  Serial.println("------ Leitura ------");
  Serial.println("Umidade do Ar: " + String(umidadeAr,1) + " %");
  Serial.println("Temperatura: " + String(temperatura,1) + " °C");
  Serial.println("Vento (m/s): " + String(vento,2));
  Serial.println("Chuva (mL): " + String(chuva,2));
  Serial.println("Mensagem LoRa: " + mensagem);
  Serial.println("---------------------\n");

  delay(10000);
}
