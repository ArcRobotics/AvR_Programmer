/*
 * Avr_Enums.h
 *
 * Created: 8/12/2023 5:08:06 PM
 *  Author: omar
 */ 


#ifndef AVR_ENUMS_H_
#define AVR_ENUMS_H_

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




#endif /* AVR_ENUMS_H_ */