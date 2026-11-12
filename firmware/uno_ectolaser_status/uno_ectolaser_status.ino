/*
  EctoLaser v0.2 - demonstrador de indicador por Arduino UNO R3
  NENHUM acionamento de laser, rele, servo ou motor.
  Comandos seriais: PING, INDICATE, CLEAR. Resposta: PONG/OK/ERR.
*/

#include <Arduino.h>
#include <string.h>

static const unsigned long BAUD = 115200UL;
static const unsigned long INDICATOR_MS = 600UL;
static const unsigned long LINK_TIMEOUT_MS = 2500UL;
static const size_t MAX_LINE = 24;

char lineBuffer[MAX_LINE + 1];
size_t lineLength = 0;
unsigned long lastSeenMs = 0;
unsigned long lastIndicateMs = 0;
bool indicating = false;

void clearIndicator() {
  digitalWrite(LED_BUILTIN, LOW);
  indicating = false;
}

void processCommand(const char *command) {
  lastSeenMs = millis();

  if (strcmp(command, "PING") == 0) {
    Serial.println(F("PONG"));
  } else if (strcmp(command, "INDICATE") == 0) {
    digitalWrite(LED_BUILTIN, HIGH);
    indicating = true;
    lastIndicateMs = millis();
    Serial.println(F("OK"));
  } else if (strcmp(command, "CLEAR") == 0) {
    clearIndicator();
    Serial.println(F("OK"));
  } else {
    clearIndicator();
    Serial.println(F("ERR"));
  }
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  clearIndicator();
  Serial.begin(BAUD);
  lastSeenMs = millis();
}

void loop() {
  while (Serial.available() > 0) {
    const int incoming = Serial.read();
    if (incoming < 0) {
      break;
    }

    if (incoming == '\r') {
      continue;
    }
    if (incoming == '\n') {
      lineBuffer[lineLength] = '\0';
      processCommand(lineBuffer);
      lineLength = 0;
      continue;
    }
    if (lineLength < MAX_LINE) {
      lineBuffer[lineLength++] = (char)incoming;
    } else {
      lineLength = 0;
      clearIndicator();
      Serial.println(F("ERR:TOO_LONG"));
    }
  }
  const unsigned long now = millis();
  if (indicating && (now - lastIndicateMs) >= INDICATOR_MS) {
    clearIndicator();
  }
  if ((now - lastSeenMs) >= LINK_TIMEOUT_MS) {
    clearIndicator();
  }
}
