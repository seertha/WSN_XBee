/*
 * Funciones para la comunicación I2C
 */
//#ifndef I2C_COMM
//#define I2C_COMM
//#endif

#include <xc.h>
#include "sensorNode_v2_1.h"


void i2c_start(void){
    SDA_TRIS=1;                 //SDA y SCL en alto
    SCL=1;
    SDA_TRIS=0;                 //SDA como salida
    SDA=0;                      //línea SDA en bajo
    NOP();
    SCL=0;                      //línea SCL en bajo
}

void i2c_stop(void){
    SCL=0;                      //SCL en bajo
    SDA_TRIS=0;                 //SDA como salida
    SDA=0;                      //SDA en bajo
    NOP();
    SCL=1;                      //SCL alto
    SDA_TRIS=1;                 //línea SDA en alto
    SCL=0;                      //SCL en bajo
}

void bit_out(unsigned char data){
    SCL=0;                      //SCL en bajo
    SDA_TRIS=0;                 //SDA como salida
    SDA=(data>>7);              //salida MSB
    NOP();
    SCL=1;                      //SCL en alto
    NOP();
    SCL=0;                      //SCL en bajo
}

void bit_in(unsigned char *data)
{
    SCL=0;                      //SCL en bajo
    SDA_TRIS=1;                 //SDA como entrada
    SCL=1;                      //SCL en alto para iniciar transferencia
    NOP();
    *data |=SDA;                //recepción de datos
    SCL=0;                      //SCL en bajo
}

unsigned char i2c_wr(unsigned char data){
    unsigned char i;            //contador loop
    unsigned char ack;          //ACK bit
    
    ack=0;
    for (i=0;i<8;i++){          //loop por cada bit
        bit_out(data);
        data=data<<1;           //recorrer 1 bit izquierda
    }           
    bit_in(&ack);
    return ack;
}

unsigned char i2c_rd(unsigned char ack){
    unsigned char i;
    unsigned char ret=0;        //datos recibidos
    
    for(i=0;i<8;i++){
        ret=ret<<1;             //recorrer 1 bit izquierda
        bit_in(&ret);
    }
    bit_out(ack);               //responder ACK/NAK bit
    return ret;
}
