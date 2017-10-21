/* How to use the DHT-22 sensor with Arduino uno
   Temperature and humidity sensor
   More info: http://www.ardumotive.com/how-to-use-dht-22-sensor-en.html
   Dev: Michalis Vasilakis // Date: 1/7/2015 // www.ardumotive.com */

//Libraries
#include <DHT.h>;

//Constants
#define DHTPIN 2     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino
const unsigned int TRIG_PIN=3;
const unsigned int ECHO_PIN=4;
const unsigned int BAUD_RATE=9600;
int distance=0;
int duration=0;
//Variables
int chk;
float hum;  //Stores humidity value
float temp; //Stores temperature value

void setup()
{
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    Serial.begin(BAUD_RATE);
    dht.begin();

}

void loop()
{
    
    //Read humidity and store it to variables hum 
    hum = dht.readHumidity();
    
    //Read temperature and store it to variables temp
    temp= dht.readTemperature();
    
    //print humidity and temperature
    print_hum_and_temp(hum,temp);
    
    //Calculate duration
    duration = calculate_duration();
    
    //Calculate distance
    distance= duration/29/2;
    
    //print distance 
    print_distance (distance, duration);
     
}




void print_hum_and_temp(int hum0,int temp0)
  {
      //Print temp and humidity values to serial monitor
      Serial.print("Humidity: ");
      Serial.print(hum0);
      Serial.print(" %, Temp: ");
      Serial.print(temp0);
      Serial.println(" Celsius");
      delay(2000); //Delay 2 sec.
  }



void print_distance(int duration0, int distance0)
{
     if(duration0==0){
        Serial.println("Warning: no pulse from sensor");
     } 
     else{
        Serial.print("distance to nearest object:");
        Serial.print(distance0);
        Serial.println(" cm");
    }
    delay(100);
}  


int calculate_duration(){
  // sensor de posicion 
    
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);  

    const unsigned long duration0= pulseIn(ECHO_PIN, HIGH);
    //int distance= duration0/29/2;

    return duration0;
    }

 
