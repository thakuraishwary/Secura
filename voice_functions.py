import speech_recognition as sr
import image_functions

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 500
        r.pause_threshold = 0.5
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
    
    except Exception as e:
        # print(e)
        print("Said that again please")
        return "None"
    return query

def operations(user, window):
    query = takeCommand().lower()
    
    if "login to linkedin" in query:
        user.login_linkedin(window)
        
    elif "logout" in query:
        if user.is_using == 'linkedin':
            user.logout_linkedin()
        elif user.is_using == 'instagram':
            user.logout_instagram()

    if "login to instagram" in query:
        user.login_instagram(window)

    elif "exit" in query or "quit" in query:
        exit()
    
    image_functions.check_presence(window, user)
    operations(user, window)
    
    