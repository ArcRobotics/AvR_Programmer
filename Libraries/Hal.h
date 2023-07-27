#ifndef Hal_H_
#define Hal_H_
#include <string.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <util/atomic.h>
#include "GPIO_src/Gpio.h"
#include "ADC_src/ADC_lib.h"
#include "I2C_src/i2c.h"
#include "UART_src/uart.h"





	
class hal:public I2C {

private:
unsigned long FCPU;
bool Disable_Int;	

AdC		_ADC;
I2C		_I2C;
IO		_GPIO;
Uart	_UART;
public:
	void init(AdC* classPointer);
	void init(I2C* classPointer);
	void init(IO* classPointer);
	void init(Uart* classPointer);
	inline void Enable_interrupts(){sei();};
	inline void Disable_interrupts(){cli();};
	inline void delay(double ms);
	inline void HAL_delay(double ms);
	void MCU_Freq(unsigned long Freq){FCPU=Freq;};
	
	
	AdC  *adc;//Pointer to adc class object
	I2C  *TWI;//point to I2C class object
	IO   *GPIO;//point to IO class object
	Uart *Serial;//point to Uart class object
	
	hal(bool Dis_Int=false){
		Disable_Int=Dis_Int;
		if (!Disable_Int)//To disable Interrupts Change the initialization to ->HAL(true) 
		{
			Enable_interrupts();
			
		adc=&_ADC;//Pointer to adc class object
		TWI=&_I2C;//point to I2C class object
		GPIO=&_GPIO;//point to IO class object
		Serial=&_UART;//point to Uart class object
		}
	}

}HAL(false);

//===========================================//
void hal::init(AdC* classPointer)
{
	adc=classPointer;
	adc->Fcpu=&FCPU;
	if(adc !=NULL){adc->INIT();}	
}
//===========================================//
void hal::init(I2C* classPointer)
{
	TWI=classPointer;
	if(TWI !=NULL){TWI->INIT();}
}
//===========================================//
void hal::init(IO* classPointer)
{
	GPIO=classPointer;
}
//===========================================//
void hal::init(Uart* classPointer)
{
	Serial=classPointer;
	Serial->Fcpu=&FCPU;
}
//===========================================//
inline void hal::delay(double ms){
	_delay_ms(ms);
}
//===========================================//
#endif /* HAL_H_ */

/*


		ISR(USART_RXC_vect)
		{
			//when data is received we should:
			// Store it in the buffer increment the Head
			//if the Head > buffer size make it go to zero
			//Make sure there is data received not equal null
			if (HAL.Serial->RX_Head<(HAL.Serial->RX_Buffer+(sizeof(HAL.Serial->RX_Buffer)-1)))
			{
				*HAL.Serial->RX_Head=UDR;
				HAL.Serial->RX_Head++;
			}
			else HAL.Serial->RX_Head=HAL.Serial->RX_Buffer;
		}
		ISR(USART_UDRE_vect)
		{
			ATOMIC_BLOCK(ATOMIC_RESTORESTATE)
			{
				if(HAL.Serial->Transmit==true)
				{
					HAL.Serial->Next_TX_Tail=HAL.Serial->TX_Tail+1;
					if (HAL.Serial->ptrOutofBound(HAL.Serial->Next_TX_Tail))
					{
						HAL.Serial->Next_TX_Tail=HAL.Serial->TX_Buffer;
					}
					
					if (*HAL.Serial->TX_Tail!='\0'){
						UDR=*HAL.Serial->TX_Tail;
						*HAL.Serial->TX_Tail='\0';
					}
					if (*HAL.Serial->Next_TX_Tail=='\0'&&((UCSRA&(1<<TXC))==0))
					{
						HAL.Serial->Transmit=false;
						HAL.Serial->isTransmitting=false;
					}
					HAL.Serial->TX_Tail=HAL.Serial->Next_TX_Tail;
					
				}
			}
		}


		if (HAL.Serial->isready && (HAL.Serial->Numofbytes==0||*HAL.Serial->Next_TX_Tail!=Null))
		{
			HAL.Serial->Transmitting=true;
			HAL.Serial->Next_TX_Tail= HAL.Serial->TX_Tail+1;
			if ( HAL.Serial->Next_TX_Tail<( HAL.Serial->TX_Buffer+(sizeof( HAL.Serial->TX_Buffer))))
			{
				//Don't throw garbage!
				//if(* TX_Tail!='\0')UDR=* TX_Tail;
				UDR=* HAL.Serial->TX_Tail;
			}
			else {
				HAL.Serial->Next_TX_Tail= HAL.Serial->TX_Buffer;
				//Don't throw garbage!
				//if(* Next_TX_Tail!='\0')UDR=* TX_Tail;
				UDR=* HAL.Serial->TX_Tail;
			}
			* HAL.Serial->TX_Tail='\0';
			if ( HAL.Serial->Next_TX_Tail==( HAL.Serial->TX_Head)) HAL.Serial->Next_TX_Tail= HAL.Serial->TX_Head;
			HAL.Serial->TX_Tail= HAL.Serial->Next_TX_Tail;
		}
		else {
			HAL.Serial->Transmitting=false;
			HAL.Serial->isready=false;
		}
	}
*/