import urllib.request
import os
import glob
import time
from fpdf import FPDF

def makeDirectories():
    if not os.path.exists('download'):
        os.makedirs('download')
    if not os.path.exists('output'):
        os.makedirs('output')
        
def clearDownloadFolder():
    trash = glob.glob('download/*')
    for t in trash:
        os.remove(t)
    
def downloadImg():
    bookID = input("Book ID [Example= kdisn/jqao]: ")
    
    srcURL = "https://online.anyflip.com/" + bookID

    numberOfImg = int(input("Last Page Number: "))

    for i in range(1, numberOfImg + 1):
        start = time.time()

        fileName = str(i) + '.jpg'

        maxTries = 5
        tries = maxTries
        while tries > 0:
            try:
                if tries < maxTries:
                    print('\n## Retrying... (' + str(tries - 1) +
                          ' attempt(s) remaining)')
                urllib.request.urlretrieve(
                    srcURL + "/files/mobile/" +  fileName, "download/" + fileName)
            except:
                tries -= 1
                time.sleep(1)
            else:
                break
        if tries == 0:
            os.system("cls")
            print('Download failed! Server down/Check your connection.\n')
            clearDownloadFolder()
            downloadImg()

        end = time.time()

        diff = end - start
        progress = i/numberOfImg * 100
        estimate = int(diff * float(numberOfImg - i))

        os.system("cls")
        print('Downloaded (' + str(i) + '/' + str(numberOfImg) + ')')
        print('Progress: '+"{:3.2f}".format(progress) +
              '% (Estimated ' + str(estimate) + 's remaining)')

    print("Done!\n")
    
def convertToPDF():
    images = sorted(glob.glob('download/*'), key=os.path.getmtime)
    pdf = FPDF()
    title = input("> Title of output file: ")

    print("Converting to pdf (this takes a while)...")

    for image in images:
        pdf.add_page()
        pdf.image(image, 0, 0, 210, 297)

    pdf.output("output/" + title + ".pdf", "F")
    print("Done!\n")
    
    os.system("pause")


os.system("cls")
makeDirectories()
clearDownloadFolder()
downloadImg()
convertToPDF()
clearDownloadFolder()