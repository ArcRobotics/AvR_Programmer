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

#ifndef	LCD //if not defined
#define LCD //define LCD
#include "../I2C_src/i2c.h"
#include<avr/io.h>
#include<util/delay.h>
#include<stdlib.h>

// commands
#define LCD_CLEARDISPLAY 0x01
#define LCD_RETURNHOME 0x02
#define LCD_ENTRYMODESET 0x04
#define LCD_DISPLAYCONTROL 0x08
#define LCD_CURSORSHIFT 0x10
#define LCD_FUNCTIONSET 0x20
#define LCD_SETCGRAMADDR 0x40
#define LCD_SETDDRAMADDR 0x80

// flags for display entry mode
#define LCD_ENTRYRIGHT 0x00
#define LCD_ENTRYLEFT 0x02
#define LCD_ENTRYSHIFTINCREMENT 0x01
#define LCD_ENTRYSHIFTDECREMENT 0x00

// flags for display on/off control
#define LCD_DISPLAYON 0x04
#define LCD_DISPLAYOFF 0x00
#define LCD_CURSORON 0x02
#define LCD_CURSOROFF 0x00
#define LCD_BLINKON 0x01
#define LCD_BLINKOFF 0x00

// flags for display/cursor shift
#define LCD_DISPLAYMOVE 0x08
#define LCD_CURSORMOVE 0x00
#define LCD_MOVERIGHT 0x04
#define LCD_MOVELEFT 0x00

// flags for function set
#define LCD_8BITMODE 0x10
#define LCD_4BITMODE 0x00
#define LCD_2LINE 0x08
#define LCD_1LINE 0x00
#define LCD_5x10DOTS 0x04
#define LCD_5x8DOTS 0x00

// flags for backlight control
#define LCD_BACKLIGHT 0x08
#define LCD_NOBACKLIGHT 0x00
/*/================================================//

	LCD Pin Configuration:
	+---+---+---+---+---+---+---+---+
	| D7| D6| D5| D4| X | E |RW |RS |
	+---+---+---+---+---+---+---+---+
	|  7|  6|  5|  4|  3|  2|  1|  0|
	+---+---+---+---+---+---+---+---+
	This is the PCF connection
	
//================================================/*/

class lcd:public I2C{
	
	private:
		byte x_CUR;
		byte y_CUR;
		byte _LCD_Address;
		byte _backlightval;
		//char rowspos[2]={0,64};
	public:
		enum _Mode{
			CMD=0,
			DTA=1,
			_4bit=2,
		};
		 void init_lcd();	
		 void sendCMD(byte data);		
		 void print(byte data);			
		 void print(byte data,_Mode mode);
		 void println(char* ptr);
		 void noBacklight(void);
		 void Backlight(void);
		 void flash(byte data,_Mode mode);
		 void clear_lcd();
		 
		//compatibility API function aliases
		void blink_on();							// alias for blink()
		void blink_off();       					// alias for noBlink()
		void cursor_on();      	 					// alias for cursor()
		void cursor_off();      					// alias for noCursor()
		void load_custom_character(uint8_t char_num, uint8_t *rows);	// alias for createChar()
		void printstr(const char[]);
			 
	lcd(byte address){
		x_CUR=0;
		y_CUR=0;
		_backlightval= LCD_BACKLIGHT;
		_LCD_Address=address;
		init_lcd();

	}
};
#endif