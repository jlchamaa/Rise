const byte numChars = 32;
char receivedChars[numChars]; // an array to store the received data
byte red; byte green; byte blue; // bytes are 8-bit values, 0-255 unsigned
bool software=false;
boolean newData = false;

void apply(byte r, byte g, byte b){
    analogWrite(9, r);
    analogWrite(11,b);
    analogWrite(3,g);
}


void setup(){

	Serial.begin(38400); //start Serial comm
	pinMode(A0, INPUT); // potentiometer input pins
	pinMode(A1, INPUT);
	pinMode(A4, INPUT);
	pinMode(9, OUTPUT); // PWM output pins
	pinMode(11, OUTPUT);
	pinMode(3, OUTPUT);
	red=0; green=0; blue=0; // visual test of succesful program launch
}

void recieveCommand() {
	static byte ndx = 0;
	char endMarker = '\0'; //carriage return marks end of serial line
	char rc;
	while (Serial.available() > 0 && newData == false) {
		rc = Serial.read(); // reads in one byte from serial buffer
		if (rc != endMarker) { //continue to read in serial data
			receivedChars[ndx] = rc;
			ndx++;
			if (ndx >= numChars) {
				ndx = numChars - 1;
			}
		}
		else {
			receivedChars[ndx] = '\0'; // demarcate the end of OUR string.
			ndx = 0;
			newData = true;
			byte r0=receivedChars[0]-1;
			byte r1=receivedChars[1]-1;
			byte r2=receivedChars[2]-1;
			byte r3=receivedChars[3]-1;
			if(r3!=0){ // check final byte about whether to accept or ignore incoming data
				red=r0; // if byte!=0, set values to recieved data
				green=r1;
				blue=r2;
				software=true;
			}
			else{
				software=false; 
			}
		}
	}
	newData=false;
}

void loop(){
		if(!software){
			
			int noOfChanges=0;
			byte redcur=byte(analogRead(A4)/4); //assign current Red to 'cur'
			if(abs(red-redcur)>1){ // if red changed
				red=redcur;  // assign red
				noOfChanges++; // prep for serial change
			}
			byte greencur=byte(analogRead(A1)/4);  //assign current Green to 'cur'
			if(abs(green-greencur)>1){
				green=greencur;
				noOfChanges++;
			}
			byte bluecur=byte(analogRead(A0)/4);  //assign current Blue to 'cur'
			if(abs(blue-bluecur)>1){ // if blue changed
				blue=bluecur;  // assign blue
				noOfChanges++;
			}
			if(noOfChanges>0){
				// TODO make sure that we don't ship any zeros except for zero byte
				Serial.write(min(red+1,255));
				Serial.write(min(green+1,255));
				Serial.write(min(blue+1,255));
				Serial.write('\0');
			}		
		}
		recieveCommand(); // recieve values and set numbers
		apply(red,green,blue); // apply the set numbers
}