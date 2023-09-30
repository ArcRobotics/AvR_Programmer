from PySide6.QtCore import QFile
from functools import partial
from Resources import App_Functions
from PySide6.QtGui import QTextCursor
#================================================================================#
#                        Get and set pin and ports                               #
#================================================================================#
def PinIscliked(self):
        #Create & Check Pin  variable with it's Name PA0....PA7
        for i in range(0, 8):
            Pin = f"PA{i}"
            if Pin is not None:
                setattr(self, Pin , self.Button_dict.get(Pin))
                #Connecy the pin B variable with the function setPin
                getattr(self, Pin).clicked.connect(partial(Set_GPIO_Parameter_tab,self,Pin))

        #Create & Check Pin  variable with it's Name PB0....PB7
        for i in range(0, 8):
            Pin = f"PB{i}"
            if Pin is not None:
                setattr(self, Pin , self.Button_dict.get(Pin))
                #Connecy the pin B variable with the function setPin
                getattr(self, Pin).clicked.connect(partial(Set_GPIO_Parameter_tab,self,Pin))

       
        #Create & Check Pin  variable with it's Name PC0....PC7
        for i in range(0, 8):
            Pin = f"PC{i}"
            if Pin is not None:
                setattr(self, Pin , self.Button_dict.get(Pin))
                #Connecy the pin B variable with the function setPin
                getattr(self, Pin).clicked.connect(partial(Set_GPIO_Parameter_tab,self,Pin))

        
        #Create & Check Pin  variable with it's Name PD0....PD7
        for i in range(0, 8):
            Pin = f"PD{i}"
            if Pin is not None:
                setattr(self, Pin , self.Button_dict.get(Pin))
                #Connecy the pin B variable with the function setPin
                getattr(self, Pin).clicked.connect(partial(Set_GPIO_Parameter_tab,self,Pin))
#================================================================================#
#                        Remove line between sections                            #
#================================================================================#
def NewIsClicked(self):
    self.filePath=None
    NewTexT = '''#define F_CPU 16000000UL
#include <avr/io.h>
#include "Libs/Hal.h"

/* USER Define BEGIN 1 */
/* USER Define END 1 */

int main(void)
{
HAL.MCU_Freq(F_CPU);

/* USER INIT BEGIN 1 */
/* USER INIT END 1 */

/* USER CODE BEGIN 1 */
/* USER CODE END 1 */

while(1)
{
    // Add your recurring code here
}

return 0;
}
    '''
    self.CodeViwer_m.setPlainText(NewTexT)
#================================================================================#
#                      Make a variable name with pin no                          #
#================================================================================#
def set_GPIO_PIN(self):
    cmd = None
    pinNumber=self.PinSelection.currentIndex()
    RegisterName=self.RegSelection.currentText()
    PinName=self.PinName.toPlainText()
    Mode=self.ModeSelection.currentText()
    Pin=App_Functions.Find_Pin(self,RegisterName,pinNumber)

    if Pin.toolTip() =="":
        cmd=f"HAL.GPIO->pinMode(HAL.GPIO->{RegisterName},{pinNumber},{Mode});\n"
        #if the Class pointer is not defined , define it
        if "HAL.init(HAL.GPIO);" not in self.CodeViwer_m.toPlainText():
            App_Functions.addline(self,self.UserInitSection_end,"HAL.init(HAL.GPIO);\n")

        if cmd not in self.CodeViwer_m.toPlainText():
            #if there is a varibale name
            if self.PinName.toPlainText() !="":
                App_Functions.addline(self,self.UserDefineSection_end,f"#define {PinName} {pinNumber}\n")
                cmd=f"HAL.GPIO->pinMode(HAL.GPIO->{RegisterName},{PinName},{Mode});\n"
                App_Functions.ChangeToolTip(self,PinName,App_Functions.Find_Pin(self,RegisterName,pinNumber),Mode)
                #clear the text box after setting the pin
                self.PinName.setPlainText("")
            else:
                App_Functions.ChangeToolTip(self,None,App_Functions.Find_Pin(self,RegisterName,pinNumber),Mode)
            App_Functions.addline(self,self.UserCodeSection_end,cmd)
            App_Functions.HighlightPin(self,RegisterName,pinNumber,Mode)               
#================================================================================#
#                        Sets the GPIO Tab parameters                            #
#================================================================================#
def Set_GPIO_Parameter_tab(self,cmd):  
    #find the {letter} in the cmd and make the selection accordingly
    if "A" in cmd:
        self.RegSelection.setCurrentIndex(0)
        self.ADC_SelectChannel.setCurrentIndex(int(cmd[2]))
    elif "B" in cmd:
        self.RegSelection.setCurrentIndex(1)
    elif "C" in cmd:
        self.RegSelection.setCurrentIndex(2)
    elif "D" in cmd:
        self.RegSelection.setCurrentIndex(3)

    self.PinSelection.setCurrentIndex(int(cmd[2]))
    self.SelectedPinName=None
    App_Functions.FindSelectedPinName(self)
#================================================================================#
#                        Remove line between sections                            #
#================================================================================#
def remove_code_section(plain_text_edit, start_marker, end_marker):
    # Get the first block (line) of the QPlainTextEdit
    block = plain_text_edit.document().firstBlock()
    
    # Initialize variables to keep track of the starting and ending positions
    start_position = None
    end_position = None
    
    # Find the positions of the start and end markers
    while block.isValid():
        text = block.text()
        if start_marker in text:
            start_position = block.position() + text.index(start_marker)
        elif end_marker in text:
            end_position = block.position() + text.index(end_marker)
        
        if start_position is not None and end_position is not None:
            break
        
        block = block.next()
    
    if start_position is not None and end_position is not None:
        # Get the text cursor and set the selection to the code section
        cursor = plain_text_edit.textCursor()
        cursor.setPosition(start_position+24)
        cursor.setPosition(end_position-23 + len(end_marker), QTextCursor.KeepAnchor)
        
        # Remove the selected code section
        cursor.removeSelectedText()
#================================================================================#
#                        Function to remove Pin Config                           #
#================================================================================#
def ResetPin(self):
    pinNumber=self.PinSelection.currentIndex()
    RegisterName=self.RegSelection.currentText()
    Mode=self.ModeSelection.currentText()
    cmd=f"HAL.GPIO->pinMode(HAL.GPIO->{RegisterName},{pinNumber},{Mode});\n"
    cmd2=f"#define {self.SelectedPinName} {pinNumber}\n"
    if self.PinName.toPlainText() !="":
        cmd=f"HAL.GPIO->pinMode(HAL.GPIO->{RegisterName},{self.PinName.toPlainText()},{Mode});\n"
    App_Functions.removeline(self,self.UserInitSection_Begin,cmd)
    App_Functions.ChangeToolTip(self,None,App_Functions.Find_Pin(self,RegisterName,pinNumber),"RM")
    App_Functions.HighlightPin(self,RegisterName,pinNumber,"RM")
    App_Functions.removeline(self,self.UserDefineSection_Begin,cmd2)
    App_Functions.ResetVariableBox(self)