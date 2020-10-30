
const int analogIn = A0; // define pin number
int analogVal = 0; // variable

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
