//Programa: Conectando Sensor Ultrassonico HC-SR04 ao Arduino
//Autor: Marcone Augusto
 
//Carrega a biblioteca do sensor ultrassonico
#include <Ultrasonic.h>
 
//Define os pinos para o trigger e echo
#define pino_trigger 49
#define pino_echo 48
 
//Inicializa o sensor nos pinos definidos acima
Ultrasonic ultrasonic(pino_trigger, pino_echo);
//Declarando os pinos dos LEDs
int ledVerde = 47, ledVermelho = 46;

void setup(){
  Serial.begin(9600);
  pinMode(ledVerde , OUTPUT);
  pinMode(ledVermelho , OUTPUT);
}
 
void loop()
{
  //Le as informacoes do sensor e converte para centímetros
  digitalWrite(ledVerde , LOW);
  float cmMsec, inMsec;
  long microsec = ultrasonic.timing();
  cmMsec = ultrasonic.convert(microsec, Ultrasonic::CM);
  Serial.print("Distancia em cm: ");
  Serial.println(cmMsec);
  if(cmMsec <= 10){
      digitalWrite(ledVerde , HIGH);
      digitalWrite(ledVermelho , LOW);
      delay(1000);
  }else
      digitalWrite(ledVermelho , HIGH);
      delay(1000); 
}
