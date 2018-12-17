
import sys
from PyQt4.QtGui import QApplication,QDialog,QSizeGrip
from PyQt4 import QtCore, QtGui

##from PyRecordMenu import Ui_MainWindow
from Ui_MainWindow import Ui_MainWindow
from AudioRecorderFunctions import *
import GlobalVars



def RescanInputsButtonPushed():
    import GlobalVars    
    RescanInputs()    
    ui.InputSelectionSpinBox.setMinimum(0)
    ui.InputSelectionSpinBox.setMaximum(GlobalVars.numdevices)

  
def StopPushButton():   
    import GlobalVars
    GlobalVars.isRunning=0
    
    ui.StartPushButton.setEnabled(True)
    ui.RescanInputsPushButton.setEnabled(True)
    ui.ThresholdLineEdit.setEnabled(True)
    ui.BirdNameLineEdit.setEnabled(True)   
    ui.InputSelectionSpinBox.setEnabled(True)
    ui.WorkingDirpushButton.setEnabled(True)
    ui.BufferTimeSpinBox.setEnabled(True)    
    ui.ListeningTextBox.setText('')
    ui.radioButton.setEnabled(True);
    
    if not GlobalVars.Stereo:
        GlobalVars.ThreshChan=1             # Set Mono, trigger on only channel
        ui.radioButton_2.setEnabled(False)
        ui.radioButton_3.setEnabled(False)
    else:
        ui.radioButton_2.setEnabled(True)
        ui.radioButton_3.setEnabled(True)

def StartPushButton():
    import threading
    import GlobalVars
    
    ui.StartPushButton.setEnabled(False)
    ui.RescanInputsPushButton.setEnabled(False)
    ui.ThresholdLineEdit.setEnabled(False)
    ui.BirdNameLineEdit.setEnabled(False)
    ui.InputSelectionSpinBox.setEnabled(False)
    ui.WorkingDirpushButton.setEnabled(False)
    ui.BufferTimeSpinBox.setEnabled(False)
    ui.radioButton.setEnabled(False);
    ui.radioButton_2.setEnabled(False);
    ui.radioButton_3.setEnabled(False);    
    
    GlobalVars.isRunning=1
   # threading.Thread(target=TriggeredRecordAudio, args=arg1).start()
    TriggeredRecordAudio(ui)
    

def ThresholdLineEditChanged(newvalue):
    import GlobalVars
    GlobalVars.threshold=int(newvalue)

def radioButtonClicked():
      import GlobalVars
      print str(GlobalVars.ThreshChan)
      GlobalVars.Stereo= not GlobalVars.Stereo # Set stereo, trigger on L/R
      if not GlobalVars.Stereo:
          #GlobalVars.ThreshChan=          # Set Mono, trigger on only channel
          ui.radioButton_2.setEnabled(False)
          ui.radioButton_3.setEnabled(False)
      else:
          ui.radioButton_2.setEnabled(True)
          ui.radioButton_3.setEnabled(True)
          

def radioButton_2Clicked(): #left
      import GlobalVars
      GlobalVars.ThreshChan='left'

def radioButton_3Clicked(): #right
    import GlobalVars  
    GlobalVars.ThreshChan='right'

    
def BufferTimeSpinBoxChanged(newvalue):
    import GlobalVars
    GlobalVars.buffertime=int(newvalue)
    
def InputSelectionSpinBoxChanged(newvalue):
    import GlobalVars
    GlobalVars.inputdeviceindex=int(newvalue)
    p = pyaudio.PyAudio()
    print (p.get_device_info_by_host_api_device_index(0,newvalue).get('maxInputChannels'))
    
    if (p.get_device_info_by_host_api_device_index(0,newvalue).get('maxInputChannels'))>1:
        ui.radioButton.setEnabled(True)
    else:
        ui.radioButton.setEnabled(False);

    p.terminate
  
def BirdNameLineEditChanged(newvalue):
    import GlobalVars
    GlobalVars.filename=str(newvalue)

def WorkingDirpushButtonClicked():
    import os
    import GlobalVars
    
    dialog = QtGui.QFileDialog()
    dialog.setFileMode(QtGui.QFileDialog.Directory)
    dialog.setOption(QtGui.QFileDialog.ShowDirsOnly, True)
    
    directory = QtGui.QFileDialog.getExistingDirectory(dialog, 'Select Drive')
    directory = str(directory)
    print directory
    GlobalVars.path=directory+'/'


app = QApplication(sys.argv)
window = QDialog()
ui = Ui_MainWindow()
ui.setupUi(window)
GlobalVars.buffertime=1
GlobalVars.threshold=50
GlobalVars.filename='birdname'
GlobalVars.inputdeviceindex=0
GlobalVars.Stereo=False;
GlobalVars.ThreshChan='left'
GlobalVars.CHANNELS=1;



ui.RescanInputsPushButton.connect(ui.RescanInputsPushButton,
                                        QtCore.SIGNAL(("clicked()")),
                                        RescanInputsButtonPushed)

ui.StopPushButton.connect(ui.StopPushButton,
                                        QtCore.SIGNAL(("clicked()")),
                                        StopPushButton)

ui.StartPushButton.connect(ui.StartPushButton,
                                        QtCore.SIGNAL(("clicked()")),
                                        StartPushButton)

ui.ThresholdLineEdit.connect(ui.ThresholdLineEdit,
                                        QtCore.SIGNAL(("textChanged(QString)")),
                                        ThresholdLineEditChanged)

ui.BirdNameLineEdit.connect(ui.BirdNameLineEdit,
                                        QtCore.SIGNAL(("textChanged(QString)")),
                                        BirdNameLineEditChanged)
                                       
ui.BufferTimeSpinBox.connect(ui.BufferTimeSpinBox,
                                        QtCore.SIGNAL(("valueChanged(int)")),
                                        BufferTimeSpinBoxChanged) 

ui.InputSelectionSpinBox.connect(ui.InputSelectionSpinBox,
                                        QtCore.SIGNAL(("valueChanged(int)")),
                                        InputSelectionSpinBoxChanged)        

ui.WorkingDirpushButton.connect(ui.WorkingDirpushButton,
                                        QtCore.SIGNAL(("clicked()")),
                                        WorkingDirpushButtonClicked)
#
ui.radioButton.connect(ui.radioButton,
                                        QtCore.SIGNAL(("clicked()")),
                                        radioButtonClicked)
ui.radioButton_2.connect(ui.radioButton_2,
                                        QtCore.SIGNAL(("clicked()")),
                                        radioButton_2Clicked)
ui.radioButton_3.connect(ui.radioButton_3,
                                        QtCore.SIGNAL(("clicked()")),
                                        radioButton_3Clicked)

ui.radioButton_2.setEnabled(False)
ui.radioButton_3.setEnabled(False)

window.show()
sys.exit(app.exec_())


    


