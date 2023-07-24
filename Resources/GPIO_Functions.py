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
    remove_code_section(self.CodeViwer_m, self.UserDefineSection_Begin, self.UserDefineSection_end)
    remove_code_section(self.CodeViwer_m,self.UserInitSection_Begin,self.UserInitSection_end)
    remove_code_section(self.CodeViwer_m,self.UseCodeSection_Begin,self.UseCodeSection_end)
#================================================================================#
#                      Make a variable name with pin no                          #
#================================================================================#
def set_GPIO_PIN(self):
    cmd = None
    pinNumber=self.PinSelection.currentIndex()
    RegisterName=self.RegSelection.currentText()
    PinName=self.PinName.toPlainText()
    Mode=self.ModeSelection.currentText()

    cmd=f"HAL.GPIO->pinMode(HAL.GPIO->{RegisterName},{pinNumber},{Mode});\n"
    
    #if the Class pointer is not defined , define it
    if "HAL.init(HAL.GPIO);" not in self.CodeViwer_m.toPlainText():
        App_Functions.addline(self,self.UserInitSection_end,"HAL.init(HAL.GPIO);\n")

    if cmd not in self.CodeViwer_m.toPlainText():
        #if there is a varibale name
        if self.PinName.toPlainText() !="":
            App_Functions.addline(self,self.UserDefineSection,f"#define {PinName} {pinNumber}\n")
            cmd=f"HAL.GPIO->pinMode(HAL.GPIO->{RegisterName},{PinName},{Mode});\n"
            App_Functions.addline(self,self.UseCodeSection_end,cmd)

            App_Functions.HighlightPin(self,RegisterName,pinNumber,Mode)
            App_Functions.ChangeToolTip(self,PinName,App_Functions.Find_Pin(self,RegisterName,pinNumber),Mode)
        else:
            App_Functions.addline(self,self.UseCodeSection_end,cmd)

            App_Functions.HighlightPin(self,RegisterName,pinNumber,Mode)
            App_Functions.ChangeToolTip(self,None,App_Functions.Find_Pin(self,RegisterName,pinNumber),Mode)
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
        cursor.setPosition(end_position-22 + len(end_marker), QTextCursor.KeepAnchor)
        
        # Remove the selected code section
        cursor.removeSelectedText()

def ResetPin(self):
    pinNumber=self.PinSelection.currentIndex()
    RegisterName=self.RegSelection.currentText()
    Mode=self.ModeSelection.currentText()
    cmd=f"HAL.GPIO->pinMode(HAL.GPIO->{RegisterName},{pinNumber},{Mode});\n"
    if self.PinName.toPlainText() !="":
        App_Functions.removeline(self,self.UserInitSection_Begin,cmd)
        #App_Functions.ChangeToolTip(self,PinName,App_Functions.Find_Pin(self,RegisterName,pinNumber),Mode)
    else:
        App_Functions.removeline(self,self.UserInitSection_Begin,cmd)
        App_Functions.ChangeToolTip(self,None,App_Functions.Find_Pin(self,RegisterName,pinNumber),"RM")
        App_Functions.HighlightPin(self,RegisterName,pinNumber,"RM")
        