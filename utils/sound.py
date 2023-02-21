import pyttsx3
from pydub import AudioSegment
import os
def makeVoice(text,tempdir, audisavedir, audioname,minaudiolen):

    try:
        os.mkdir(tempdir)
    except FileExistsError:
        pass
    try:
        os.mkdir(audisavedir)
    except FileExistsError:
        pass

    converter = pyttsx3.init()
    converter.setProperty('rate', 150)
    converter.setProperty('volume', 1)
    i = 0
    audiopaths = []
    for line in text:
        converter.save_to_file(line,f"{tempdir}{audioname}{i}.mp3")
        converter.runAndWait()
        speach = AudioSegment.from_file(f"{tempdir}{audioname}{i}.mp3")
        #change the milliseconds if you want less silence
        if speach.duration_seconds < minaudiolen:
            editedspeach =speach + AudioSegment.silent(duration=(minaudiolen-speach.duration_seconds)*1000+500)
        else:
            editedspeach = speach + AudioSegment.silent(duration=1000)
        editedspeach.export(audisavedir+audioname+str(i)+".mp3",format="mp3")
        audiopaths.append(audisavedir+audioname+str(i)+".mp3")
        os.remove(f"{tempdir}{audioname}{i}.mp3")
        i += 1
    return audiopaths

# get all voices
def getVoices():
    converter = pyttsx3.init()
    voices = converter.getProperty('voices')

    for voice in voices:
        # to get the info. about various voices in our PC
        print("Voice:")
        print("ID: %s" % voice.id)
        print("Name: %s" % voice.name)
        print("Age: %s" % voice.age)
        print("Gender: %s" % voice.gender)
        print("Languages Known: %s" % voice.languages)

