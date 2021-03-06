
//Билиотека RFID создана мигелем бальбова (circuitto.com)
#include <RFID.h>
#include <SPI.h>
#define SS_PIN 10
#define RST_PIN 9

RFID rfid(SS_PIN, RST_PIN);

// определение переменных
int serNum0;
int serNum1;
int serNum2;
int serNum3;
int serNum4;

// buzzer
int speaker_pin = 8;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  SPI.begin();
  rfid.init();

  pinMode(speaker_pin, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  // в этом цикле выполняется поиск карт для считывания
  if (rfid.isCard()){
    if (rfid.readCardSerial()){
      if (rfid.serNum[0] != serNum0
          && rfid.serNum[1] != serNum1
          && rfid.serNum[2] != serNum2
          && rfid.serNum[3] != serNum3
          && rfid.serNum[4] != serNum4
          ){
            // Если карта найдена, выполняется следующий код
            //Serial.println(" ");
//            Serial.println("Card found");
            serNum0 = rfid.serNum[0];
            serNum1 = rfid.serNum[1];
            serNum2 = rfid.serNum[2];
            serNum3 = rfid.serNum[3];
            serNum4 = rfid.serNum[4];
  
            //выводится идентификатор карты в мониторе порта IDE
//            Serial.println("Cardnumber:");
//            Serial.print("Dec: ");
            Serial.print(rfid.serNum[0], DEC);
//            Serial.print(", ");
            Serial.print(rfid.serNum[1], DEC);
//            Serial.print(", ");
            Serial.print(rfid.serNum[2], DEC);
//            Serial.print(", ");
            Serial.print(rfid.serNum[3], DEC);
//            Serial.print(", ");
            Serial.print(rfid.serNum[4], DEC);
//            Serial.println(" ");
            
//            Serial.print("Hex: ");
//            Serial.print(rfid.serNum[0], HEX);
//            Serial.print(", ");
//            Serial.print(rfid.serNum[1], HEX);
//            Serial.print(", ");
//            Serial.print(rfid.serNum[2], HEX);
//            Serial.print(", ");
//            Serial.print(rfid.serNum[3], HEX);
//            Serial.print(", ");
//            Serial.print(rfid.serNum[4], HEX);
            Serial.print("\n");

            for (int i=0; i<150; i++){
              digitalWrite(speaker_pin, HIGH);
              delay(1);
              digitalWrite(speaker_pin, LOW);
              delay(1);
            }
            
            
          } 
          //else {
            //если индентификатор совпадает, выводится точка в мониторе порта
           // Serial.print(".");
          //}
  }
  
}
  rfid.halt();
  delay(500);
}
