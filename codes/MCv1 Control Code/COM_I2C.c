#include "COM_I2C.h"

#define MAX_RETRY       5

// private enum
typedef enum I2CTransmitionState_e{
    STATE_COMMAND,
    STATE_START,
    STATE_ADDRESS,
    STATE_ACK_ADDRESS,
    STATE_WDATA,
    STATE_ACK_WDATA,
    STATE_STOP,
    STATE_EXIT,
    STATE_RETRY,
    STATE_ACK_RETRY,
    STATE_NACK,
    STATE_IDLE,
    STATE_RCEN,
    STATE_RDATA,
    STATE_ACK_RDATA
} I2CTransmitionState_t;

typedef enum I2CCommandType_e{
    CMD_READ,
    CMD_WRITE,
    CMD_ERROR,
    CMD_IDLE
} I2CCommandType_t;

// private typedef
typedef struct DataSend_s{
    uint8_t *Buffer;
    uint16_t BufferCount;
    uint16_t BufferTransfer;
    PFN_ON_COM_TRANSFER OnTransferComplete;
}DataSend_t;

typedef struct DataCommunication_s{
    DataSend_t RX;
    DataSend_t TX;
} DataCommunication_t;

// private function prototypes
void __attribute__ ((__interrupt__, no_auto_psv)) _MI2C1Interrupt(void);
void I2C_StateMachine(void);
void I2C_Start_Timer();
void I2C_Stop_Timer();


static volatile DataCommunication_t COM_Data;
static volatile I2CTransmitionState_t State;
static volatile I2CCommandType_t Command;
static volatile uint8_t done;
uint8_t retry_counter;

char timeout_done = 0;

void Init_I2C(){        // configure I2C module for master mode, 100khz, and enable interrupt
	PMD1bits.I2C1MD = 0;	// enable I2C1 module
	// setup as master
	I2C1CON1bits.I2CEN = 0;		// disable i2c	
	I2C1CON1bits.I2CSIDL = 0;	// continue module operation in idle mode
	I2C1CON1bits.A10M = 0;		// 7-bit address
	I2C1CON1bits.DISSLW = 1;		// disable slew rate control
	I2C1CON1bits.SMEN = 0;		// disable SMB levels
	I2C1CON1bits.ACKDT = 0;		// ACK
	I2C1CON2 = 0x0000;
    
    // clear status registers
	I2C1STAT = 0x0000;
	// setup baud rate generator
	I2C1BRG = 195;				// 100khz operation
	// setup interrupt handler
	IPC4bits.MI2C1IP = 4;		// interrupt priority
	IFS1bits.MI2C1IF = 0;		// clear i2c interrupt flag
	IEC1bits.MI2C1IE = 1;		// enable i2c interrupt
    I2C1CON1bits.I2CEN = 1;		// enable i2c	
//    #ifdef I2C_DEBUG_ON
//    TX.address = 0x44;
//    RX.address = 0x45;
//    #endif
    
    T5CONbits.TON = 0;
    T5CONbits.TCS = 0;
    T5CONbits.TGATE = 0;
    T5CONbits.TCKPS = 0b11;
    
    TMR5 = 0x0000;
    PR5 = 7813;    // 50ms i2c retry timeout
    
    IPC7bits.T5IP = 3;
    IFS1bits.T5IF = 0;
    IEC1bits.T5IE = 1;    
}

void I2C_ResetTX(){
    COM_Data.TX.Buffer = NULL;
    COM_Data.TX.BufferCount = 0;
    COM_Data.TX.BufferTransfer = 0;
    COM_Data.TX.OnTransferComplete = NULL;
}

void I2C_ResetRX(){
    COM_Data.RX.Buffer = NULL;
    COM_Data.RX.BufferCount = 0;
    COM_Data.RX.BufferTransfer = 0;
    COM_Data.RX.OnTransferComplete = NULL;
}

void I2C_SendBuffer(uint8_t *pBuffer, uint16_t sizeToSend, PFN_ON_COM_TRANSFER pfDataSend){
    if(pBuffer!=0 && sizeToSend!=0){
        uint8_t timeout_retry = 0;
        while(timeout_retry<1){
            COM_Data.TX.Buffer = pBuffer;
            COM_Data.TX.BufferCount = sizeToSend;
            COM_Data.TX.BufferTransfer = 0;
            COM_Data.TX.OnTransferComplete = pfDataSend;
            
            Command = CMD_WRITE;
            done = 0;
            retry_counter = 0;
            State = STATE_COMMAND;
            I2C1CON1bits.SEN = 1;                // start TX sequence

            I2C_Start_Timer();
            while(timeout_done==0 && State != STATE_IDLE){
                I2C_StateMachine();
            }
            I2C_Stop_Timer();
            
            if(timeout_done==1 || Command == CMD_ERROR){
                timeout_retry++;
            }else{
                break;
            }
        }
    }
}

uint8_t I2C_ReceiveBuffer(uint8_t *pBuffer, uint16_t sizeToReceive, PFN_ON_COM_TRANSFER pfDataReceived){
    if(pBuffer!=0 && sizeToReceive!=0){
        uint8_t timeout_retry = 0;
        while(timeout_retry < 1){
            COM_Data.RX.Buffer = pBuffer;
            COM_Data.RX.BufferCount = sizeToReceive;
            COM_Data.RX.BufferTransfer = 0;
            COM_Data.RX.OnTransferComplete = pfDataReceived;

            Command = CMD_READ;
            done = 0;
            retry_counter = 0;
            State = STATE_COMMAND;

            I2C_Start_Timer();
            while(timeout_done==0 && State != STATE_IDLE){
                I2C_StateMachine();
            }
            I2C_Stop_Timer();

            if(timeout_done==1 || Command == CMD_ERROR){
                timeout_retry++;
            }else{
                return 1;
            }
        }
    }
    return 0;
}

void __attribute__ ((__interrupt__, no_auto_psv)) _MI2C1Interrupt(void){
    done = 1;
    IFS1bits.MI2C1IF = 0;
}

void I2C_StateMachine(void){
    switch(State){
        case STATE_COMMAND:
            if(Command==CMD_READ || Command==CMD_WRITE){
                State = STATE_START;
            }
            break;
        case STATE_START:                                 // initiate start sequence
            I2C1CON1bits.SEN = 1;
            State = STATE_ADDRESS;
            break;
        case STATE_ADDRESS:                               // send device address
            if(done==1){
                done = 0;
                if(Command==CMD_WRITE){
                    I2C1TRN = COM_Data.TX.Buffer[COM_Data.TX.BufferTransfer++];
                }else if(Command==CMD_READ){
                    I2C1TRN = COM_Data.RX.Buffer[COM_Data.RX.BufferTransfer++];
                }
                State = STATE_ACK_ADDRESS;
            }
            break;
        case STATE_ACK_ADDRESS:     // wait for address byte TX to complete
            if(done==1){
                done = 0;
                if(I2C1STATbits.ACKSTAT == 1){      // slave replied NACK
                    if(retry_counter < MAX_RETRY){  // try to TX/RX
                        State = STATE_RETRY;
                    }else{                          // enter error state
                        State = STATE_NACK;
                    }
                }else{                              // slave replied ACK
                    retry_counter = 0;
                    if(Command==CMD_WRITE){
                        State = STATE_WDATA;
                    }else if (Command==CMD_READ){
                        State = STATE_RCEN;
                    }
                }
            }
            break;
        case STATE_WDATA:                           // write data
            I2C1TRN = COM_Data.TX.Buffer[COM_Data.TX.BufferTransfer++];
            State = STATE_ACK_WDATA;
            break;
        case STATE_ACK_WDATA:                       
            if(done==1){                            // wait for data byte to complete
                done = 0;
                State = STATE_WDATA;
                if(I2C1STATbits.ACKSTAT == 1){      // NACK received
                    State = STATE_NACK;
                }else{                              // ACK received
                    if(COM_Data.TX.BufferTransfer == COM_Data.TX.BufferCount){
                        State = STATE_STOP;
                    }
                }
            }
            break;
        case STATE_STOP:
            I2C1CON1bits.PEN = 1;
            State = STATE_EXIT;
            Command = CMD_IDLE;
            break;
        case STATE_EXIT:
            if(done==1){
                done = 0;
                State = STATE_IDLE;
            }
            break;
        case STATE_RETRY:
            I2C1CON1bits.PEN = 1;
            State = STATE_ACK_RETRY;
            retry_counter++;
            break;
        case STATE_ACK_RETRY:
            if(done==1){
                done = 0;
                State = STATE_COMMAND;
                if(Command==CMD_WRITE){
                    COM_Data.TX.BufferTransfer = 0;
                }else if (Command==CMD_READ){
                    COM_Data.RX.BufferTransfer = 0;
                }
            }
            break;
        case STATE_NACK:
            I2C1CON1bits.PEN = 1;
            State = STATE_EXIT;
            Command = CMD_ERROR;
            break;
        case STATE_RCEN:
            I2C1CON1bits.RCEN = 1;
            State = STATE_RDATA;
            break;
        case STATE_RDATA:
            if(done == 1){
                done = 0;
                State = STATE_ACK_RDATA;
                *(COM_Data.RX.Buffer+COM_Data.RX.BufferTransfer) = I2C1RCV;
                COM_Data.RX.BufferTransfer++;
                if(COM_Data.RX.BufferTransfer == COM_Data.RX.BufferCount){
                    I2C1CON1bits.ACKDT = 1;  // NACK
                }else{
                    I2C1CON1bits.ACKDT = 0;  // ACK
                }
                I2C1CON1bits.ACKEN = 1;
            }
            break;
        case STATE_ACK_RDATA:
            if(done == 1){
                done = 0;
                if(COM_Data.RX.BufferTransfer == COM_Data.RX.BufferCount){
                    State = STATE_STOP;
                }else{
                    State = STATE_RCEN;
                }
            }
    }
}

void __attribute__ ((__interrupt__, no_auto_psv)) _T5Interrupt(void){   // tx time out
    timeout_done = 1;
    IFS1bits.T5IF = 0;
}

void I2C_Start_Timer(){ // start timeout timer here
    timeout_done = 0;
    TMR5 = 0x00;
    T5CONbits.TON = 1;
}

void I2C_Stop_Timer(){  // stop timeout timer here
    T5CONbits.TON = 0;
}