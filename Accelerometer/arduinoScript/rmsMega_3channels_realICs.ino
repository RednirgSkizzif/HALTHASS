/*2016.10.05
 *by Hyoyeon Lee
 *
 *Read rmsIC signal[V], convert to [g] and print grms.
 *
 *Accelerometer( ADXL001-500z  )
 *          Sensitivity = 1[g]/0.0022[V]
 *          Range = +-500[g] (== +-1.1[V])
 *grms IC ( AD8436B )
 *[1]reading[digits] = AanlogRead-offset 
 *[2]G [g] = reading[digits]*d2v*v2g
 *[3]grms = sqrt(G0^2+G1^2+G2^2)                                         
 *[4]PRINT grms(or G0~2 all together) to SerialPort 
 *[*]Without any delay, it writes grms every 30[ms]. 
 *   The time can be adjustable by setting delay(t[ms])                    
 *               
 *d2v = 1.1[v]/(max-offset)[digits]
 *v2g = 1.0[g]/0.0022[V]
 
 */ 

//revised for real ICs

float     d2v    = 5.0 / 1024.0;
float     v2g    = 1.0 / 0.0022;


char    a;


void setup() {
//Serial Start, BaudRate Setting
        Serial.begin(9600);




//Set up PinModes
   for (int i=0;i<54;i++){
             pinMode(i,OUTPUT);
             if (i>2 && i<16){
                  a='A'+i;
                  pinMode(a,OUTPUT);
             }
    }
} 

void loop() {
//  dt=millis();

//[1]reading[digits] = AanlogRead-offset 
  int reading0 = analogRead(A0);
  int reading1 = analogRead(A1);
  int reading2 = analogRead(A2);

//[2]G [g] = d2v   *v2g*reading[digits]
  float G0 = d2v*v2g*reading0;
  float G1 = d2v*v2g*reading1;
  float G2 = d2v*v2g*reading2;

//[3]grms = sqrt(G0^2+G1^2+G2^2)
  float grms = sqrt(G0*G0+G1*G1+G2*G2);


  Serial.println(grms);
  
}
