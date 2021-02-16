/* Pi Printer
 * Make a Royal Professional 2100PD 
 * Electronic Adding Machine print out 
 * 1,000,000 digits of Pi in 12-character lines.
 *
 * 3/10/2020
 * Created by als0052
 *
 * 1,000,000 characters
 * 999,993 digits of pi
 * Last 6 characters are 0 because Python's numpy must work with
 * rectangular matricies. The printer can only print 12 characters 
 * per line.
 * 
 * 83,335 lines of digits.
 * After every 10th line add a blank line to help keep track
 * thus ==> 91,668 lines
 * 
 * lines print on 5mm centers, thus 458.34 meters of paper needed...
 * 
 * 
 * // See the following help pages //
 * https://www.arduino.cc/en/Tutorial/ReadWrite
 * https://forum.arduino.cc/index.php?topic=368621.0
 * https://forum.arduino.cc/index.php?topic=42585.0
 * 
 * Get the SDFat library and see if it can read line by line
 * https://www.arduinolibraries.info/libraries/sd-fat
 * 
 */ 
 
// header libraries
#include <SPI.h>
#include <SD.h>

File inFile;
File outFile;

 
// define the io pins
const int key_0 = 0;	// key 0 
const int key_1 = 1;	// key 1 
const int key_2 = 2;	// key 2 
const int key_3 = 3;	// key 3 
const int key_4 = 4;	// key 4 
const int key_5 = 5;	// key 5 
const int key_6 = 6;	// key 6 
const int key_7 = 7;	// key 7 
const int key_8 = 8;	// key 8 
const int key_9 = 9;	// key 9 
const int print_date = 12;	// key printdate
const int feed = 13;	// line feed key
const int sd_card_pin = 10;	// sd card read/write


void setup() {
// IO pin modes
	pinMode(LED_BUILTIN, OUTPUT);
	pinMode(key_0, OUTPUT);
	pinMode(key_1, OUTPUT);
	pinMode(key_2, OUTPUT);
	pinMode(key_3, OUTPUT);
	pinMode(key_4, OUTPUT);
	pinMode(key_5, OUTPUT);
	pinMode(key_6, OUTPUT);
	pinMode(key_7, OUTPUT);
	pinMode(key_8, OUTPUT);
	pinMode(key_9, OUTPUT);
	pinMode(print_date, OUTPUT);
	pinMode(feed, OUTPUT);
	pinMode(sd_card_pin, OUTPUT);
	
// open serial port
	Serial.begin(11500);	// use high baud rate
	Serial.println("Initializing SD Card...");
	if (!SD.begin(sd_card_pin)){
		Serial.println("Initialization failed!");
		return;
	}
	Serial.println("Initialization completed...");

// Set up the memory buffer
	char* pBuffer;	// declare a pointer to the buffer
	inFile = SD.open(F("pi_printer_12 x 999993_white_spaced.txt"));	// open the pi file for reading

	if (inFile){	// check that the file opened properly
		Serial.println("File opened sucessfully...");
		Serial.println("");	// print blank white space line
		Serial.println("");	// print blank white space line
		
		/* ---------- */
		
		unsigned int fileSize = inFile.size();	// get the file size
		pBuffer = (char*)malloc(fileSize+1);	// allocate memory for the file and a terminating nullchar.
		inFile.read(pBuffer, fileSize);	// read the file into the buffer
		pBuffer[fileSize] = '\0';	// add the terminating null char
		Serial.println(pBuffer);	// print the file to the serial monitor
				
		// read from file until there is nothing left to read
		//while (inFile.available()){
		//	Serial.writed(inFile.read());
		//}

		inFile.close();	// close the file
	} else {
		Serial.println("Error opening the file...");
	}
	
	// *** Use the buffer as needed here. *** //
	free(pBuffer);	// free the memory that was used by the buffer.
	
}

void loop() {
	// blyat
}
