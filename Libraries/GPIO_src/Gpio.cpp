/*
 * Gpio.cpp
 *
 * Created: 18/07/2023 15:34:38
 *  Author: omar
 */ 

#include "Gpio.h"

// Function to set the pin mode (INPUT or OUTPUT) for a specific pin on the port.
void IO::pinMode(const uint8_t* Register, uint8_t pin, GpIoMode mode)
{
    uint8_t* _Register = (uint8_t*)Register;

    // Check the mode and configure the pin accordingly.
    if (mode == OUTPUT)
    {
        // Set the corresponding bit (pin) in the Register to configure it as an OUTPUT.
        *_Register |= (1 << pin);
    }
    else
    {
        // Clear the corresponding bit (pin) in the Register to configure it as an INPUT.
        *_Register &= ~(1 << pin);
    }
}

//==================================================================//
// Overloaded digitalWrite function with bool state
// Calls the original digitalWrite function with HIGH or LOW state based on the bool value.
void IO::digitalWrite(const uint8_t* port, uint8_t pin, bool state)
{
    digitalWrite(port, pin, state ? HIGH : LOW);
}

//==================================================================//
// Function to write the state (HIGH or LOW) to a specific pin on the port.
void IO::digitalWrite(const uint8_t* port, uint8_t pin, GpIoState state)
{
    // Dereference the pointer (casted to uint8_t) to get the actual port address.
    uint8_t* _port = (uint8_t*)port;

    // Check the desired state and set or clear the corresponding bit (pin) in the port.
    if (state == HIGH)
    {
        *_port |= (1 << pin);   // Set the pin to HIGH.
    }
    else
    {
        *_port &= ~(1 << pin);  // Set the pin to LOW.
    }
}

//==================================================================//
// Function to read the state (HIGH or LOW) of a specific pin on the port.
bool IO::digitalRead(const uint8_t* port, uint8_t pin)
{
    // Dereference the pointer (casted to uint8_t) to get the actual port address.
    uint8_t* _port = (uint8_t*)port;

    // Check the state of the desired pin by reading the corresponding bit in the port.
    // If the bit is set (HIGH), return true. Otherwise, return false.
    if ((*_port & (1 << pin)))
    {
        return true;  // Pin is HIGH.
    }
    else
    {
        return false; // Pin is LOW.
    }
}
