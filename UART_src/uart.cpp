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
 *
 * uart.cpp
 *
 * Created: 21/07/2023 19:06:50
 *  Author: Omar
 */ 
#include "uart.h"
//==============================================//
void Uart::Begin(uint16_t Baud)
{
	BaudRate=Baud;
	
	//Make the ptr Tx_Head/Tail point to the start of the char array
	TX_Head=TX_Buffer;
	TX_Tail=TX_Buffer;
	
	//Make the ptr Rx_Head/Tail point to the start of the char array
	RX_Head=RX_Buffer;
	RX_Tail=RX_Buffer;
	
	INIT();
}
//==============================================//
void Uart::INIT()
{
	//16UL->unsigned Long: must be added in front of the value 16 to make the division correct
	uint16_t UBRR = ((*Fcpu) / (16UL * BaudRate)) - 1;
    UBRRH = (UBRR >> 8) ;
    UBRRL = UBRR;
	if(RXE)UCSRB|=(1<<RXEN);	//Enable RX
	if(TXE)UCSRB|=(1<<TXEN);	//Enable TX
	//if(TXIE)UCSRB|=(1<<UDRIE);	//Enable TX UDR empty Interrupts
	//if(RXIE)UCSRB|=(1<<RXCIE);	//Enable RX complete Interrupts
	UCSRC|=(1<<URSEL);			//selects UCSRC to change it's values
	UCSRC|=(1<<UCSZ1)|(1<<UCSZ0);//sets 8 bit data length
	UCSRC&=~(1<<UMSEL);			//Asynchronous Mode
}
//==============================================//
unsigned char Uart::read()								//receive data
{
	while(!(UCSRA &(1<<RXC)));						//while RXC  flag is clear wait for the response
	return(UDR);									//return the UDR data
}
//==============================================//
void Uart::print(uint8_t *data)							//send Data
{
	while(!(UCSRA &(1<<UDRE)));							//while UDRE  flag is clear
	UDR=*data;									//Fill UART Data register with data
	while(!(UCSRA &(1<<TXC)));
}
//==============================================//
void Uart::print(char data)							//send Data
{
	print((uint8_t *)&data);
}
//==============================================//
void  Uart::println(char *string,int value,PrintMode printType)
{
	Type=printType;
	println(string,value);
}
//==============================================//
void Uart::println(const char *string)
{
	//Convert constant char pointer to char pointer
	println((char *)string);
}
//==============================================//
void Uart::println(char *string)
{

	while(*string!='\0')
	{
		print((uint8_t *)string);
		string++;
	}
	print('\n');
	print('\r');
}
//==============================================//
void Uart::println(const char *string,int value)
{
	char data[10];
	char *dataPtr=data;
	itoa(value,data,Type);

	while(*string!=Null)
	{
		print((uint8_t *)string);
		string++;
	}
	
	while(*dataPtr!=Null)
	{
		print((uint8_t *)dataPtr);
		dataPtr++;
	}
	print((uint8_t *)'\r');
}



























































/*
//==============================================//
char Uart::read(){	
	
	//Create a temp char to return it
	volatile char temp;
	Next_RX_Tail=RX_Tail+1;
	if(Next_RX_Tail<(RX_Buffer+(sizeof(RX_Buffer)-1)))
	{
		temp=*RX_Tail;
	}
	else {Next_RX_Tail=RX_Buffer;}
	
	*RX_Tail='\0';
	RX_Tail=Next_RX_Tail;
	
	return temp;
}
//==============================================//
void Uart::print(char data)
{
	ATOMIC_BLOCK(ATOMIC_RESTORESTATE)
	{
		if (!isTransmitting )
		{
			Next_TX_Head=TX_Head+1;
			// Make sure that my pointer is still below the buffer maximum
			if (*TX_Head==Null)
			{
							if (!ptrOutofBound(Next_TX_Head))
							{
								*TX_Head=data;
								TX_Head=Next_TX_Head;
								Numofbytes--;
							}
							else{
								*TX_Head=data;
								Next_TX_Head=TX_Buffer;
								TX_Head=Next_TX_Head;
								Numofbytes--;
							}
			}
		}
	}
}
//==============================================//
void Uart::println(const char *string){
	
	ATOMIC_BLOCK(ATOMIC_RESTORESTATE)
	{
		if (!isTransmitting)
		{
			//memset((void *)TX_Buffer, '\0', sizeof(TX_Buffer));
			Numofbytes=strlen(string)+1;
			//TX_Head=TX_Buffer;
			while(*string!=Null)
			{
				print(*string);
				string++;
			}
			print('\r');	
			isready=true;
			Transmit=true;
			isTransmitting=true;
		}
	}
}
//==============================================//
void Uart::println(char string){
	
	ATOMIC_BLOCK(ATOMIC_RESTORESTATE)
	{
		if (!isTransmitting)
		{
			while(string!=Null)
			{
				print(string);
				string++;
			}
			print('\r');
			isready=true;
			Transmit=true;
			isTransmitting=true;
		}
	}
}
//======================================================================//
bool Uart::ptrOutofBound(volatile unsigned char *ptr){
	if (ptr>(TX_Buffer+(sizeof(TX_Buffer)-1)))return true;
	else return false;
}
//======================================================================//

//==============================================//
uint8_t Uart::available()
{	
	volatile unsigned char *tempPTR;
	tempPTR=RX_Tail;
	uint8_t i=0;
	while(*tempPTR!=Null)
	{tempPTR++;
		i++;
		}
	return (i);
}
//==============================================//
bool Uart::TX_buffer_full()
{
	// Check if the next position after head is equal to tail (buffer is full)
	 return (Next_TX_Head == TX_Tail || (Next_TX_Head == TX_Buffer + sizeof(TX_Buffer) && TX_Tail == TX_Buffer));
}
//==============================================//
void Uart::println(const char *string,float value)
{
	char data[10];
	char *dataPtr=data;
	dtostrf(value,3,3,data);
	
	while(*string!=Null)
	{
		print(*string);
		string++;
	}
	
	while(*dataPtr!=Null)
	{
		print(*dataPtr);
		dataPtr++;
	}
	print('\r');
}
//==============================================//
void Uart::println(const char *string,int value)
{
	char data[10];
	char *dataPtr=data;
	itoa(value,data,10);		
	ATOMIC_BLOCK(ATOMIC_RESTORESTATE)
	{
		if (!isTransmitting)
		{
			memset((void *)TX_Buffer, '\0', sizeof(TX_Buffer));
			TX_Head=TX_Buffer;
			while(*string!=Null)
			{
				print(*string);
				string++;
			}
			
			while(*dataPtr!=Null)
			{
				print(*dataPtr);
				dataPtr++;
			}
			print('\r');
			isready=true;
			Transmit=true;
			isTransmitting=true;
		}
	}
}

void Uart::println(char *string,double *value);*/
