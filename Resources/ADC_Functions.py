
from Resources import App_Functions
#================================================================================#
#                              set ADC Channel                                   #
#================================================================================#
def setChannel(self):
    cmd = None
    pinNumber=self.ADC_SelectChannel.currentIndex()
    RegisterName="RegA"
    self.RegSelection.setCurrentText(RegisterName)
    PinName=self.PinName_2.toPlainText()
    Mode="Analog"
    Line="HAL.init(HAL.adc);"
    if 'A' in RegisterName :
        #if the Class pointer is not defined , define it
        if Line not in self.CodeViwer_m.toPlainText():
            App_Functions.addline(self,self.UserInitSection_end,Line+'\n')
        if PinName !="":
            App_Functions.addline(self,self.UserDefineSection_end,f"#define {PinName} {pinNumber}\n")
            App_Functions.ChangeToolTip(self,PinName,App_Functions.Find_Pin(self,RegisterName,pinNumber),Mode)
            #clear the text box after setting the pin
            self.PinName_2.setPlainText("")
        else:   
            App_Functions.ChangeToolTip(self,None,App_Functions.Find_Pin(self,RegisterName,pinNumber),Mode)       
        App_Functions.HighlightPin(self,RegisterName,pinNumber,Mode)
            
#================================================================================#
#                              Reset ADC Pin  Channel                            #
#================================================================================#
def ResetADCPin(self):
    pinNumber=self.PinSelection.currentIndex()
    RegisterName=self.RegSelection.currentText()
    Mode=self.ModeSelection.currentText()
    cmd=f"HAL.GPIO->pinMode(HAL.GPIO->{RegisterName},{pinNumber},{Mode});\n"
    if self.SelectedPinName!="":
        cmd2=f"#define {self.SelectedPinName} {pinNumber}\n"
    App_Functions.removeline(self,self.UserInitSection_Begin,cmd)
    App_Functions.ChangeToolTip(self,None,App_Functions.Find_Pin(self,RegisterName,pinNumber),"RM")
    App_Functions.HighlightPin(self,RegisterName,pinNumber,"RM")
    App_Functions.removeline(self,self.UserDefineSection_Begin,cmd2)
    App_Functions.ResetVariableBox(self)
#================================================================================#
#                     Enable or disable ADC TAB  widgets                         #
#================================================================================#
def En_Dis(self):
    if self.ADC_checkBox.isChecked():
        Enable_Adc_Buttons(self)
    else:
        Disable_Adc_Buttons(self)
#================================================================================#
#                         Enable  ADC TAB  widgets                               #
#================================================================================#
def Enable_Adc_Buttons(self):
        self.ADC_setChannel.setEnabled(True)
        self.ADC_SelectChannel.setEnabled(True)
        self.ADC_ModeSelect.setEnabled(True)
        self.PinName_2.setEnabled(True)
        self.ReSetChannel.setEnabled(True)
#================================================================================#
#                         Disable  ADC TAB  widgets                              #
#================================================================================#
def Disable_Adc_Buttons(self):
        self.ADC_setChannel.setEnabled(False)
        self.ADC_SelectChannel.setEnabled(False)
        self.ADC_ModeSelect.setEnabled(False)
        self.PinName_2.setEnabled(False)
        self.ReSetChannel.setEnabled(False)