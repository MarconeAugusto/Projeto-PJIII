//Sensor ultrassom, RFID e Sigfox
///////Estados Representados por inteiros de 1 a 4
///////estado 1 = vaga livre e autenticação OK
///////estado 2 = vaga livre e autenticação NOK
///////estado 3 = vaga ocupada e autenticação OK
///////estado 4 = vaga ocupada e autenticação NOK

//Bibliotecas
#include <SPI.h>
#include <MFRC522.h>
#include <Ultrasonic.h>
#include <elapsedMillis.h>
#include <Thread.h>
#include <ThreadController.h>
#include <WISOL.h>
#include <Wire.h>
#include <avr/wdt.h>

//Constantes RFID
#define SS_PIN 53
#define RST_PIN 49
//Constantes Ultrassônico
#define pino_trigger 47
#define pino_echo 45

MFRC522 mfrc522(SS_PIN, RST_PIN); //Instância MFRC522.
Ultrasonic ultrasonic(pino_trigger, pino_echo);//Instancia Sensor

//Variáveis
String mensagem, TAG = "", IdVaga = "A02";  //exemplo 7 bytes, limitado a 8 bytes no node-red
char msgSigfox[9];
int watchdogCounter, ledVerde = 43, ledCadastro = 39, buzzer = 25, estado = 2, estado_tmp, interruptPin = 41, tempoEspera = 10000; // 10 segundos.
float distancia = 10.0, dist; // distancia utilizada 15 cm
boolean autentica_tmp, autentica = false, debug = true, cadastro = false;
uint8_t PublicModeSF, stateLED, ledCounter;

// ThreadController que controlará todos os threads
ThreadController controll = ThreadController();
ThreadController controll2 = ThreadController();

Thread* myThread = new Thread();
Thread hisThread = Thread();

Isigfox *Isigfox = new WISOL();

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void configInit() {
  Serial.begin(9600);   // Inicia a serial
  Serial.println();
  Serial.println("Iniciando Serial...");
  Serial.println();
  getDistancia();       //Obtem a distancia inicial
  pinMode(ledVerde , OUTPUT);
  pinMode(ledCadastro , OUTPUT);
  digitalWrite(ledCadastro , LOW); // identificaçao visual para o cadastro
  pinMode(buzzer , OUTPUT);
  pinMode(interruptPin, INPUT);
  Serial.println("Iniciando Sensor Ultrassonico...");
  Serial.println();
  digitalWrite(ledVerde , LOW); // identificaçao visual para sensor ultrassonico
  estado = 2; // inicia no estado 2
  Serial.println("Iniciando aplicacao...");
  Serial.println();
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void setup() {
  int flagInit;
  Wire.begin();
  Wire.setClock(10000000);
  configInit();
  watchdogCounter = 0;
  flagInit = -1;
  while (flagInit == -1) {
    Serial.println(""); // Make a clean restart
    delay(1000);
    PublicModeSF = 0;
    flagInit = Isigfox->initSigfox();
    Isigfox->testComms();
    GetDeviceID();
  }
  // Init LED
  stateLED = 0;
  ledCounter = 0;
  // Configure Threads
  myThread->onRun(getDistancia);
  myThread->setInterval(600);  //verifica o sensor ultrassonico
  hisThread.onRun(getAutenticacao);
  hisThread.setInterval(500);  //verifica o RFID
  // add as Threads ao controle
  controll.add(myThread);
  controll2.add(&hisThread);
  buzzer_init();
  strcpy(msgSigfox, IdVaga.c_str()); //copia a string com id_vaga para a mensagem a ser enviada
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void loop() {
  estado_tmp = estado;
  cadastro = false;
  wdt_reset();
  controll.run();   //metodo verifica distancia
  controll2.run();  //metodo verifica RFID
  //Cadastro tag
  while (digitalRead(interruptPin) != HIGH) {
    digitalWrite(ledCadastro , HIGH); // identificaçao visual para o cadastro
    cadastroTAG();
    Serial.print("var cadastro: ");
    Serial.println(cadastro);
    if (cadastro == true and digitalRead(interruptPin) != HIGH) {
      while (digitalRead(interruptPin) != HIGH) {
        getTAG(); // tempo para autenticar a vaga
      }
    }
  }
  digitalWrite(ledCadastro , LOW); // identificaçao visual para o cadastro
  //Estados
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
    getDistancia();
    if (autentica_tmp == true and dist < distancia) {
      autentica = autentica_tmp;
      mensagem = "Vaga: " + IdVaga + ", ocupada e autenticada com sucesso.";
      estado_tmp = 3;
    }
    else if (autentica_tmp == false and dist > distancia) {
      mensagem = "Vaga: " + IdVaga + ", livre com saida não autenticada.";
      estado_tmp = 2;
    }
    else {
      autentica = autentica_tmp;
      //autentica = false;
      mensagem = "Vaga: " + IdVaga + ", ocupada e não autenticada.";
      estado_tmp = 4;
    }
  }
  if (dist < distancia and autentica_tmp != autentica) {
    if (debug) {
      Serial.println("if(dist < distancia and autentica_tmp != autentica)");
    }
    elapsedMillis waiting;
    while (waiting < tempoEspera) {
      getDistancia(); // tempo para autenticar a vaga
    }
    if (dist > distancia) {
      mensagem = "Vaga: " + IdVaga + ", livre e autenticada.";
      estado_tmp = 1;
    } else {
      autentica_tmp = autentica;
    }
  }

  if (dist > distancia and (estado_tmp == 3 or estado_tmp == 4)) {
    if (debug) {
      Serial.println("if(dist > distancia and (estado_tmp == 3 or estado_tmp == 4))");
    }
    mensagem = "Vaga: " + IdVaga + ", livre com saida não autenticada.";
    estado_tmp = 2;
  }

  if (estado_tmp != estado) {
    // invocar método para enviar via sigfox
    SendMSG(estado_tmp);
    if (debug) {
      Serial.println("####################################################");
      Serial.println(mensagem);
      Serial.println("####################################################");
      Serial.println();
    }
    delay(1000);
  } else {
    delay(1000);
    if (debug) {
      Serial.println("Nenhuma alteração detectada...");
      Serial.print("TAG: ");
      Serial.println(TAG);
    }
  }
  estado = estado_tmp;
  autentica = autentica_tmp;
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void getDistancia() {
  //Le as informacoes do sensor e converte para centímetros
  float cmMsec;
  long microsec = ultrasonic.timing();
  cmMsec = ultrasonic.convert(microsec, Ultrasonic::CM);
  dist = cmMsec;
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void getAutenticacao() {
  SPI.begin();          // Inicia o barramento SPI
  mfrc522.PCD_Init();   // Inicia MFRC522
  if (debug) {
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
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(mfrc522.uid.uidByte[i], HEX);
    conteudo.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    conteudo.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.println();
  Serial.println();
  conteudo.toUpperCase();
  if (conteudo.substring(1) == TAG) { //UID 1 - Chaveiro
    if (autentica_tmp == false) {
      autentica_tmp = true;  //altera a variavel
    } else {
      autentica_tmp = false;  //altera a variavel
    }
    //Serial.println("Vaga autenticada");
    buzzer_aprovado();
    delay(1500);
  } else {
    autentica_tmp = false;
    buzzer_rejeitado();
    delay(1500);
  }
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void buzzer_init() {
  int frequencia = 8000;
  tone(buzzer, frequencia, 500);
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void buzzer_aprovado() {
  int frequencia = 3500;
  tone(buzzer, frequencia, 500);
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void buzzer_rejeitado() {
  int frequencia = 300;
  tone(buzzer, frequencia, 500);
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void cadastroTAG() {
  if (debug) {
    Serial.println("Aguardando TAG ADM, para liberar o cadastro");
  }
  SPI.begin();          // Inicia o barramento SPI
  mfrc522.PCD_Init();   // Inicia MFRC522
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
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(mfrc522.uid.uidByte[i], HEX);
    conteudo.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    conteudo.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.println();
  Serial.println();
  conteudo.toUpperCase();
  if (conteudo.substring(1) == "39 13 35 5B") { //UID 1 - Cartão
    buzzer_init();
    if (debug) {
      Serial.println("TAG Adiministrador ativada");
      Serial.println("Cadastrar nova TAG");
    }
    delay(1000);
    cadastro = true;
  } else {
    cadastro = false;
  }
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void getTAG() {
  if (debug) {
    Serial.println("GET TAG");
  }
  SPI.begin();          // Inicia o barramento SPI
  mfrc522.PCD_Init();   // Inicia MFRC522
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
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(mfrc522.uid.uidByte[i], HEX);
    conteudo.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    conteudo.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.println();
  conteudo.toUpperCase();
  TAG = conteudo.substring(1); // retira o primeiro espaço
  if (TAG != "") {
    Serial.print("TAG cadastrada: ");
    Serial.println(TAG);
    buzzer_aprovado();
  } else {
    delay(2000);
  }
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void Send_Pload(uint8_t *sendData, const uint8_t len) {
  // No downlink message require
  recvMsg *RecvMsg;
  RecvMsg = (recvMsg *)malloc(sizeof(recvMsg));
  Isigfox->sendPayload(sendData, len, 0, RecvMsg);
  for (int i = 0; i < RecvMsg->len; i++) {
    Serial.print(RecvMsg->inData[i]);
  }
  Serial.println("");
  free(RecvMsg);
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void SendMSG(int estado_tmp) {
  msgSigfox[8] = (char)estado_tmp;
  const uint8_t payloadSize = 9; //in bytes
  //  byte* buf_str = (byte*) malloc (payloadSize);
  uint8_t buf_str[payloadSize];
  buf_str[0] = msgSigfox[0] == 0x00 ? ' ' : msgSigfox[0];
  buf_str[1] = msgSigfox[1] == 0x00 ? ' ' : msgSigfox[1];
  buf_str[2] = msgSigfox[2] == 0x00 ? ' ' : msgSigfox[2];
  buf_str[3] = msgSigfox[3] == 0x00 ? ' ' : msgSigfox[3];
  buf_str[4] = msgSigfox[4] == 0x00 ? ' ' : msgSigfox[4];
  buf_str[5] = msgSigfox[5] == 0x00 ? ' ' : msgSigfox[5];
  buf_str[6] = msgSigfox[6] == 0x00 ? ' ' : msgSigfox[6];
  buf_str[7] = msgSigfox[7] == 0x00 ? ' ' : msgSigfox[7];
  buf_str[8] = msgSigfox[8] == 0x00 ? ' ' : msgSigfox[8];
  Send_Pload(buf_str, payloadSize);
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void sendInterval() {
  Serial.println("Mensagem temporizada");
  SendMSG(5); //sem alteracao
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void watchdog_disable() { // Disable watchdog timer
  cli();  // disable all interrupts
  WDTCSR |= B00011000;
  WDTCSR = B00110001;
  sei();
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
ISR(WDT_vect) // Watchdog timer interrupt.
{
  // Include your code here - be careful not to use functions they may cause the interrupt to hang and
  // prevent a reset.
  Serial.print("WD reset: ");
  Serial.println(watchdogCounter);
  watchdogCounter++;
  if (watchdogCounter == 20) { // reset CPU after about 180 s
    // Reset the CPU next time
    // Enable WD reset
    cli();  // disable all interrupts
    WDTCSR |= B00011000;
    WDTCSR = B01111001;
    sei();
    wdt_reset();
  } else if (watchdogCounter < 8) {
    wdt_reset();
  }
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void GetDeviceID() {
  recvMsg *RecvMsg;
  const char msg[] = "AT$I=10";
  RecvMsg = (recvMsg *)malloc(sizeof(recvMsg));
  Isigfox->sendMessage(msg, 7, RecvMsg);
  Serial.print("Device ID: ");
  for (int i = 0; i < RecvMsg->len; i++) {
    Serial.print(RecvMsg->inData[i]);
  }
  Serial.println("");
  free(RecvMsg);
}
