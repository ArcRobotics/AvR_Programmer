#define F_CPU 16000000UL
#include <avr/io.h>
#include "Hal.h"

/* USER Define BEGIN 1 */	
#define Led 0
/* USER Define END 1 */

int main(void)
{
HAL.MCU_Freq(F_CPU);

/* USER INIT BEGIN 1 */	
HAL.init(HAL.GPIO);
/* USER INIT END 1 */
	
/* USER CODE BEGIN 1 */
HAL.GPIO->pinMode(HAL.GPIO->RegB,Led,OUTPUT);
/* USER CODE END 1 */

while(1)
{
//Add you recurring code here
}

     return 0;
}#define F_CPU 16000000UL
#include <avr/io.h>
#include "Hal.h"
/* USER Define BEGIN 1 */
#define Led 0
/* USER Define END 1 */

int main(void)
{
	HAL.MCU_Freq(F_CPU);

	/* USER INIT BEGIN 1 */
	HAL.init(HAL.GPIO);
	/* USER INIT END 1 */
	
	/* USER CODE BEGIN 1 */
	HAL.GPIO->pinMode(HAL.GPIO->RegB,Led,OUTPUT);
	/* USER CODE END 1 */

	while(1)
	{
		HAL.GPIO->digitalWrite(HAL.GPIO->PortB,Led,HIGH);
		HAL.delay(500);
		
		HAL.GPIO->digitalWrite(HAL.GPIO->PortB,Led,LOW);
		HAL.delay(500);
	}

	return 0;
}
