#ifndef PRINT_H
#define	PRINT_H

#include "COM_I2C.h"
#include <string.h>
#include <stdint.h>

#define I2C_ADDRESS 34

void print_string(char *str);
void print_int(uint32_t n);
void print_char(char c);
void println_string(char *str);
void println_int(uint32_t n);
void println_char(char c);

char read_char();

#endif	/* PRINT_H */

