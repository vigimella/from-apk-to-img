# from-apk-to-img

This tool, built thanks flask, allows to get an APK in input and converts it in image. The tool returns in output two kinds of images:

- grayscale image in png extension
- image in RGB in jpg extension 

Files will be stored into the APK_STORAGE with hash code to avoid duplicate applications with a different name.

The idea at the bottom of this tool is to get the dex file stored in APK, converting it into hexadecimal and convert the hex string in colors.

  
