from tkinter import *
from tkinter import ttk
from utils import scraper,sound,texts,imageeditor,utilitis as utl,videoeditor as editor
import json,random,csv,os,shutil
from PIL import Image,ImageTk


MINTIMEPERIMG = 7
ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)
BASE_DIR += "\\"
bgaudiopath =os.path.join(BASE_DIR,"videofiles\\bgmusic\\Bikerides.mp3")
settingpath = BASE_DIR + "setting.json"
currentimagenum = 0
with open(settingpath) as jsonfile:
    setting = json.load(jsonfile)
def savesetting():
    with open(settingpath,"w") as file:
        json.dump(setting,file,indent=2)


def makeImagesAndText():
    sm = setting["Misc"]
    si = setting["Images"]
    st = setting["Text"]
    print("scraping images")
    scraper.scrape(sm["CromePath"],sm["SiteURL"],si["HowManyImage"],BASE_DIR + sm["Temp"],si["ImageExtention"])

    print("resizeing images")
    images = utl.getFilesInDir(BASE_DIR + sm["Temp"], "png")
    imageeditor.resize(1920,1080,images,BASE_DIR+sm["Temp"],BASE_DIR+si["VideoReadyImageDir"])

    print("removing dulicateimages")
    compeingimg = utl.getFilesInDir(BASE_DIR+si["VideoReadyImageDir"],si["ImageExtention"])
    #30min i just appeded 2 [][] not one elements to anather dont be supid like me
    comperatorimg = utl.getFilesInDir(BASE_DIR+si["UsedImageDir"],si["ImageExtention"])
    comperatorimg2 = utl.getFilesInDir(BASE_DIR+si["AdsImageDir"],si["ImageExtention"])
    for imagepath in comperatorimg2:
        comperatorimg.append(imagepath)
    gotcopydir =imageeditor.imgtester(compeingimg,comperatorimg)
    for copy in gotcopydir:
        os.remove(copy)
    images = utl.getFilesInDir(BASE_DIR + si["VideoReadyImageDir"], "png")
    print("geting more images")
        #todo implement to get more image and filter them in random spots as show it how much more needid or shutit down if it more than 50% reused
    print("geting texts")
    texts.makescript(images, BASE_DIR +st["TextsDir"], str(st["BiggestTextNum"]) + ".csv")
    #st["BiggestTextNum"] += 1"""

    print("loading texts")
    textfile = BASE_DIR + setting["Text"]["TextsDir"] + str(setting["Text"]["BiggestTextNum"]) + ".csv"
    with open(textfile, 'r') as csvfile:
        text = csv.reader(csvfile, delimiter=";")
        for line in text:
            textslist.append([BASE_DIR +si["VideoReadyImageDir"]+os.path.basename(line[0]),line[1]])

    print("clearing temporary files")
    tempfiles = utl.getFilesInDir(BASE_DIR + sm["Temp"])
    for tempfile in tempfiles:
        os.remove(tempfile)
    print("done")


global textslist
textslist = []
global bgimagedir
bgimagedir = "D:\\daniprojectek\\videocreator\\videofiles\\images\\0.png"
global imagetexts
imagetexts = "Press 'Scrape and get text' button"
global imgnum
imgnum = -1

def gettextsandimagesup():
    global imgnum
    if imgnum + 1 >= 0 and imgnum + 1 < len(textslist):
        if imgnum >= 0 and imgnum < len(textslist) and imagetext.get() !="Deleted":
            textandimages = textslist[imgnum]
            textandimages[1] = imagetext.get()
        else:
            imagetext.delete(0, "end")
        imgnum += 1
        textandimages = textslist[imgnum]
        bgimagedir = textandimages[0]
        imagetexts = textandimages[1]
        print(imagetexts)
        global backgrund
        imagetext.delete(0, "end")
        imagetext.insert(END,imagetexts)
        im = Image.open(bgimagedir)
        resizedimage = im.resize((1280,720),Image.ANTIALIAS)
        ph = ImageTk.PhotoImage(resizedimage)
        backgrund.config(image=ph)
        backgrund.image = ph


def gettextsandimagesdown():
    global imgnum
    if imgnum + -1 >= 0 and imgnum + -1 < len(textslist):
        if imgnum >= 0 and imgnum < len(textslist):
            textandimages = textslist[imgnum]
            textandimages[1] = imagetext.get()
        else:
            imagetext.delete(0, "end")
        imgnum += -1
        textandimages = textslist[imgnum]
        bgimagedir = textandimages[0]
        imagetexts = textandimages[1]
        global backgrund
        imagetext.delete(0, "end")
        imagetext.insert(END,imagetexts)
        im = Image.open(bgimagedir)
        resizedimage = im.resize((1280,720),Image.ANTIALIAS)
        ph = ImageTk.PhotoImage(resizedimage)
        backgrund.config(image=ph)
        backgrund.image = ph


def deleteimg():
    textandimages = textslist[imgnum]
    bgimagedir = textandimages[0]
    os.remove(bgimagedir)
    textslist.pop(imgnum)
    imagetext.delete(0, "end")
    imagetext.insert(END, "Deleted")


def movetoads():
    textandimages = textslist[imgnum]
    bgimagedir = textandimages[0]
    newname = setting["Images"]["AdsImageDir"] + str(setting["Images"]["AdsImageNum"])+setting["Images"]["ImageExtention"]
    shutil.copy(bgimagedir,newname)
    os.remove(bgimagedir)
    textslist.pop(imgnum)
    setting["Images"]["AdsImageNum"]+= 1
    imagetext.delete(0, "end")
    imagetext.insert(END,"Deleted")
    savesetting()


def savetexts():
    textfile = BASE_DIR + setting["Text"]["TextsDir"] + str(setting["Text"]["BiggestTextNum"]) + ".csv"
    with open(textfile, 'w') as csvfile:
        csv_writer = csv.writer(csvfile,delimiter=';',lineterminator='\r')
        for line in textslist:
            csv_writer.writerow(line)


def makevideo():
    savetexts()
    #textospeech.getVoices()
    videoname = setting["Video"]["VideoName"]
    videoFormat = setting["Video"]["VideoFormat"]
    videoSaveDir = setting["Video"]["VideoSaveDir"]
    videonum = setting["Video"]["BigestVideoNum"]
    audioName = str(setting["Audio"]["AudioName"])
    audioSaveDir = setting["Audio"]["AudioSaveDir"]
    imageSaveDir = setting["Images"]["VideoReadyImageDir"]
    sendabletext = []
    textfile = BASE_DIR + setting["Text"]["TextsDir"] + str(setting["Text"]["BiggestTextNum"]) + ".csv"
    with open(textfile, 'r') as csvfile:
        text = csv.reader(csvfile, delimiter=';')
        for line in text:
            sendabletext.append(line[1])
    tempdir = setting["Misc"]["Temp"]
    imagedir = []

    with open(textfile, 'r') as csvfile:
        text = csv.reader(csvfile, delimiter=';')
        for line in text:
            imagedir.append(imageSaveDir+os.path.basename(line[0]))

    """for image in imagedirlist:
        imagedir.append(image)
    for i in range(len(imagedir)):
        fullpaht = setting["Images"]["VideoReadyImageDir"]+imagedir[i]
        imagedir[i] = fullpaht
        forsaveingimage.append(fullpaht)"""

    #getting more images not in here becose no text for it
    """moreimagenames = os.listdir(setting["Images"]["UsedImageDir"])
    indexes = []
    while len(imagedir)+ len(indexes) < setting["Images"]["HowManyImage"]:
        randomindex = random.randint(0, len(moreimagenames))
        for index in indexes:
            if index == randomindex:
                break
        else:
            indexes.append(randomindex)
    
    for index in indexes:
        imagedir.append(setting["Images"]["UsedImageDir"]+moreimagenames[index])"""



    minaudioleninsec = 5
    audiodirs = sound.makeVoice(sendabletext, tempdir, audioSaveDir, audioName, MINTIMEPERIMG)
    editor.makevideos(imagedir, audiodirs, videoSaveDir, videoname+str(videonum), videoFormat,60,bgaudiopath) #todo add a musicpath for the bg music
    setting["Video"]["BigestVideoNum"] += 1
    saveusedimages(imagedir,setting["Images"]["UsedImageDir"],setting["Images"]["HowManyUsedImage"],setting["Images"]["ImageExtention"])
    savesetting()
    #deletefiles()
    for image in imagedir:
        os.remove(image)
    for audiopath in audiodirs:
        os.remove(audiopath)
    #label.configure(text=f"{videoname}.{videoFormat} \n video was made at {videoSaveDir}")

def saveusedimages(savebleimagepaths,tosave,firstname,extention):
    namenum = firstname
    for imagepath in savebleimagepaths:
        print(imagepath)
        with open(imagepath,"r+b") as f:
            with Image.open(f) as image:
                image.save(tosave+str(namenum)+extention)
        namenum +=1
    setting["Images"]["HowManyUsedImage"] = namenum
    savesetting()

if __name__ == "__main__":

    root = Tk()
    global backgrund
    backgrund = Label(root)
    root.minsize(1800, 1000)
    backgrund.pack(fill=BOTH, expand=True)
    button = Button(backgrund, text="Scrape and get text\n        (press first)", command=makeImagesAndText)

    nextimage = Button(backgrund, text="nextimage and text", command=gettextsandimagesup)
    previusimage = Button(backgrund, text="previusimage and text", command=gettextsandimagesdown)
    delete = Button(backgrund, text="delete img", command=deleteimg)
    movetoad = Button(backgrund, text="fund an ad", command=movetoads)
    savetext = Button(backgrund, text="save texts", command=savetexts)
    makevideo = Button(backgrund, text="All done make video", command=makevideo)

    imagetext = Entry(backgrund,font=("Helvetica",24),width=100)
    previusimage.grid(row=0, column=1)
    nextimage.grid(row=0, column=2)
    movetoad.grid(row=0,column=3)
    delete.grid(row=0,column=4)
    savetext.grid(row=0,column=5)
    makevideo.grid(row=0,column=6)
    imagetext.grid(row=1, column=0,columnspan=25)
    button.grid(row=0, column=0)
    root.mainloop()


"""
#unreadable
class MainApplication(Frame):
    def __init__(self, parent, *args, **kwargs):
        global textslist
        Frame.__init__(self, parent, *args, **kwargs)
        self.bgimagedir = "D:\\daniprojectek\\videocreator\\videofiles\\images\\0.png"
        self.imagetexts = "Press 'Scrape and get text' button"
        #self.image1= PhotoImage(file=self.bgimagedir)
        self.parent = parent
        self.backgrund = Label(root)#image=self.image1
        self.backgrund.pack(fill=BOTH, expand=True)
        self.button = Button(self.backgrund, text="Scrape and get text\n        (press first)", command=makeImagesAndText)
        self.nextimage = Button(self.backgrund, text="nextimage and text", command=self.gettextsandimagesup)
        self.previusimage = Button(self.backgrund, text="previusimage and text", command=self.gettextsandimagesdown)
        self.imagetext = Entry(self.backgrund)
        self.imagetext.insert(0, self.imagetexts)
        self.imgnum = -1

        self.nextimage.grid(row=0, column=2)
        self.previusimage.grid(row=0, column=1)
        self.imagetext.grid(row=1, column=0)
        self.button.grid(row=0, column=0)
    def gettextsandimagesdown(self):
        if self.imgnum + -1 >= 0 and self.imgnum + -1 < len(textslist):
            if self.imgnum >= 0 and self.imgnum < len(textslist):
                self.textandimages = textslist[self.imgnum]
                self.textandimages[1] = self.imagetext.get()
            else:
                self.imagetext.delete(0, "end")
            self.imagetext.delete(0, "end")
            self.imgnum += -1
            self.textandimages = textslist[self.imgnum]
            self.bgimagedir = self.textandimages[0]
            self.imagetexts = self.textandimages[1]
            self.imagetext.insert(0, self.imagetexts)
            self.backgrund.config(image=ImageTk.PhotoImage(Image.open(self.bgimagedir)))
            #self.backgrund.image = ImageTk.PhotoImage(Image.open(self.bgimagedir))
            print(self.bgimagedir)
            self.nextimage.grid(row=0, column=2)
            self.previusimage.grid(row=0, column=1)
            self.imagetext.grid(row=1, column=0)
            self.button.grid(row=0, column=0)
            self.backgrund.pack(fill=BOTH, expand=True)

    def gettextsandimagesup(self):
        if self.imgnum + 1 >= 0 and self.imgnum + 1 < len(textslist):
            if self.imgnum >= 0 and self.imgnum < len(textslist):
                textandimages = textslist[self.imgnum]
                textandimages[1] = self.imagetext.get()
            else:
                self.imagetext.delete(0, "end")
            self.imgnum += 1
            self.textandimages = textslist[self.imgnum]
            self.bgimagedir = self.textandimages[0]
            self.imagetexts = self.textandimages[1]
            self.backgrund.config(image=ImageTk.PhotoImage(Image.open(self.bgimagedir)))
            self.imagetext.delete(0, "end")
            #self.backgrund.image = ImageTk.PhotoImage(Image.open(self.bgimagedir))
            print(self.bgimagedir)
            self.nextimage.grid(row=0, column=2)
            self.previusimage.grid(row=0, column=1)
            self.imagetext.grid(row=1, column=0)
            self.button.grid(row=0, column=0)
            self.backgrund.pack(fill=BOTH, expand=True)

if __name__ == "__main__":
    root = Tk()
    MainApplication(root).pack(fill="both", expand=True)
    root.minsize(1280, 720)
    root.mainloop()"""