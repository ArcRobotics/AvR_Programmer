from Resources import GPIO_Functions
from Resources import App_Functions

def GetActions(self):     
    self.Actions_dict.get("actionNew").triggered.connect(lambda:GPIO_Functions.NewIsClicked(self))
    self.Actions_dict.get("actionSaveAS").triggered.connect(lambda:App_Functions.SaveAsFile(self))
    self.Actions_dict.get("actionSave").triggered.connect(lambda:App_Functions.SaveFile(self))
    self.Actions_dict.get("actionOpen").triggered.connect(lambda:App_Functions.OpenFile(self))
    self.Actions_dict.get("actionExit").triggered.connect(self.close)
    self.Actions_dict.get("actionAbout").triggered.connect(lambda:self.OpenAbout_Screen())
    self.Actions_dict.get("actionView_C_Code").triggered.connect(lambda:self.OpenCode_Screen())