const int accelerateurSensor = A0;
long accelerateurValue = 0L;
const int tauxActu = 1000/30;

// the setup function runs once when you press reset or power the board
void setup() {
  Serial.begin(9600);
}

// the loop function runs over and over again forever
void loop() {
  accelerateurValue = 0;
  for(int i = 0; i < tauxActu; i++) {
    accelerateurValue += analogRead(accelerateurSensor);
    delay(1);
  }
  if(accelerateurValue/tauxActu == 1022) {
    accelerateurValue = 1023;
  }
  else {
    accelerateurValue = accelerateurValue/tauxActu;
  }
  
  //Variables de simulation
  int batterieValue = 512;

  //Renvoi console sous forme csv (séparateur ;)
  Serial.print(accelerateurValue);
  Serial.print(";");
  Serial.print(batterieValue);
  Serial.print("\n");
}
