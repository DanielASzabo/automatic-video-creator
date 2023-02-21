from PIL import Image,ImageChops
import os,cv2,math



def imgtester(comperableimgpaths,comperatorimgpaths):
    haveaduplicatepath = []
    for image in comperableimgpaths:
        comperableimg = cv2.imread(image)
        for comperatorimgpath in comperatorimgpaths:
            comperatorimg = cv2.imread(comperatorimgpath)
            diff = cv2.subtract(comperableimg,comperatorimg)
            b,g,r, = cv2.split(diff)
            cv2.countNonZero(b)
            cv2.countNonZero(g)
            cv2.countNonZero(r)
            if cv2.countNonZero(r) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(b) == 0:
                haveaduplicatepath.append(image)
                break
    return haveaduplicatepath


def resize(width,hegith,imagedirs,tempdir,savedir):
    try:
        os.mkdir(savedir)
    except FileExistsError:
        pass

    for imagedir in imagedirs:
        imgname = os.path.basename(imagedir)
        img = cv2.imread(imagedir)
        oldimgheigth = img.shape[0]
        oldimgwidth = img.shape[1]
        if hegith/oldimgheigth < width/oldimgwidth:
            imgresized = cv2.resize(img, (int(oldimgwidth*(hegith/oldimgheigth)), hegith))
        else:
            imgresized = cv2.resize(img, (width, int(oldimgheigth*(width/oldimgwidth))))
        cv2.imwrite(tempdir+os.path.basename(imagedir),imgresized)
        with open(tempdir+imgname,"r+b") as f:
            with Image.open(f) as image:
                cover = resize_contain(image, [width, hegith],resample=Image.LANCZOS,bg_color=(0, 0, 0))
                cover.save(savedir+imgname)



def resize_contain(image, size, resample=Image.LANCZOS, bg_color=(255, 255, 255, 0)):
    img_format = image.format
    img = image.copy()
    img.thumbnail((size[0], size[1]), resample)
    background = Image.new('RGBA', (size[0], size[1]), bg_color)
    img_position = (
        int(math.ceil((size[0] - img.size[0]) / 2)),
        int(math.ceil((size[1] - img.size[1]) / 2))
    )
    background.paste(img, img_position)
    background.format = img_format
    return background.convert('RGBA')