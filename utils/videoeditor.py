from moviepy.editor import *
import os


def makevideos(imagepaths, audipaths, tosavedir, videoname, videoformat, fps, *backgrundmusicpahs):

    try:
        os.mkdir(tosavedir)
    except FileExistsError:
        pass

    outputvideo = os.path.join(tosavedir, videoname + videoformat)
    # concataneted audio  clip to make the speach and composite audi clip to do bg music

    myaudios = []
    for path in audipaths:
        myaudios.append(AudioFileClip(path))
    myaudioslen = []
    for audio in myaudios:
        myaudioslen.append(audio.duration)

    #tweeking the audio
    #>> > newclip = volumex(clip, 2.0)  # doubles audio volume
    #>> > newclip = clip.fx(volumex, 0.5)  # half audio, use with fx
    #>> > newclip = clip.volumex(2)  # only if you used "moviepy.editor"

    #todo make it read the bg folder then randomize the bg music
    if len(backgrundmusicpahs) != 0:
        concatenatedaudio = concatenate_audioclips(myaudios)
        concatenatedaudio = concatenatedaudio.volumex(1.5)
        bgaudio = AudioFileClip("D:\\daniprojectek\\videocreator\\videofiles\\bgmusic\\Bikerides.mp3")
        mybgaudios =[]
        fulltime = 0
        for i in range(len(myaudioslen)):
            fulltime += myaudioslen[i]
        for _ in range( int(fulltime/bgaudio.duration)+1):
            mybgaudios.append(bgaudio)

        concatenatedbgaudio = concatenate_audioclips(mybgaudios)
        bgaudiowhitrigthtime = concatenatedbgaudio.subclip(0,concatenatedaudio.duration)
        bgaudiowhitrigthtime = bgaudiowhitrigthtime.volumex(0.20)
        doneaudio = CompositeAudioClip([concatenatedaudio,bgaudiowhitrigthtime])
    else:
        doneaudio = concatenate_audioclips(myaudios)
    myclips = []
    for i in range(len(imagepaths)):
        print(imagepaths[i])
        frame = ImageClip(imagepaths[i])
        for _ in range(int(fps * myaudioslen[i])):
            myclips.append(frame.img)
    clip = ImageSequenceClip(myclips, fps=fps)
    finalclip = clip.set_audio(doneaudio)
    finalclip.write_videofile(outputvideo, codec='libx264', audio_codec="aac")
