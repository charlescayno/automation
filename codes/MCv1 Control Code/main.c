//#include <p33EV256GM106.h>
#include <xc.h>
#include <stdint.h>
#include "print.h"
#include "COM_I2C.h"
#include <math.h>

#define         MRELAY      _LATC10
#define         TRISRELAY   _TRISC10
#define         LED1        _LATE12
#define         TRISLED1    _TRISE12
#define         LED2        _LATE13
#define         TRISLED2    _TRISE13
#define         LED3        _LATE14
#define         TRISLED3    _TRISE14
#define         FCAN        40000000                // Fcyc = 1/2Fpll
#define         BAUD9600    ((FCAN/9600)/16) - 1
#define         BAUD19200   ((FCAN/19200)/16) - 1
#define         BAUD38400   ((FCAN/38400)/16) - 1   // this is what the demo UART serial baud rate is
#define         BAUD576000  ((FCAN/57600)/16) - 1   // selection of transmitter baud rate divisors
#define         ANSEL_RTS   _ANSE12
#define         ANSEL_CTS   _ANSE13
#define         TRIS_RTS    _TRISE12
#define         TRIS_MON    _TRISB4
#define         TRANSMIT    1
#define         RECEIVE     0
#define         ACCEL       250   // value used to change acceleration value by varying increment rate of MDC

#define         L           0xC383
#define         X           0xC303
#define         H           0xC203
#define         FWD         0
#define         REV         1


/* CAN filter and mask defines */
/* Macro used to write filter/mask ID to Register CiRXMxSID and
CiRXFxSID. For example to setup the filter to accept a value of
0x123, the macro when called as CAN_FILTERMASK2REG_SID(0x123) will
write the register space to accept message with ID 0x123
USE FOR STANDARD MESSAGES ONLY */
#define CAN_FILTERMASK2REG_SID(x) ((x & 0x07FF)<< 5)
/* the Macro will set the "MIDE" bit in CiRXMxSID */
#define CAN_SETMIDE(sid) (sid | 0x0008)
/* the macro will set the EXIDE bit in the CiRXFxSID to
accept extended messages only */
#define CAN_FILTERXTD(sid) (sid | 0x0008)
/* the macro will clear the EXIDE bit in the CiRXFxSID to
accept standard messages only */
#define CAN_FILTERSTD(sid) (sid & 0xFFF7)
// End of CAN filter and Mask Defines


// DSPIC33EV256GM106 Configuration Bit Settings

// Configuration Bits

//  Macros for Configuration Fuse Registers
_FOSCSEL(FNOSC_PRIPLL);
_FOSC(FCKSM_CSDCMD & OSCIOFNC_OFF & POSCMD_XT);
// Startup directly into XT + PLL
// OSC2 Pin Function: OSC2 is Clock Output
// Primary Oscillator Mode: XT Crystal
#pragma config PWMLOCK = OFF            // PWM Lock Enable Bit (PWM registers may be written without key sequence)
_FWDT(FWDTEN_OFF);      // Watchdog Timer Enabled/disabled by user software

_FICD(ICS_PGD2);        // PGD3 for external PK3/ICD3/RealIce, use PGD2 for PKOB
_FPOR(BOREN0_OFF);      // no brownout detect
_FDMT(DMTEN_DISABLE);   // no deadman timer  <<< *** New feature, important to DISABLE

// #pragma config statements should precede project file includes.
// Use project enums instead of #define for ON and OFF.


#define NUM_OF_ECAN_BUFFERS 32
#define MSG_SID 0x122               // the arbitrary CAN SID of the transmitted message
                                    // MC - 0x123; BMS - 0x122
#define RTR_SID 0x122               //SID for RTR

/* ECAN message type identifiers */

#define CAN_MSG_DATA 0x01
#define CAN_MSG_RTR 0x02
#define CAN_FRAME_EXT 0x03
#define CAN_FRAME_STD 0x04
#define CAN_BUF_FULL 0x05
#define CAN_BUF_EMPTY 0x06

#define NUM_DIGITS 5               // floating point digits to print
#define STRING_BUFFER_SIZE 64      // arbitrary length message buffer
#define LIN_MESSAGE_SIZE 8         // message size of the received LIN demo message

volatile unsigned int ecan1MsgBuf[NUM_OF_ECAN_BUFFERS][8]
__attribute__((aligned(NUM_OF_ECAN_BUFFERS * 16)));

/* CAN receive message structure in RAM */
typedef struct{
	/* keep track of the buffer status */
	unsigned char buffer_status;
	/* RTR message or data message */
	unsigned char message_type;
	/* frame type extended or standard */
	unsigned char frame_type;
	/* buffer being used to send and receive messages */
	unsigned char buffer;
	/* 29 bit id max of 0x1FFF FFFF
	*  11 bit id max of 0x7FF */
	unsigned long id;
	unsigned int data[8];
	unsigned char data_length;
}mID;

// Prototype Declarations
void rxECAN(mID *message);
void clearRxFlags(unsigned char buffer_number);
void clearIntrflags(void);
void ecan1WriteMessage(void);
void init_hw(void);
void delay_10ms(unsigned char num);
void Delayus(int);
void ADCInit(void);
void ADCConvert(int);
void Calc_Checksum(int);
void InitCAN(void);
void CAN_Transmit(void);
void Transmit_Data(void);
void Receive_Data(void);
void Can_RX_to_I2C(void);
void init_RTR(void);

volatile int channel, PotValue, TempValue, i;
volatile int f_tick, s_tick, p0, p1, id_byte, data_byte, checksum;
volatile int tickTime = 50; // Tick time in us
volatile char can_rx;       // receive message flags

char Buf_result[NUM_DIGITS + 2];        // digits + '.' and allow for '-'
char *pBuf;                             // buffer for ASCII result of a float
char s[STRING_BUFFER_SIZE];             // s[] holds a string to transmit
unsigned char mode;
unsigned int ascii_lo, ascii_hi, hex_dig;

volatile int datal;
volatile int datah;

mID canRxMessage;

//End of code from uChip

//IOCON Arrays for PWM Config
unsigned int IOCONFwd1[8] = {X, H, L, X, X, H, L, X};   //For PWM 3
unsigned int IOCONFwd2[8] = {X, X, H, H, L, L, X, X};   //For PWM 2
unsigned int IOCONFwd3[8] = {X, L, X, L, H, X, H, X};   //For PWM 1

//unsigned int IOCONRev2[8] = {X, X, H, H, L, L, X, X};   //For PWM 3
//unsigned int IOCONRev3[8] = {X, H, L, X, X, H, L, X};   //For PWM 2
//unsigned int IOCONRev1[8] = {X, L, X, L, H, X, H, X};   //For PWM 1

unsigned int hallNextF[8] = {0,5,3,1,6,4,2,0};  // forward sequence for RPM
unsigned int hallNextR[8] = {0,3,6,2,5,1,4,0};  //reverse sequence for RPM

//unsigned int IOCONRev1[8] = {0xC304, 0xC344, 0xC304, 0xC344, 0xC104, 0xC304, 0xC104, 0xC304};
//unsigned int IOCONRev2[8] = {0xC304, 0xC304, 0xC104, 0xC104, 0xC344, 0xC344, 0xC304, 0xC304};
//unsigned int IOCONRev3[8] = {0xC304, 0xC104, 0xC344, 0xC304, 0xC304, 0xC104, 0xC344, 0xC304};


//Init functions - Private Fxns
void InitOscillator(void);
void InitGPIO(void);
void InitADC(void);
void InitPWM(void);
void initCNInterrupt(void);
int getPedalOffset(void);

//Operations
int getThrot(void);
int getTemp(void);
void test_transmit(void);

volatile  uint16_t j = 0;
int ADCValue = 0;
int blink = 0;
int32_t adcOffsetCh0 = 0, adcOffsetCh1 = 0, adcOffsetCh2 = 0, adcOffsetCh3 = 0;
unsigned int HallValue, prevHallValue1, prevHallValue2;
unsigned int rpmCounter = 0;
int throtOffset = 0;
int RPM = 0;
int Direction = 0;

typedef enum MC_state_t{
    FREEWHEEL,
    MOTORING,
    IDLE
}MC_state_e;

static volatile MC_state_e MC_State;

int main(void) {
    int tcnt = 0, x = 0;
    int duty = 0;
    float temp = 0;
    //float dutycom = 0.0;
    float fdutyreq = 0.0;
    int idutyreq = 0;
    int idutyreq_temp = 0;

    TRISRELAY = 0;
    MRELAY = 0;

    InitOscillator();
    clearIntrflags();
    InitGPIO();
    init_hw();
    Init_I2C();
    InitADC();
    initCNInterrupt();
    InitPWM();
    

    s_tick = 0;
    LED1 = 1; //Turn ON LED


     //NOTE: test to get MIN MAX - expected is from 1648 to 2714
     while(1){               //comment out after test
//         duty = getThrot();
//         println_int(duty);
//         println_string("ADC Test");
//         delay_10ms(100);
         MDC = 500;
         
                    IOCON1 = IOCONFwd1[1];
                    IOCON2 = IOCONFwd2[1];
                    IOCON3 = IOCONFwd3[1];
         
     }                       //comment out after test


    //High pedal lockout code - user must release throttle at startup

    while(getThrot() > 1680){ //NOTE: adjust according to min - set to MIN + 30
        println_string("High Pedal");
        //insert code here to transmit status thru CAN to alert BMS
        MRELAY = 0;
    }

    //Get throttle offset voltage to get true zero throttle
    throtOffset = getPedalOffset(); // Future code must allow measurement of offset and max value to allow use of different pedal types;
    while (s_tick <= 3);    // wait for 1 second
    s_tick = 0;             // clear flag
    LED1 = 0;               // Offset get complete
    LED2 = 1;
    LED3 = 0;



    while (s_tick <= 19);    // wait for 5 second
    MRELAY = 1;
    LED1 = 0;
    LED2 = 0;
    LED3 = 0;

    //Initialize state machine here
    if(RPM >= 100) MC_State = FREEWHEEL;
    else MC_State = IDLE;
    println_string("Start Main Loop");
    MC_State = MOTORING;
    while (1)
    {

        //Start of MC operation loop

        Delayus(ACCEL);     //delay to limit acceleration dMDC/dt



        duty = getThrot();  //get throttle signal level
        //check if throttle value is within bounds


        if(duty <= (throtOffset + 10)) duty = 0;
        else if(duty >= 2500) duty = 2500; //NOTE: set to MAX actual from test
        else{
            duty = duty - throtOffset;
            temp = duty * 2.35;
            duty = (int)floor(temp);
        }


        //comment in to test duty values------------TEST THIS!!!!!
        //println_int(duty); //must be zero to 2500

        //fdutyreq = RPM * 0.26; //NOTE: SET TO ZERO IF POWER LOSS AFTER RUNNING
        fdutyreq=0;
        idutyreq = (int)floor(fdutyreq); //value in integer - used to prevent unwanted regen

        //ecan1MsgBuf[0][2] = 0x0006;
        //ecan1MsgBuf[0][3] = duty;
        //ecan1MsgBuf[0][4] = RPM;
        //ecan1MsgBuf[0][5] = ((MC_State << 8) & 0xFF00) + 0xFF;

        //Start of state machine

        switch(MC_State){
            case MOTORING:
                
                LED2 = 1;
                LED3 = 1;

//                if(duty == 0 && idutyreq == 0){
//                    MC_State = IDLE;
//                    IOCON1 = IOCONFwd1[0];
//                    IOCON2 = IOCONFwd2[0];
//                    IOCON3 = IOCONFwd3[0];
//                    MDC = 0;
//                    break;
//                }

//                if((duty - idutyreq) < -250 || duty <= 30){
//                    MC_State = FREEWHEEL;
//                    IOCON1 = IOCONFwd1[0];
//                    IOCON2 = IOCONFwd2[0];
//                    IOCON3 = IOCONFwd3[0];
//                    MDC = 0;
//                    break;
//                }

                if(duty > MDC) MDC = MDC + 1;
                else if(duty < MDC){
                    MDC = MDC - 1;
                    if(MDC <= 0) MDC = 0;
                }

                break;

            case FREEWHEEL:
                //print_string("  Freewheel  ");
                //println_int(idutyreq);

                LED2 = 0;
                LED3 = 1;
                MDC = 0;

                if(duty == 0 && idutyreq == 0) MC_State = IDLE;

                if(duty >= idutyreq){
                    MC_State = MOTORING;
                    HallValue = PORTC  & 0x7;
                    prevHallValue1 = HallValue;

                    IOCON1 = IOCONFwd1[HallValue];
                    IOCON2 = IOCONFwd2[HallValue];
                    IOCON3 = IOCONFwd3[HallValue];
                    MDC = 0;
                    break;
                }

                break;

            case IDLE:
                //print_string("  Idle  ");
                //println_int(idutyreq);

                IOCON1 = IOCONFwd1[0];
                IOCON2 = IOCONFwd2[0];
                IOCON3 = IOCONFwd3[0];
                MDC = 0;

                //Get Hall value
                HallValue = PORTC  & 0x7;
                prevHallValue1 = HallValue;

                //Check conditions
                if(idutyreq > 50){          //motor spins
                    MC_State = FREEWHEEL;
                    break;
                }

                if(duty >= idutyreq + 50){
                    MC_State = MOTORING;
                    HallValue = PORTC  & 0x7;
                    prevHallValue1 = HallValue;

                    IOCON1 = IOCONFwd1[HallValue];
                    IOCON2 = IOCONFwd2[HallValue];
                    IOCON3 = IOCONFwd3[HallValue];
                    MDC = 0;
                    break;
                }

                break;

            default:
                MRELAY = 0;
                while(1){
                    while(s_tick <= 3);
                    s_tick = 0;
                    LED1 ^= 1;
                    LED2 ^= 1;
                    LED3 ^= 1;
                    //println_string("State Error");
                    //insert code here to transmit status thru CAN to alert BMS
                };
                break;
        }

        /*
        if(tcnt == 100){
            if(C1TR01CONbits.TXREQ0 == 0){
            CAN_Transmit();
            }
            LED1 ^= 1;
            tcnt = 0;
        }

        else tcnt++;
        */
    }

    return 0;
}

void clearIntrflags(void){
    /* Clear Interrupt Flags */

    IFS0 = 0;
    IFS1 = 0;
    IFS2 = 0;
    IFS3 = 0;
    IFS4 = 0;
    IPC16bits.U1EIP = 6;        //service the LIN framing error before the RX
    IPC2bits.U1RXIP = 4;
}

void InitOscillator(void){

    //  Configure Oscillator to operate the device at 80MHz/40MIPs
    // 	Fosc= Fin*M/(N1*N2), Fcy=Fosc/2
    // 	Fosc= 8M*40/(2*2)=80Mhz for 8M input clock
    // To be safe, always load divisors before feedback


    CLKDIVbits.PLLPOST = 0;     // N1=2
    CLKDIVbits.PLLPRE = 0;      // N2=2
    PLLFBD = 38;                // M=(40-2), Fcyc = 40MHz for ECAN baud timer


    // Disable Watch Dog Timer

    RCONbits.SWDTEN = 0;
}

void init_hw(void){
    // set up the LED ports

    TRISLED1 = 0;
    TRISLED2 = 0;
    TRISLED3 = 0;
    TRISRELAY = 0;
    MRELAY = 0;
    s_tick = 0;
    f_tick = 0;                 // the timer ticks

    //
    // Timer 1 to generate an interrupt every 250ms
    //
    T1CONbits.TON = 0;          // Disable Timer1
    T1CONbits.TCS = 0;          // Select internal instruction cycle clock
    T1CONbits.TGATE = 0;        // Disable Gated Timer mode
    T1CONbits.TCKPS = 0x3;      // Select 1:256 Prescaler
    PR1 = 39062;                // Load the period value (250ms/(256*25ns))
    IPC0bits.T1IP = 0x03;       // Set Timer 1 Interrupt Priority Level
    IFS0bits.T1IF = 0;          // Clear Timer 1 Interrupt Flag
    IEC0bits.T1IE = 1;          // Enable Timer1 interrupt

    //
    // Timer 2 to generate an interrupt every 10ms
    //
    T2CONbits.TON = 0;          // Disable Timer2
    T2CONbits.TCS = 0;          // Select internal instruction cycle clock
    T2CONbits.TGATE = 0;        // Disable Gated Timer mode
    T2CONbits.TCKPS = 0x3;      // Select 1:256 Prescaler
    TMR2 = 0x00;                // Clear timer register
    PR2 = 1562;                 // Load the period value (10ms/(256*25ns))
    IPC1bits.T2IP = 0x02;       // Set Timer 2 Interrupt Priority Level
    IFS0bits.T2IF = 0;          // Clear Timer 2 Interrupt Flag
    IEC0bits.T2IE = 1;          // Enable Timer2 interrupt

    T2CONbits.TON = 1;          // Start Timer2
    T1CONbits.TON = 1;          // Start Timer1
}

void InitGPIO(void){
    /* Port E Init*/
    ANSELE = 0x0000;
    TRISE = 0x0000;
    LATE = 0x0000;

    /* Port B Init*/
    ANSELB = 0x0003;
    TRISB = 0x0013;
    LATB = 0x0000;

    /*Port C Init*/
    ANSELC = 0x0000;
    TRISC = 0x0007;
    LATC = 0x00;

    /*POrt A Init*/
    ANSELA = 0x0003;
    TRISA = 0x0003;
    LATA = 0x0000;
}

void InitADC(void){

    adcOffsetCh0 = 0;
    adcOffsetCh1 = 0;
    adcOffsetCh2 = 0;
    adcOffsetCh3 = 0;

    /* Initialize and enable ADC module */
    AD1CON1bits.ADON = 0;
    AD1CON1bits.ADSIDL = 0;
    AD1CON1bits.ADDMABM = 0;
    AD1CON1bits.AD12B = 1;
    AD1CON1bits.FORM = 0b00;
    AD1CON1bits.SSRC = 0b000;
    AD1CON1bits.SSRCG = 0;
    AD1CON1bits.ASAM = 1;

    AD1CON2 = 0x0000;
    AD1CON3bits.ADRC = 0;
    AD1CON3bits.SAMC = 8;
    AD1CON3bits.ADCS = 8;
    AD1CON4 = 0x0000;

    AD1CON2bits.CHPS = 00; //Convert channel 0 only for now

    //Connect Analog Ports to Channel 0 and 1
    //CH0 is AN2 - Throttle
    //CH1 is AN3 - Temp
    AD1CHS0bits.CH0NA = 0;
    AD1CHS0bits.CH0NB = 0;
    AD1CHS0bits.CH0SA = 0;
    AD1CHS0bits.CH0SB = 0;


    AD1CSSH = 0x0000;
    AD1CSSLbits.CSS0 = 1;
    //AD1CSSLbits.CSS3 = 1;
    AD1CON1bits.ADON = 1;
    Delayus(40);
}

int getThrot(void){
    AD1CHS0bits.CH0NA = 0;
    AD1CHS0bits.CH0NB = 0;
    AD1CHS0bits.CH0SA = 0;
    AD1CHS0bits.CH0SB = 0;

    AD1CON1bits.SAMP = 0;
	while (!AD1CON1bits.DONE);

    return ADC1BUF0;
}

int getTemp(void){
    AD1CHS0bits.CH0NA = 0;
    AD1CHS0bits.CH0NB = 0;
    AD1CHS0bits.CH0SA = 1;
    AD1CHS0bits.CH0SB = 1;

    AD1CON1bits.SAMP = 0;
	while (!AD1CON1bits.DONE);

    return ADC1BUF0;
}

void InitCAN(void){
    //
    // drive the CAN STANDBY driver pin low
    //
    TRISCbits.TRISC9 = 0;
    LATCbits.LATC9 = 0;
    TRISFbits.TRISF1 = 0;
    TRISFbits.TRISF0 = 1;

    //
    // remap the CAN module to the proper pins on the board
    //
    RPINR26 = 0x60;         // connect CAN RX to RPI96
    RPOR9 = 0x000E;         // connect CAN TX to RP97


    //enter config mode
    C1CTRL1bits.REQOP = 4;

    while (C1CTRL1bits.OPMODE != 4);

    /* Set up the CAN module for 250kbps speed with 10 Tq per bit. */

    C1CFG1 = 0x47;          // BRP = 8 SJW = 2 Tq
    C1CFG2 = 0x2D2;
    C1FCTRL = 0xC01F;       // No FIFO, 32 Buffers

    /* 4 CAN Messages to be buffered in DMA RAM */
	C1FCTRLbits.DMABS=0b000;

    /* Filter configuration */
	/* enable window to access the filter configuration registers */
	C1CTRL1bits.WIN = 0b1;
	/* select acceptance mask 0 filter 0 buffer 1 */
	C1FMSKSEL1bits.F0MSK = 0;

    /* setup the mask to check every bit of the standard message, the macro when called as */
    /* CAN_FILTERMASK2REG_SID(0x7FF) will write the register C1RXM0SID to include every bit in */
    /* filter comparison */
    C1RXM0SID = CAN_FILTERMASK2REG_SID(0x000); //changed to 0x7F0 to include up to 16 devices

    	/* configure acceptance filter 0
	setup the filter to accept a standard id of 0x123,
	the macro when called as CAN_FILTERMASK2REG_SID(0x123) will
	write the register C1RXF0SID to accept only standard id of 0x123
	*/
	C1RXF0SID = CAN_FILTERMASK2REG_SID(MSG_SID);

    /* set filter 0 to check for standard ID and accept standard id only */
	C1RXM0SID = CAN_SETMIDE(C1RXM0SID);
	C1RXF0SID = CAN_FILTERSTD(C1RXF0SID);

    /* acceptance filter to use buffer 0 for incoming messages */
	C1BUFPNT1bits.F0BP = 0b0000;
    /* enable filter 0 */
	C1FEN1bits.FLTEN0 = 1;

    /* clear window bit to access ECAN control registers */
	C1CTRL1bits.WIN = 0;

    // Place the ECAN module in Normal mode.
    C1CTRL1bits.REQOP = 0;
    while (C1CTRL1bits.OPMODE != 0);

    /* clear the buffer and overflow flags */
	C1RXFUL1=C1RXFUL2=C1RXOVF1=C1RXOVF2=0x0000;
    C1TR01CONbits.TXEN0 = 0x1;          // Buffer 0 is the Transmit Buffer
    C1TR01CONbits.TX0PRI = 0x3;         // transmit buffer priority

    // set up the CAN DMA0 for the Transmit Buffer
    //
    DMAPWC = 0;
    DMARQC = 0;
    DMA0CON = 0x2020;
    DMA0REQ = 70;
    DMA0CNT = 7;
    DMA0PAD = (volatile unsigned int)&C1TXD;
    DMA0STAL = (unsigned int)&ecan1MsgBuf;
    DMA0STAH = (unsigned int)&ecan1MsgBuf;
    DMA0CONbits.CHEN = 0x1;
    //end of DMA Code

    //C1TR01CONbits.RTREN0 = 1;

    // CAN RX interrupt enable - 'double arm' since 2-level nested interrupt
    //
    C1INTEbits.RBIE = 1;
    C1INTEbits.TBIE = 1;
    IEC2bits.C1IE = 1;
}

void init_RTR(void){
    ecan1MsgBuf[0][0] = MSG_SID << 2;
    ecan1MsgBuf[0][1] = 0x0000;
    /* CiTRBnDLC = 0b0000 0000 xxx0 1111
    EID<17:6> = 0b000000
    RTR = 0b0
    RB1 = 0b0
    RB0 = 0b0
    DLC = 8 */
    ecan1MsgBuf[0][2] = 0x0008;
    ecan1MsgBuf[0][3] = 0xABCD; // switch data, leading zeros
    ecan1MsgBuf[0][4] = 0x1234;
    ecan1MsgBuf[0][5] = 0x5678;
    ecan1MsgBuf[0][6] = 0xABCD;
}

void CAN_Transmit(void){
    ecan1MsgBuf[0][0] = MSG_SID << 2;
    ecan1MsgBuf[0][1] = 0x0000;
    /* CiTRBnDLC = 0b0000 0000 xxx0 1111
    EID<17:6> = 0b000000
    RTR = 0b0
    RB1 = 0b0
    RB0 = 0b0
    DLC = 6 */
    //ecan1MsgBuf[0][2] = 0x0006;
    // Write message 6 data bytes as follows:
    //
    // POTH POTL TEMPH TEMPL 0000 S3S2S1
    //
    //ecan1MsgBuf[0][3] = 0x5678; // switch data, leading zeros
    //ecan1MsgBuf[0][4] = 0xABCD;
    //ecan1MsgBuf[0][5] = 0x1234;

    Nop();
    Nop();
    Nop();
    /* Request message buffer 0 transmission */
    C1TR01CONbits.TXREQ0 = 1;
    /* The following shows an example of how the TXREQ bit can be polled to check if transmission
    is complete. */
    Nop();
    Nop();
    Nop();
    //println_string("preloop");
    //while (C1TR01CONbits.TXREQ0 == 1);
    //println_string("postloop");
    // Message was placed successfully on the bus, return
}

void Receive_Data(void){

    // have we received any messages from somewhere?
    if(can_rx == 1){
        println_string("receive");
        Can_RX_to_I2C();
        can_rx = 0;
    }
}

void Transmit_Data(void){

    // read the pot value and save it
    PotValue = getThrot();
    Delayus(100);

    // Send data to PC
    println_string("Transmit Data");
    println_string("***TRANSMITTING ON-BOARD SENSOR VALUES***");
    print_string("Local Pot Voltage: Reading = ");
    println_int(PotValue);

    // read temperature sensor and save it
    TempValue = getTemp();
    Delayus(100);

    // test print the temperature reading
    print_string("Local Temperature: Reading = ");
    println_int(TempValue);

    Delayus(8000);

    // format and send out the CAN port
    // In order for the demo to run, the CAN controller needs an ACK signal
    // If you desire to run the demo for SENT/LIN only, then comment out the
    // following line of code and recompile

    CAN_Transmit();     // Transmit CAN
    Delayus(5000);
    println_int(9);
}

void delay_10ms(unsigned char num){
    f_tick = 0;                         //f_tick increments every 10ms
    while (f_tick < num);               // wait here until 'num' ticks occur
    f_tick = 0;
}

void Delayus(int delay){
    int i;
    for (i = 0; i < delay; i++)
    {
        __asm__ volatile ("repeat #39");
        __asm__ volatile ("nop");
    }
}

/******************************************************************************
*
*    Function:			rxECAN
*    Description:       moves the message from the DMA memory to RAM
*
*    Arguments:			*message: a pointer to the message structure in RAM
*						that will store the message.
******************************************************************************/
void rxECAN(mID *message){
	unsigned int ide=0;
	unsigned int rtr=0;
	unsigned long id=0;

	/*
	Standard Message Format:
	Word0 : 0bUUUx xxxx xxxx xxxx
			     |____________|||
 					SID10:0   SRR IDE(bit 0)
	Word1 : 0bUUUU xxxx xxxx xxxx
			   	   |____________|
						EID17:6
	Word2 : 0bxxxx xxx0 UUU0 xxxx
			  |_____||	     |__|
			  EID5:0 RTR   	  DLC
	word3-word6: data bytes
	word7: filter hit code bits

	Remote Transmission Request Bit for standard frames
	SRR->	"0"	 Normal Message
			"1"  Message will request remote transmission
	Substitute Remote Request Bit for extended frames
	SRR->	should always be set to "1" as per CAN specification

	Extended  Identifier Bit
	IDE-> 	"0"  Message will transmit standard identifier
	   		"1"  Message will transmit extended identifier

	Remote Transmission Request Bit for extended frames
	RTR-> 	"0"  Message transmitted is a normal message
			"1"  Message transmitted is a remote message
	Don't care for standard frames
	*/

	/* read word 0 to see the message type */
	ide=ecan1MsgBuf[message->buffer][0] & 0x0001;

	/* check to see what type of message it is */
	/* message is standard identifier */
	if(ide==0)
	{
		message->id=(ecan1MsgBuf[message->buffer][0] & 0x1FFC) >> 2;
		message->frame_type=CAN_FRAME_STD;
		rtr=ecan1MsgBuf[message->buffer][0] & 0x0002;
	}
	/* mesage is extended identifier */
	else
	{
		id=ecan1MsgBuf[message->buffer][0] & 0x1FFC;
		message->id=id << 16;
		id=ecan1MsgBuf[message->buffer][1] & 0x0FFF;
		message->id=message->id+(id << 6);
		id=(ecan1MsgBuf[message->buffer][2] & 0xFC00) >> 10;
		message->id=message->id+id;
		message->frame_type=CAN_FRAME_EXT;
		rtr=ecan1MsgBuf[message->buffer][2] & 0x0200;
	}
	/* check to see what type of message it is */
	/* RTR message */
	if(rtr==1)
	{
		message->message_type=CAN_MSG_RTR;
	}
	/* normal message */
	else
	{
		message->message_type=CAN_MSG_DATA;
		message->data[0]=(unsigned char)ecan1MsgBuf[message->buffer][3];
		message->data[1]=(unsigned char)((ecan1MsgBuf[message->buffer][3] & 0xFF00) >> 8);
		message->data[2]=(unsigned char)ecan1MsgBuf[message->buffer][4];
		message->data[3]=(unsigned char)((ecan1MsgBuf[message->buffer][4] & 0xFF00) >> 8);
		message->data[4]=(unsigned char)ecan1MsgBuf[message->buffer][5];
		message->data[5]=(unsigned char)((ecan1MsgBuf[message->buffer][5] & 0xFF00) >> 8);
		message->data[6]=(unsigned char)ecan1MsgBuf[message->buffer][6];
		message->data[7]=(unsigned char)((ecan1MsgBuf[message->buffer][6] & 0xFF00) >> 8);
		message->data_length=(unsigned char)(ecan1MsgBuf[message->buffer][2] & 0x000F);
	}
	clearRxFlags(message->buffer);
}

void clearRxFlags(unsigned char buffer_number){
	if((C1RXFUL1bits.RXFUL1) && (buffer_number==1))
		/* clear flag */
		C1RXFUL1bits.RXFUL1=0;
	/* check to see if buffer 2 is full */
	else if((C1RXFUL1bits.RXFUL2) && (buffer_number==2))
		/* clear flag */
		C1RXFUL1bits.RXFUL2=0;
	/* check to see if buffer 3 is full */
	else if((C1RXFUL1bits.RXFUL3) && (buffer_number==3))
		/* clear flag */
		C1RXFUL1bits.RXFUL3=0;
	else;

}

/* code for Timer1 ISR, called every 250ms*/
void __attribute__((__interrupt__, no_auto_psv)) _T1Interrupt(void){
    s_tick++; // increment the 'slow tick'
    RPM = rpmCounter * 26;
    //println_int(RPM);
    rpmCounter = 0;
    IFS0bits.T1IF = 0; //Clear Timer1 interrupt flag

}

/* code for Timer2 ISR, called every 10ms*/
void __attribute__((__interrupt__, no_auto_psv)) _T2Interrupt(void){
    f_tick++; // we increment the variable f_tick

    IFS0bits.T2IF = 0; //Clear Timer2 interrupt flag

}

void __attribute__((interrupt, no_auto_psv))_C1Interrupt(void){
    IFS2bits.C1IF = 0; // clear interrupt flag
    if (C1INTFbits.TBIF)
    {
        C1INTFbits.TBIF = 0;
    }

    if (C1INTFbits.RBIF){

    /*check to see if buffer 1 is full */
        if(C1RXFUL1bits.RXFUL1){
            /* set the buffer full flag and the buffer received flag */
            canRxMessage.buffer_status = CAN_BUF_FULL;
            canRxMessage.buffer = 1;
            can_rx = 1;
        }
    C1INTFbits.RBIF = 0;
    }
}

void __attribute__((interrupt, no_auto_psv)) _DMA0Interrupt(void){
    IFS0bits.DMA0IF = 0; // Clear the DMA0 Interrupt Flag;
}

void __attribute__((interrupt, no_auto_psv)) _DMA1Interrupt(void){
    IFS0bits.DMA1IF = 0; // Clear the DMA1 Interrupt Flag;
}

void __attribute__((interrupt, no_auto_psv)) _DMA2Interrupt(void){
    IFS1bits.DMA2IF = 0; // Clear the DMA2 Interrupt Flag;
}

void __attribute__((interrupt, no_auto_psv)) _DMA3Interrupt(void){
    IFS2bits.DMA3IF = 0; // Clear the DMA3 Interrupt Flag;
}

void __attribute__((interrupt, auto_psv)) _DefaultInterrupt(void){
    LED1 = 1;
    LED2 = 1;
    LED3 = 1;

    while (1);
}

void __attribute__((interrupt, auto_psv)) _OscillatorFail(void){
    LED1 = 1;
    LED2 = 1;
    LED3 = 1;

    while (1);
}

void __attribute__((interrupt, no_auto_psv)) _MathError(void){
    LED1 = 1;
    LED2 = 1;
    LED3 = 1;

    while (1);
}

void __attribute__((interrupt, no_auto_psv)) _StackError(void){
    LED1 = 1;
    LED2 = 1;
    LED3 = 1;

    while (1);
}

void __attribute__((interrupt, no_auto_psv)) _AddressError(void){
    LED1 = 1;
    LED2 = 1;
    LED3 = 1;

    while (1);
}

void Can_RX_to_I2C(void){
    // CAN message out to I2C

    print_string("*** REMOTE CAN MESSAGE ID = 0x");

    // display remote ID byte
    hex_dig = (char)((canRxMessage.id & 0xff00) >> 8);   // upper byte
    ascii_hi = hex_dig & 0xF0;                  // Obtain the upper 4 bits (MSBs) of hex number
    ascii_hi = (ascii_hi >> 4) + 0x30;          // ASCII conversion
    ascii_lo = (hex_dig & 0x0F) + 0x30;         // Obtain the lower 4 bits (LSBs) of hex number

    print_char(ascii_hi);
    print_char(ascii_lo);                    // send out the upper ID byte as ASCII

    hex_dig = (char)(canRxMessage.id & 0x00ff); // lower byte
    ascii_hi = hex_dig & 0xF0;                  // Obtain the upper 4 bits (MSBs) of hex number
    ascii_hi = (ascii_hi >> 4) + 0x30;          // ASCII conversion
    ascii_lo = (hex_dig & 0x0F) + 0x30;         // Obtain the lower 4 bits (LSBs) of hex number

    print_char(ascii_hi);
    println_char(ascii_lo);                    // send out the lower ID byte as ASCII

    println_string(" RECEIVED ***");
    println_string("Data: ");

    print_char(((canRxMessage.data[5] >> 4)& 0x0F)+ 0x30);
    println_char((canRxMessage.data[5] & 0x0F)+ 0x30);
    print_char(((canRxMessage.data[4] >> 4)& 0x0F)+ 0x30);
    println_char((canRxMessage.data[4] & 0x0F)+ 0x30);
    print_char(((canRxMessage.data[3] >> 4)& 0x0F)+ 0x30);
    println_char((canRxMessage.data[3] & 0x0F)+ 0x30);
    print_char(((canRxMessage.data[2] >> 4)& 0x0F)+ 0x30);
    println_char((canRxMessage.data[2] & 0x0F)+ 0x30);
    print_char(((canRxMessage.data[1] >> 4)& 0x0F)+ 0x30);
    println_char((canRxMessage.data[1] & 0x0F)+ 0x30);
    print_char(((canRxMessage.data[0] >> 4)& 0x0F)+ 0x30);
    println_char((canRxMessage.data[0] & 0x0F)+ 0x30);


    LED1 = 1;
    //
    // wait 100ms, turn off LED1
    //
    delay_10ms(10);
    LED1 = 0;
}

void InitPWM(void){

    PTCON = 0x0000;
    PTCON2 = 0x0001; //Prescale: 2
    PTPER = 2500; // for 16kHz frequency
    SEVTCMP = 0x0001;
    CHOP = 0x0000;
    MDC = 0; // Master duty cycle

    //MDC controls duty for all
    PWMCON1 = 0x0100;
    PWMCON2 = 0x0100;
    PWMCON3 = 0x0100;

    //current limit enabled
	//note that IOCONx settings all use FAULT 32
	FCLCON1bits.CLSRC = 0b11111;
    FCLCON2bits.CLSRC = 0b11111;
    FCLCON3bits.CLSRC = 0b11111;

    FCLCON1bits.CLPOL = 1;
	FCLCON2bits.CLPOL = 1;
	FCLCON3bits.CLPOL = 1;

	FCLCON1bits.CLMOD = 1;
	FCLCON2bits.CLMOD = 1;
	FCLCON3bits.CLMOD = 1;

	FCLCON1bits.FLTMOD = 3;
	FCLCON2bits.FLTMOD = 3;
	FCLCON3bits.FLTMOD = 3;

    HallValue = PORTC  & 0x7;
	prevHallValue1 = HallValue;
    IOCON1 = IOCONFwd1[HallValue];
	IOCON2 = IOCONFwd2[HallValue];
	IOCON3 = IOCONFwd3[HallValue];

    PTCONbits.PTEN = 1; //Enable PWM
}

void initCNInterrupt(void){
	//enable CN interrupt pins
	_CNIEC0 = 1;
    _CNIEC1 = 1;
    _CNIEC2 = 1;

	_CNIF = 0;					//clear bit
	_CNIP = 0x04;				//set interrupt priority
	_CNIE = 1;					//enable interrupt bit
}

void __attribute__((interrupt, no_auto_psv)) _CNInterrupt(){

    HallValue = PORTC  & 0x7;

    if(HallValue == hallNextF[prevHallValue1]) rpmCounter++;
    else rpmCounter = 0;
    prevHallValue1 = HallValue;

    if(MC_State == MOTORING){
        IOCON1 = IOCONFwd1[HallValue];
        IOCON2 = IOCONFwd2[HallValue];
        IOCON3 = IOCONFwd3[HallValue];
	}
    else{
        IOCON1 = IOCONFwd1[0];
        IOCON2 = IOCONFwd2[0];
        IOCON3 = IOCONFwd3[0];
    }
	_CNIF = 0;
}

int getPedalOffset(void){
   uint16_t min =  0;
   uint16_t test2 =  0;

   while(getThrot() >= 1680); //NOTE: ensure min is really min - set so same as high pedal limit

   for(i = 0; i < 100; i++){
       min = getThrot();
       test2 = getThrot();
       if(test2 < min) min = test2;
       delay_10ms(1);
   }

   return min;
}
