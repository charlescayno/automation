

#include <Wire.h>
//#include <PWM.h>
//#include <Dali.h>
#include <SPI.h>
#include <SoftwareSerial.h> 

//const int DALI_TX = 3;
//const int DALI_RX_A = 0;
//#define BROADCAST_DP 0b11111110 - org


//int pwm = 9;  
//int32_t frequency = 10000; //frequency (in Hz)
//float duty = 0;
//float vset = 0;

int test_type = 0;
int deviceAddress;
int registerAddress;
int dataLength;
int data1;
float data2;
uint8_t response;
uint8_t response2;
bool ack;
byte c;
//float resistance;


//String inString = "";    // string to hold input - org 
//bool stringComplete = false;  // whether the string is complete

const int SS_PIN = 10;
const int MOSI_PIN = 11;
const int MISO_PIN = 12;
const int CLK_PIN = 13; 

// const byte enableUpdateMSB = 0x18; //B00011000 //for AD5292
// const byte enableUpdateLSB = 0x02; //B00000010
// const byte command = 0x04; //B00000100






// void digitalPotWrite(int csPin, int value) {
// 
//  digitalWrite(csPin, LOW); //select slave
//
//
//    byte shfitedValue = (value >> 8);
//
//  byte byte1 = (command | shfitedValue);
//
//
//  byte byte0 = (value & 0xFF); //0xFF = B11111111 trunicates value to 8 bits
//
//
//  //Write to the RDAC Register to move the wiper
//  SPI.transfer(byte1);
//  SPI.transfer(byte0);
//
//
//  digitalWrite(csPin, HIGH); //de-select slave
//
//
// }

//void initRheostat() {
//
//    digitalWrite(SS_PIN, LOW);
//    SPI.transfer(enableUpdateMSB);
//    SPI.transfer(enableUpdateLSB);
//    digitalWrite(SS_PIN, HIGH);
//}


//Needed By bluetooth 
SoftwareSerial BLE(6, 7); // RX | TX

 
void setup() {

// Initialize SPI
    pinMode(SS_PIN, OUTPUT);
    SPI.begin();
    // SPI_MODE1 (CPOL = 0, CPHA = 1) - From the datasheet
    SPI.setDataMode(SPI_MODE1);
    // MSBFIRST - From the data sheet
    SPI.setBitOrder(MSBFIRST);
    // Call to init and enable RDAC register write access.
    
//initRheostat() ;

 
      Wire.begin();

      BLE.begin(38400);   //from 115k
      BLE.setTimeout(50); 

  //enable setClock to change the SCL bitrate in Hz
  //Wire.setClock(50000); 
  
  // Open serial communications and wait for port to open:
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }


// the ff setup is for PWM frequency setting
  //initialize all timers except for 0, to save time keeping functions
  //InitTimersSafe(); 

  //sets the frequency for the specified pin
  //bool success = SetPinFrequencySafe(pwm, frequency);

// Org start
//  if the pin frequency was set successfully, turn pin 13 on / conflict with other pin 13
//  if(success) {
//    pinMode(13, OUTPUT);
//    digitalWrite(13, HIGH);    
//}
// Org end

////initialize DALI
//  dali.setupTransmit(DALI_TX);
//  dali.setupAnalogReceive(DALI_RX_A);
//  dali.busTest();
//  dali.msgMode = true;

  
}





void loop() {


while (BLE.available() > 0)

{

    //data sequence is (1:test_type, 2:i2c Address/ DALI Command1, 3:Register address/Command2, 4:data length, 5:Data1 , 6:Data 2)

    //1: test_type (0 = none, 1 = i2c write, 2 = i2c read, 3 = DALI, 4 = PWM, 5 = Analog, 6 = Digipot)
    test_type = BLE.parseInt(); 

    //2: device address
    deviceAddress = BLE.parseInt();

    //3: Register address/DALI command2
    registerAddress = BLE.parseInt();

    //4: i2c data length
    dataLength = BLE.parseInt();

    //5:Data1
    data1 = BLE.parseInt();

    //6: data2
    data2 = BLE.parseFloat();


    if (BLE.read() == '\n') {

    testTypeBLE();

}



}


while (Serial.available()> 0) {


    //data sequence is (1:test_type, 2:i2c Address/ DALI Command1, 3:Register address/Command2, 4:data length, 5:Data1 , 6:Data 2)

    //1: test_type (0 = none, 1 = i2c write, 2 = i2c read, 3 = DALI, 4 = PWM, 5 = Analog, 6 = Digipot)
    test_type = Serial.parseInt(); 

    //2: device address
    deviceAddress = Serial.parseInt();

    //3: Register address/DALI command2
    registerAddress = Serial.parseInt();

    //4: i2c data length
    dataLength = Serial.parseInt();

    //5:Data1
    data1 = Serial.parseInt();

    //6: data2
    data2 = Serial.parseFloat();


    if (Serial.read() == '\n') {

    testTypeSerial();

    }
  
  }


}



void testTypeBLE()
{


  switch (test_type) {

      case 0:
          break;
    
      case 1: 
      
          Wire.beginTransmission(deviceAddress);   
          Wire.write(registerAddress); // register address
      
          Wire.write(data1); 
      
          if (dataLength == 2) {
          Wire.write(int(data2));   
          }
                
          Wire.endTransmission(); 
      
          ack =  Wire.endTransmission();
          BLE.flush();
          BLE.println(ack);  
          BLE.flush();
          
//          if (ack ==0) {
//          //BLE.print("Successfully sent: ");
//          BLE.println(ack);                   //BLE.println(data1);
//          }
//          else
//          {
//          BLE.println(ack);    //BLE.println("not acknowledged");
//          }
          break;
    
      case 2:
          Wire.beginTransmission(deviceAddress);   
          Wire.write(registerAddress); // register address
      
          Wire.write(data1); 
      
          if (dataLength == 2) {
          Wire.write(int(data2));   
          }
                
          Wire.endTransmission(); 
      
          //ack =  Wire.endTransmission();
          
          Wire.requestFrom(deviceAddress,dataLength);

          if (Wire.available()) {
          while (Wire.available()) {
            c = Wire.read();
    
            //BLE.print("data is: ");
            BLE.flush();
            BLE.println(int(c));
            BLE.flush();
          }
          //delay(500);
          //Wire.flush();
          }
          else {
          BLE.flush();
          BLE.println(255);
          BLE.flush();
          BLE.println(255);
          //delay(100);
       
          }

          break;

//       case 3:
//           
//           dali.transmit(byte(deviceAddress), byte(registerAddress));
//           delay(20);
//           dali.transmit(byte(deviceAddress), byte(registerAddress));
//            
//          
//           BLE.println("DALI TX successful");
//           
//          
//          response2 = dali.receive();
//          
//          delay(20);
//
//          if (dali.getResponse) {
//            
//            BLE.println(response2);
//            
//          }
//          else {
//            
//            BLE.println("not success");
//          
//          }
//         
//
//           break;
//           
//    
//        case 4: 
//        
//            duty = data2 * 65535 / 100;
//            frequency = data1;
//
//            //set the frequency
//            SetPinFrequencySafe(pwm, frequency);
//            
//            //set the duty
//            pwmWriteHR(pwm, duty);         
//            
//            //BLE.print("Frequency set to: ");
//            BLE.println(data1);
//            //BLE.print("PWM duty set to: ");
//            BLE.println(data2);
//
//            
//            break;
//      
//        case 5: 
//        
//            vset = data2 * 65535 / 10;
//            pwmWriteHR(pwm, vset);
//
//            
//            //set the frequency to 2000 Hz
//            SetPinFrequencySafe(pwm, frequency);
//            
//            //BLE.print("Analog voltage set to: ");
//            BLE.println(data2);  
//            
//            break;    
//
//          case 6:   
//          initRheostat();
//          delay(10);
//          digitalPotWrite(SS_PIN, int(data2));   //should be from 1 to 1023
//
//          resistance = 100000 * data2 / 1023;
//
//          //BLE.print("Resistance set to: ");
//          BLE.println(resistance); 
//          
//          break;


//case 7: 
//
//          if (data1 < dataLength) {
//
//                while (data1 <= dataLength){
//                Wire.beginTransmission(deviceAddress);   
//                Wire.write(registerAddress); // CC register address
//                Wire.write(data1); 
//                Wire.endTransmission(); 
//                data1++;
//                delay(int(data2));
//                }
//            } else
//                while (data1 >= dataLength){
//                Wire.beginTransmission(deviceAddress);   
//                Wire.write(registerAddress); // CC register address
//                Wire.write(data1); 
//                Wire.endTransmission(); 
//                data1--;
//                delay(int(data2));
//                }         
//                break;
          
  }
}


void testTypeSerial()
{


  switch (test_type) {

      case 0:
          break;
    
      case 1: 
      
          Wire.beginTransmission(deviceAddress);   
          Wire.write(registerAddress); // register address
      
          Wire.write(data1); 
      
          if (dataLength == 2) {
          Wire.write(int(data2));   
          }
                
          ack =  Wire.endTransmission(); 
      
          if (ack ==0) {
          //Serial.print("Successfully sent: ");
          Serial.println(ack);                      //Serial.println(data1); 
          }
          else
          {
          Serial.println(ack);                      //Serial.println("not acknowledged");
          }
          
          break;
    
      case 2:

         Wire.requestFrom(deviceAddress,dataLength);

        if (Wire.available()) {
          while (Wire.available()) {
            c = Wire.read();
            //Serial.print("data is: ");
            Serial.println(int(c));
            
          }
          delay(500);
        }
        else {
          Serial.println(65535);
        }
          
      
          break;

//       case 3:
//          
//           dali.transmit(byte(deviceAddress), byte(registerAddress));
//           delay(90);
//           dali.transmit(byte(deviceAddress), byte(registerAddress));
//           
//           
//           Serial.println("DALI TX successful");
//           
//
//          
//          response = dali.receive();
//          
//          delay(20);
//
//          if (dali.getResponse) {
//            Serial.println(response);
//           
//          }
//          else {
//            Serial.println("");
//            
//          }
//
//           break;
//           
//    
//        case 4:
//            duty = data2 * 65535 / 100;
//            frequency = data1;
//
//            //set the frequency
//            SetPinFrequencySafe(pwm, frequency);
//            
//            //set the duty
//            pwmWriteHR(pwm, duty);         
//            
//            
//
//            //Serial.print("Frequency set to: ");
//            Serial.println(data1);  
//            //Serial.print("PWM duty set to: ");
//            Serial.println(data2); 
//            
//            break;
//      
//        case 5: 
//        
//            vset = data2 * 65535 / 10;
//            pwmWriteHR(pwm, vset);
//            
//            //set the frequency to 2000 Hz
//            SetPinFrequencySafe(pwm, frequency);
//            
//            
//            //Serial.print("Analog voltage set to: ");
//            Serial.println(data2); 
//            break;    
//
//          case 6:   
//          initRheostat();
//          delay(10);
//          digitalPotWrite(SS_PIN, int(data2));   //should be from 1 to 1023
//
//          resistance = 100000 * data2 / 1023;
//
//         
//          //Serial.print("Resistance set to: ");
//          Serial.println(resistance); 
//          break;
//
//          case 7: 
//
//          if (data1 < dataLength) {
//
//                while (data1 <= dataLength){
//                Wire.beginTransmission(deviceAddress);   
//                Wire.write(registerAddress); // CC register address
//                Wire.write(data1); 
//                Wire.endTransmission(); 
//                data1++;
//                delay(int(data2));
//                }
//            } else
//                while (data1 >= dataLength){
//                Wire.beginTransmission(deviceAddress);   
//                Wire.write(registerAddress); // CC register address
//                Wire.write(data1); 
//                Wire.endTransmission(); 
//                data1--;
//                delay(int(data2));
//                }         
//                break;

            
          
  }
}
