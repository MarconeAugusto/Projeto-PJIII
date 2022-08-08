//Integração sesnsor ultrassom e RFID

//Bibliotecas
#include <SPI.h>
#include <MFRC522.h>
#include <Ultrasonic.h>
#include <elapsedMillis.h>
#include <Thread.h>
#include <ThreadController.h>

//Constantes RFID
#define SS_PIN 53
#define RST_PIN 49
//Constantes Ultrassônico
#define pino_trigger 47
#define pino_echo 46


MFRC522 mfrc522(SS_PIN, RST_PIN); //Instância MFRC522.
Ultrasonic ultrasonic(pino_trigger, pino_echo);//Instancia Sensor

//Declarando os pinos dos LEDs
String IdVaga = "VG01";   //exemplo
String mensagem;

int ledVerde = 45, buzzer = 48, estado, estado_tmp, tempoEspera = 10000; // 10 segundos.

float distancia = 20.0, dist; // distancia utilizada 20 cm

//estados
boolean autentica_tmp, autentica = false;

//Debug
boolean debug = true;

//Estados Representados por inteiros de 1 a 4
//estado 1 = vaga livre e autenticação OK
//estado 2 = vaga livre e autenticação NOK
//estado 3 = vaga ocupada e autenticação OK
//estado 4 = vaga ocupada e autenticação NOK


// ThreadController que controlará todos os threads
ThreadController controll = ThreadController();
ThreadController controll2 = ThreadController();

//My Thread  (como um ponteiro)
Thread* myThread = new Thread();
//His Thread (not pointer)
Thread hisThread = Thread();

void configInit() {
  Serial.begin(9600);   // Inicia a serial
  Serial.println();
  Serial.println("Iniciando Serial...");
  Serial.println();
  getDistancia();       //Obtem a distancia inicial
  delay(500);
  pinMode(ledVerde , OUTPUT);
  pinMode(buzzer , OUTPUT);
  Serial.println("Iniciando Sensor Ultrassonico...");
  Serial.println();
  SPI.begin();          // Inicia o barramento SPI
  mfrc522.PCD_Init();   // Inicia MFRC522
  digitalWrite(ledVerde , LOW); // identificaçao visual para sensor ultrassonico
  estado = 2; // inicia no estado 2
  Serial.println("Iniciando aplicacao...");
  Serial.println();
  buzzer_init();
}


void setup() {
  configInit();       //Inicia Serial
  // Configure Threads
  myThread->onRun(getDistancia);
  myThread->setInterval(500);  //verifica o sensor ultrassonico 
  hisThread.onRun(getAutenticacao);
  hisThread.setInterval(500);  //verifica o RFID 
  // add as Threads ao controle
  controll.add(myThread);
  controll2.add(&hisThread);
}

void loop() {
  estado_tmp = estado;
  controll.run();   //metodo verifica distancia
  controll2.run();  //metodo verifica RFID
  if (dist > distancia) {
    digitalWrite(ledVerde , LOW);  // identificaçao visual para sensor ultrassonico
  }
  if (debug) {
    Serial.print("Distancia = ");
    Serial.print(dist);
    Serial.print(" cm. Estado = ");
    Serial.println(estado_tmp);
  }
  if (dist < distancia and (estado_tmp == 1 or estado_tmp == 2)) {
    if (debug) {
      Serial.println("if(dist < distancia and (estado_tmp == 1 or estado_tmp == 2)");
    }
    digitalWrite(ledVerde , HIGH);  // identificaçao visual para sensor ultrassonico
    elapsedMillis waiting;
    while (waiting < tempoEspera) {
      getAutenticacao(); // tempo para autenticar a vaga
    }
    if (autentica_tmp == true) {
      autentica = autentica_tmp;
      mensagem = "Vaga: " + IdVaga + ", ocupada e autenticada com sucesso.";
      estado_tmp = 3;
    } else {
      autentica = autentica_tmp;
      //autentica = false;
      mensagem = "Vaga: " + IdVaga + ", ocupada e não autenticada.";
      estado_tmp = 4;
    }
  }
  if(dist < distancia and autentica_tmp != autentica){
    if (debug) {
      Serial.println("if(dist < distancia and autentica_tmp != autentica)");
    }
    elapsedMillis waiting;
    while (waiting < tempoEspera) {
      getDistancia(); // tempo para autenticar a vaga
    }
    if(dist > distancia){
      mensagem = "Vaga: " + IdVaga + ", livre e autenticada.";
      estado_tmp = 1;
    }else{
      autentica_tmp = autentica;
    }
  }
  
  if(dist > distancia and (estado_tmp == 3 or estado_tmp == 4)){
    if (debug) {
      Serial.println("if(dist > distancia and (estado_tmp == 3 or estado_tmp == 4))");
    }
    mensagem = "Vaga: " + IdVaga + ", livre com saida não autenticada.";
    estado_tmp = 1;
  }

  if (estado_tmp != estado) {
    // invocar método para enviar via sigfox
    if (debug) {
      delay(500);
      Serial.println();
      Serial.println(mensagem);
      Serial.println();
      delay(500);
    }
  } else {
    delay(500);
    if (debug) {
      Serial.println("Nenhuma alteração detectada...");
    }
  }
  estado = estado_tmp;
}

void getDistancia() { // myThread
  //Serial.println("Verifica distancia"); // debug
  //Le as informacoes do sensor e converte para centímetros
  float cmMsec;
  long microsec = ultrasonic.timing();
  cmMsec = ultrasonic.convert(microsec, Ultrasonic::CM);
  dist = cmMsec;
}

void getAutenticacao() { // hisThread
  if(debug){
    Serial.println("Verifica RFID"); // debug
  }
  if ( ! mfrc522.PICC_IsNewCardPresent()) {
    return;
  }
  // Selecione um dos cartões
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    return;
  }
  //Mostra o UID na serial
  Serial.println();
  Serial.println();
  Serial.print("UID da tag :");
  String conteudo = "";
  for (byte i = 0; i < mfrc522.uid.size; i++)
  {
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(mfrc522.uid.uidByte[i], HEX);
    conteudo.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    conteudo.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.println();
  Serial.println();
  //Serial.print("Mensagem : ");
  conteudo.toUpperCase();
  if (conteudo.substring(1) == "40 1F 63 46") { //UID 1 - Chaveiro
    if (autentica_tmp == false) {
      autentica_tmp = true;  //altera a variavel
    } else {
      autentica_tmp = false;  //altera a variavel
    }
    //Serial.println("Vaga autenticada");
    buzzer_aprovado();
    delay(2500);
  } else {
    autentica_tmp = false;
    //Serial.println("Vaga nao autenticada");
    buzzer_rejeitado();
    delay(2500);
  }
}

void buzzer_init() {
  int frequencia = 8000;
  tone(buzzer, frequencia, 500);
}

void buzzer_aprovado() {
  int frequencia = 3500;
  tone(buzzer, frequencia, 500);
}

void buzzer_rejeitado() {
  int frequencia = 300;
  tone(buzzer, frequencia, 500);
}
