const int led_red = 3;
const int led_yellow = 4;
const int led_green = 5;
const int btn = 2;

//LED FOR PEOPLE
const int ledp_red = 6;
const int ledp_green = 7;

void setup() {
  pinMode(led_red, OUTPUT);    
  pinMode(led_yellow, OUTPUT);    
  pinMode(led_green, OUTPUT);    
  pinMode(ledp_red, OUTPUT);    
  pinMode(ledp_green, OUTPUT);         
  pinMode(btn, INPUT);
  Serial.begin(9600);
}

void loop(){
  if(digitalRead(btn) == HIGH){
    digitalWrite(ledp_red, HIGH);
    digitalWrite(led_green, LOW);
    delay(500);
    digitalWrite(led_green, HIGH);
    delay(500);
    digitalWrite(led_green, LOW);
    delay(500);
    digitalWrite(led_green, HIGH);
    delay(500);
    digitalWrite(led_green, LOW);
    delay(500);
    digitalWrite(led_green, HIGH);
    delay(500);
    digitalWrite(led_green, LOW);
    digitalWrite(led_yellow,HIGH);
    delay(3000);
    digitalWrite(led_yellow, LOW);
    digitalWrite(led_red, HIGH);
    delay(3000);
        //FOR PEOPLE
    digitalWrite(ledp_red, LOW);
    digitalWrite(ledp_green, HIGH);
    delay(14000);
    digitalWrite(ledp_green, LOW);
    delay(500);
    digitalWrite(ledp_green, HIGH);
    delay(500);
    digitalWrite(ledp_green, LOW);
    delay(500);
    digitalWrite(ledp_green, HIGH);
    delay(500);
    digitalWrite(ledp_green, LOW);
    delay(500);
    digitalWrite(ledp_green, HIGH);
    delay(500);
    digitalWrite(ledp_green, LOW);
    delay(3000);
    digitalWrite(led_red, LOW);
  }
  else{
     digitalWrite(led_green, HIGH);
     digitalWrite(ledp_red, HIGH);
  }
}
