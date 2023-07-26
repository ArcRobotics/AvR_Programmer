from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QTextCursor,QPixmap,QImage,QPalette,QColor,Qt

#================================================================================#
#                          Initilization Function                                #
#================================================================================#
def App_init(self):
    HideTab(self,"UART_TAB")
    HideTab(self,"SPI_TAB")
    HideTab(self,"I2C_TAB")
#================================================================================#
#                           ShowHideTabs Function                                #
#================================================================================#
def ShowHideTabs(self,checkBox):
    if checkBox.isChecked():
        #Enable_Adc_Buttons(self)
        if checkBox.objectName()=="UART_checkBox":
             showTab(self,"UART_TAB")
        elif checkBox.objectName()=="SPI_checkBox":
            showTab(self,"SPI_TAB")
        elif checkBox.objectName()=="I2C_checkBox":
            showTab(self,"I2C_TAB")
    else:
        if checkBox.objectName()=="UART_checkBox":
            HideTab(self,"UART_TAB")
        if checkBox.objectName()=="SPI_checkBox":
            HideTab(self,"SPI_TAB")
        if checkBox.objectName()=="I2C_checkBox":
            HideTab(self,"I2C_TAB")
#================================================================================#
#                              HideTab Function                                  #
#================================================================================#
def HideTab(self,TabName):
        # If the second tab is visible, remove it to hide it
        TabIndex=self.peripherals_Tab.indexOf(self.Tabs_dict.get(TabName))
        self.peripherals_Tab.removeTab(TabIndex)
#================================================================================#
#                              showTab Function                                  #
#================================================================================#
def showTab(self,TargetTab):
    TabIndex=self.peripherals_Tab.indexOf(self.Tabs_dict.get(TargetTab))
    TargetTab=self.Tabs_dict.get(TargetTab)
    TabName=TargetTab.objectName()
    TabName = TabName[:-4]
    self.peripherals_Tab.insertTab(TabIndex,TargetTab,TabName)
#================================================================================#
#                               SaveAs Function                                  #
#================================================================================#
def SaveFile(self):
    if self.filePath is not None:
        Code = self.CodeViwer_m.toPlainText()
        with open(self.filePath [0],'w') as File:
            File.write(Code)
    else:
        SaveAsFile(self)
#================================================================================#
#                               SaveAs Function                                  #
#================================================================================#
def SaveAsFile(self):
    File_path = QFileDialog.getSaveFileName(self,'Save Code','','C++ (*.cpp)')
    Code = self.CodeViwer_m.toPlainText()
    with open(File_path[0],'w') as File:
        File.write(Code)
#================================================================================#
#                            Open File Function                                  #
#================================================================================#
def OpenFile(self):
    self.filePath  = QFileDialog.getOpenFileName(self,'Open Code','','C++ (*.cpp)')
    with open(self.filePath [0],'r') as File:
        Code=File.read()
        Code = self.CodeViwer_m.setPlainText(Code)
        #File.write(Code)
#================================================================================#
#                           Add line between sections                            #
#================================================================================#
def addline(self,Section,cmd):
    text = self.CodeViwer_m.toPlainText()
    cursor = QTextCursor(self.CodeViwer_m.document())

    init_end_pos = text.find(Section)
    if init_end_pos != -1:
        cursor.setPosition(init_end_pos)
        self.CodeViwer_m.setTextCursor(cursor)
        self.CodeViwer_m.insertPlainText(cmd)
#================================================================================#
#                        Function to Heighlight Pins                             #
#================================================================================#
def HighlightPin(self,Reg,pinNum,Mode):

    pin=Find_Pin(self,Reg,pinNum) 
    if Mode =="OUTPUT":
        pin.setStyleSheet("QPushButton{background-color: rgb(85, 255, 0);\
            color: \
                rgb(255, 255, 255);};")
    elif Mode =="INPUT":
        pin.setStyleSheet("QPushButton{background-color: rgb(255, 255, 0);\
            color: \
                rgb(0, 0, 0);};")
    elif Mode =="Analog":
        pin.setStyleSheet("QPushButton{background-color: rgb(170, 0, 255);\
            color: \
                rgb(255, 255, 255);};")
    else:
        pin.setStyleSheet("")        
#================================================================================#
#                        Function to Heighlight Pins                             #
#================================================================================#
def Find_Pin(self,Reg,pinNum):
    pin = None
    if 'A' in Reg:
        pin=f"PA{pinNum}"
    elif 'B' in Reg:
        pin=f"PB{pinNum}"
    elif 'C' in Reg:
        pin=f"PC{pinNum}"
    elif 'D' in Reg:
        pin=f"PD{pinNum}"
    return getattr(self, pin)
#================================================================================#
#                       Function to Change tool tip                              #
#================================================================================#
def ChangeToolTip(self,VariableName,pin,Mode):
    if Mode=="RM":
        pin.setToolTip('')
    else:
        cmd =f"Register:{self.RegSelection.currentText()}\
    \nName:{VariableName}\
    \nPin:{self.PinSelection.currentIndex()}\
    \nMode:{Mode}"
        pin.setToolTip(cmd)
#================================================================================#
#                       Function to Change tool tip                              #
#================================================================================#
def invert_image_colors(label):
    pixmap = label.pixmap()
    if pixmap:
        image = pixmap.toImage()
        if not image.isNull():
            image.invertPixels(QImage.InvertRgb)
            inverted_pixmap = QPixmap.fromImage(image)
            label.setPixmap(inverted_pixmap)   
#================================================================================#
#                       Function to remove line                                  #
#================================================================================#
def removeline(self, Section, line_to_remove):
    cursor = QTextCursor(self.CodeViwer_m.document())

    if Section in self.CodeViwer_m.toPlainText():
        cursor.setPosition(self.CodeViwer_m.toPlainText().find(Section))
        cursor.movePosition(QTextCursor.StartOfBlock)

        while not cursor.atEnd():
            cursor.select(QTextCursor.LineUnderCursor)
            selected_text = cursor.selectedText().strip()

            if line_to_remove.strip() == selected_text:
                cursor.removeSelectedText()
                cursor.deletePreviousChar()  # Remove the extra newline character after the removed line
                cursor.movePosition(QTextCursor.PreviousBlock)  # Move cursor to the previous line
                self.CodeViwer_m.setTextCursor(cursor)
                return

            cursor.movePosition(QTextCursor.NextBlock)
#================================================================================#
#                        Function to Find Pin Name                               #
#================================================================================#
def FindSelectedPinName(self):        
    pinNumber=self.PinSelection.currentIndex()
    RegisterName=self.RegSelection.currentText()
    pin=Find_Pin(self,RegisterName,pinNumber)

    Mode_index = pin.toolTip().find("Mode:")
    if Mode_index != -1:
        # Extract the value after "Name:" until the end of the line
        line_end_index = pin.toolTip().find("\n", Mode_index)
        Mode = pin.toolTip()[Mode_index + len("Mode:"):line_end_index].strip()
        if Mode =="OUTPU":
            self.ModeSelection.setCurrentIndex(0)
        elif Mode=="INPU":
            self.ModeSelection.setCurrentIndex(1)


    # Check if "Name:" is in the tooltip
    name_index = pin.toolTip().find("Name:")
    if name_index != -1:
        # Extract the value after "Name:" until the end of the line
        line_end_index = pin.toolTip().find("\n", name_index)
        PinName = pin.toolTip()[name_index + len("Name:"):line_end_index].strip()
        if PinName.isdigit():
            self.PinName.setPlainText("")
        elif PinName=="None":
            self.PinName.setPlainText("")
        else:
            self.PinName.setPlainText(PinName)
            self.PinName_2.setPlainText(PinName)
            self.SelectedPinName=PinName
    else:
        ResetVariableBox(self)
#================================================================================#
#                           Function to clear Var Name box                       #
#================================================================================#
def ResetVariableBox(self):
    self.PinName.setPlainText("")
    self.PinName_2.setPlainText("")  

def setDarkMode(self):
    # Define dark mode colors
    dark_palette = QPalette()
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText,Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)