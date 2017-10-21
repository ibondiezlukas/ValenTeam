/* How to use the DHT-22 sensor with Arduino uno
   Temperature and humidity sensor
   More info: http://www.ardumotive.com/how-to-use-dht-22-sensor-en.html
   Dev: Michalis Vasilakis // Date: 1/7/2015 // www.ardumotive.com */

//Libraries
#include <DHT.h>

//Constants
#define DHTPIN 2     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino


String typoPapelera = "paper";
String posit = "40.446;79.982";
String id = "01";


const unsigned int TRIG_PIN=3;
const unsigned int ECHO_PIN=4;
const unsigned int BAUD_RATE=9600;
int distance=0;
int duration=0;
//Variables
int chk;
float hum;  //Stores humidity value
float temp; //Stores temperature value
const int buttonPin = 5;     // the number of the pushbutton pin
const int firePin = 6;     
long buttonTimer = 0;
long longPressTime = 500;

boolean buttonActive = false;
boolean longPressActive = false;
boolean fire = false;

// Variables will change:
int buttonPushCounter = 0;   // counter for the number of button presses
int buttonState = 0;         // current state of the button
int lastButtonState = 0;     // previous state of the button


String inputString = "";         // a String to hold incoming data
boolean stringComplete = false;  // whether the string is complete
void setup()
{
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    Serial.begin(BAUD_RATE);
    dht.begin();
    // initialize the pushbutton pin as an input:
    pinMode(buttonPin, INPUT);
    pinMode(firePin, INPUT);
      // reserve 200 bytes for the inputString:
  inputString.reserve(200);

}

void loop()
{
  bool lleno;
if (digitalRead(buttonPin) == LOW) {

    if (buttonActive == false) {

      buttonActive = true;
      buttonTimer = millis();

    }

    if ((millis() - buttonTimer > longPressTime) && (longPressActive == false)) {

      longPressActive = true;

      print_id();
      print_pos_type();

      
    }

  } else {

    if (buttonActive == true) {

      if (longPressActive == true) {

        longPressActive = false;

      } else {
          //Read humidity and store it to variables hum 
          hum = dht.readHumidity();
          
          //Read temperature and store it to variables temp
          temp= dht.readTemperature();
          
          //Calculate duration
          distance = calculate_duration();
          if(distance < 10) lleno = HIGH;
          else lleno = LOW;

          fire = digitalRead(firePin);

          print_id();
        //print humidity and temperature
          print_hum_and_temp(hum,temp);
          
          //print distance 
          print_distance (lleno);

          print_fire(fire);
}

      buttonActive = false;

    }

  }
  if (stringComplete) {
    
  }
}




void print_hum_and_temp(int hum0,int temp0)
  {
      //Print temp and humidity values to serial monitor
      Serial.print("$hum:");
      Serial.print(hum0);
      Serial.print("$temp:");
      Serial.print(temp0);

  }



void print_distance(int container)
{
        Serial.print("$lleno:");
        Serial.print(container);
}  
void print_fire(bool fire)
{
        Serial.print("$fire:");
        Serial.print(fire);
} 
int calculate_duration(){
  // sensor de posicion 
    
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);  

    const unsigned long duration0= pulseIn(ECHO_PIN, HIGH);
    int distance= duration0/29/2;

    return distance;
    }
void print_pos_type(){
        Serial.print("$type:");
        Serial.print(typoPapelera);
        Serial.print("$pos:");
        Serial.print(posit);
 }
 void print_id(){
        Serial.print("$id:");
        Serial.print(id);
 }


