const int analogInPin = A0;
const int openPin = 2;
const int closePin = 3;

int sensorValue = 0;

void setup() {
//  Serial.begin(9600);
  pinMode(openPin, OUTPUT);
  pinMode(closePin, OUTPUT);
}

#define STATE_OFF 0
#define STATE_DEBOUNCE_ON 1
#define STATE_ON 2
#define STATE_DEBOUNCE_OFF 3

int state = STATE_OFF;
int debounce_counter = 0;
int debounce_limit = 10;

void loop() {


//  if (state == STATE_OFF)
//    Serial.println("STATE_OFF");
//  else if (state == STATE_DEBOUNCE_ON)
//    Serial.println("STATE_DEBOUNCE_ON");
//  else if (state == STATE_ON)
//    Serial.println("STATE_ON");
//  else if (state == STATE_DEBOUNCE_OFF)
//    Serial.println("STATE_DEBOUNCE_OFF");


  if (state == STATE_OFF) {
    digitalWrite(openPin, LOW);
    digitalWrite(closePin, LOW);
    sensorValue = analogRead(analogInPin);
    if (sensorValue > 400) {
      state = STATE_DEBOUNCE_ON;
    }
  }

  else if (state == STATE_DEBOUNCE_ON) {
    debounce_counter++;
    sensorValue = analogRead(analogInPin);
    if (sensorValue < 400) {
      debounce_counter = 0;
      state = STATE_OFF;
    }
    else if (debounce_counter == debounce_limit) {
      debounce_counter = 0;
      digitalWrite(openPin, LOW);
      digitalWrite(closePin, HIGH);
      delay(250);
      state = STATE_ON;
    }
  }

  else if (state == STATE_ON) {
    digitalWrite(openPin, LOW);
    digitalWrite(closePin, LOW);
    sensorValue = analogRead(analogInPin);
    if (sensorValue < 400) {
      state = STATE_DEBOUNCE_OFF;
    }
  }
  
  else if (state == STATE_DEBOUNCE_OFF) {
    sensorValue = analogRead(analogInPin);
    if (sensorValue < 400) {
      debounce_counter++;
    }
    if (debounce_counter == debounce_limit) {
      debounce_counter = 0;
      digitalWrite(openPin, HIGH);
      digitalWrite(closePin, LOW);
      delay(250);
      state = STATE_OFF;
    }
  }
  
  delay(50);
}
