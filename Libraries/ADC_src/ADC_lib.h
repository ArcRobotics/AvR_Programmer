#ifndef ADC_lib_H_
#define ADC_lib_H_

#include <avr/io.h>
#include <math.h>
/*
#ifndef F_CPU
# warning "F_CPU not defined"
# define F_CPU 1000000UL
#endif*/
//=========================================================
class AdC 
{
	private:
	//You cannot override these values
	int16_t ADC_ConversionValue;	//Store output Values here
	unsigned long PreS;
	unsigned long *Fcpu;
	bool Mode;
	bool TenBitMode;

	public:
	void StartConversion(){ADCSRA|=(1<<ADSC);};
	void WaitforConversion(){while(ADCSRA&(1<<ADSC));}
	void SelectChannel();
	void setMode(uint8_t Mode);
	void INIT();
	float analogRead(uint8_t channel);
	void setFreq(unsigned long *freq){Fcpu=freq;};
	
	AdC(bool RunningMode = true,bool Resloution= true)
	{
		Mode=RunningMode;
		TenBitMode=Resloution;
		INIT();
	}
};

#endif /* INCFILE1_H_ */