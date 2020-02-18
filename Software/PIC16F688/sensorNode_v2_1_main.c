/******************************************************************************
 * Nodo sensor                                                  version: 2.1
 * Lectura de datos de temperatura, humedad relativa e intensidad luminosa.
 * Sensores: DHT22, BH1750.
 * Micocontrolador: PIC16F688.
 * Salida por puerto serial.
 * Comunicación por I2C simulada por software
 * Wake-up por interrupción externa en RA2
 * Control XBee: RC3
 * Detalles:
 *  -FOsc:              4MHz (interno)
 *  -Baudrate:          9600 bps.
 *  -SDA:               RA4
 *  -SCL:               RA5
 *  -DHT22:             RC1
 *  -debugLed:          RC2
 * 
 ******************************************************************************/
#include <xc.h>
#include <stdio.h>
#include "sensorNode_v2_1.h"

// CONFIG
#pragma config FOSC = INTOSCIO  // Oscillator Selection bits (INTOSCIO oscillator: I/O function on RA4/OSC2/CLKOUT pin, I/O function on RA5/OSC1/CLKIN)
#pragma config WDTE = OFF       // Watchdog Timer Enable bit (WDT disabled)
#pragma config PWRTE = ON       // Power-up Timer Enable bit (PWRT enabled)
#pragma config MCLRE = ON       // MCLR Pin Function Select bit (MCLR pin function is MCLR)
#pragma config CP = OFF         // Code Protection bit (Program memory code protection is disabled)
#pragma config CPD = OFF        // Data Code Protection bit (Data memory code protection is disabled)
#pragma config BOREN = OFF      // Brown Out Detect (BOR disabled)
#pragma config IESO = OFF       // Internal External Switchover bit (Internal External Switchover mode is disabled)
#pragma config FCMEN = OFF      // Fail-Safe Clock Monitor Enabled bit (Fail-Safe Clock Monitor is disabled)

#define debugLed        PORTCbits.RC2
#define xbeePin         PORTCbits.RC3

void configuraciones(void);

void main(void){
    configuraciones();
    USARTinicio();
    
    //variables locales
    
    unsigned int humR=0;
    unsigned int lux=0;
    int temp=0;
    unsigned char DHT22_status=0;
    unsigned char error_control=0;
    
    debugLed=1;
    __delay_ms(500);
    debugLed=0;
    //printf("*****LECTURAS SENSOR2 - DHT22 - BH1750*****\n\r");    
    bh1750_inicio(ONE_H_MODE);
    
    while(1){
        INTCON=0b01010000;              //Int. Externa, GIE off,PIE on,timer0 int off
        xbeePin=1;                      //XBee sleep
        SLEEP();
        if(INTCONbits.INTF==1){
            INTCON=0;                   //PIE off,INTF 0
            debugLed=1;
            __delay_ms(200);
            debugLed=0;
        }
//        bh1750_inicio(ONE_H_MODE);
        __delay_ms(2500);
        lux=lecturaLux(ONE_H_MODE);
        DHT22_status=DHT22_read();
        //INTCON=0;                   //interrupciones deshabilitadas, TOIF 0
        
        switch(DHT22_status){
            case OK:
                humR=datos_hum();
                temp=datos_temp();
                error_control=0;
                break;
            case TIMEOUT:
                //humR=0;
                //temp=0;
                error_control=TIMEOUT;
                break;
            case CHECKSUM:
                error_control=CHECKSUM;
        }
        xbeePin=0;                          //XBee on
        if(error_control==0){
            //printf("TEMPERATURA: %d\tHUMEDAD RELATIVA: %u\tLUX: %u\n\r",
            //        temp,humR,lux);
            printf("%u>%d>%u",humR,temp,lux);
        }
        else{
            printf("%d",error_control);
        }
    }   
}

void configuraciones(void){
    CMCON0=0b00000111;          //comparadores en off
    ANSEL=0;                    //todos los puertos en digital
    TRISA=0b00010100;           //RA4 en alto a través de pull-up, RA2 input
    TRISC=0;
    OSCCON=0b01100001;          //INTOsc 4MHz
    OPTION_REG=0b10000000;       //TMR0 preescaler 1:2,reloj interno,interrupción RA2 1-0,no pull-up
    PORTC=0;
    PORTA=0b00100000;           //RC5 alto
    INTCON=0;                   //interrupciones deshabilitadas, TOIF 0
    TMR0=0;
    
}