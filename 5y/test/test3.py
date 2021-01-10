count = 1

with open("inpt.data","r") as fn:
    listLines = fn.readlines()

for fileNumber, line in enumerate(listLines):
    with open("input{}.data".format(count), "w") as fileOutput:
        count += 1
        fileOutput.write(str(count))



      #img_name = "ImageSave_{}.png".format(image_Counter)
      #cv2.imwrite(img_name, frame)
      #print("{} written!".format(img_name))
      #image_Counter += 1
      #f = open("image.txt", "w")
      #f.write(str(image_Counter))
      #f.close()
