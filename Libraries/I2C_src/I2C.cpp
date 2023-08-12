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

#include "I2C.h"

//========================================//
void I2C::INIT()
{
	//clear the TWSR
   TWSR = 0; // Clear the pre-scaler bits
   TWBR =(((*Fcpu) / (BAUD * 1000UL))-16UL) / 2UL;
   //TWCR |= (1 << TWEA); // Enable acknowledgment
   TWCR = (1 << TWEN); // Enable I2C
}
//========================================//
void I2C::Begin(uint8_t* slave_adress)
{
	_SlaveAdress=*slave_adress;
	TWCR = (1 << TWSTA) | (1 << TWEN) | (1 << TWINT);
	waitForTWI();		//Wait For ACK 0x08
	
	if(GetTWIF()!=ACK && GetTWIF()!=MT_SlA_ACK)Error();
}
//========================================//
void I2C::BeginSlave(uint8_t slave_adress)
{
	TWAR=slave_adress;	//Start	
}

//========================================//
void I2C::Write(uint8_t data)					//Write a byte of Data
{
	//Shift the slave address to the left by one as to add Write bit =0
	TWDR=_SlaveAdress<<1;		//Repeated Start with SLA+W
	clearTWIF();			//CLear TWI
	waitForTWI();			//Wait For ACK 0x18
	//if(GetTWIF()!=MT_SlA_ACK)Error();
	
	TWDR=data;				//Load The data to the TWDR
	clearTWIF();			//CLear TWI
	waitForTWI();			//Wait For ACK 0x28
	//if(GetTWIF()!=MT_DATA_ACK)Error();
}
//========================================//
char I2C::read(){
	
	TWDR=(_SlaveAdress<<1)|0x01;		//Repeated Start with SLA+R
	clearTWIF();			//CLear TWI
	waitForTWI();			//Wait For ACK 0x40 or 0x48 or 0x28
	if(GetTWIF()!=MR_SLA_ACK && GetTWIF()!=MR_SLA_NACK && GetTWIF()!=MT_DATA_ACK)Error();

	clearTWIF();			//CLear TWI
	waitForTWI();			//Wait For ACK 0x50 or 0x58
	if(GetTWIF()!=MR_DATA_ACK && GetTWIF()!=MR_DATA_NACK)Error();
	return(TWDR);
}
//========================================//
char I2C::readSlave(){
	clearTWIF();		//CLear 
	waitForTWI();		//Wait For ACK 0x80
	if (GetTWIF()!=0x80)return(Error());
	else return(TWDR);
}
//========================================//
void I2C::SendString(char* Data)
{
	int i=0;
	Write(&Data[i]);
	i++;
	while(Data[i]!='\0'){
		Begin(&_SlaveAdress);
		Write(&Data[i]);
		i++;
	}
}
//========================================//
char I2C::Error()
{
	return(GetTWIF());
}
//========================================//
void I2C::end()
{
	TWCR = (1 << TWSTO) | (1 << TWINT) | (1 << TWEN);
	while (TWCR & (1 << TWSTO));
}
//========================================//
void I2C::waitForTWI()
{
	while(!(TWCR&(1<<TWINT)));
}
//========================================//
void I2C::clearTWIF()
{
	TWCR=(1<<TWINT)|(1<<TWEN);
}
//========================================//
uint8_t I2C::GetTWIF()
{
	return(TWSR&0xF8);
}
//========================================//
bool I2C::available()
{
	clearTWIF();		//CLear TWI
	waitForTWI();		//Wait For ACK 0x80
	if(GetTWIF()!=0x60 && GetTWIF()!=0x80)return(false);
	else return(true);
}
//========================================//
void I2C::SendACK()
{
	TWCR |= (1 << TWEA);   // Send ACK (more data expected)
}
//========================================//
uint8_t I2C::Scan()
{
	for (uint8_t i=0;i<127;i++)
	{
		Begin(&i);
		TWDR=_SlaveAdress;		//Repeated Start with SLA+W
		clearTWIF();			//CLear TWI
		waitForTWI();			//Wait For ACK 0x18
		if(GetTWIF()==MT_SlA_ACK || GetTWIF()==ACK)
		{
			end();
			break;
		}
		end();
	}
	return (_SlaveAdress>>1);
}