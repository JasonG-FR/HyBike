const int accelerateurSensor = A0;
const int freinSensor = A1;
long accelerateurValue = 0L;
long freinValue = 0L;
const int tauxActu = 1000/30;

// the setup function runs once when you press reset or power the board
void setup() {
  Serial.begin(9600);
}

// the loop function runs over and over again forever
void loop() {
  accelerateurValue = 0;
  freinValue = 0;
  for(int i = 0; i < tauxActu; i++) {
    accelerateurValue += analogRead(accelerateurSensor);
    freinValue += analogRead(freinSensor);
    delay(1);
  }
  
  if(accelerateurValue/tauxActu == 1022) {
    accelerateurValue = 1023;
  }
  else {
    accelerateurValue = accelerateurValue/tauxActu;
  }

  if(freinValue/tauxActu == 1022) {
    freinValue = 1023;
  }
  else {
    freinValue = freinValue/tauxActu;
  }
  
  //Variables de simulation à développer
  int batterieValue = 512;

  //Renvoi console sous forme csv (séparateur ;)
  Serial.print(accelerateurValue);
  Serial.print(";");
  Serial.print(freinValue);
  Serial.print(";");
  Serial.print(batterieValue);
  Serial.print("\n");
}
