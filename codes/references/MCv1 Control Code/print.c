#include "print.h"

typedef struct MyStruct_s{
    uint8_t address;
    uint8_t buffer[30];
}MyStruct_t;

static MyStruct_t TX;
static MyStruct_t RX;

void print_string(char *str){
    int i, j=strlen(str);
    TX.address = (I2C_ADDRESS<<1)+0;
    for(i=0; i<j; i++)
        TX.buffer[i] = str[i];
    I2C_SendBuffer((uint8_t*)&TX, j+1, NULL);
}

void print_int(uint32_t n){
	char buffer[20];		// assume max number of digits < 20
	char temp, isNegative = 0;
	int index = 0, length = 0;

	if(n<0){				// if n is negative
		isNegative = 1;
		n = -n;
	}else if(n==0){			// if n is zero
		buffer[length++] = '0';
	}

	while(n>0){
		buffer[length++] = (n%10) + '0';
		n = n/10;
	}
	buffer[length] = 0;	// EOF
	// invert the string
	for(index = 0; index < (length>>1); index++){	// while index is less than half of length
		temp = buffer[index];
		buffer[index] = buffer[length-index-1];
		buffer[length-index-1] = temp;
	}
	if(isNegative == 1){
		print_char('-');
	}
	print_string(buffer);
}

void print_char(char c){
    TX.address = (I2C_ADDRESS<<1)+0;
    TX.buffer[0] = c;
    I2C_SendBuffer((uint8_t*)&TX, 2, NULL);   
}

void println_string(char *str){
    print_string(str);
    print_char('\n');
}
void println_int(uint32_t n){
    print_int(n);
    print_char('\n');
}

void println_char(char c){
    print_char(c);
    print_char('\n');
}

char read_char(){
    RX.address = (I2C_ADDRESS<<1)+1;
    while(I2C_ReceiveBuffer((uint8_t*)&RX, 2, NULL)==0);
    return (char)RX.buffer[0];
}