"""
Author: Giovanni Ciaramella

Date: February 14th 2021

Description: This tool gets an APK file in input, extracts from it dex file and converts it both in image in grayscale
and color image. The APK files, after the upload,  will be stored into the APK_STORAGE with hash code to avoid duplicate
applications with a different name.

IF YOU USE THIS TOOL PLEASE QUOTE ME :)

"""

import os, zipfile, math, codecs, shutil, hashlib

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
    target = os.path.join(APP_ROOT, 'apk_to_img_files')
    print(target)

    # if folder apk_to_img_files doesn't exist it will be created
    if not os.path.isdir(target):
        os.mkdir(target)
    print("'apk_to_img_files' folder has been created")

    # creation of a new folder where apk files will be stored
    apkStorage = os.path.join(APP_ROOT, 'apk_to_img_files/APK_STORAGE')

    # if folder APK_STORAGE doesn't exist it will be created
    if not os.path.isdir(apkStorage):
        os.mkdir(apkStorage)
    print("'APK_STORAGE' folder has been created")

    # going to store file previously uploaded into ZIP folder
    # going to store file previously uploaded into APK_STORAGE folder

    for file in request.files.getlist('file'):
        # changing the extension of the file previously from APK to ZIP

        fileName = 'apk-to-convert.zip'
        destination = "\\".join([target, fileName])
        print(destination)
        file.save(destination)

    print("File has been stored inside the folder")

    # copy app into APK_STORAGE changing the extension from .zip to .apk

    filePath = os.path.join(target, 'apk-to-convert.zip')
    newPath = shutil.copy(filePath, apkStorage)
    new_file_name = apkStorage + '/apk-to-convert.apk'
    os.rename(newPath, new_file_name)

    # hash code of APK to avoid storing duplicate application with a different name

    hashName = hashlib.md5(open(new_file_name, 'rb').read()).hexdigest()

    new_file_hash_name = apkStorage + '/' + hashName + '.apk'

    # check if APK already exists in APK_STORAGE. If yes it will be removed
    # else it will be renamed with the hash code generated

    if not os.path.isfile(new_file_hash_name):
        os.rename(new_file_name, new_file_hash_name)
    else:
        os.remove(new_file_name)
        print('File already exists')

    # going to unzip file previously uploaded in 'unzipped_files' folder
    unZipFolder = os.path.join(target, 'unzipped_files')

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

    source = os.path.join(target, 'unzipped_files/classes.dex')

    copyfile(source, 'binFile.txt')

    byteFile = open('binFile.txt', 'rb').read()

    # conversion from binary to hexadecimal
    hex_data = codecs.encode(byteFile, "hex_codec")

    # deleting leftovers of byte file

    hex_data = str(hex_data)
    hex_data = (hex_data.replace("b'", ""))
    hex_data = (hex_data.replace("'", ""))

    # splitting the previous list in n list of length 6 characters

    long_list = [hex_data[i:i + 6] for i in range(0, len(hex_data), 6)]
    long_list.pop()

    # creation of a new list where RGB code will be stored of each sublist previously created

    colorList = []

    # calculation of RGB code of each sublist

    for element in long_list:
        colorList.append(tuple(int(element[i:i + 2], 16) for i in (0, 2, 4)))

    # creation of a new image of dimension sqrt(len(colorList)

    img_size = int(math.sqrt(len(colorList)))
    print(img_size)

    img = Image.new("RGB", (img_size, img_size))

    pixels = img.load()

    # filling matrix with the colors

    for x in range(img_size):
        for y in range(img_size):
            pixels[x, y] = colorList[img_size * x + y]

    # creation of a new directory where images will be saved

    imgFolder = os.path.join(target, 'images')

    # if folder images doesn't exist it will be created
    if not os.path.isdir(imgFolder):
        os.mkdir(imgFolder)

    img.save(imgFolder + "/new-malware-img.jpg")

    # resizing of the image previously created

    img = Image.open(imgFolder + '/new-malware-img.jpg')

    # rotate img of 90 degrees

    degrees = -90
    new_img = img.rotate(degrees, expand=True)
    new_img = new_img.resize((300, 300))
    new_img.save(imgFolder + "/new-malware-img-300-300.jpg", "JPEG", optimize=True)

    # grayscale image conversion

    grayScaleImg = Image.open(imgFolder + '/new-malware-img-300-300.jpg').convert('LA')
    grayScaleImg.save(imgFolder + '/new-malware-img-300-300-greyscale.png')

    # elimination of elements that are no longer useful

    os.remove('binFile.txt')
    print('binFile has been removed \n')
    os.remove(imgFolder + '/new-malware-img.jpg')
    print('new-malware-img has been removed \n')
    shutil.rmtree(unZipFolder, ignore_errors=True)
    print('unzipped_files folder has been removed \n')
    os.remove(filePath)
    print('apk-to-convert.zip has been removed \n')

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
