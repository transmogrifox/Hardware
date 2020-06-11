static const float Res = 15.0;
static float val;
static const int k = 1000;
static int count;
int cell_sense;
int r_sense;
float Vdc;
float Ima;
float cell_volt;
float r_sense_current;

void setup() {
  analogReadResolution(16);
  Serial.begin(9600);
  analogWriteResolution(12);
  val = 930;
  count = 0;
}


void loop() {
  cell_volt = 0.0;
  r_sense_current=0.0;
  
  for(int i = 0; i<k;i++)
  {
   cell_sense = analogRead(A1);
   r_sense = analogRead(A0);
   cell_volt = cell_volt + cell_sense;  
   r_sense_current = r_sense_current + r_sense;
  }
  
  Vdc = (cell_volt * (3.3 * 2/ 65535)/k);
  Ima = ((r_sense_current * (3.3 / 65535)/(Res / 1000))/k) + Vdc / 48800;
  
  
  Serial.print(count);
  Serial.print("\t");
  Serial.print(Vdc);
  Serial.print("\t");
  Serial.print(Ima);
  Serial.print("\n");
  
  count = count+1;
 
 
  val = val + 1;
  if (val >= 4095) 
  {  
   val = 930;
   Serial.print("\n Cycle Start\n\n");
   count = 0;
  }
  analogWrite(A12, (int)val);
  delay(20);
  
    
}