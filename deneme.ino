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


void setup()
{
Serial.begin(9600);
sol_goz_y.attach(4);
sol_goz_x.attach(5);
sag_goz_y.attach(2);
sag_goz_x.attach(3);
sol_kas.attach(7);
sag_kas.attach(6);
}

void loop()
{
  int kas = analogRead(sag_kas_potpin);
  int kasMapped = map(kas, 0, 1023, 0, 100);
  //Serial.println(kasMapped);

  int gozx = analogRead(sol_kas_potpin);
  int gozMappedx = map(gozx, 0, 1023, -100, 100);
  //Serial.println(gozMapped);

  int gozY = analogRead(sol_goz_x_potpin);
  int gozYMapped = map(gozY, 0, 1023, -100, 100);
  //Serial.println(gozYMapped);

  synch_kas(kasMapped);
  sync_goz(gozMappedx,gozYMapped);
  delay(150);
}

//void gozler_xyz()
//{
//goz_y_lim_0=0;
//goz_y_lim_1=179;
//
//goz_x_lim_0=0;
//goz_x_lim_1=180;
//
//
//x= analogRead(0);  
//x = map(x, 0, 1023, goz_x_lim_0, goz_x_lim_1*5/6); 
//
//y = analogRead(1);  
//y = map(y, 0, 1023, goz_y_lim_0, goz_y_lim_1); 
//
//z = analogRead(2);  
//z = map(z, 0, 1023, -1*(goz_x_lim_1/6), goz_x_lim_1/6); 
//
//sol_goz_y.write(y);
//sag_goz_y.write(180-y);
//
//sol_goz_x.write(x+z);
//sag_goz_x.write(x-z);
//
//delay(50);
//}

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
int sag_kas_lim_0=15;
int sag_kas_lim_1=90;
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
int sol_kas_lim_0=0;
int sol_kas_lim_1=75 ;
int isInverse=1;
  if(isInverse==1){
  kasLocation=100-kasLocation;
  }
solkasMapped = map(kasLocation, 0, 100, sol_kas_lim_0, sol_kas_lim_1); 
sol_kas.write(solkasMapped);
//Serial.println(solkasMapped);
}

void sag_goz_Xmove(int Location){
int sag_goz_lim_0=60;
int sag_goz_lim_1=120;
int saggozMapped = map(Location, -100, 100, sag_goz_lim_0, sag_goz_lim_1); 
sag_goz_x.write(saggozMapped);
//Serial.println(saggozMapped);
}
void sol_goz_Xmove(int Location){
int sol_goz_lim_0=60;
int sol_goz_lim_1=120;
int solgozMapped = map(Location, -100, 100, sol_goz_lim_0, sol_goz_lim_1); 
Serial.println(solgozMapped);
sol_goz_x.write(solgozMapped);
//Serial.println(sagkasMapped);
}

void sag_goz_Ymove(int Location){
int sag_goz_Ylim_0=70+5;
int sag_goz_Ylim_1=110+5;
int saggozYMapped = map(Location, -100, 100, sag_goz_Ylim_0, sag_goz_Ylim_1); 
sag_goz_y.write(saggozYMapped);
//Serial.println(saggozMapped);
}
void sol_goz_Ymove(int Location){
int sol_goz_Ylim_0=70+10;
int sol_goz_Ylim_1=110+10;
int solgozYMapped = map(Location*-1, -100, 100, sol_goz_Ylim_0, sol_goz_Ylim_1); 
sol_goz_y.write(solgozYMapped);
//Serial.println(sagkasMapped);
}


//void asynch_kas()
//{
//kas_lim_0=0;
//kas_lim_1=179;
//val4 = analogRead(sag_kas_potpin);  
//val4 = map(val4, 0, 1023, kas_lim_0, kas_lim_1); 
//sag_kas.write(val4);  
//
//val5 = analogRead(sol_kas_potpin);  
//val5 = map(val5, 0, 1023, kas_lim_0, kas_lim_1); 
//sol_kas.write(val5); 
//
//delay(50);
//}


//void six_pot()
//{
//val0 = analogRead(sag_goz_y_potpin);  
//val0 = map(val0, 0, 1023, 0, 179); 
//sag_goz_y.write(val0);  
//
//val1 = analogRead(sag_goz_x_potpin);  
//val1 = map(val1, 0, 1023, 0, 179); 
//sag_goz_x.write(val1);  
//
//val2 = analogRead(sol_goz_y_potpin);  
//val2 = map(val2, 0, 1023, 0, 179); 
//sol_goz_y.write(val2);  
//
//val3 = analogRead(sol_goz_x_potpin);  
//val3 = map(val3, 0, 1023, 0, 179); 
//sag_goz_y.write(val3);  
//
//val4 = analogRead(sag_kas_potpin);  
//val4 = map(val4, 0, 1023, 0, 179); 
//sag_kas.write(val4);  
//
//val5 = analogRead(sol_kas_potpin);  
//val5 = map(val5, 0, 1023, 0, 179); 
//sol_kas.write(val5);    
//
//delay(15);
//}
