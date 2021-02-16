"""
Author: Giovanni Ciaramella
Date: February 14th 2021
Description: gets apk file in input, extracts from it dex file and converts all in image in grayscale.

"""


import os, zipfile, math, codecs, shutil

from flask import Flask, render_template, request
from shutil import copyfile
from PIL import Image

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route("/upload-apk", methods=['POST'])
def upload_apk():

    target = os.path.join(APP_ROOT, 'ZIP')
    print(target)

    # if folder ZIP doesn't exist it will be created
    if not os.path.isdir(target):
        os.mkdir(target)
    print("'ZIP' folder has been created")

    # going to store file previously uploaded into ZIP folder
    for file in request.files.getlist('file'):
        # changing the extension of the file previously from APK to ZIP
        fileName = 'apk-to-convert.zip'
        destination = "\\".join([target, fileName])
        print(destination)
        file.save(destination)
    print("File has been stored inside the folder")

    # going to unzip file previously uploaded in 'unzipped_files' folder
    filePath = 'ZIP/apk-to-convert.zip'

    unZipFolder = target + '/unzipped_files'

    # if folder unzipped_files doesn't exist it will be created
    if not os.path.isdir(unZipFolder):
        os.mkdir(unZipFolder)
    print("'unzipped_files' folder has been created")

    with zipfile.ZipFile(filePath, 'r') as zip_ref:
        zip_ref.extractall(unZipFolder)

    # getting all .dex files store in a zip file
    # in one APK file can be stored more then one dex file only if the application is over 4GB (not impossible case)

    asps = []

    for item in os.listdir(unZipFolder):
        if item.endswith('.dex'):
            asps.append(item)

    print('************** all files with extension dex ************** \n')
    print(*asps)
    print('********************************************************** \n')

    # creation of the new file if doesn't exist

    open('binFile.txt', 'w')

    # opens binary file old dex file and copy it in the file previously created

    copyfile('ZIP/unzipped_files/classes.dex', 'binFile.txt')


    byteFile = open('binFile.txt', 'rb').read()

    # conversion from binary to hexadecimal
    hex_data = codecs.encode(byteFile, "hex_codec")

    print(hex_data)

    # deleting leftovers of byte file

    hex_data = str(hex_data)
    hex_data = (hex_data.replace("b'", ""))
    hex_data = (hex_data.replace("'", ""))

    print(hex_data)

    # splitting the previous list in n list of length 6 characters

    long_list = [hex_data[i:i + 6] for i in range(0, len(hex_data), 6)]
    long_list.pop()
    print(long_list)

    # creation of a new list where RGB code will be stored of each sublist previously created

    colorList = []

    # calculation of RGB code of each sublist

    for element in long_list:
        colorList.append(tuple(int(element[i:i + 2], 16) for i in (0, 2, 4)))

    print(colorList)

    print(colorList)

    print(len(colorList))

    # creation of a new image of dimension sqrt(len(colorList)

    img_size = int(math.sqrt(len(colorList)))
    print(img_size)

    img = Image.new("RGB", (img_size, img_size))

    pixels = img.load()

    # filling matrix with the colors

    for x in range(img_size):
        for y in range(img_size):
            pixels[x, y] = colorList[img_size * x + y]

    img.save("new-malware-img.jpg")

    # resizing of the image previously created

    img = Image.open('new-malware-img.jpg')

    # rotate img of 90 degrees

    degrees = -90
    new_img = img.rotate(degrees, expand=True)
    new_img = new_img.resize((300, 300))
    new_img.save("new-malware-img-300-300.jpg", "JPEG", optimize=True)

    # grayscale image conversion

    grayScaleImg = Image.open('new-malware-img-300-300.jpg').convert('LA')
    grayScaleImg.save('new-malware-img-300-300-greyscale.jpg')

    # elimination of elements that are no longer useful

    os.remove('binFile.txt')
    print('binFile has been removed \n')
    os.remove('new-malware-img.jpg')
    print('new-malware-img has been removed \n')
    shutil.rmtree('ZIP', ignore_errors=True)
    print('ZIP folder has been removed \n')


    return render_template('index.html')





if __name__ == '__main__':
    app.run()
