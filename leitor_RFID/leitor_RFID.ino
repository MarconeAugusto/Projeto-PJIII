//Programa : RFID - Controle de Acesso leitor RFID
//Autor : MARCONE AUGUSTO
 
#include <SPI.h>
#include <MFRC522.h>
 
#define SS_PIN 53
#define RST_PIN 22
MFRC522 mfrc522(SS_PIN, RST_PIN);   // Crie a instância MFRC522.
 
char st[20];
// selecione os pinos para os LEDs e buzzer
int ledVerde = 33, ledVermelho = 31, ledAzul = 35, buzzer = 37;

void setup() 
{
  Serial.begin(9600);   // Inicia a serial
  // declara o pinos dos LEDs como um OUTPUT:
  pinMode(ledVerde , OUTPUT);
  pinMode(ledVermelho , OUTPUT);
  pinMode(ledAzul , OUTPUT);
  pinMode(buzzer , OUTPUT);
  SPI.begin();     // Inicia o barramento SPI
  mfrc522.PCD_Init();   // Inicia MFRC522
  Serial.println("Aproxime o seu cartao do leitor...");
  Serial.println();
}
 
void loop() 
{
  digitalWrite(ledAzul , LOW);
  digitalWrite(ledVerde , HIGH);
  digitalWrite(ledVermelho , HIGH);
  // Procure por novos cartões
  if ( ! mfrc522.PICC_IsNewCardPresent()){
    return;
  }
  // Selecione um dos cartões
  if ( ! mfrc522.PICC_ReadCardSerial()){
    return;
  }
  //Mostra o UID na serial
  Serial.print("UID da tag :");
  String conteudo= "";
  byte letra;
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
     Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
     Serial.print(mfrc522.uid.uidByte[i], HEX);
     conteudo.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     conteudo.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.println();
  Serial.print("Mensagem : ");
  conteudo.toUpperCase();
  digitalWrite(ledAzul , HIGH);
  if (conteudo.substring(1) == "40 1F 63 46") //UID 1 - Chaveiro
  {
    Serial.println("Ola Marcone Augusto !");
    Serial.println("Vaga autenticada");
    Serial.println();
    digitalWrite(ledVerde , LOW);
    buzina_aprovado();
    delay(2500);
    digitalWrite(ledVerde , HIGH);
  }
 
  if (conteudo.substring(1) == "39 13 35 5B") //UID 2 - Cartao
  {
    Serial.println("Ola Vinicius Luz !");
    Serial.println("Vaga não autenticada");
    Serial.println();
    digitalWrite(ledVermelho , LOW);
    buzina_rejeitado();
    delay(2500);
    digitalWrite(ledVermelho , HIGH);
  }
} 

void buzina_aprovado(){
    int frequencia = 3500;
    tone(buzzer,frequencia,500);
}
void buzina_rejeitado(){
    int frequencia = 300;
    tone(buzzer,frequencia,500);
}
