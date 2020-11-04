
void setup() {
  Serial.begin(115200);
}
     
void loop() {
  if (Serial.available()) {
    if (Serial.read() == 'p'){
      Serial.print(analogRead(A0));
      Serial.print("\n");
    }
  }
}
