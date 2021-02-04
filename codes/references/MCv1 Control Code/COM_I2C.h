#ifndef COM_I2C_H
#define	COM_I2C_H

#include <xc.h> // include processor files - each processor file is guarded.  
#include <stdint.h>
#include <stdlib.h>

typedef void( *PFN_ON_COM_TRANSFER)(uint8_t *pBuffer, uint16_t sizeTransfered);
void Init_I2C();
void I2C_ResetTX();
void I2C_ResetRX();
void I2C_SendBuffer(uint8_t *pBuffer, uint16_t sizeToSend, PFN_ON_COM_TRANSFER pfDataSend);
uint8_t I2C_ReceiveBuffer(uint8_t *pBuffer, uint16_t sizeToReceive, PFN_ON_COM_TRANSFER pfDataReceived);

#endif	/* COM_I2C_H */