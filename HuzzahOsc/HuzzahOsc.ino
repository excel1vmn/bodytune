#if defined(ESP8266)
#include <ESP8266WiFi.h>
#else
#include <WiFi.h>
#endif
#include <WiFiUdp.h>
#include <OSCMessage.h>
#define USE_ARDUINO_INTERRUPTS false
#include <PulseSensorPlayground.h>

char ssid[] = "lel";          // your network SSID (name) //huzzah
char pass[] = "majorlel";                    // your network password //hazzuhosc

WiFiUDP Udp;                                // A UDP instance to let us send and receive packets over UDP
const IPAddress outIp(192,168,43,162);        // remote IP of your computer  Hotspot 192,168,43,162
const unsigned int outPort = 9001;          // remote port to receive OSC
const unsigned int localPort = 8888;        // local port to listen for OSC packets (actually not used for sending)
const int OUTPUT_TYPE = SERIAL_PLOTTER;

const int PIN_INPUT = A0;
const int THRESHOLD = 550;   // Adjust this number to avoid noise when idle

byte samplesUntilReport;
const byte SAMPLES_PER_SERIAL_SAMPLE = 10;

PulseSensorPlayground pulseSensor;

void setup() {
    Serial.begin(115200);

    // Connect to WiFi network
    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);
    WiFi.begin(ssid, pass);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");

    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());

    Serial.println("Starting UDP");
    Udp.begin(localPort);
    Serial.print("Local port: ");
#ifdef ESP32
    Serial.println(localPort);
#else
    Serial.println(Udp.localPort());
#endif
    // Configure the PulseSensor manager.
  pulseSensor.analogInput(PIN_INPUT);

  pulseSensor.setSerial(Serial);
  pulseSensor.setOutputType(OUTPUT_TYPE);
  pulseSensor.setThreshold(THRESHOLD);

  // Skip the first SAMPLES_PER_SERIAL_SAMPLE in the loop().
  samplesUntilReport = SAMPLES_PER_SERIAL_SAMPLE;

  // Now that everything is ready, start reading the PulseSensor signal.
}

void loop() {
    if (pulseSensor.sawNewSample()) {
    /*
       Every so often, send the latest Sample.
       We don't print every sample, because our baud rate
       won't support that much I/O.
    */
    if (--samplesUntilReport == (byte) 0) {
      samplesUntilReport = SAMPLES_PER_SERIAL_SAMPLE;

      pulseSensor.outputSample();
      OSCMessage msg("/BPM");
          msg.add(pulseSensor.getLatestSample());
          msg.add(pulseSensor.getBeatsPerMinute()); 
          Udp.beginPacket(outIp, outPort);
          msg.send(Udp);
          Udp.endPacket();
          msg.empty();
      /*
      OSCMessage msg2("/BPM");
          msg2.add(pulseSensor.getBeatsPerMinute()); 
          Udp.beginPacket(outIp, outPort);
          msg2.send(Udp);
          Udp.endPacket();
          msg2.empty();
      */
      /*
         At about the beginning of every heartbeat,
         report the heart rate and inter-beat-interval.
      */
      if (pulseSensor.sawStartOfBeat()) {
        pulseSensor.outputBeat();
      }
    }

    /*******
      Here is a good place to add code that could take up
      to a millisecond or so to run.
    *******/
  }
}
