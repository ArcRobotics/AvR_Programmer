/*
 * LCD.cpp
 *
 * Created: 8/11/2023 4:30:05 PM
 *  Author: omar
 */ 
#include "LCD.h"
//================================================//
void lcd::init_lcd()
{
	Begin(&_LCD_Address);
	Write(0);
	end();
	_delay_ms(50);

	sendCMD(0x01); // clear display
	sendCMD(0x02); // back to home
	sendCMD(0x28); // 4bit,2line,5x7 pixel
	sendCMD(0x06); // entry mode,cursor increments by cursor shift
	sendCMD(0x0c); // display ON,cursor OFF
	sendCMD(0x80); // force cursor to begin at line1
}
//================================================//
void lcd::print(byte data,_Mode mode)
{
	uint8_t highnib=data&0xf0;
	uint8_t lownib=(data<<4)&0xf0;
	
	Begin(&_LCD_Address);
	Write(highnib|_backlightval);
	end();
	
	if (mode==_4bit)
	{
		flash((highnib|_backlightval),CMD);
	}
	else
	{
		flash((highnib|_backlightval),mode);
		
		Begin(&_LCD_Address);
		Write((lownib| _backlightval));
		end();
		
		flash((lownib| _backlightval),mode);
	}

}
//================================================//
void lcd::flash(byte data,_Mode mode)
{
	Begin(&_LCD_Address);
	if (mode==CMD) Write(data|0x04);
	else if(mode==DTA)Write(data|0x05);
	end();
	_delay_us(1);		// enable pulse must be >450ns

	Begin(&_LCD_Address);
	if (mode==CMD) Write(data&0xF0);
	else if(mode==DTA)Write(data|0x01);
	end();
	_delay_us(50);		// commands need > 37us to settle
}
//================================================//
void lcd::clear_lcd()
{
	sendCMD(0x01);
}
//================================================//
void lcd::sendCMD(byte data)
{
	print(data,CMD);
}
//================================================//
void lcd::print(byte data)
{
	print(data,DTA);
}
//================================================//
void lcd::println(char* ptr)
{
	while(*ptr!='\0')
	{
		print(*ptr);
		ptr++;
	}
}
//================================================//
void lcd::noBacklight(void)
{
	_backlightval=LCD_NOBACKLIGHT;
}
//================================================//
void lcd::Backlight(void)
{
	_backlightval=LCD_BACKLIGHT;
}