count = 1


f = open("image.txt", "r")
print(f.read(count))

img_name = "ImageSave_{}.png".format(count)
print("{} written!".format(img_name))
count += 1
f= open("image.txt", "w")
f.write(str(count))
f.close()
