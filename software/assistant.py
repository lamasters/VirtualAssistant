from gtts import gTTS
import speech_recognition as sr
from playsound import playsound
import wikipedia, random, os, time

# A function for loading file inputs
def load_messages(f_name):
    f = open(f_name, 'r')
    messages = f.readlines()
    f.close()

    for m in range(len(messages)):
        messages[m] = messages[m].split('\n')[0]

    return messages

timers = []

err_msg = load_messages('error_messages.txt')
greetings = load_messages('greetings.txt')
shopping_list = load_messages('shopping_list.txt')
wake_words = load_messages('wake_words.txt')

# Search the phrase on wikipedia
def search(text):
    text = text[7:]

    try:
        resp = wikipedia.summary(text).split('.')[0]
    except:
        resp = 'I couldn\'t find anything'

    return resp

# Add an item to the shopping list
def addItem(text):
    text = text.split('add ')[1].split(' to my shopping list')[0]
    shopping_list.append(text + '\n')

    f = open('shopping_list.txt', 'w')
    for item in shopping_list:
        f.write(item)
    f.close()

    return text

# Read back the shopping list
def readList():
    list_text = ' '
    for i in range(len(shopping_list)):
        list_text = list_text + shopping_list[i][:-1] + ' '
        if i == len(shopping_list) - 2:
            list_text = list_text + 'and '

    return list_text

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

    if 'hello' in command or 'hi' in command or 'hey' in command:
        greeting = random.choice(greetings)
        talk(greeting)
    elif 'shopping list' in command and ('add' in command or 'ad' in command):
        item = addItem(command)
        talk('I added ' + item + ' to your shopping list')
    elif 'what' in command and 'on my shopping list' in command:
        talk('Your list is ' + readList())
    elif 'search' in command:
        talk(search(command))
    elif 'judy' in command and 'valentine' in command:
        talk('Oh Carl! This is so... sweet')
    elif 'timer' in command:
        start = 0
        end = 0
        
        for c in range(len(command)):
            if end != 0:
                break
            
            if command[c].isnumeric() and command[c] != ' ':
                if start == 0:
                    start = c
            if command[c].isalpha() and start != 0:
                end = c

        if end == 0:
            end = start + 1
        count = int(command[start:end]) * 60
        timers.append((time.time(), count))
        talk('I set a timer for ' + str(count // 60) + ' minutes')
            
    else:
        error = random.choice(err_msg)
        talk(error)

talk('Ah shit, I\'m awake')

# Main loop
# Check for assistant inputs and run timers
while True:
    assistant(getCommand())

    ctime = time.time()
    t = 0
    while t < len(timers):
        timer = timers[t]
        if ctime - timer[0] > timer[1]:
            playsound('alarm.mp3')
            timers.pop(t)
            t -= 1
        t += 1
