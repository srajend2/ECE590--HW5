#define DXL_BUS_SERIAL1 1  //Dynamixel on Serial1(USART1)  <-OpenCM9.04
#define DXL_BUS_SERIAL2 2  //Dynamixel on Serial2(USART2)  <-LN101,BT210
#define DXL_BUS_SERIAL3 3  //Dynamixel on Serial3(USART3)  <-OpenCM 485EXP
#define ID1 2
#define ID2 1


Dynamixel Dxl(DXL_BUS_SERIAL1);
void setup()
{
SerialUSB.begin();
Dxl.begin(3);
Dxl.wheelMode(ID1);
Dxl.wheelMode(ID2);
SerialUSB.attachInterrupt(MOTOR_VALUES);
pinMode(BOARD_LED_PIN, OUTPUT);
}


void loop() 
{
 Dxl.goalSpeed(ID2, 100);
  Dxl.goalSpeed(ID1, 100);
 delay(100);
}
 
void MOTOR_VALUES( byte* buffer, byte n)
{
int Mod_val_M1 = ((buffer[0]-48)*1000)+((buffer[1]-48)*100)+((buffer[2]-48)*10)+(buffer[3]-48);
int Mod_val_M2 = ((buffer[5]-48)*1000)+((buffer[6]-48)*100)+((buffer[7]-48)*10)+(buffer[8]-48);
  
Dxl.goalSpeed(ID1, Mod_val_M1);
Dxl.goalSpeed(ID2, Mod_val_M2);
delay(100);
}

