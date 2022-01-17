EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:soilMoisture-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L CONN_01X03 P1
U 1 1 56D19DCB
P 3450 1250
F 0 "P1" H 3450 1450 50  0000 C CNN
F 1 "CONN_01X03" V 3550 1250 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x03" H 3450 1250 60  0001 C CNN
F 3 "" H 3450 1250 60  0000 C CNN
	1    3450 1250
	0    -1   -1   0   
$EndComp
$Comp
L R R1
U 1 1 56D19E2E
P 4300 2400
F 0 "R1" V 4380 2400 50  0000 C CNN
F 1 "470k" V 4300 2400 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM7mm" V 4230 2400 30  0001 C CNN
F 3 "" H 4300 2400 30  0000 C CNN
	1    4300 2400
	-1   0    0    1   
$EndComp
$Comp
L R R2
U 1 1 56D19E5B
P 4500 2650
F 0 "R2" V 4580 2650 50  0000 C CNN
F 1 "470k" V 4500 2650 50  0000 C CNN
F 2 "Resistors_ThroughHole:Resistor_Horizontal_RM7mm" V 4430 2650 30  0001 C CNN
F 3 "" H 4500 2650 30  0000 C CNN
	1    4500 2650
	0    1    1    0   
$EndComp
$Comp
L C C1
U 1 1 56D19E78
P 2200 2850
F 0 "C1" H 2225 2950 50  0000 L CNN
F 1 "10nF" H 2225 2750 50  0000 L CNN
F 2 "Capacitors_ThroughHole:C_Disc_D3_P2.5" H 2238 2700 30  0001 C CNN
F 3 "" H 2200 2850 60  0000 C CNN
	1    2200 2850
	1    0    0    -1  
$EndComp
Wire Wire Line
	2750 2450 2550 2450
Wire Wire Line
	2550 2450 2550 3350
Wire Wire Line
	2550 3350 4300 3350
Wire Wire Line
	4650 2650 4650 2850
Wire Wire Line
	4650 2850 4150 2850
Wire Wire Line
	4300 3350 4300 2850
Connection ~ 4300 2850
Wire Wire Line
	4350 2650 4150 2650
Wire Wire Line
	3550 2050 2650 2050
Wire Wire Line
	3450 2050 3450 2250
Wire Wire Line
	2400 1450 2400 3600
Wire Wire Line
	2400 3600 4200 3600
Wire Wire Line
	3450 3600 3450 3050
Wire Wire Line
	4150 1950 4150 2450
Wire Wire Line
	4300 1650 4300 2250
Connection ~ 3550 1650
Wire Wire Line
	4300 2550 4300 2650
Connection ~ 4300 2650
Wire Wire Line
	2750 2700 2200 2700
Wire Wire Line
	2200 3000 2400 3000
Connection ~ 2400 3000
Wire Wire Line
	2750 2950 2650 2950
Wire Wire Line
	2650 2950 2650 2050
Connection ~ 3450 2050
Wire Wire Line
	4550 2850 4550 3600
Wire Wire Line
	4550 3600 4350 3600
Connection ~ 4550 2850
Connection ~ 3450 3600
$Comp
L PWR_FLAG #FLG01
U 1 1 56D1A3F5
P 3850 1550
F 0 "#FLG01" H 3850 1645 50  0001 C CNN
F 1 "PWR_FLAG" H 3850 1730 50  0000 C CNN
F 2 "" H 3850 1550 60  0000 C CNN
F 3 "" H 3850 1550 60  0000 C CNN
	1    3850 1550
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG02
U 1 1 56D1A47C
P 3250 3750
F 0 "#FLG02" H 3250 3845 50  0001 C CNN
F 1 "PWR_FLAG" H 3250 3930 50  0000 C CNN
F 2 "" H 3250 3750 60  0000 C CNN
F 3 "" H 3250 3750 60  0000 C CNN
	1    3250 3750
	-1   0    0    1   
$EndComp
Wire Wire Line
	3250 3750 3250 3600
Connection ~ 3250 3600
Wire Wire Line
	3850 1550 3850 1650
Connection ~ 3850 1650
$Comp
L LM555 U1
U 1 1 56D1A9EA
P 3450 2650
F 0 "U1" H 3450 2750 70  0000 C CNN
F 1 "LM555" H 3450 2550 70  0000 C CNN
F 2 "Housings_DIP:DIP-8_W7.62mm" H 3450 2650 60  0001 C CNN
F 3 "" H 3450 2650 60  0000 C CNN
	1    3450 2650
	1    0    0    -1  
$EndComp
Wire Wire Line
	3550 1450 3550 2050
Wire Wire Line
	2400 1450 3350 1450
Wire Wire Line
	4150 1950 3450 1950
Wire Wire Line
	3450 1950 3450 1450
Wire Wire Line
	3550 1650 4300 1650
Text Label 4350 3600 0    60   ~ 0
Sense_pwr
Text Label 4200 3600 2    60   ~ 0
Sense_GND
$EndSCHEMATC
