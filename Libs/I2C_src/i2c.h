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
 * i2c.h
 *
 * Created: 6/7/2023 4:01:23 PM
 *  Author: omar
 */ 


#ifndef I2C_H_
#define I2C_H_
#include <avr/io.h>


/************************************************************************/
/*						MASTER Transmitter MODE							*/
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
 * i2c.h
 *
 * Created: 6/7/2023 4:01:23 PM
 *  Author: omar
 */ 


#ifndef I2C_H_
#define I2C_H_
#include <avr/io.h>


/************************************************************************/
/*						MASTER Transmitter MODE							*/
>>>>>>> e0af3a95c7a0a2ae9d668fcb6b205505750c3c7c
/************************************************************************/
#define ACK 0x08			//Start
#define	MT_SlA_ACK 0x18		//SLA+W+ACK
#define MT_SLA_NACK 0x20	//SLA+W+NACK
#define MT_DATA_ACK 0x28	//Data Transmitted ACK
#define MT_DATA_NACK 0x30	//Data Transmitted NACk
<<<<<<< HEAD
/************************************************************************/
/*						MASTER Receiver MODE							*/
=======
/************************************************************************/
/*						MASTER Receiver MODE							*/
>>>>>>> e0af3a95c7a0a2ae9d668fcb6b205505750c3c7c
/************************************************************************/
#define MR_REP_STRT 0x10	//Repeated start
#define MR_ATT_LOST 0x38	//Attribution lost
#define MR_SLA_ACK 0x40		//SLA+R+ACK
#define MR_SLA_NACK 0x48	//SLA+R+NACK 
#define MR_DATA_ACK 0x50	//SLA+R+Data+ACK
#define MR_DATA_NACK 0x58	//SLA+R+Data+NACK
<<<<<<< HEAD
/************************************************************************/
/*						SLAVE TRANSMITTER MODE							*/
=======
/************************************************************************/
/*						SLAVE TRANSMITTER MODE							*/
>>>>>>> e0af3a95c7a0a2ae9d668fcb6b205505750c3c7c
/************************************************************************/
#define SLVR_ACK 0x60			//SLV+W ACK
#define SLV_NACK 0x68			//SLA+W NACK
#define	SLVR_RSTRT_ACK 0x80		//SLA+W ACK Repeated Start
#define	SLV_RSTRT_NACK 0x88		//SLA+W NACK Repeated Start
#define SLV_STOP 0xA0			//Stop condition
<<<<<<< HEAD
/************************************************************************/
/*						SLAVE RECIVER MODE								*/
=======
/************************************************************************/
/*						SLAVE RECIVER MODE								*/
>>>>>>> e0af3a95c7a0a2ae9d668fcb6b205505750c3c7c
/************************************************************************/
#define SLVW_ACK 0xA8			//SLV+R ACK
#define SLV_DATA_ACK 0x80		//Data Received

typedef uint8_t byte;
class I2C
{
	private:
	
	unsigned long *Fcpu;
	uint8_t GetTWIF();	//Return the TWI in The TSCR status code
	void waitForTWI();	//Wait for The TWI Flag to Be set
	void clearTWIF();	//Clear the TWI Flag
	char Error();	//Return the TWI in The TSCR status code
	public:
	byte _SlaveAdress;
	uint32_t BAUD;
	
	I2C(uint32_t BAUD_freq=100){
		BAUD=BAUD_freq;
	}
	void Begin(uint8_t* slave_adress);	//Begin Communication As a master
	void BeginSlave(uint8_t slave_adress);	//Begin Communication As a slave
	void Write(char* data);					//Write a byte of Data
	void Write(uint8_t data);		//Write a byte of Data
	void Write(int data){Write((uint8_t)data);};		//Write a byte of Data
	void SendString(char* Data);			//Send A string of Data
	char read();							//Reads a byte of data
	char readSlave();						//Reads a byte of data
	char readUntil(char Termnitnator);		//Reads a string of data
	bool available();	//Wait Until it's being addressed
	void end();			//End Wire transmission as a slave
	void SendACK();     //Send ACK if you want to receive more than one byte
	void SendNACK();     //Send NACK if you Don't want to receive more than one byte
	void setSlaveAddress(int8_t address){_SlaveAdress=(int8_t)address;}
	void setFreq(unsigned long *freq){Fcpu=freq;};
	uint8_t Scan();
	void INIT();			//Initialize the TWI Module
	void INIT(uint32_t freqKHZ){BAUD=freqKHZ;INIT();};			//Initialize the TWI Module

<<<<<<< HEAD
};

=======
};

>>>>>>> e0af3a95c7a0a2ae9d668fcb6b205505750c3c7c
#endif /* I2C_H_ */