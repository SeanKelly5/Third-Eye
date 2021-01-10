import os
count = 1
os.path.isfile('demofile2.txt')
if True:
    print("yes")
    f = open("demofile2.txt", "a")
    vid_name = "ImageSave_{}.png".format(count)
    print("{} written!".format(vid_name))
    count += 1
    f.write(str(count))
    

    
if False:
    print("no")
