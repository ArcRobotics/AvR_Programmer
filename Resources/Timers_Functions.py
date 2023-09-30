
from Resources import App_Functions
from Resources import GPIO_Functions
#================================================================================#
#                                   set Timmer                                   #
#================================================================================#
def setTimer(self):

    #Variables that have self will be stored accross the 
    #Entire Program so that they could be later used in restting the settings
    self.TimmerSetting = None                       #String to store all the timer settings
    self.Interrupt_setting=None                     #String to store the interrupt Setting
    self.Interrupt_FunctionBlock1=None              #String to store the interrupt FunctionBlock
    self.Interrupt_FunctionBlock2=None              #String to store the interrupt FunctionBlock
    self.OCR_setting = None                         #Varibale to be used to store the OCR value
    self.Interrupt_LibCall=None                     #Varibale to be used to store the include of interrupt libarary

    #These variables are use only in this function
    TimerNum=self.Timer_Select.currentIndex()       #Variable used to add timer number to the timer setting ex(TCCR0)
    Timer_Mode=self.Timer_ModeSelect.currentText()  #Variable to store the timer Mode CTC/PWM
    ClockDev=self.Timer_PsSelect.currentText()      #Varibale to store the clock devision 
    Interrupt=self.Timer_Interrupt.currentText()    #Varibale to store the interrupt Setting
    InterruptVector=None                       #String to store the interrupt vector
    output = None

   
    #Timmer Settings
    #These settings are as mentioned in the Data sheet
    Cs=[f"(1<<CS{TimerNum}0)",f"(1<<CS{TimerNum}1)",f"(1<<CS{TimerNum}2)"]
    WGM=[f"(1<<WGM{TimerNum}0)",f"(1<<WGM{TimerNum}1)"]
    COM=[f"(1<<COM{TimerNum}0)",f"(1<<COM{TimerNum}1)",f"(1<<COM{TimerNum}0)|(1<<COM{TimerNum}1)"]

    #By default select thhe preScaler to none
    PreScaler = Cs[0]
    if ClockDev == '8':
        PreScaler = Cs[1]
    elif ClockDev == '32':
        PreScaler = Cs[0]+'|'+Cs[1]
    elif ClockDev == '64':
        if TimerNum == 2:
            PreScaler = Cs[2]
        else :
            PreScaler = Cs[0]+'|'+Cs[1]
    elif ClockDev == '128':
        PreScaler = Cs[2]+'|'+Cs[0]
    elif ClockDev == '256':
        if TimerNum == 2:
            PreScaler = Cs[2]+'|'+Cs[1]
        else :
            PreScaler = Cs[2]  
    elif ClockDev == '1024':
        if TimerNum == 2:
            PreScaler = Cs[2]+'|'+Cs[1]+'|'+Cs[0]
        else :
            PreScaler = Cs[0]+'|'+Cs[2]  
        
    #This section only apply to the 8 bit timers ->Timer 0,2
    if TimerNum == 0 or TimerNum == 2:
        if "Norm" in Timer_Mode:
            self.TimmerSetting=(f"TCCR{TimerNum}={PreScaler};")  
        elif "CTC" in Timer_Mode:
            if 'OFF' not in self.Timer_Output.currentText():
                output=COM[self.Timer_Output.currentIndex()-1]
                self.TimmerSetting=(f"TCCR{TimerNum}={WGM[1]}|{output}|{PreScaler}")
                setTimerOutPiN(self,TimerNum)
            else:
                self.TimmerSetting=(f"TCCR{TimerNum}={WGM[1]}|{PreScaler}")  
        elif "FAST" in Timer_Mode:
            if 'OFF' not in self.Timer_PWMout.currentText():
                output=COM[self.Timer_PWMout.currentIndex()]
                self.TimmerSetting=(f"TCCR{TimerNum}={WGM[0]}|{WGM[1]}|{output}|{PreScaler}") 
                setTimerOutPiN(TimerNum)
            else:
                self.TimmerSetting=(f"TCCR{TimerNum}={WGM[0]}|{WGM[1]}|{PreScaler}") 
        elif "PWM" in Timer_Mode:
            if 'OFF' not in self.Timer_PWMout.currentText():
                output=COM[self.Timer_PWMout.currentIndex()]            
                self.TimmerSetting=(f"TCCR{TimerNum}={WGM[0]}|{output}|{PreScaler}")
                setTimerOutPiN(TimerNum)
            else :
                self.TimmerSetting=(f"TCCR{TimerNum}={WGM[0]}|{output}|{PreScaler}")

        #Add Timer Settings line
        App_Functions.addline(self,self.UserInitSection_end,f"{self.TimmerSetting};\n")
        
        #Add Interrupt Register selection
        if "OFF" not in Interrupt:
            if "OVF"  in Interrupt:
                self.Interrupt_setting=f"TIMSK=(1<<TOIE{TimerNum});\n"
                InterruptVector=f"TIMER{TimerNum}_OVF"
            elif "COMP" in Interrupt:
                self.Interrupt_setting=f"TIMSK=(1<<OCIE{TimerNum});\n"
                InterruptVector=f"TIMER{TimerNum}_COMP"
            App_Functions.addline(self,self.UserInitSection_end,self.Interrupt_setting)
            #Add the Setting to the ISR
            self.Interrupt_FunctionBlock1=f"ISR({InterruptVector}_vect)\n"
            self.Interrupt_FunctionBlock2="{"+"/*Write your interrupt code here*/"+"}\n"
            self.Interrupt_LibCall=f"#include {self.Interrupt_LIB_Dirc}\n"
             
            App_Functions.addline(self,self.UserLIBsSection_end,self.Interrupt_LibCall)
            App_Functions.addline(self,self.UserISRSection_end,self.Interrupt_FunctionBlock1)
            App_Functions.addline(self,self.UserISRSection_end,self.Interrupt_FunctionBlock2)


        #Add OCR line
        self.OCR_setting=f"OCR{TimerNum}={int(self.Tics)};\n"
        App_Functions.addline(self,self.UserCodeSection_end,self.OCR_setting)

    #To be later added support for 16Bit timer ,Timer 1 
    elif TimerNum == 1 :
        self.Timer_ModeSelect.addItems("CTC(OCR)")
#================================================================================#
#                              Reset ADC Pin  Channel                            #
#================================================================================#
def ResetTimer(self):
    pinNumber=self.PinSelection.currentIndex()
    RegisterName=self.RegSelection.currentText()
    cmd=f"HAL.GPIO->pinMode(HAL.GPIO->{RegisterName},{pinNumber},OUTPUT);\n"

    App_Functions.removeline(self,self.UserInitSection_Begin,"HAL.init(HAL.GPIO);")
    App_Functions.removeline(self,self.UserInitSection_Begin,f"{self.TimmerSetting};\n")
    App_Functions.removeline(self,self.UserCodeSection_Begin,self.OCR_setting)
    App_Functions.ChangeToolTip(self,None,App_Functions.Find_Pin(self,RegisterName,pinNumber),"RM")
    App_Functions.HighlightPin(self,RegisterName,pinNumber,"RM")
    App_Functions.removeline(self,self.UserDefineSection_Begin,cmd)

    #Remove the Interrupt Section
    App_Functions.removeline(self,self.UserLIBsSection_Begin,self.Interrupt_LibCall)
    App_Functions.removeline(self,self.UserInitSection_Begin,self.Interrupt_setting)
    App_Functions.removeline(self,self.UserInitSection_Begin,self.Interrupt_FunctionBlock1)
    App_Functions.removeline(self,self.UserInitSection_Begin,self.Interrupt_FunctionBlock2)
#================================================================================#
#                     Enable or disable Timer TAB  widgets                       #
#================================================================================#
def En_Dis(self):
    if self.Enable_Timer_checkBox.isChecked():
        Enable_Timer_Buttons(self)
    else:
        Disable_Timer_Buttons(self)
#================================================================================#
#                         Enable  Timer TAB  widgets                             #
#================================================================================#
def Enable_Timer_Buttons(self):
        self.Timer_Select.setEnabled(True)
        self.Timer_ModeSelect.setEnabled(True)
        self.Timer_PsSelect.setEnabled(True)
        self.Timer_Reset.setEnabled(True)
        self.Timer_Set.setEnabled(True)
        self.Timer_TriggerSec.setEnabled(True)
        self.Timer_Ticbox.setEnabled(True)
        self.Timer_Interrupt.setEnabled(True)
#================================================================================#
#                         Disable  Timer TAB  widgets                            #
#================================================================================#
def Disable_Timer_Buttons(self):
        self.Timer_Select.setEnabled(False)
        self.Timer_ModeSelect.setEnabled(False)
        self.Timer_PsSelect.setEnabled(False)
        self.Timer_Reset.setEnabled(False)
        self.Timer_Set.setEnabled(False)
        self.Timer_Output.setEnabled(False)
        self.Timer_PWMout.setEnabled(False)
        self.Timer_TriggerSec.setEnabled(False)
        self.Timer_Ticbox.setEnabled(False)
        self.Timer_Interrupt.setEnabled(False)
#================================================================================#
#                         Calculate Timer Trigegr                                #
#================================================================================#
def Calculate_Timer_Trigger(self):
    TimeInMills=self.Timer_TriggerSec.toPlainText()
    TimerNum=self.Timer_Select.currentIndex()
    Timer_Mode=self.Timer_ModeSelect.currentText()
    ClockDev=self.Timer_PsSelect.currentIndex()
    TimerSelect=True
    self.Tics=0
    CS=[8,32,64,128,256,1024]
    if  "CTC" in Timer_Mode:
        if TimeInMills!='' and float(TimeInMills) > 0 :
            if TimerNum == 0 or TimerNum == 2:
                for i in range(6):
                        if (i == 2 or i==3)and TimerNum == 0 :
                            continue
                        self.Tics=(float(TimeInMills)*1000)/(CS[i]/16)
                        if self.Tics < 256 :
                            TimerSelect=True
                            if ClockDev != (i+1):
                                self.Timer_PsSelect.setCurrentIndex(i+1)
                            break
                        elif self.Tics > 256 :
                            TimerSelect=False
            if  TimerSelect == False or TimerNum == 1:
                self.Timer_Select.setCurrentIndex(1)
                for i in range(4):
                    self.Tics=(float(TimeInMills)*1000)/(CS[i]/16)
                    if self.Tics <65536:
                        break
                if ClockDev != (i+1):
                    self.Timer_PsSelect.setCurrentIndex(i+1)

    self.Timer_Ticbox.setPlainText(str(int(self.Tics)))
#================================================================================#
#                         Set Timer output pin                                   #
#================================================================================#
def setTimerOutPiN(self,Timer):
    if Timer == 0:
        self.RegSelection.setCurrentIndex(1)
        self.PinSelection.setCurrentIndex(3)
        self.ModeSelection.setCurrentIndex(0)
    elif Timer == 2:
        self.RegSelection.setCurrentIndex(3)
        self.PinSelection.setCurrentIndex(7)
        self.ModeSelection.setCurrentIndex(0)

    pinNumber=self.PinSelection.currentIndex()
    RegisterName=self.RegSelection.currentText()
    App_Functions.ChangeToolTip(self,None,App_Functions.Find_Pin(self,RegisterName,pinNumber),'Timer')
    App_Functions.addline(self,self.UserInitSection_end,"HAL.init(HAL.GPIO);\n")
    App_Functions.HighlightPin(self,RegisterName,pinNumber,'Timer')   
    cmd=f"HAL.GPIO->pinMode(HAL.GPIO->{RegisterName},{pinNumber},OUTPUT);\n"
    App_Functions.addline(self,self.UserCodeSection_end,cmd)
#================================================================================#
#                         Set Timer output pin                                   #
#================================================================================#
def ChangeTimer(self):
    if self.Timer_PsSelect.currentIndex() == 2 or self.Timer_PsSelect.currentIndex()==4:
        self.Timer_Select.setCurrentIndex(2)
#================================================================================#
#                         En/Dis Timer output                                    #
#================================================================================#
def ChangeTimerOutput(self):
    if "CTC" in self.Timer_ModeSelect.currentText():
        self.Timer_Output.setEnabled(True)
        self.Timer_PWMout.setEnabled(False)
    elif "PWM" in self.Timer_ModeSelect.currentText():
        self.Timer_Output.setEnabled(False)
        self.Timer_PWMout.setEnabled(True)