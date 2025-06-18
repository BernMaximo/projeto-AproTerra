#include <WiFi.h>
#include <HTTPClient.h>
#include <HardwareSerial.h>

// ===== CONFIGURAÇÕES =====
const char* ssid     = "Claro_2.4G";
const char* password = "Maximobernardo@";
const char* serverUrl = "http://192.168.0.33:5000/dados";

HardwareSerial LoRaSerial(1);

void setup() {
  Serial.begin(115200);
  LoRaSerial.begin(115200, SERIAL_8N1, 16, 17);

  Serial.print("Conectando ao Wi-Fi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi conectado. IP: " + WiFi.localIP().toString());
}

void loop() {
  if (LoRaSerial.available()) {
    String dadosRecebidos = LoRaSerial.readStringUntil('\n');  // espera nova linha
    Serial.println("Recebido via LoRa: " + dadosRecebidos);

    String jsonPayload = converterParaJSON(dadosRecebidos);

    if (jsonPayload != "") {
      Serial.println("Enviando para servidor: " + jsonPayload);
      enviarParaServidor(jsonPayload);
    }
  }

  delay(500);
}

String converterParaJSON(String mensagem) {
  mensagem.trim();
  int valoresEsperados = 5;
  float valores[5];

  int i = 0;
  int pos = 0;
  while (i < valoresEsperados && pos >= 0) {
    int nextPos = mensagem.indexOf(',', pos);
    if (nextPos == -1) nextPos = mensagem.length();

    String valorStr = mensagem.substring(pos, nextPos);
    valores[i] = valorStr.toFloat();

    pos = nextPos + 1;
    i++;
  }

  if (i < valoresEsperados) {
    Serial.println("Erro: dados incompletos recebidos.");
    return "";
  }

  String json = "{\"umidade_ar\":" + String(valores[0], 2) +
                ",\"umidade_solo\":" + String(valores[1], 2) +
                ",\"vento\":" + String(valores[2], 2) +
                ",\"chuva\":" + String(valores[3], 2) +
                ",\"temperatura\":" + String(valores[4], 2) + "}";

  return json;
}


void enviarParaServidor(String payload) {
  if ((WiFi.status() == WL_CONNECTED)) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(payload);

    if (httpResponseCode > 0) {
      String resposta = http.getString();
      Serial.println("Resposta do servidor: " + resposta);
    } else {
      Serial.print("Erro no envio. Código HTTP: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("Wi-Fi desconectado. Tentando reconectar...");
    WiFi.begin(ssid, password);
  }
}
