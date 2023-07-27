/*
 * PCF8574.h
 *
 * Created: 7/26/2023 1:35:14 PM
 *  Author: omar
 */ 


#ifndef PCF8574_H_
#define PCF8574_H_

class I2COExpander{
	private:
	uint8_t  _PCFAddress;	//Default Slave Address
	int8_t pin;
	public:
	void setPin(uint8_t pinNum);
	void ClearPin(uint8_t Clear);
	void init();
	void init(int8_t address);
	void setAllPins();
	void ClearAllPins();
	bool readPin(uint8_t pinNum);
	I2COExpander()
	{
		_PCFAddress=0x40;	//Default Slave Address
		pin=0xFF;
	}
		

}IOexp;
//===============================================//
void I2COExpander::init(int8_t address)
{
	_PCFAddress=address;
}
//===============================================//
void I2COExpander::setPin(uint8_t pinNum)
{
	HAL.TWI->Begin(&_PCFAddress);
	pin|=(1<<pinNum);
	HAL.TWI->Write(pin);
	HAL.TWI->end();		
}
//===============================================//
void I2COExpander::ClearPin(uint8_t pinNum)
{	
	HAL.TWI->Begin(&_PCFAddress);
	pin&=~(1<<pinNum);
	HAL.TWI->Write(pin);
	HAL.TWI->end();		
}
//===============================================//
void I2COExpander::setAllPins()
{
	int8_t value=0xFF;
	HAL.TWI->Begin(&_PCFAddress);
	HAL.TWI->Write(value);
	HAL.TWI->end();		
}
//===============================================//
void I2COExpander::ClearAllPins()
{	
	int8_t value=0;
	HAL.TWI->Begin(&_PCFAddress);
	HAL.TWI->Write(value);
	HAL.TWI->end();	
}
//===============================================//
bool I2COExpander::readPin(uint8_t pinNum)
{
    _PCFAddress|=(1<<0);  //the write address + 1 ->0x41
	
    int8_t PinStatus = 0;
    uint8_t dataToSend = 0;
	
    dataToSend |= (1 << pinNum);  // Set the specific pin in the dataToSend variable
    HAL.TWI->Begin(&_PCFAddress);  // Begin I2C communication to read from the PCF8574
    HAL.TWI->Write(dataToSend);    // Send the data to the PCF8574 (the pin you want to read from)
    HAL.TWI->end();

    HAL.TWI->Begin(&_PCFAddress); // Begin I2C communication to read from the PCF8574 again
    PinStatus = HAL.TWI->read();   // Read the data from the PCF8574
    HAL.TWI->end();
	
	_PCFAddress&=~(1<<0);  //write address 0x40

    return (PinStatus & (1 << pinNum)) != 0;  // Check if the specific pin is HIGH or LOW and return the result
}

#endif /* PCF8574_H_ */