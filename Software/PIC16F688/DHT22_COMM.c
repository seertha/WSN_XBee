/*
 * Funciones para la comunicación con el sensor DHT22
 */

//#define DHT22_COMM
#include <xc.h>
#include "sensorNode_v2_1.h"



//Variables globales
unsigned char DHT22_data[5];        //5 bytes of data

unsigned char DHT22_start(void){
    TRISC=0;
    PORTCbits.RC1=0;                    //DHT pin low
    __delay_ms(20);                     //esperar mínimo 1ms.
    PORTCbits.RC1=1;                    
    __delay_us(40);
    TRISCbits.TRISC1=1;                 //DHT input 
    __delay_us(10);
    
    //la línea de datos se mantiene en estado alto hasta que el sensor baja la
    //línea (40us aprox.)
    DHT22_expect(0);                        //a
    if(INTCONbits.T0IF){
        //printf("Error a\n\r");
        return TIMEOUT;
    }
    //80us en bajo
    DHT22_expect(1);                        //b
    if(INTCONbits.T0IF){
        //printf("Error b\n\r");
        return TIMEOUT;
    }
    //80us en alto
    DHT22_expect(0);                        //c
    if(INTCONbits.T0IF){
        //printf("Error c\n\r");
        return TIMEOUT;
    }
    //printf("START OK\n\r");
    return OK;
}

unsigned char DHT22_read(void){
    unsigned char bitmask;
    unsigned int t1val=0;
    unsigned char start=0;
    //envío señal de start
    start=DHT22_start();
    //si start no es OK muestra la causa
    if (start!=OK) return start;
    //si start OK se leen los datos
    DHT22_data[0]=0;
    DHT22_data[1]=0;
    DHT22_data[2]=0;
    DHT22_data[3]=0;
    DHT22_data[4]=0;
    for(unsigned char i=0;i<5;i++){
        bitmask=128;                //para introducir 1 donde corresponde        
        
        //recepción de 8 bits para cada elemento del array
        for(unsigned char j=0;j<8;j++){
            /*Cada transmición de datos empieza con un 0. La duración del pulso
             * en estado alto define si el dato es 1 o 0. 
             * 26-28us: 0
             * 70us: 1
             */
             
            DHT22_expect(1);            //aa
            DHT22_expect(0);             //bb
            //t1val=TMR1;
            if (TMR0>25){              //si t1val es mayor a 50us el valor es 1
                DHT22_data[i]=DHT22_data[i]|bitmask;
            }
            bitmask>>=1;                 //rotación para verificar los bits
        }
    }
    
    //el checksum debe ser igual a los 8bits menos significativos de la suma de
    //los 4 bytes anteriores.
    //printf("%x\t%x\t%x\t%x\t%x\n\r",DHT22_data[0],DHT22_data[1],DHT22_data[2],DHT22_data[3],DHT22_data[4]);
    
    unsigned char suma=(DHT22_data[0]+DHT22_data[1]+DHT22_data[2]+DHT22_data[3]);
    //printf("SUMA: %x\n\r",suma);
    if(DHT22_data[4]!=suma){
        return CHECKSUM;
    }
    return OK;                          //no checksum o timerout
        
}

void DHT22_expect(unsigned char nivel){
    //Reseteo de timer1
    TMR0=0;                 //reset contador
    INTCONbits.T0IF=0;      //reset flag
       
    //línea de datos alta se espera 0
    if(nivel==0){
        while(PORTCbits.RC1==1 && INTCONbits.T0IF==0);           //exit 0 o timer overflow
        
    }
    //línea de datos en bajo se espera 1
    else{
        while(PORTCbits.RC1==0 && INTCONbits.T0IF==0);          //exit 1 o timer overflow
    }
}

int datos_temp(void){
    int f;
    f=DHT22_data[2] & 0x7f;
    f*=256;
    f+=DHT22_data[3];

    //if (DHT22_data[2] & 0x80) {
      //  f *= -1;
    //}
    return f;
}

unsigned int datos_hum(void){
    int f;
    f=DHT22_data[0];
    f*=256;
    f+=DHT22_data[1];
    
    return f;   
}