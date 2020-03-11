#include <Servo.h>
Servo sol_goz_x;
Servo sol_goz_y;
Servo sag_goz_x;
Servo sag_goz_y;
Servo sol_kas;
Servo sag_kas;

int sag_goz_y_potpin = 0;
int sag_goz_x_potpin = 1;
int sol_goz_y_potpin = 2;
int sol_goz_x_potpin = 3;
int sag_kas_potpin = 4;
int sol_kas_potpin = 5;
int val0,val1,val2,val3,val4,val5,x,y,z,kas,kas_lim_0,kas_lim_1,goz_y_lim_0,goz_y_lim_1,goz_x_lim_0,goz_x_lim_1;

int xPin = A2; // A0-A5 analog pinlerinden herhangi birine bağlanabilir.
int yPin = A1; // A0-A5 analog pinlerinden herhangi birine bağlanabilir.
int butonPin = 9; // Joystick buton pini arduino bağlantısı (Joystick SW çıkışı)
 
int xPozisyonu = 0;
int yPozisyonu = 0;
int butonDurum = 0;
 
void setup()
{
Serial.begin(9600);
sol_goz_y.attach(4);
sol_goz_x.attach(5);
sag_goz_y.attach(2);
sag_goz_x.attach(3);
sol_kas.attach(7);
sag_kas.attach(6);
pinMode(xPin, INPUT);
pinMode(yPin, INPUT);
pinMode(butonPin, INPUT_PULLUP);
}

void loop()
{
  xPozisyonu = analogRead(xPin);
  yPozisyonu = analogRead(yPin);
  butonDurum = digitalRead(butonPin);
  
  int kas = analogRead(sag_kas_potpin);
  int kasMapped = map(kas, 0, 1023, 0, 100);
  //Serial.println(kasMapped);

  int gozx = analogRead(sol_kas_potpin);
  int gozMappedx = map(yPozisyonu, 0, 1023, -100, 100);
  //Serial.println(gozMapped);

  int gozY = analogRead(sol_goz_x_potpin);
  int gozYMapped = map(xPozisyonu, 0, 1023, -100, 100);
  //Serial.println(gozYMapped);

  synch_kas(kasMapped);
  sync_goz(gozMappedx,gozYMapped);
  delay(150);
}

void synch_kas(int kasMapped)
{
  
sag_kas_move(kasMapped);
sol_kas_move(kasMapped);
}

void sync_goz(int gozMappedx,int gozYMapped)
{

sag_goz_Xmove(gozMappedx);
sol_goz_Xmove(gozMappedx);


sag_goz_Ymove(gozYMapped);
sol_goz_Ymove(gozYMapped);
 
}

void sag_kas_move(int kasLocation){
int sag_kas_lim_0=70;
int sag_kas_lim_1=107;
int isInverse=0;
  if(isInverse==1){
  kasLocation=100-kasLocation;
  }
int sagkasMapped = map(kasLocation, 0, 100, sag_kas_lim_0, sag_kas_lim_1); 
sag_kas.write(sagkasMapped);
//Serial.println(sagkasMapped);
}
void sol_kas_move(int kasLocation){
int solkasMapped=0;
int sol_kas_lim_0=18;
int sol_kas_lim_1=48 ;
int isInverse=1;
  if(isInverse==1){
  kasLocation=100-kasLocation;
  }
solkasMapped = map(kasLocation, 0, 100, sol_kas_lim_0, sol_kas_lim_1); 
sol_kas.write(solkasMapped);
//Serial.println(solkasMapped);
}

void sag_goz_Xmove(int Location){
int sag_goz_lim_0=85;
int sag_goz_lim_1=125;
int saggozMapped = map(Location, -100, 100, sag_goz_lim_0, sag_goz_lim_1); 
sag_goz_x.write(saggozMapped);
//Serial.println(saggozMapped);
}
void sol_goz_Xmove(int Location){
int sol_goz_lim_0=75;
int sol_goz_lim_1=110;
int solgozMapped = map(Location, -100, 100, sol_goz_lim_0, sol_goz_lim_1); 
Serial.println(solgozMapped);
sol_goz_x.write(solgozMapped);
//Serial.println(sagkasMapped);
}

void sag_goz_Ymove(int Location){
int sag_goz_Ylim_0=85;
int sag_goz_Ylim_1=125;
int saggozYMapped = map(Location, -100, 100, sag_goz_Ylim_0, sag_goz_Ylim_1); 
sag_goz_y.write(saggozYMapped);
//Serial.println(saggozMapped);
}
void sol_goz_Ymove(int Location){
int sol_goz_Ylim_0=70+5;
int sol_goz_Ylim_1=110+5;
int solgozYMapped = map(Location*-1, -100, 100, sol_goz_Ylim_0, sol_goz_Ylim_1); 
sol_goz_y.write(solgozYMapped);
//Serial.println(sagkasMapped);
}
