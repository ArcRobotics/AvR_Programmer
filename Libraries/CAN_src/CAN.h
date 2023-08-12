/*
 * CAN.h
 *
 * Created: 8/9/2023 1:22:37 AM
 *  Author: omar
 */ 


#ifndef CAN_H_
#define CAN_H_
/* USER Define END 1 */

//CAN 2.0A (standard CAN) CRC field is 15 bits long.
//CAN 2.0B (extended CAN) CRC field is 17 bits long.
class _CAN{
private:
	/*				
					Can Data packet structure
	| Identifier (ID) | RTR | Data Length Code (DLC) | Data |    CRC	 |
	|-----------------|-----|------------------------|------|------------|
	|     11 or 29    |  1  |         4 bits         | 0-8  |  15 or 17  |
															*/

public:

	_CAN(){
		Frame.CRC_POLYNOMIAL=0xC867;//
	}	
	typedef struct CAN_Frame{
		uint16_t ID;		//CAN ID 2 bytes
		uint8_t	DLC;		//Data Length Code num of data bytes
		uint8_t RTR;
		uint16_t CRC;
		uint16_t CRC_POLYNOMIAL;
		uint8_t *Data;		//Message that will be transmitted/received
	}_Frame;
	_Frame Frame;
		void CAN_send(CAN_Frame *DataPacket);
		void CAN_recive(CAN_Frame *DataPacket);
		uint16_t calculateCRC();// Function to calculate CRC-15 for a given data frame
		 
};
//========================================================================//
void _CAN::CAN_send(CAN_Frame *DataPacket)
{
	//Create a union to save Space
	union {
		uint8_t MSB;
		uint8_t LSB;
	};
	
	//Calculate the CRC and save it 
	Frame.CRC=calculateCRC();

	//Send ID
	MSB=Frame.ID>>8;
	HAL.Serial->print(&MSB);	//Send the ID MSB first
	LSB=Frame.ID & 0xFF;
	HAL.Serial->print(&LSB);	//Send the ID LSB first
	
	//Send RTR
	HAL.Serial->print(&Frame.RTR);	//Send the RTR
	
	
	//Send DLC
	HAL.Serial->print(&Frame.DLC);	//Send the DLC
	
	//Send DATA
	for (uint8_t i=0;i<Frame.DLC;i++)
	{	
		HAL.Serial->print(&Frame.Data[i]);	//Send the DATA
	}
	
	//Send CRC
	MSB=Frame.CRC>>8;
	HAL.Serial->print(&MSB);	//Send the CRC MSB first
	LSB=Frame.CRC & 0xFF;
	HAL.Serial->print(&LSB);	//Send the CRC LSB first
}
//========================================================================//
uint16_t _CAN::calculateCRC() {
	uint8_t* data=(uint8_t*)Frame.Data;
	uint16_t crc = 0xFFFF;
	//Note!
	//*data is the same as data[i]
	for (uint8_t i = 0; i < Frame.DLC; i++) {
		crc ^= (data[i] << 8);
		for (uint8_t j = 0; j < 8; j++) {
			crc = (crc & 0x8000) ? ((crc << 1) ^ Frame.CRC_POLYNOMIAL) : (crc << 1);
		}
	}

	return crc;
}




#endif /* CAN_H_ */



/*
 *		_CAN CAN;
 
 uint8_t data[]="1234";
 CAN.Frame.ID=0xFFA5;
 CAN.Frame.Data=data;
 CAN.Frame.DLC=4;
 */