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
 *
 *
 * PCF8574.h
 *
 * Created: 7/26/2023 1:35:14 PM
 *  Author: omar
 */ 


#ifndef PCF8574_H_
#define PCF8574_H_
#include <util/delay.h>
#include "I2C_src/i2c.h"
#include "Avr_Enums.h"

class I2COExpander:public I2C {
	private:
	uint8_t  _PCFAddress;	//Default Slave Address
	int8_t pin;
	public:
	void digitalWrite(uint8_t pinNum,GpIoState state);
	void ClearPin(uint8_t Clear);
	void init(int8_t address,unsigned long freq);
	void init(int8_t address);
	void setAllPins();
	void ClearAllPins();
	bool digitalRead(uint8_t pinNum);

	I2COExpander()
	{
		_PCFAddress=0x20;	//Default Slave Address
		pin=0x00;
	}
}IOexp;
//===============================================//
void I2COExpander::init(int8_t address)
{
	INIT();
	_PCFAddress=address;
}
//===============================================//
void I2COExpander::init(int8_t address,unsigned long freq)
{
	INIT();
	_PCFAddress=address;
	setFreq(&freq);
}
//===============================================//
void I2COExpander::digitalWrite(uint8_t pinNum,GpIoState state)
{
	if (state==HIGH)
	{
		Begin(&_PCFAddress);
		pin|=(1<<pinNum);
		Write(pin);
		end();
	} 
	else if (state==LOW)
	{
			Begin(&_PCFAddress);
			pin&=~(1<<pinNum);
			Write(pin);
			end();
	}

}
//===============================================//
void I2COExpander::ClearPin(uint8_t pinNum)
{	

}
//===============================================//
void I2COExpander::setAllPins()
{
	int8_t value=0xFF;
	Begin(&_PCFAddress);
	Write(value);
	end();		
}
//===============================================//
void I2COExpander::ClearAllPins()
{	
	int8_t value=0;
	Begin(&_PCFAddress);
	Write(value);
	end();	
}
//===============================================//
bool I2COExpander::digitalRead(uint8_t pinNum)
{
    _PCFAddress|=(1<<0);  //the write address + 1 ->0x41
	
    int8_t PinStatus = 0;
    uint8_t dataToSend = 0;
	
    dataToSend |= (1 << pinNum);  // Set the specific pin in the dataToSend variable
    Begin(&_PCFAddress);  // Begin I2C communication to read from the PCF8574
    Write(dataToSend);    // Send the data to the PCF8574 (the pin you want to read from)
    end();

    Begin(&_PCFAddress); // Begin I2C communication to read from the PCF8574 again
    PinStatus = read();   // Read the data from the PCF8574
    end();
	
	_PCFAddress&=~(1<<0);  //write address 0x40

    return (PinStatus & (1 << pinNum)) != 0;  // Check if the specific pin is HIGH or LOW and return the result
}

#endif /* PCF8574_H_ */



/*
	HAL.GPIO->pinMode(HAL.GPIO->RegD,7,OUTPUT);

	HAL.GPIO->digitalWrite(HAL.GPIO->PortD,7,IOexp.readPin(6));
	_delay_ms(500);
	
	IOexp.ClearPin(0);
	_delay_ms(100);
	
	IOexp.setPin(0);
	_delay_ms(100);
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
 *
 *
 * PCF8574.h
 *
 * Created: 7/26/2023 1:35:14 PM
 *  Author: omar
 */ 


#ifndef PCF8574_H_
#define PCF8574_H_
#include <util/delay.h>
#include "I2C_src/i2c.h"
#include "Avr_Enums.h"

class I2COExpander:public I2C {
	private:
	uint8_t  _PCFAddress;	//Default Slave Address
	int8_t pin;
	public:
	void digitalWrite(uint8_t pinNum,GpIoState state);
	void ClearPin(uint8_t Clear);
	void init(int8_t address,unsigned long freq);
	void init(int8_t address);
	void setAllPins();
	void ClearAllPins();
	bool digitalRead(uint8_t pinNum);

	I2COExpander()
	{
		_PCFAddress=0x20;	//Default Slave Address
		pin=0x00;
	}
}IOexp;
//===============================================//
void I2COExpander::init(int8_t address)
{
	INIT();
	_PCFAddress=address;
}
//===============================================//
void I2COExpander::init(int8_t address,unsigned long freq)
{
	INIT();
	_PCFAddress=address;
	setFreq(&freq);
}
//===============================================//
void I2COExpander::digitalWrite(uint8_t pinNum,GpIoState state)
{
	if (state==HIGH)
	{
		Begin(&_PCFAddress);
		pin|=(1<<pinNum);
		Write(pin);
		end();
	} 
	else if (state==LOW)
	{
			Begin(&_PCFAddress);
			pin&=~(1<<pinNum);
			Write(pin);
			end();
	}

}
//===============================================//
void I2COExpander::ClearPin(uint8_t pinNum)
{	

}
//===============================================//
void I2COExpander::setAllPins()
{
	int8_t value=0xFF;
	Begin(&_PCFAddress);
	Write(value);
	end();		
}
//===============================================//
void I2COExpander::ClearAllPins()
{	
	int8_t value=0;
	Begin(&_PCFAddress);
	Write(value);
	end();	
}
//===============================================//
bool I2COExpander::digitalRead(uint8_t pinNum)
{
    _PCFAddress|=(1<<0);  //the write address + 1 ->0x41
	
    int8_t PinStatus = 0;
    uint8_t dataToSend = 0;
	
    dataToSend |= (1 << pinNum);  // Set the specific pin in the dataToSend variable
    Begin(&_PCFAddress);  // Begin I2C communication to read from the PCF8574
    Write(dataToSend);    // Send the data to the PCF8574 (the pin you want to read from)
    end();

    Begin(&_PCFAddress); // Begin I2C communication to read from the PCF8574 again
    PinStatus = read();   // Read the data from the PCF8574
    end();
	
	_PCFAddress&=~(1<<0);  //write address 0x40

    return (PinStatus & (1 << pinNum)) != 0;  // Check if the specific pin is HIGH or LOW and return the result
}

#endif /* PCF8574_H_ */



/*
	HAL.GPIO->pinMode(HAL.GPIO->RegD,7,OUTPUT);

	HAL.GPIO->digitalWrite(HAL.GPIO->PortD,7,IOexp.readPin(6));
	_delay_ms(500);
	
	IOexp.ClearPin(0);
	_delay_ms(100);
	
	IOexp.setPin(0);
	_delay_ms(100);
>>>>>>> e0af3a95c7a0a2ae9d668fcb6b205505750c3c7c
*/