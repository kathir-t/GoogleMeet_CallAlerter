from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from time import sleep
import clipboard
from playsound import playsound
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume


meeturl = clipboard.paste()
if meeturl is None or "https://meet.google.com/" not in meeturl:
	print("Copy the Meet link URL first")
	playsound('.\\audio\\copy_url.wav')
	exit(1)

# Dictionary
alertWords = [ "your_name_here", "are you there", "unmute yourself", "say something", "can you hear me"]

# HTML Class Names
captionsToggleBtnClass = "iTTPOb"
joinNowBtnClass = "NPEfkd"
captionsSpanClass = "VbkSUe"

# Functions

def waitTillPageLoad(showMessage):
	if showMessage:
		print("Loading",end='')
	while True:
		if showMessage:
			print(".",end='')
		if "Meet" in browser.title:
			print("")
			break
		sleep(2)

def setFirefoxVolume(vol):
	sessions = AudioUtilities.GetAllSessions()
	for session in sessions:
		volume = session._ctl.QueryInterface(ISimpleAudioVolume)
		if session.Process and session.Process.name() == "firefox.exe":
			volume.SetMasterVolume(vol, None)

# PROGRAM STARTS here
print("Opening",meeturl)

playsound('.\\audio\\opening_meet.wav')

profile = webdriver.FirefoxProfile(".\\cachedir\\")
browser = webdriver.Firefox(profile)
browser.get(meeturl)

setFirefoxVolume(0.1)

waitTillPageLoad(True)
sleep(4)

browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'd')
sleep(1)

joinNowBtn = browser.find_element_by_class_name(joinNowBtnClass)
joinNowBtn.click()
sleep(2)

try:
	ccBtn = browser.find_element_by_class_name(captionsToggleBtnClass)
	ccBtn.click()
	sleep(5)
except NoSuchElementException:
	print("Could not enable captions automatically")
	playsound('.\\audio\\enable_captions.wav')

while True:
	try:
		elems = browser.find_element_by_class_name(captionsSpanClass)
		captioTextLower = str(elems.text).lower()
		for word in alertWords:
			if word in captioTextLower:
				playsound('.\\audio\\someone_calling.wav')
				setFirefoxVolume(0.8)
				sleep(2)
		sleep(0.5)
	except (NoSuchElementException, StaleElementReferenceException):
		sleep(1)