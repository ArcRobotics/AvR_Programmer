/*
 * AVR Programmer V1.0
 * Created by Omar Al Rafei
 * 
 * This code is distributed under the GNU General Public License (GPL) version 3 or later.
 * For more details, see: https://www.gnu.org/licenses/gpl.html
 *
 * This code is intended for educational purposes only. Commercial use is prohibited.
 * You are required to provide proper attribution to the author, Omar Al Rafei, whenever
 * using or distributing this code.
 */

#ifndef uart_H_
#define uart_H_

#include <avr/io.h>
#include <string.h>
#include <stdlib.h>
#include <avr/interrupt.h>
#include <util/atomic.h>
#include <util/delay.h>

#define Null '\0'

enum PrintMode{
	HEX=16,
	BIN=2,
	DEC=10
};
class Uart{

private:
	bool TXE;
	bool RXE;
	bool TXIE;
	bool RXIE;
	uint16_t BaudRate;
	bool TX_buffer_full();

public:
	void Begin(uint16_t Baud);
	void INIT();
	void print(uint8_t *data);
	void print(char data);
	void print(float data);
	void print(double data);	
	void println(char *string);
	void println(const char *string);
	void println(const char *string,int value);
	void println(char *string,int value,PrintMode printType);
	void println(const char *string,float value);
	void println(const char *string,double value);
	unsigned char read();
	void readStringUntil(char Terminator);
	bool ptrOutofBound(volatile unsigned char *ptr);
	uint8_t available(); //Get number of available bytes in the buffer
	PrintMode Type;


	unsigned long *Fcpu;
	
	//Create a ring buffer for Non-Blocking UART operation
	//To reduce some of the stack you can reduce the buffer sizes 
	//This would lead to some data loss on long strings
	volatile unsigned char RX_Buffer[20];
	volatile unsigned char *RX_Head;
	volatile unsigned char *RX_Tail;
	volatile unsigned char *Next_RX_Tail;
	
	volatile unsigned char TX_Buffer[20];
	volatile unsigned char *TX_Head;
	volatile unsigned char *TX_Tail;
	volatile unsigned char *Next_TX_Head;
	volatile unsigned char *Next_TX_Tail;
	
	
	Uart(bool TX_Enable=true,bool RX_Enable=true,\
		bool RX_INT=true,bool TX_INT=true){
		TXE=TX_Enable;
		RXE=RX_Enable;
		TXIE=TX_INT;
		RXIE=RX_INT;
	}
};
#endif /* UART_H_ */
