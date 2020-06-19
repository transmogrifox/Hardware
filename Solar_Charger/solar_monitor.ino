static const float Res = 15.0;
static float val;
static const int k = 1000;
static int count;
static float pMax;
static float vMax;
static float iMax;

int cell_sense;
int r_sense;
float Vdc;
float Ima;
float PmW;
float cell_volt;
float r_sense_current;

void setup() {
  analogReadResolution(16);
  Serial1.begin(115200);
  analogWriteResolution(12);
  val = 930;
  count = 0;

  pMax = 0.0;
  vMax = 0.0;
  iMax = 0.0;
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
  PmW = Vdc*Ima;

  if(PmW > pMax)
  {
    pMax = PmW;
    vMax = Vdc;
    iMax = Ima;
  }
  
  Serial1.print(count);
  Serial1.print("\t");
  Serial1.print(Vdc);
  Serial1.print("\t");
  Serial1.print(Ima);
  Serial1.print("\t");
  Serial1.print(PmW);
  Serial1.print("\n");
  delay(1);
  
  count = count+1;
 
 
  val = val + 1;
  if (val >= 4095) 
  {  
   val = 930;
   Serial1.print("Summary: \n");
   Serial1.print("vMax (V)\tiMax (mA)\tpMax (mW)\n");
   Serial1.print(vMax);
   Serial1.print("\t");
   Serial1.print(iMax);
   Serial1.print("\t");
   Serial1.print(pMax);
   Serial1.print("\n");
   
   Serial1.print("\nCycle Start\n\n");
   Serial1.print("");
   count = 0;
   pMax = 0.0;
   vMax = 0.0;
   iMax = 0.0;
  }
  analogWrite(A12, (int)val);
  delay(20);
  
    
}
