
from PyQt4 import QtGui

import pyaudio 
import wave
import audioop
from collections import deque
import os
import time
import math
import GlobalVars
import copy
#from numpy import arange, sin, pi
#from numpy import histogram as hist
import pyqtgraph as pg

#import pyqtgraph.exporters




CHUNK = 1024 # CHUNKS of bytes to read each time from mic
FORMAT = pyaudio.paInt16 #this is the standard wav data format (16bit little endian)
#CHANNELS = 2# number of channels
RATE = 44100# sampling frequency
#THRESHOLD = 10500 # amplitude threshold
#SILENCE_LIMIT = 1 # amount of silence required to stop recording in seconds
#PREV_AUDIO = 0.5 # Previous audio (in seconds) to prepend
MIN_DUR=1 #minimum duration in seconds

MAX_DUR=30 #max dur in seconds

def RescanInputs():
    import GlobalVars

   
    inputdevices = 0
    
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    
    
    #for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
    for i in range (0,numdevices):
        if p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
            print "DevID ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name')
            inputdevices+=1

    GlobalVars.numdevices=inputdevices
    p.terminate()

def TriggeredRecordAudio(ui):

 import GlobalVars
 
 MIN_DUR=GlobalVars.buffertime*2+0.1;#
 #isRunning 

 threshold=GlobalVars.threshold;
 SILENCE_LIMIT = 2;
 PREV_AUDIO = GlobalVars.buffertime;

 p = pyaudio.PyAudio()

 if GlobalVars.Stereo:
        CHANNELS=2
 else:
        CHANNELS=1
#if not GlobalVars.Stereo:

        
    
 
 stream=p.open(format=FORMAT,input_device_index=GlobalVars.inputdeviceindex,channels=CHANNELS,rate=RATE,
               input=True,
               frames_per_buffer=CHUNK)

    
 ui.ListeningTextBox.setText('<span style="color:green">quiet</span>')
 audio2send = []
 #cur_data = '' # current chunk of audio data
 rel = RATE/CHUNK
 slid_win = deque(maxlen=SILENCE_LIMIT * rel) #amplitude threshold running buffer
 prev_audio = deque(maxlen=PREV_AUDIO * rel) #prepend audio running buffer
 perm_win = deque(maxlen=PREV_AUDIO*rel)
 started = False
 cur_data=stream.read(CHUNK)


 count=1;
 
 while (GlobalVars.isRunning==1):
  

  cur_data = stream.read(CHUNK)


  
  count=count+1
  if (count>20):
      count=0
      QtGui.qApp.processEvents()


  if (CHANNELS==2):
      
      left=audioop.tomono(cur_data,2,1,0)
      right=audioop.tomono(cur_data,2,0,1)

      if GlobalVars.ThreshChan=='left':
          thresh=left #audioop.tomono(cur_data,2,GlobalVars.ThreshChan,1)
      else:      
          thresh=right
          
      slid_win.append(audioop.rms(thresh, 2))
      #print str(audioop.rms(thresh,2))


  if (CHANNELS==1):      
      slid_win.append(audioop.rms(cur_data, 2))
      #print str(audioop.rms(cur_data, 2))


  ui.GraphWidget.clear();
  ui.GraphWidget.plot(slid_win);

    
  
  
  
  perm_win.append(cur_data)

  if(sum([x > threshold for x in slid_win])>0 and len(audio2send)<MAX_DUR*rel):    
   if(not started):
    ui.ListeningTextBox.setText('<span style="color:red">singing</span>')
    started = True
   audio2send.append(cur_data)
  elif (started is True and len(audio2send)>MIN_DUR*rel):
   print "Finished"
   filename = save_audio(list(prev_audio) + audio2send)
   started = False
   slid_win = deque(maxlen=SILENCE_LIMIT * rel)
   prev_audio = copy.copy(perm_win)
   ui.ListeningTextBox.setText('<span style="color:green">quiet</span>')
   audio2send=[]
  elif (started is True):
   ui.ListeningTextBox.setText('too short')
   started = False
   slid_win = deque(maxlen=SILENCE_LIMIT * rel)
   prev_audio = copy.copy(perm_win)
   audio2send=[]
   ui.ListeningTextBox.setText('<span style="color:green">quiet</span>')
  else:
   prev_audio.append(cur_data)
 print "done recording"
 stream.close()
 
 

 p.terminate()

def save_audio(data):
 import GlobalVars
    
 """ Saves mic data to  WAV file. Returns filename of saved
 file """
# filename = GlobalVars.path+'_'+str(int(time.time()))
 # writes data to WAV file
 T=time.localtime()
 outtime=str("%02d"%T[0])+str("%02d"%T[1])+str("%02d"%T[2])+str("%02d"%T[3])+str("%02d"%T[4])+str("%02d"%T[5])
 filename = GlobalVars.path+GlobalVars.filename+'_'+outtime
 
 data = ''.join(data)
 wf = wave.open(filename + '.wav', 'wb')
 wf.setnchannels(CHANNELS);
 wf.setsampwidth(2)
 wf.setframerate(RATE) 
 wf.writeframes(data)
 wf.close()
 return filename + '.wav'
 

##
##if(__name__ == '__main__'):
## audio_int()
## record_song()

