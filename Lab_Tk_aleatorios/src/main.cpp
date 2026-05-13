#include <Wire.h>
#include <SPI.h>
#include <Adafruit_BMP280.h>
#define BMP280_ADDRESS 0x76
Adafruit_BMP280 bmp;  // use I2C interface
#include <DHT.h>  
// Set up the DHT sensor 
DHT dht(4, DHT22);
float temp ;
float  hum;
float pres ;
float alt;
int n;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Hola, ESP32!");  
  while (!Serial) delay(100);  // wait for native usb
  Serial.println(F("BMP280 test"));

  unsigned status;
  status = bmp.begin(BMP280_ADDRESS);
  if (!status) {
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring or "
                     "try a different address!"));
    while (1) delay(10);  // Stop code execution if the sensor is not found.
  }

  /* Default settings from datasheet. */
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
}

void loop() {
  // put your main code here, to run repeatedly:

 temp  = dht.readTemperature();
  hum    = dht.readHumidity();
  pres = bmp.readPressure();
  alt = bmp.readAltitude(pres);
  // Comprobamos si ha habido algún error en la lectura inicial o global
  if (isnan(temp) || isnan(hum)) {
    Serial.println("Error obteniendo los datos del sensor DHT22");
    return;
  }

    Serial.print(n);
    Serial.print(",");
    Serial.print(temp, 2); // 2 decimales
    Serial.print(",");
    Serial.print(pres, 2);
    Serial.print(",");
    Serial.print(hum, 2);
    Serial.print(",");
    Serial.println(alt, 2);

  delay(1000); // this speeds up the simulation
  n++;
}

