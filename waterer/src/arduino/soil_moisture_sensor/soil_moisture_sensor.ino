/*
Capacative Soil Moisture Sensor

This code is to be used with a 555 timer, capacative based soil moisture sensor.
This code heavily uses native avr port definitions and a pinout of the pro mini
is handy to follow some of the logic, mostly it saves on code and allows me to
read data in a for loop pretty fast.

Author: Lukas Jaworski
2016
v0.1.0
*/

//------------------------------------------------------------------------------
//Dependencies
//------------------------------------------------------------------------------

#include <avr/io.h> 
#include <util/delay.h> 
#include <avr/interrupt.h> 
#include <avr/power.h> 
#include <Arduino.h>
#include <Wire.h>

//------------------------------------------------------------------------------
//TYPEDEFS
//------------------------------------------------------------------------------

//------------------------------------------------------------------------------
//defineMACRO and global variables
//------------------------------------------------------------------------------

#define MEASURE_TIME 31250 //the ammount of cycles it takes to get to .5 seconds

volatile uint32_t       freqList[16];
uint32_t                freqOut[16];
volatile uint8_t        portBhistory = 0;
volatile uint8_t        portChistory = 0;
volatile uint8_t        portDhistory = 0;

volatile bool           run_continuously;
uint32_t                time_counter;

//--------------------------------------------------------------------------
// Helper Functions
//-----------------------------------------------------------------------------------

void setupPCinterrupts(void){ 
/*
sets the pins A0-A3 as pin change interrupts to read the frequency generated by the 555 timer
this frequency should be related to soil moisture content, by measuring capacitance.
note: actual frequency will be half of the counts here, no real need to use actual frequency
in code as soil moisture is desired input and will be based on end user calibration due to
soil variation
*/
    for (uint8_t i = 0; i<16; i++){
        freqList[i] = 0;
    }
    // Serial.println("setPCinterrupts");
    DDRB &= ~(0b00111111); //pins 10-13 as inputs
    DDRC &= ~(0b00001111); //pins A0-A3 as inputs
    DDRD &= ~(0b11111100);
    PCMSK0 = 0b00111111; //PCinterrupts enabled on 10-13
    PCMSK1 = 0b00001111; //PCinterrupts enabled on pins A0-A3
    PCMSK2 = 0b11111100; //PCinterrupts enabled on pins A0-A3
    PCICR |= (1<<PCIE0) | (1<<PCIE1) | (1<<PCIE2); //globally enables pin change interrupts
}

void resetPCinterrupts(void){
    for (uint8_t i = 0; i<16; i++){
        freqList[i] = 0;
    }
    PCICR |= (1<<PCIE0) | (1<<PCIE1) | (1<<PCIE2); //globally enables pin change interrupts
}

void disablePCinterrupts(void){
    PCICR &= ~((1<<PCIE0) | (1<<PCIE1) | (1<<PCIE2)); //globally disables PC interrupts
}

void timer1init(void){
    //set timer compare register
    TCCR2B = ((1<<CS22)|(1<<CS21)|(1<<CS20)); // normal mode and Clock at CPU/256 frequency
    TIMSK2 = ( 1 << TOIE2); //enable timer 2 overflow interrupt
}

void timer2stop(void){
  TIMSK2 &= ~( 1 << TOIE2); //disable timer compare interrupt
}

//----------------------------------------------------------------------------------------------------------
//ISRs
//-----------------------------------------------------------------------------

ISR(TIMER2_OVF_vect){//timer used in calculating sensor frequency
    disablePCinterrupts();
    timer2stop();
    freqOut = freqList;
}

//The ISRs for ports B and C are almost identical only shifted to accomdate used pins
//and a global array
ISR(PCINT0_vect){//ISR to read 555 timer output on connected portB pins
    uint8_t changedBitsB;
    changedBitsB = PINB ^ portBhistory;//finds only the pins that have fired during the interrupt
    portBhistory = PINB;
    for (uint8_t i = 0; i<6; i++){
         if (changedBitsB & (1 << i)){
             freqList[i+PORTB_OFFSET] += 1;
         }
     }
 }

    DDRB &= ~(0b00111111); //pins 10-13 as inputs
    DDRC &= ~(0b00001111); //pins A0-A3 as inputs
    DDRD &= ~(0b11111100);
ISR(PCINT1_vect){//ISR to read 555 timer output on connected portC pins
    uint8_t changedBitsC;
    changedBitsC = PINC ^ portChistory; 
    portChistory = PINC;
    for (uint8_t i = 0; i<4; i++){
        if (1 & (changedBitsC >> i)){
            freqList[i+6] += 1;
        }
    }
}

ISR(PCINT2_vect){//ISR to read 555 timer output on connected portC pins
    uint8_t changedBitsD;
    changedBitsD = PIND ^ portDhistory; 
    portDhistory = PIND;
    for (uint8_t i = 0; i<6; i++){
        if (1 & (changedBitsD >> i+2)){ // pins 0 and 1 are used for serial coms
                                        // so we need to skip them
            freqList[i+10] += 1;
        }
    }
}

void stateUpdate(){
    // timer_count = millis();
    // Serial.println(millis());
    setPCinterrupts();
    timer1init();
}

//----------------------------------------------------------------------------
//Main code
//-------------------------------------------------------------------------------------

void setup() {
    Serial.begin(115200);
    Wire.begin(15);

    sei();
}

void loop() {
    stateUpdate();


    delay(10000);
}