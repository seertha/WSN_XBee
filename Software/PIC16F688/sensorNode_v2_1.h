/******************************************************************************
 * Definiciones generales y prototipo de funciones:
 *  -I2C
 *  -BH1750
 *  -DHT22
 *  -USART
 ******************************************************************************/


#ifndef NODESENSOR
#define NODESENSOR
#define _XTAL_FREQ      4000000

//#ifdef I2C_COMM
//definiciones y prototipo de funciones I2C
#define SDA_TRIS        TRISAbits.TRISA4
#define SCL_TRIS        TRISAbits.TRISA5
#define SDA             PORTAbits.RA4
#define SCL             PORTAbits.RA5
#define ACK             0x00
#define NACK            0x80

void i2c_start(void);
void i2c_stop(void);
void bit_out(unsigned char data);
void bit_in(unsigned char *data);
unsigned char i2c_wr(unsigned char i2c_data);
unsigned char i2c_rd(unsigned char ack);
//#endif //I2C_COMM

//#ifdef BH1750_COMM
//definiciones sensor y prototipo de funciones BH1750
#define ACK             0x00
#define NACK            0x80
#define ADDR_WR         0x46
#define ADDR_RD         0x47
#define ONE_H_MODE      0x20
#define C_H_MODE        0x10

void bh1750_inicio(unsigned char modo);
unsigned int lecturaRaw(void);
unsigned int lecturaLux(unsigned char modo);
//#endif //BH1750_COMM

//#ifdef DHT22_COMM
//definiciones sensor y prototipo de funciones DHT22
#define OK 3
#define TIMEOUT 5
#define CHECKSUM 7

unsigned char DHT22_start(void);
void DHT22_expect(unsigned char);
unsigned char DHT22_read (void);
int datos_temp (void);
unsigned int datos_hum (void);
//#endif //DHT22_COM

//#ifdef USART_COMM
//definiciones sensor y prototipo de funciones USART
void USARTinicio(void);
void putch(unsigned char);
//#endif //USART_COMM
#endif