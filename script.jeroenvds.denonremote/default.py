import xbmc
import telnetlib
import time
import xbmcaddon
import json

__addon__ = xbmcaddon.Addon(id='script.jeroenvds.denonremote')

def turnOnDenon():
	tn = telnetlib.Telnet(__addon__.getSetting("denonip"))
	tn.write("PWON\r")
	time.sleep(1)
	tn.write("SI"+__addon__.getSetting("denoninput")+"\r")
	#print tn.read_eager()
	tn.close()

def changeVolumeDenon(volume):
	if volume > 98:
		volume = 98
	elif volume < 0:
		volume = 0
		
	tn = telnetlib.Telnet(__addon__.getSetting("denonip"))	
	tn.write("MV"+"{0:02d}".format(volume)+"\r")
	tn.close()
	

class DenonWatcher(xbmc.Monitor):
	def __init__(self, *args, **kwargs):
		xbmc.Monitor.__init__(self)
				
	def onNotification(self, sender, method, data):
		if method == "Player.OnPlay":
			turnOnDenon()
		elif method == "Player.OnVolumeChanged":
			dataDecoded = json.loads(data)
			changeVolumeDenon(dataDecoded['volume'])
			
		
		

class PlayerWhichStartsDenon(xbmc.Player):
	def onPlayBackStarted(self):
		tn = telnetlib.Telnet(HOST)
		tn.write("PWON\r")
		time.sleep(1)
		tn.write("SIMPLAY\r")
		#print tn.read_eager()
		tn.close()
		
#player = PlayerWhichStartsDenon()
monitor = DenonWatcher()

while not xbmc.abortRequested:
	xbmc.sleep(60000)
