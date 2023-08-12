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
 * ADC_lib.h
 *
 * Created: 17/7/2023 6:03:23 PM
 *  Author: Omar
 */ 
#include "ADC_lib.h"

//=========================================================
void AdC::INIT(){
	//Enable ADC
	ADCSRA|=(1<<ADEN);
	ADMUX|=(1<<REFS0);
	PreS=*Fcpu/(200e3);	//Get a preScale value that satisfies the Range from 50KHz to 200KHz
	for(int8_t i=0;i<8;i++)
	{
		if (pow(2,i)>=PreS)
		{
			ADCSRA=ADCSRA|i;
			break;
		}
	}
	if (!TenBitMode)ADMUX|=(1<<ADLAR);
}
//=========================================================
float AdC::analogRead(uint8_t channel)
{
	//Voltage=channel;
	ADMUX=ADMUX&0xf0;
	ADMUX=ADMUX|channel;
	StartConversion();
	WaitforConversion();
	if(TenBitMode)ADC_ConversionValue=ADCL|ADCH<<8;
	else ADC_ConversionValue=ADCH;
	return ADC_ConversionValue;
}
//=========================================================
void AdC::setMode(uint8_t Mode)
{
	if(Mode==8)TenBitMode=false;
	else TenBitMode=true;
		
}
//=========================================================