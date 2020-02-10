#include <Stepper.h>

#define leftMic 0
#define rightMic 1
#define thresh 200

#define SPR 200
#define RPM 60

int steps = SPR / 8;

Stepper looker(spr, 8, 9, 10, 11);

void setup() {
  pinMode(leftMic, INPUT);
  pinMode(rightMic, INPUT);

  looker.setSpeed(RPM);

  Serial.begin(115200);
}

void loop() {
  leftSamp = analogRead(leftMic);
  rightSamp = analogRead(rightSamp);

  if (rightSamp - leftSamp > thresh) {
    looker.step(steps); 
  } else if (leftSamp - rightSamp > thresh) {
    looker.step(-steps);
  }
}
