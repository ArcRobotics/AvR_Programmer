#define F_CPU 16000000UL
#include <avr/io.h>
#include "Hal.h"
/* USER Define BEGIN 1 */
#define button 0
#define LED 0
/* USER Define END 1 */

int main(void)
{
	HAL.MCU_Freq(F_CPU);

	/* USER INIT BEGIN 1 */
	HAL.init(HAL.GPIO);
	/* USER INIT END 1 */
	
	/* USER CODE BEGIN 1 */
	HAL.GPIO->pinMode(HAL.GPIO->RegD,button,INPUT);
	HAL.GPIO->pinMode(HAL.GPIO->RegB,LED,OUTPUT);
	/* USER CODE END 1 */

	while(1)
	{
		HAL.GPIO->digitalWrite(HAL.GPIO->RegB,LED,HAL.GPIO->digitalRead(HAL.GPIO->RegD,button));	
	}

	return 0;
}
