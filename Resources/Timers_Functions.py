
from Resources import App_Functions
from Resources import GPIO_Functions
#================================================================================#
#                                   set Timmer                                   #
#================================================================================#
def setTimer(self):

    #Variables that have self will be stored accross the 
    #Entire Program so that they could be later used in restting the settings
    self.TimmerSetting = None                       #String to store all the timer settings
    self.TimmerSetting2 = None                      #String to store all the timer extra settings
    self.Interrupt_setting=None                     #String to store the interrupt Setting
    self.Interrupt_FunctionBlock1=None              #String to store the interrupt FunctionBlock
    self.Interrupt_FunctionBlock2=None              #String to store the interrupt FunctionBlock
    self.OCR_setting = None                         #Varibale to be used to store the OCR value
    self.Interrupt_LibCall=None                     #Varibale to be used to store the include of interrupt libarary

    #These variables are use only in this function
    self.TimerNum=self.Timer_Select.currentIndex()       #Variable used to add timer number to the timer setting ex(TCCR0)
    self.Timer_Mode=self.Timer_ModeSelect.currentText()  #Variable to store the timer Mode CTC/PWM
    self.ClockDev=self.Timer_PsSelect.currentText()      #Varibale to store the clock devision 
    Interrupt=self.Timer_Interrupt.currentText()         #Varibale to store the interrupt Setting
    InterruptVector=None                                 #String to store the interrupt vector
    output = None


   
    #Timmer Settings
    #These settings are as mentioned in the Data sheet
    Cs=[f"(1<<CS{ self.TimerNum}0)",f"(1<<CS{ self.TimerNum}1)",f"(1<<CS{ self.TimerNum}2)"]
    WGM=[f"(1<<WGM{ self.TimerNum}0)",f"(1<<WGM{ self.TimerNum}1)"]
    COM=[f"(1<<COM{ self.TimerNum}0)",f"(1<<COM{ self.TimerNum}1)",f"(1<<COM{ self.TimerNum}0)|(1<<COM{ self.TimerNum}1)"]

    #By default select thhe preScaler to none
    self.PreScaler = Cs[0]
    if  self.ClockDev == '8':
         self.PreScaler = Cs[1]
    elif  self.ClockDev == '32':
         self.PreScaler = Cs[0]+'|'+Cs[1]
    elif  self.ClockDev == '64':
        if  self.TimerNum == 2:
             self.PreScaler = Cs[2]
        else :
             self.PreScaler = Cs[0]+'|'+Cs[1]
    elif  self.ClockDev == '128':
         self.PreScaler = Cs[2]+'|'+Cs[0]
    elif  self.ClockDev == '256':
        if  self.TimerNum == 2:
             self.PreScaler = Cs[2]+'|'+Cs[1]
        else :
             self.PreScaler = Cs[2]  
    elif  self.ClockDev == '1024':
        if  self.TimerNum == 2:
             self.PreScaler = Cs[2]+'|'+Cs[1]+'|'+Cs[0]
        else :
             self.PreScaler = Cs[0]+'|'+Cs[2]  
        
    #This section only apply to the 8 bit timers ->Timer 0,2
    if  self.TimerNum == 0 or  self.TimerNum == 2:
        if "Norm" in self.Timer_Mode:
            self.TimmerSetting=(f"TCCR{ self.TimerNum}={ self.PreScaler};")  
        elif "CTC" in self.Timer_Mode:
            #If Output Pin is selected Configure the pin
            if 'OFF' not in self.Timer_Output.currentText():
                output=COM[self.Timer_Output.currentIndex()-1]
                self.TimmerSetting=(f"TCCR{ self.TimerNum}={WGM[1]}|{output}|{ self.PreScaler}")
                setTimerOutPiN(self, self.TimerNum)
            else:
                self.TimmerSetting=(f"TCCR{ self.TimerNum}={WGM[1]}|{ self.PreScaler}")  
        elif "FAST" in self.Timer_Mode:
            if 'OFF' not in self.Timer_PWMout.currentText():
                output=COM[self.Timer_PWMout.currentIndex()]
                self.TimmerSetting=(f"TCCR{ self.TimerNum}={WGM[0]}|{WGM[1]}|{output}|{ self.PreScaler}") 
                setTimerOutPiN( self.TimerNum)
            else:
                self.TimmerSetting=(f"TCCR{ self.TimerNum}={WGM[0]}|{WGM[1]}|{ self.PreScaler}") 
        elif "PWM" in self.Timer_Mode:
            if 'OFF' not in self.Timer_PWMout.currentText():
                output=COM[self.Timer_PWMout.currentIndex()]            
                self.TimmerSetting=(f"TCCR{ self.TimerNum}={WGM[0]}|{output}|{ self.PreScaler}")
                setTimerOutPiN( self.TimerNum)
            else :
                self.TimmerSetting=(f"TCCR{ self.TimerNum}={WGM[0]}|{output}|{ self.PreScaler}")

        #Add Timer Settings line
        App_Functions.addline(self,self.UserCodeSection_end,f"{self.TimmerSetting};\n")
        
        #Add Interrupt Register selection
        if "OFF" not in Interrupt:
            if "OVF"  in Interrupt:
                self.Interrupt_setting=f"TIMSK=(1<<TOIE{ self.TimerNum});\n"
                InterruptVector=f"TIMER{ self.TimerNum}_OVF"
            elif "COMP" in Interrupt:
                self.Interrupt_setting=f"TIMSK=(1<<OCIE{ self.TimerNum});\n"
                InterruptVector=f"TIMER{ self.TimerNum}_COMP"
            App_Functions.addline(self,self.UserInitSection_end,self.Interrupt_setting)
            #Add the Setting to the ISR
            self.Interrupt_FunctionBlock1=f"ISR({InterruptVector}_vect)\n"
            self.Interrupt_FunctionBlock2="{"+"/*Write your interrupt code here*/"+"}\n"
            self.Interrupt_LibCall=f"#include {self.Interrupt_LIB_Dirc}\n"
             
            App_Functions.addline(self,self.UserLIBsSection_end,self.Interrupt_LibCall)
            App_Functions.addline(self,self.UserISRSection_end,self.Interrupt_FunctionBlock1)
            App_Functions.addline(self,self.UserISRSection_end,self.Interrupt_FunctionBlock2)

        #Add OCR line
        self.OCR_setting=f"OCR{ self.TimerNum}={int(self.Tics)};\n"
        App_Functions.addline(self,self.UserCodeSection_end,self.OCR_setting)


    #To be later added support for 16Bit timer ,Timer 1 
    elif  self.TimerNum == 1 :
        SetTimer1(self)
#================================================================================#
#                              Reset ADC Pin  Channel                            #
#================================================================================#
def ResetTimer(self):
    pinNumber=self.PinSelection.currentIndex()
    RegisterName=self.RegSelection.currentText()
    cmd=f"HAL.GPIO->pinMode(HAL.GPIO->{RegisterName},{pinNumber},OUTPUT);\n"

    App_Functions.removeline(self,self.UserInitSection_Begin,"HAL.init(HAL.GPIO);")
    App_Functions.removeline(self,self.UserCodeSection_Begin,f"{self.TimmerSetting};\n")
    if(self.TimmerSetting2!=None):#Remove Settings two only if timer1 is selected
        App_Functions.removeline(self,self.UserCodeSection_Begin,f"{self.TimmerSetting2};\n")
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

   #Add CTC ICR option if timer 1 is selected and remove it if any other timer is selected
   #This bit of code added Here because this fucntion is called every time settings changed in timer tab
    if self.Timer_Select.currentIndex()==1 :
        #Add the ICR option
        if self.Timer_ModeSelect.findText("CTC(ICR)")<0:
            self.Timer_ModeSelect.addItem("CTC(ICR)")
            self.Timer_ModeSelect.addItem("PWM(ICR)")
            self.Timer_ModeSelect.addItem("PWM(OCR)")
    else :
        self.Timer_ModeSelect.removeItem(4)
        self.Timer_ModeSelect.removeItem(4)
        self.Timer_ModeSelect.removeItem(4)
    CS=[8,32,64,128,256,1024]

    if  "CTC" or "PWM" in Timer_Mode:
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
            #if timer 0,2 won't satisfy the timer required or Timer 1 is selected Calculate the Clock devsion
            if  TimerSelect == False or TimerNum == 1:
                self.Timer_Select.setCurrentIndex(1)
                for i in range(4):
                    self.Tics=(float(TimeInMills)*1000)/(CS[i]/16)
                    if self.Tics <65536:
                        break
                if ClockDev != (i+1):
                    self.Timer_PsSelect.setCurrentIndex(i+1)
    #Print Time in ms
    self.Timer_Ticbox.setPlainText(str(int(self.Tics)))
#================================================================================#
#                         Set Timer output pin                                   #
#================================================================================#
def setTimerOutPiN(self,Timer):

    #We assume none of the timer pins have been configured elsewhere
    if Timer == 0:
        self.RegSelection.setCurrentIndex(1)
        self.PinSelection.setCurrentIndex(3)
        self.ModeSelection.setCurrentIndex(0)
    elif Timer == 2:
        self.RegSelection.setCurrentIndex(3)
        self.PinSelection.setCurrentIndex(7)
        self.ModeSelection.setCurrentIndex(0)
    elif Timer == 1:
        #If timer 1 is select output pin to be something by default and it will be changed later
        #Timer 1 we have two output pins that's why we have to see if one 
        #of the pins is selected or not so that we could select the other 
        if self.Timer_Output2.currentText() =='A':
            self.RegSelection.setCurrentIndex(3)
            self.PinSelection.setCurrentIndex(5)
            self.ModeSelection.setCurrentIndex(0)

        elif self.Timer_Output2.currentText() =='B':
            self.RegSelection.setCurrentIndex(3)
            self.PinSelection.setCurrentIndex(4)
            self.ModeSelection.setCurrentIndex(0)


    Pin=App_Functions.Find_Pin(self,self.RegSelection.currentText(),self.PinSelection.currentIndex())

    #if the pin has not been configured we will set the pin
    if Pin.toolTip() =="":
        pinNumber=self.PinSelection.currentIndex()
        RegisterName=self.RegSelection.currentText()
        App_Functions.ChangeToolTip(self,None,App_Functions.Find_Pin(self,RegisterName,pinNumber),'Timer')

        #Do not define Hal init twice
        if "HAL.init(HAL.GPIO);\n" not in self.CodeViwer_m.toPlainText():
            App_Functions.addline(self,self.UserInitSection_end,"HAL.init(HAL.GPIO);\n")

        App_Functions.HighlightPin(self,RegisterName,pinNumber,'Timer')   
        cmd=f"HAL.GPIO->pinMode(HAL.GPIO->{RegisterName},{pinNumber},OUTPUT);\n"
        App_Functions.addline(self,self.UserCodeSection_end,cmd)
#================================================================================#
#                             Change Timer                                       #
#================================================================================#
def ChangeTimer(self):
    #Since timer 2 has two addtional prescaler Settings 
    #We enforce it's selection if these vales are selected 
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
#================================================================================#
#                         Set Timer 1  Settings                                  #
#================================================================================#
def SetTimer1(self):

    #Time 1 Registeres
    #TCCR1A=["WGM10","WGM11","FOC1B","FOC1A","COM1B0","COM1B1","COM1A0","COM1A1"]
    #TCCR1B=["CS10","CS11","CS12", "WGM12",WGM13","– ","ICES1","ICNC1"] 
    Interrupt=self.Timer_Interrupt.currentText()         #Varibale to store the interrupt Setting
    self.TimmerSetting=None                                   #Variable to store TCCR1A
    self.TimmerSetting2=None                                   #Variable to store TCCR1B

    
    Cs=[f"(1<<CS{self.TimerNum}0)",f"(1<<CS{self.TimerNum}1)",f"(1<<CS{self.TimerNum}2)"]
    WGM=[f"(1<<WGM{self.TimerNum}0)",f"(1<<WGM{self.TimerNum}1)",f"(1<<WGM{self.TimerNum}2)",f"(1<<WGM{self.TimerNum}3)"]
    COM=[f"(1<<COM{self.TimerNum}{self.Timer_Output2.currentText()}0)",f"(1<<COM{self.TimerNum}{self.Timer_Output2.currentText()}1)",f"(1<<COM{self.TimerNum}{self.Timer_Output2.currentText()}0)|(1<<COM{self.TimerNum}{self.Timer_Output2.currentText()}1)"]    
    
    
    # Timer/Counter Mode of Operation
    # Mode  | WGM13 | WGM12 | WGM11 | WGM10 | TimerMOde | TOP     | Update of OCR1x | TOV1 Flag Set on
    # -----------------------------------------------------------------------------------------------------------------------
    # 0     | 0     | 0     | 0      | 0     | Normal   | 0xFFFF  | Immediate     | MAX
    # 1     | 0     | 0     | 0      | 1     | PWM      | 8-bit   | TOP           | BOTTOM
    # 2     | 0     | 0     | 1      | 0     | PWM      | 9-bit   | TOP           | BOTTOM
    # 3     | 0     | 0     | 1      | 1     | PWM      | 10-bit  | TOP           | BOTTOM
    # 4     | 0     | 1     | 0      | 0     | CTC      | OCR1A   | Immediate     | MAX         
    # 5     | 0     | 1     | 0      | 1     | Fast PWM | 8-bit   | 0x00FF        | BOTTOM    
    # 6     | 0     | 1     | 1      | 0     | Fast PWM | 9-bit   | 0x01FF        | BOTTOM     
    # 7     | 0     | 1     | 1      | 1     | Fast PWM | 10-bit  | 0x03FF        | BOTTOM      
    # 8     | 1     | 0     | 0      | 0     | PWM      | ICR1    | BOTTOM        | BOTTOM        
    # 9     | 1     | 0     | 0      | 1     | PWM      | OCR1A   | BOTTOM        | BOTTOM       
    # 10    | 1     | 0     | 1      | 0     | PWM      | ICR1    | TOP           | BOTTOM       
    # 11    | 1     | 0     | 1      | 1     | PWM      | OCR1A   | TOP           | BOTTOM        
    # 12    | 1     | 1     | 0      | 0     | CTC      | ICR1    | Immediate     | MAX          
    # 13    | 1     | 1     | 0      | 1     | Reserved | –       | –             | –             
    # 14    | 1     | 1     | 1      | 0     | Fast PWM | ICR1    | BOTTOM        | TOP           
    # 15    | 1     | 1     | 1      | 1     | Fast PWM | OCR1A   | BOTTOM        | TOP           
    # ----------------------------------------------------------------------------------------------------------------------
    if "Norm" in self.Timer_Mode:
        #Normal Mode just select the Prescaler to enbale the timer
        self.TimmerSetting=(f"TCCR{self.TimerNum}B={self.PreScaler};")  
        self.TimmerSetting2="TCCR1A=0;"
    elif "CTC" in self.Timer_Mode:
        #If Output Pin is selected, Configure the pin
        if 'OFF' not in self.Timer_Output.currentText():
            output=COM[self.Timer_Output.currentIndex()-1]
            
            if "OCR" in self.Timer_Mode:
             self.TimmerSetting=(f"TCCR{self.TimerNum}B={WGM[2]}|{ self.PreScaler}")
             self.TimmerSetting2=(f"TCCR{self.TimerNum}A={output}")
            else:
             self.TimmerSetting=(f"TCCR{self.TimerNum}B={WGM[2]}|{WGM[3]}|{self.PreScaler}") 
             self.TimmerSetting2=(f"TCCR{self.TimerNum}A={output}")
            setTimerOutPiN(self, self.TimerNum)
        else:
            if "OCR" in self.Timer_Mode:
                self.TimmerSetting=(f"TCCR{self.TimerNum}B={WGM[2]}|{self.PreScaler}")
            else:
                self.TimmerSetting=(f"TCCR{self.TimerNum}B={WGM[2]}|{WGM[3]}|{self.PreScaler}") 
    elif "FAST" or "PWM(ICR)" or "PWM(OCR)" in self.Timer_Mode:
        #If Output Pin is selected , Configure the pin
        if 'OFF' not in self.Timer_Output.currentText():
            output=COM[self.Timer_Output.currentIndex()-1]
            
            if "OCR" in self.Timer_Mode:
             self.TimmerSetting=(f"TCCR{self.TimerNum}B={WGM[2]}|{WGM[3]}{self.PreScaler}")
             self.TimmerSetting2=(f"TCCR{self.TimerNum}A={WGM[0]}|{WGM[1]}|{output}")
            else:#ICR
             self.TimmerSetting=(f"TCCR{self.TimerNum}B={WGM[2]}|{WGM[3]}{self.PreScaler}")
             self.TimmerSetting2=(f"TCCR{self.TimerNum}A={WGM[1]}|{output}")
            setTimerOutPiN(self, self.TimerNum)
        else:
            if "OCR" in self.Timer_Mode:
                self.TimmerSetting=(f"TCCR{self.TimerNum}B={WGM[2]}|{WGM[3]}{self.PreScaler}")
                self.TimmerSetting2=(f"TCCR{self.TimerNum}A={WGM[0]}|{WGM[1]}")
            else:
                self.TimmerSetting=(f"TCCR{self.TimerNum}B={WGM[2]}|{WGM[3]}{self.PreScaler}")
                self.TimmerSetting2=(f"TCCR{self.TimerNum}A={WGM[1]}")
    """
    #PWM Mode should be added later
    elif "PWM" in self.Timer_Mode:
        if 'OFF' not in self.Timer_PWMout.currentText():
            output=COM[self.Timer_PWMout.currentIndex()]            
            self.TimmerSetting=(f"TCCR{self.TimerNum}B={WGM[0]}|{output}|{ self.PreScaler}")
            setTimerOutPiN( self.TimerNum)
        else :
            self.TimmerSetting=(f"TCCR{self.TimerNum}B={WGM[0]}|{output}|{ self.PreScaler}")
    """

    #Add Timer Settings line
    App_Functions.addline(self,self.UserCodeSection_end,f"{self.TimmerSetting};\n")
    App_Functions.addline(self,self.UserCodeSection_end,f"{self.TimmerSetting2};\n")
        
    """ 
    #Support for Interrupt should be added later
    #Add Interrupt Register selection
    if "OFF" not in Interrupt:
        if "OVF"  in Interrupt:
            self.Interrupt_setting=f"TIMSK=(1<<TOIE{self.TimerNum});\n"
            InterruptVector=f"TIMER{self.TimerNum}_OVF"
        elif "COMP" in Interrupt:
            self.Interrupt_setting=f"TIMSK=(1<<OCIE{self.TimerNum});\n"
            InterruptVector=f"TIMER{self.TimerNum}_COMP"
        App_Functions.addline(self,self.UserInitSection_end,self.Interrupt_setting)
        #Add the Setting to the ISR
        self.Interrupt_FunctionBlock1=f"ISR({InterruptVector}_vect)\n"
        self.Interrupt_FunctionBlock2="{"+"/*Write your interrupt code here*/"+"}\n"
        self.Interrupt_LibCall=f"#include {self.Interrupt_LIB_Dirc}\n"
    """    

    #if CTC is selected Add either the OCR config or the ICR config
    if "CTC" or "PWM" in self.Timer_Mode:
        if "OCR" in self.Timer_Mode:
            #Add OCR line
            self.OCR_setting=f"OCR{self.TimerNum}A={int(self.Tics)};\n"
            App_Functions.addline(self,self.UserCodeSection_end,self.OCR_setting)
        else :
            #Add OCR line
            self.OCR_setting=f"ICR{ self.TimerNum}={int(self.Tics)};\n"
            App_Functions.addline(self,self.UserCodeSection_end,self.OCR_setting)
#================================================================================#
#                         Add Timer 1  Settings                                  #
#================================================================================#            
def AddTimer1Settings(self):
    #Add CTC ICR option if timer 1 is selected and remove it if any other timer is selected
    #the added items are added to the comboboxes
    if self.Timer_Select.currentIndex()==1 and "OFF" not in self.Timer_Output.currentText():
        #Add the ICR option
        if self.Timer_ModeSelect.findText("CTC(ICR)")<0:
            self.Timer_ModeSelect.addItem("CTC(ICR)")
            self.Timer_ModeSelect.addItem("PWM(ICR)")
            self.Timer_ModeSelect.addItem("PWM(OCR)")
        #Enable output pin selection A,B
        self.Timer_Output2.setEnabled(True)
    else :
        self.Timer_ModeSelect.removeItem(6)
        self.Timer_ModeSelect.removeItem(5)
        self.Timer_ModeSelect.removeItem(4)
        self.Timer_Output2.setEnabled(False)