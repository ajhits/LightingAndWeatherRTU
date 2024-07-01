#define DELAY_TIMEOUT 1500

int ir_right_pin = 2;
int ir_left_pin = 3;

int ir_right_state = 0;
int ir_left_state = 0;

int ir_right_state_last = -1;
int ir_left_state_last = -1;

int in_counter = 0;
int out_counter = 0;

unsigned long last_trigger_time = 0;
bool isWalkingIn = false;
bool isWalkingOut = false;

void setup() {
  Serial.begin(9600);
  pinMode(ir_right_pin, INPUT);
  pinMode(ir_left_pin, INPUT);
}

void loop() {
  ir_right_state = digitalRead(ir_right_pin);
  ir_left_state = digitalRead(ir_left_pin);

  checkWalkIn();
  checkWalkOut();
}

void checkWalkIn() {
  if (ir_right_state != ir_right_state_last) {
    ir_right_state_last = ir_right_state;
    if (!isWalkingIn && ir_right_state == LOW) {
      isWalkingIn = true;
      last_trigger_time = millis();
    }
  }

  if (millis() - last_trigger_time > DELAY_TIMEOUT) {
    isWalkingIn = false;
  }

  if (isWalkingIn && ir_left_state == LOW && ir_right_state == HIGH) {
    isWalkingIn = false;
    in_counter = 1;
    out_counter = 0; // Reset the out_counter
    last_trigger_time = millis(); // Reset last trigger time
    Serial.print(in_counter);
    Serial.print(",");
    Serial.println(out_counter);
  }


}

void checkWalkOut() {
  if (ir_left_state != ir_left_state_last) {
    ir_left_state_last = ir_left_state;
    if (!isWalkingOut && ir_left_state == LOW) {
      isWalkingOut = true;
      last_trigger_time = millis();
    }
  }

  if (millis() - last_trigger_time > DELAY_TIMEOUT) {
    isWalkingOut = false;
  }

  if (isWalkingOut && ir_right_state == LOW && ir_left_state == HIGH) {
    isWalkingOut = false;
    out_counter= 1;
    in_counter = 0; // Reset the out_counter
    if (in_counter > 0) {
      in_counter--; // Subtract one from in_counter only if it's greater than 0
    }
    last_trigger_time = millis(); // Reset last trigger time
    Serial.print(in_counter);
    Serial.print(",");
    Serial.println(out_counter);
  }

}