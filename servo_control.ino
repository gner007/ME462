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
int val0,val1,val2,val3,val4,val5;
void setup()
{
sol_goz_y.attach(4);
sol_goz_x.attach(5);
sag_goz_y.attach(2);
sag_goz_x.attach(3);
sol_kas.attach(6);
sag_kas.attach(7);
}
void loop()
{
val0 = analogRead(sag_goz_y_potpin);  
val0 = map(val0, 0, 1023, 0, 179); 
sag_goz_y.write(val0);  

val1 = analogRead(sag_goz_x_potpin);  
val1 = map(val1, 0, 1023, 0, 179); 
sag_goz_x.write(val1);  

val2 = analogRead(sol_goz_y_potpin);  
val2 = map(val2, 0, 1023, 0, 179); 
sol_goz_y.write(val2);  

val3 = analogRead(sol_goz_x_potpin);  
val3 = map(val3, 0, 1023, 0, 179); 
sag_goz_y.write(val3);  

val4 = analogRead(sag_kas_potpin);  
val4 = map(val4, 0, 1023, 0, 179); 
sag_kas.write(val4);  

val5 = analogRead(sol_kas_potpin);  
val5 = map(val5, 0, 1023, 0, 179); 
sol_kas.write(val5);  

delay(15);      
}
