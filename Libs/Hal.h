<<<<<<< HEAD
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
#ifndef Hal_H_
#define Hal_H_
#ifndef io_H_
	#include <avr/io.h>
#endif

#ifndef delay_H_
	#include <util/delay.h>
#endif

#ifdef DEBUG
	#warning "You are running debug mode"
#endif // _DEBUG

#include <string.h>
#include <avr/interrupt.h>
#include <util/atomic.h>
#include "GPIO_src/Gpio.h"
#include "ADC_src/ADC_lib.h"
#include "I2C_src/i2c.h"
#include "UART_src/uart.h"



typedef uint8_t byte;

	
=======
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
#ifndef Hal_H_
#define Hal_H_
#ifndef io_H_
	#include <avr/io.h>
#endif

#ifndef delay_H_
	#include <util/delay.h>
#endif

#ifdef DEBUG
	#warning "You are running debug mode"
#endif // _DEBUG

#include <string.h>
#include <avr/interrupt.h>
#include <util/atomic.h>
#include "GPIO_src/Gpio.h"
#include "ADC_src/ADC_lib.h"
#include "I2C_src/i2c.h"
#include "UART_src/uart.h"



typedef uint8_t byte;

	
>>>>>>> e0af3a95c7a0a2ae9d668fcb6b205505750c3c7c
class hal:public I2C {

private:
unsigned long FCPU;
bool Disable_Int;	

AdC		_ADC;
<<<<<<< HEAD
I2C		_I2C;
IO		_GPIO;
=======
I2C		_I2C;
IO		_GPIO;
>>>>>>> e0af3a95c7a0a2ae9d668fcb6b205505750c3c7c
Uart	_UART;
public:
	void init(AdC* classPointer);
	void init(I2C* classPointer);
	void init(I2C* classPointer,uint32_t Freq);
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
<<<<<<< HEAD
		if (!Disable_Int)//To disable Interrupts Change the initialization to ->HAL(true) 
		{
			Enable_interrupts();		
=======
		if (!Disable_Int)//To disable Interrupts Change the initialization to ->HAL(true) 
		{
			Enable_interrupts();		
>>>>>>> e0af3a95c7a0a2ae9d668fcb6b205505750c3c7c
		}
		adc=&_ADC;//Pointer to adc class object
		TWI=&_I2C;//point to I2C class object
		GPIO=&_GPIO;//point to IO class object
		Serial=&_UART;//point to Uart class object
	}

}HAL(false);
<<<<<<< HEAD

//===========================================//
void hal::init(AdC* classPointer)
{
	adc=classPointer;
	adc->setFreq(&FCPU);
	if(adc !=NULL){adc->INIT();}	
}
//===========================================//
void hal::init(I2C* classPointer,uint32_t Freq)
{
	TWI=classPointer;
	TWI->setFreq(&FCPU);
	if(TWI !=NULL){TWI->INIT(Freq);}
}
//===========================================//
void hal::init(I2C* classPointer)
{
	TWI=classPointer;
	TWI->setFreq(&FCPU);
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
=======

//===========================================//
void hal::init(AdC* classPointer)
{
	adc=classPointer;
	adc->setFreq(&FCPU);
	if(adc !=NULL){adc->INIT();}	
}
//===========================================//
void hal::init(I2C* classPointer,uint32_t Freq)
{
	TWI=classPointer;
	TWI->setFreq(&FCPU);
	if(TWI !=NULL){TWI->INIT(Freq);}
}
//===========================================//
void hal::init(I2C* classPointer)
{
	TWI=classPointer;
	TWI->setFreq(&FCPU);
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
>>>>>>> e0af3a95c7a0a2ae9d668fcb6b205505750c3c7c
#endif /* HAL_H_ */