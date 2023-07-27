#ifndef GPIO_H_
#define GPIO_H_

#include <avr/io.h>

enum GpIoMode
{
	INPUT,
	OUTPUT,
	TOGGLE,
};

enum GpIoState
{
	HIGH=1,
	LOW=0,
};


class IO{

public:
	void pinMode(const uint8_t *Register,uint8_t pin,GpIoMode mode);
	void digitalWrite(const uint8_t *port,uint8_t pin,GpIoState state);
	void digitalWrite(const uint8_t* port, uint8_t pin, bool state);
	bool digitalRead(const uint8_t *port,uint8_t pins);
	
		const uint8_t *RegA;//Address of DDRA
		const uint8_t *RegB;//Address of DDRB
		const uint8_t *RegC;//Address of DDRC
		const uint8_t *RegD;//Address of DDRD

		const uint8_t *PortA;//Address of PORTA
		const uint8_t *PortB;//Address of PORTB
		const uint8_t *PortC;//Address of PORTC
		const uint8_t *PortD;//Address of PORTD

		const uint8_t *PinA;//Address of PinA
		const uint8_t *PinB;//Address of PinB
		const uint8_t *PinC;//Address of PinC
		const uint8_t *PinD;//Address of PinD

    IO() {
	    RegA = (const uint8_t*)0x3A;
	    RegB = (const uint8_t*)0x37;
	    RegC = (const uint8_t*)0x34;
	    RegD = (const uint8_t*)0x31;

	    PortA = (const uint8_t*)0x3B;
	    PortB = (const uint8_t*)0x38;
	    PortC = (const uint8_t*)0x35;
	    PortD = (const uint8_t*)0x32;

		PinA = (const uint8_t*)0x39;
		PinB = (const uint8_t*)0x36;
		PinC = (const uint8_t*)0x33;
		PinD = (const uint8_t*)0x30;
    }

};



#endif /* GPIO_H_ */