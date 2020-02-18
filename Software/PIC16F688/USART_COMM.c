/*
 * Funciones para la comunicación USART
 */

//#define USART_COMM
#include <xc.h>
#include <stdio.h>
#include "sensorNode_v2_1.h"

void USARTinicio(void){
    TXSTA=0b00100100;           //HS,Async,TXEN,8bit
    RCSTA=0b10010000;           //Rx en,8bit,puerto serie habilitado
    BAUDCTL=0;                  //Auto baudrate off,Rx normal,BRG 8 bit
    SPBRG=25;                   //9600
}

void putch(unsigned char dato){
    while(PIR1bits.TXIF==0);
    TXREG=dato;
    __delay_ms(1);
}
