/*2016.09.06 
 *by Hyoyeon Lee
 *
 *This is for mimicing rmsIC signal with potentiometers.
 *
 *Accelerometer( ADXL001-500z  )
 *          Sensitivity = 1[g]/0.0022[V]
 *          Range = +-500[g] (== +-1.1[V])
 *grms IC ( AD8436B )
 *          Range of each axis  = 0~1.1[V]             (0~500[g])
 *          Range of vector sum = 0~sqrt(3)*1.1[g]     (0~866[g])
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


int    offset[3] = {   9,   9,   2};
int   maximum[3] = { 898,1023,1018};
float     d2v[3];
float     v2g    = 1.0 / 0.0022;


char    a;


void setup() {
//Serial Start, BaudRate Setting
        Serial.begin(9600);

//Calculate d2v
for (int i=0;i<3;i++){
        d2v[i]=1.1/(maximum[i]-offset[i]);
}


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
  int reading0 = analogRead(A0)-offset[0];
  int reading1 = analogRead(A1)-offset[1];
  int reading2 = analogRead(A2)-offset[2];

//[2]G [g] = d2v   *v2g*reading[digits]
  float G0 = d2v[0]*v2g*reading0;
  float G1 = d2v[1]*v2g*reading1;
  float G2 = d2v[2]*v2g*reading2;

//[3]grms = sqrt(G0^2+G1^2+G2^2)
  float grms = sqrt(G0*G0+G1*G1+G2*G2);

//[4]PRINT to SeiralPort  
  //Serial.print(G0);Serial.print(",");
  //Serial.print(G1);Serial.print(",");
  //Serial.print(G2);Serial.print(",");
  Serial.println(grms);
  
//[*]
  //delay(200);
  //Serial.println(millis()-dt);
}
