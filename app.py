from selenium import webdriver
from datetime import datetime
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1, 
    "profile.default_content_setting_values.notifications": 1 
  })

PATH = "C:\Program Files (x86)\chromedriver.exe"

#Credentials

username = "" #Your Username
password = "" #Your Password

#Time Table
codeInput = 0
flag = 0
classStartTime = []
classEndTime = []
classCode = []
classToJoin = 0
classesJoined = 0
numberOfClasses = int(input("How many classes do you have? "))
for i in range(numberOfClasses):
	classStartTime.append(input("What is the starting time of " + str(i + 1) + " class? "))
	classEndTime.append(input("What is the ending time of " + str(i + 1) + " class? "))
	classCode.append(input("What is the class code for " + str(i+1) + " class? "))

driver = webdriver.Chrome(chrome_options=opt, executable_path=PATH)
driver.get("https://meet.google.com/?hl=en")
signIn = driver.find_element_by_link_text("Sign in")
signIn.click()
try:
	userInput = WebDriverWait(driver, 30).until(
		EC.presence_of_element_located((By.ID, "identifierId"))
		)
	userInput.send_keys(username)
	userInput.send_keys(Keys.RETURN)

	userPassword = WebDriverWait(driver, 30).until(
		EC.presence_of_element_located((By.NAME, "password"))
		)
	userPassword.send_keys(password)
	userPassword.send_keys(Keys.RETURN)
	
	

except:
	print("Error")

#Current Time

while(classesJoined < numberOfClasses):
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	if(classToJoin < numberOfClasses and classStartTime[classToJoin] == str(current_time)):
		classToJoin+=1
		try:
			joinMeeting = WebDriverWait(driver, 20).until(
				EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Join or start a meeting')]"))
				)
			joinMeeting.click()

			codeInput = driver.find_element_by_class_name("poFWNe")

			codeInput.send_keys(classCode[classToJoin-1])
			codeInput.send_keys(Keys.RETURN)

			mic = WebDriverWait(driver, 30).until(
				EC.presence_of_element_located((By.XPATH, "//*[contains(@aria-label, 'Turn off microphone (ctrl + d)')]"))
				)
			mic.click();

			cam = WebDriverWait(driver, 30).until(
				EC.presence_of_element_located((By.XPATH, "//*[contains(@aria-label, 'Turn off camera (ctrl + e)')]"))
				)
			cam.click();

			join = WebDriverWait(driver, 30).until(
				EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Ask to join')]"))
				)
			join.click();
		except:
			print("Error in joining")

	if(classEndTime[classToJoin-1] == str(current_time)):
		try:
			hangUp = WebDriverWait(driver, 30).until(
				EC.presence_of_element_located((By.XPATH, "//*[contains(@aria-label, 'Leave call')]"))
				)
			hangUp.click();

			home = WebDriverWait(driver, 30).until(
				EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Return to home screen')]"))
				)
			home.click();

			classesJoined += 1;
			if(classesJoined == numberOfClasses):
				flag = 1
		except:
			print("Error in Leaving");

	time.sleep(1)

	if(flag == 1):
		time.sleep(5)
		driver.quit()