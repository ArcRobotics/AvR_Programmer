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
#ifndef ADC_lib_H_
#define ADC_lib_H_

#include <avr/io.h>
#include <math.h>

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
	}
};

#endif /* INCFILE1_H_ */