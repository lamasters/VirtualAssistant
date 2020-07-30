from gtts import gTTS
import speech_recognition as sr
from playsound import playsound
import random, os, time
from pynput.keyboard import Key, Controller

keyboard = Controller()

# A function for loading file inputs
def load_messages(f_name):
    f = open(f_name, 'r')
    messages = f.readlines()
    f.close()

    for m in range(len(messages)):
        messages[m] = messages[m].split('\n')[0]

    return messages

wake_words = load_messages('wake_words.txt')

# Speak the given phrase
def talk(audio):
    print(audio)

    for line in audio.splitlines():
        tts = gTTS(text=line, lang='en-au', )
        tts.save('audio.mp3')
        playsound('audio.mp3')
        os.remove('audio.mp3')

# Parse the command from microphone input
def getCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Ready for command')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    print('Sending...')
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    except:
        print('Command failed')
        command = getCommand()
    
    return command

# Check if a wake word is contained in the phrase
def wakeWord(text):
    for phrase in wake_words:
        if phrase in text:
            return (True, text.split(phrase)[1])
    
    return (False, '')
 
# Main assistant function
# Check for keywords in the given command
def assistant(command):
    wake, command = wakeWord(command)
    if not wake:
        print('No wake word')
        return
    else:
      time.sleep(0.3)
      keyboard.press(Key.enter)

talk('Ah shit, I\'m awake')

# Main loop
# Check for assistant inputs and run timers
while True:
    assistant(getCommand())
