import os,urllib.request,time
from  bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def scrape(cromepath,url,imagenum,imagesavedir,imageextention):
    num = 0
    try:
        os.mkdir(imagesavedir)
    except FileExistsError:
        pass
    driver = webdriver.Chrome(cromepath)
    driver.get(url)
    elem = driver.find_element_by_tag_name("body")
    while imagenum > len(BeautifulSoup(driver.page_source, "html.parser").find_all("img", attrs={"alt": "Post image"})):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    images = soup.find_all("img", attrs={"alt": "Post image"})
    for i in range(imagenum):
        image_scr = images[i]["src"]
        urllib.request.urlretrieve(image_scr, imagesavedir + str(num) + imageextention)
        num += 1
    driver.quit()


