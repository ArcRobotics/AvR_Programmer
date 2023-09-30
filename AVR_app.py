from PySide6.QtCore import (Qt,QFile,QSize)
from PySide6.QtGui import (QIcon, QColor, QPalette,QTextCursor,QKeySequence,QShortcut,QGuiApplication,QAction )
from PySide6.QtWidgets import (QApplication, QComboBox,QLabel,
    QLineEdit, QMainWindow, QPlainTextEdit, QProgressBar,
    QPushButton,QPushButton,QFileDialog,QDialog,QWidget,QVBoxLayout,QCheckBox,QTabWidget,QWidget)

QGuiApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

from PySide6.QtUiTools import QUiLoader
from functools import partial

from ICONS.rec import*
from Resources import GPIO_Functions
from Resources import ADC_Functions
from Resources import Timers_Functions
from Resources import App_Functions
from Resources import App_Actions
from Resources import App_CodeView
from Resources import AboutWindow
import sys



class AVRApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("Resources/AVR_GUI.ui")
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file)
        ui_file.close()
        self.MainWindow=QMainWindow()
        self.setFixedSize(700, 520)
        
        self.setWindowTitle("AVR Programmer")
        Logo=QIcon("ICONS/AppLogo.png")
        self.setWindowIcon(Logo)


        # Step 4: Check for any error messages or warnings
        if self.window is None:
            print("Error loading UI file!")

        
        # Set up the UI within the main window
        self.setCentralWidget(self.window)

        #Get all the buttons in the Application
        self.Buttons = self.findChildren(QPushButton)
        ComboBoxes=self.findChildren(QComboBox)
        self.checkBoxes=self.findChildren(QCheckBox)
        self.Tabs=self.findChildren(QWidget)
        # Create a dictionary of buttons with object names as keys
        self.Button_dict = {button.objectName(): button for button in self.Buttons}
        # Create a dictionary of ComboBoxes with object names as keys
        self.ComboBoxes_dict = {ComboBox.objectName(): ComboBox for ComboBox in ComboBoxes}
        # Create a dictionary of CheckBoxes with object names as keys
        self.CheckBoxes_dict = {checkBox.objectName(): checkBox for checkBox in self.checkBoxes}
        # Create a dictionary of Tabs with object names as keys
        self.Tabs_dict = {Tab.objectName(): Tab for Tab in self.Tabs}

        #Get all the buttons in the Application
        self.All_Actions = self.findChildren(QAction)
        # Create a dictionary of Actions with object names as keys
        self.Actions_dict = {AcTion.objectName(): AcTion for AcTion in self.All_Actions}

        #Create combo box / buttons / check box Variables with their crossponding names
        
        #================================================================================#
                            #Buttons
        #================================================================================#
        self.ADC_setChannel=self.Button_dict.get("ADC_setCh")
        self.setSerial=self.Button_dict.get("Set_UART_Para")        
        self.Set_I2C=self.Button_dict.get("Set_I2C") 
        self.Timer_Set=self.Button_dict.get("Timer_Set") 
        self.Timer_Reset=self.Button_dict.get("Timer_Reset") 
        self.ReSetGPIO=self.Button_dict.get("ReSetGPIO_2") 
        self.ReSetChannel=self.Button_dict.get("ReSetChannel") 
        self.CopyButton=self.Button_dict.get("copyButton") 
        #================================================================================#
                            #Check Boxes
        #================================================================================#
        self.ADC_checkBox=self.CheckBoxes_dict.get("ADC_checkBox")
        self.UART_checkBox=self.CheckBoxes_dict.get("UART_checkBox")
        self.SPI_checkBox=self.CheckBoxes_dict.get("SPI_checkBox")
        self.I2C_checkBox=self.CheckBoxes_dict.get("I2C_checkBox")
        self.Enable_Timer_checkBox=self.CheckBoxes_dict.get("Timer_checkBox")
        self.Enable_I2C_Slave_checkBox=self.ComboBoxes_dict.get("Enable_I2C_Slave_checkBox")
        #================================================================================#
                            #ComboBoxes Boxes
        #================================================================================#
        self.ADC_SelectChannel=self.ComboBoxes_dict.get("ADC_chSelect")
        self.ADC_ModeSelect=self.ComboBoxes_dict.get("ADC_ModeSelect")
        self.RegSelection=self.ComboBoxes_dict.get("comboBox_2")
        self.PinSelection=self.ComboBoxes_dict.get("comboBox_3")
        self.ModeSelection=self.ComboBoxes_dict.get("comboBox")
        self.BaudSelect=self.ComboBoxes_dict.get("BaudSelect")
        self.Timer_Select=self.ComboBoxes_dict.get("Timer_Select")
        self.Timer_ModeSelect=self.ComboBoxes_dict.get("Timer_ModeSelect")
        self.Timer_PsSelect=self.ComboBoxes_dict.get("Timer_PsSelect")
        self.Timer_Output=self.ComboBoxes_dict.get("Timer_Output")
        self.Timer_PWMout=self.ComboBoxes_dict.get("Timer_PWMout")
        self.Timer_Interrupt=self.ComboBoxes_dict.get("Interrupt_Type")
        #================================================================================#
                            #PlainTextEdit 
        #================================================================================#
        self.CodeViwer_m=self.findChild(QPlainTextEdit,"CodeViwer_m")
        self.PinName=self.findChild(QPlainTextEdit,"PinName") 
        self.PinName_2=self.findChild(QPlainTextEdit,"PinName_2")
        self.SlaveAddress=self.findChild(QPlainTextEdit,"SlaveAddress")
        self.Timer_TriggerSec=self.findChild(QPlainTextEdit,"Timer_TriggerSec")
        self.Timer_Ticbox=self.findChild(QPlainTextEdit,"Timer_Ticbox")

        #Get the main Tab object Name
        self.peripherals_Tab=self.Tabs_dict.get("peripherals_Tab")


        App_Functions.App_init(self)
        GPIO_Functions.PinIscliked(self)
        App_Actions.GetActions(self)
        
        #pyinstaller --name=AVR_app --onefile AVR_app.py
        #pyinstaller myapp.spec

        self.filePath=None

        
        self.UserDefineSection_Begin="/* USER Define BEGIN 1 */"
        self.UserInitSection_Begin="/* USER INIT BEGIN 1 */"	
        self.UserCodeSection_Begin="/* USER CODE BEGIN 1 */"
        self.UserISRSection_Begin="/* USER ISR BEGIN 1 */"

        self.UserDefineSection_end="/* USER Define END 1 */"
        self.UserInitSection_end="/* USER INIT END 1 */"	
        self.UserCodeSection_end="/* USER CODE END 1 */"
        self.UserISRSection_end="/* USER ISR END 1 */"

        #Store All libaries Directories HERE
        self.HAL_LIB_Dirc="Libs/Hal.h"
        self.LCD_LIB_Dirc="Libs/LCD_src/Hal.h"
        self.HAL_LIB_Dirc="Libs/PCF8574.h"


        #By default disable all ADC content until enable is clicked
        self.ADC_checkBox.clicked.connect(lambda:ADC_Functions.En_Dis(self))
        self.Enable_Timer_checkBox.clicked.connect(lambda:Timers_Functions.En_Dis(self))
        #By default disable Hide all coms content until enable is clicked
        self.UART_checkBox.clicked.connect(lambda:App_Functions.ShowHideTabs(self,self.UART_checkBox))
        self.I2C_checkBox.clicked.connect(lambda:App_Functions.ShowHideTabs(self,self.I2C_checkBox))
        self.SPI_checkBox.clicked.connect(lambda:App_Functions.ShowHideTabs(self,self.SPI_checkBox))

        
        self.setGpioB=self.Button_dict.get("SetGPIO")
        self.setGpioB.clicked.connect(lambda:GPIO_Functions.set_GPIO_PIN(self))
        self.ADC_setChannel.clicked.connect(lambda:ADC_Functions.setChannel(self))
        self.Timer_Set.clicked.connect(lambda:Timers_Functions.setTimer(self))
        self.Timer_Reset.clicked.connect(lambda:Timers_Functions.ResetTimer(self))
        self.setSerial.clicked.connect(lambda:self.SetSerial())
        self.Set_I2C.clicked.connect(lambda:self.SetTWI())
        self.ReSetGPIO.clicked.connect(lambda:GPIO_Functions.ResetPin(self))
        self.ReSetChannel.clicked.connect(lambda:ADC_Functions.ResetADCPin(self))
        self.Timer_TriggerSec.textChanged.connect(lambda:Timers_Functions.Calculate_Timer_Trigger(self))
        self.Timer_PsSelect.currentIndexChanged.connect(lambda:Timers_Functions.ChangeTimer(self))
        self.Timer_Select.currentIndexChanged.connect(lambda:Timers_Functions.Calculate_Timer_Trigger(self))
        self.Timer_ModeSelect.currentIndexChanged.connect(lambda:Timers_Functions.ChangeTimerOutput(self))
        self.CopyButton.clicked.connect(lambda:App_Functions.copy_text_to_clipboard(self,self.CodeViwer_m.toPlainText()))

        #x=QCheckBox()
        #x.isChecked
        
        #self.xlable=self.findChild(QLabel,"label")
        #App_Functions.invert_image_colors(self.xlable)


        # Apply dark mode colors to the application
        #Soon........!
        
        #self.dark_palette=None
        #App_Functions.setDarkMode(self)
        #self.setPalette(self.dark_palette)   


    def SetSerial(self):
        Line="HAL.init(HAL.Serial);"
        Line2=f"HAL.Serial->Begin({self.BaudSelect.currentText()});"
        if Line not in self.CodeViwer_m.toPlainText():
            App_Functions.addline(self,self.UserInitSection_end,Line+'\n')
            App_Functions.addline(self,self.UserInitSection_end,Line2+'\n')

    def SetTWI(self):
        Line="HAL.init(HAL.TWI);"
        if Line not in self.CodeViwer_m.toPlainText():
            App_Functions.addline(self,self.UserInitSection_end,Line+'\n')

    def OpenAbout_Screen(self):
        self.HelpScreen = AboutWindow.About_Dialog()
        self.HelpScreen.setupUi(self.HelpScreen)  # Call setupUi to set up the UI components
        self.HelpScreen.show()

    def OpenCode_Screen(self):
        CodeScreen=App_CodeView.CodeView_Window(self.MainWindow,self.CodeViwer_m.toPlainText())
        CodeScreen.show()
        CodeScreen.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Main_window = AVRApp()
    Main_window.show()
    sys.exit(app.exec())
