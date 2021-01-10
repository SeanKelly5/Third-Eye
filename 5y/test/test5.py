import os  
os.path.isfile('./file.txt')
if True:
    with open("inpt.data","r") as fn:
    listLines = fn.readlines()

    for fileNumber, line in enumerate(listLines):
    with open("input{0}.data".format(fileNumber), "w") as fileOutput:
        fileOutput.write(line)

if False:
