import openai
import speech_recognition as sr
import os
import json
from dotenv import load_dotenv
from elevenlabslib import *
import psycopg2
import keyboard
 
load_dotenv()

#Get the API keys from the .env file
ELEVEN_LAB_KEY = os.environ.get("ELEVEN_LAB_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

user = ElevenLabsUser(ELEVEN_LAB_KEY) # Intiaite user object

# Get a Voice object, by name or UUID
voice_choice = "Bella"
voice = user.get_voices_by_name(voice_choice)[0]

personality = "personality.txt"
usewhisper = True
isEnabled = False # Eleven labs voice is disabled by default

# openAI set-up
openai.api_key = os.getenv('OPENAI_API_KEY')
with open(personality, "r") as file:
    mode = file.read()
messages  = [{"role": "system", "content": f"{mode}"}]

#Initialize connection with postgresql database
pg_conn = psycopg2.connect(
    host = "gitready.cxz7x2iimqnj.us-east-2.rds.amazonaws.com",
    database = "postgres",
    user = "postgres",
    password = "lobsterpaste"
)

# Cursor can be used to execute SQL commands
sql = pg_conn.cursor()
    # Syntax: sql.execute("SQL COMMAND")
    # If query is a selection, sql.fetchall() will return the results as a list of tuples


######INITIATE VOICE READER#########

##################################
r = sr.Recognizer()
mic = sr.Microphone(device_index=0)
r.dynamic_energy_threshold=False
r.energy_threshold = 700

def whisper(audio):
    with open('speech.wav','wb') as f:
        f.write(audio.get_wav_data())
    speech = open('speech.wav', 'rb')
    wcompletion = openai.Audio.transcribe(
        model = "whisper-1",
        file=speech
    )
    user_input = wcompletion['text']
    print(user_input)
    return user_input

def save_conversation(save_foldername):
    '''
    Checks the folder for previous conversations and will get the next suffix that has not been used yet.  
    It returns suffix number
    Args:
        save_foldername (str) : Takes in the path to save the conversation to.
    '''
    os.makedirs(save_foldername, exist_ok=True)

    base_filename = 'interview'
    suffix = 0
    filename = os.path.join(save_foldername, f'{base_filename}_{suffix}.txt')

    while os.path.exists(filename):
        suffix += 1
        filename = os.path.join(save_foldername, f'{base_filename}_{suffix}.txt')

    with open(filename, 'w') as file:
        json.dump(messages, file, indent=4)

    return suffix

def save_inprogress(suffix, save_foldername):
    '''
    Uses the suffix number returned from save_conversation to continually update the 
    file for this instance of execution.  This is so that you can save the conversation 
    as you go so if it crashes, you don't lose to conversation.  Shouldn't be called
    from outside of the class.
    Args:
        suffix  :  Takes suffix count from save_conversation()
    '''
    os.makedirs(save_foldername, exist_ok=True)
    base_filename = 'conversation'
    filename = os.path.join(save_foldername, f'{base_filename}_{suffix}.txt')

    with open(filename, 'w') as file:
        json.dump(messages, file, indent=4)
def listen_convo():
    try: 
        return r.listen(source, timeout=5, phrase_time_limit=5)
    except:
        print("TimedOut")
        listen_convo()
# grab script location
script_dir = os.path.dirname(os.path.abspath(__file__))
foldername = "voice_assistant"
save_foldername = os.path.join(script_dir,f"conversations/{foldername}")
suffix = save_conversation(save_foldername)

# main while loop where the conversation occurs
while True:
    with mic as source:
        print("\nListening...")
        r.adjust_for_ambient_noise(source, duration = 0.5)

        audio = listen_convo()
        print('Done Listening')
        try:
            if usewhisper:
                user_input = whisper(audio)
            else:
                user_input = r.recognize_google(audio)
        except:
            continue

    messages.append({"role" : "user", "content" : user_input})

    completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.8 #Influences output of chat model
            #For temperature, higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. 
        )    

    response = completion.choices[0].message.content
    
    
    messages.append({"role": "assistant", "content": response})
    print(f"\n{response}\n")
    save_inprogress(suffix, save_foldername)

    if isEnabled:
        voice.generate_and_play_audio(response, playInBackground=False)

# Close the connection to the database
pg_conn.close()
sql.close()
