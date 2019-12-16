import os
import subprocess as sp
import time
os.system("clear")
print("""
   ╲    ╱
   ╱▔▔▔▔╲
  ┃ ▇  ▇ ┃         +-----|╲
╭╮┣━━━━━━┫╭╮       |     |_╲
┃┃┃      ┃┃┃  ===> | .APK  | 
╰╯┃      ┃╰╯       |       |
  ╰┓┏━━┓┏╯         +-------+
   ╰╯  ╰╯
---------------------------------------
ANDRO STRIPPER v1.0
=======================================
https://github.com/Saket-Upadhyay/andro-stripper 
| Dec 2019
| For *NIX Systems

* This scripts assumes that we have adb installed and working in host machine.
* DO NOT remove device during Extraction
=======================================
""")

print("Initialising ADB ...")
os.system("adb kill-server")
os.system("adb usb")
print("DONE ... Waiting for 5 seconds to let devices connect")
time.sleep(5.0)
process=sp.Popen(["adb","devices"],stdout=sp.PIPE,stderr=sp.PIPE)
stdout,stderr=process.communicate()

stdout=stdout.decode("utf8")
stdout=stdout.split('\n')
stdout.pop()
stdout.pop()
numberofdevices=len(stdout)-1

print("Total number of devices found = "+str(numberofdevices))

for i in range(1,numberofdevices+1):
    print(str(i)+" - "+str(stdout[i]))

print("select the device to Extract applications from - ")
opt=int(input("> "))

selected_device=stdout[i]

selected_device=selected_device.split('\t')
selected_device=selected_device[0]
selected_device=str(selected_device)
print("SELECTED DEVICE = "+selected_device)
print("================================================")
print("EXTRACTING DEVICE INFORMATION")
print("================================================")
os.system("adb -s "+str(selected_device)+" shell getprop ro.product.manufacturer")
os.system("adb -s "+str(selected_device)+" shell getprop ro.product.model")
os.system("adb -s "+str(selected_device)+" shell getprop ro.build.id")
os.system("adb -s "+str(selected_device)+" shell getprop ro.serialno")
os.system("adb -s "+str(selected_device)+" shell getprop ro.hw.country")
os.system("adb -s "+str(selected_device)+" shell getprop ro.product.cpu.abilist")
os.system("adb -s "+str(selected_device)+" shell getprop ro.config.cpu_info_display")
print("\n================================================")
time.sleep(2)
process_getapklist=sp.Popen(["adb","-s",selected_device,"shell","pm","list","packages"],stdout=sp.PIPE,stderr=sp.PIPE)
stdout,stderr=process_getapklist.communicate()
stdout=stdout.decode("utf8")

listapk=stdout.split('\n')
print("Total Packages found = "+str(len(listapk)))
print("\nDumping Packages ...")
with open("packageDump",'w+') as file:
    for element in listapk:
        element=element[8:]
        file.write(element)
        file.write('\n')

print("Extracting Package Path from the device...")

with open("packageDump","r") as file:
    path_read=file.read()
    path_read=path_read.split('\n')
    path_read.pop()
    path_read.pop()
    pathfile=open("packagePathDump","w+")
    enum=0
    for path_selection in path_read:
        print("[{}]\t{} :".format(enum,path_selection.strip()),end='')
        # process_getapklist=sp.Popen(["adb","-s",selected_device,"shell","pm","path",str(path_selection)],stdout=sp.PIPE,stderr=sp.PIPE)
        process_getapklist=sp.Popen(["adb","-s","XUV9X18501G03393","shell","pm","path",str(path_selection)],stdout=sp.PIPE,stderr=sp.PIPE)
        stdout,stderr=process_getapklist.communicate()
        stdout=stdout.decode("utf8")
        stdout=stdout.split('\n')
        apk_path=stdout[0]
        apk_path=apk_path[8:]
        print(apk_path)
        pathfile.write(apk_path)
        pathfile.write('\n')
        enum+=1
    pathfile.close()

print("Extracting Packages APK from the device...")

with open("packagePathDump","r") as file:
    path_read=file.read()
    path_read=path_read.split('\n')
    path_read.pop()
    path_read.pop()
    enuma=int(1)
    tol=len(path_read)
    for path_selection in path_read:
        print(" [ "+str(enuma)+" | "+str(tol)+" ]   \n")
        if 'base.apk' in path_selection:
            os.system("adb -s "+str(selected_device)+" pull "+str(path_selection.strip())+" ./ExtractedApk/"+str(enuma)+".apk")
        else:
            os.system("adb -s "+str(selected_device)+" pull "+str(path_selection.strip())+" ./ExtractedApk/")
        enuma+=1