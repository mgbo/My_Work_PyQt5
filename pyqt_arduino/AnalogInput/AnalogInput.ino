
const int analogIn = A0;
int analogVal = 0;

void setup() {
  // declare the ledPin as an OUTPUT:
  Serial.begin(9600);
  pinMode(analogIn, INPUT);
}

void loop() {
  analogVal = analogRead(analogIn);
  Serial.println(analogVal);
  delay(1000);
}
