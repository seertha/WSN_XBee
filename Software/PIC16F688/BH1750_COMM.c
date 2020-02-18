/*
 * Funciones para la comunicación con el sensor BH1750
 */

//#define BH1750_COMM
//#define I2C_COMM
#include <xc.h>
#include "sensorNode_v2_1.h"

void bh1750_inicio(unsigned char modo){
    i2c_start();
    i2c_wr(ADDR_WR);
    i2c_wr(modo);
    i2c_stop();
    __delay_ms(150);
}

unsigned int lecturaRaw(void){
    unsigned int datosRaw=0;
    i2c_start();
    i2c_wr(ADDR_RD);
    datosRaw=i2c_rd(ACK);
    datosRaw=datosRaw<<8;
    datosRaw|=i2c_rd(NACK);
    i2c_stop();
    return datosRaw;
    
    
}

unsigned int lecturaLux(unsigned char modo){
    unsigned int lux=0;
    
    switch(modo){
        case ONE_H_MODE:
            bh1750_inicio(ONE_H_MODE);
            lux=lecturaRaw();
            lux/=1.2;
            return lux;
        case C_H_MODE:
            lux=lecturaRaw();
            lux/=1.2;
            return lux;        
            
    }
}
