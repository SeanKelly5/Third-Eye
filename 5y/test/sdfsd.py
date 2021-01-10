number = 0
if my_file.exists(Ebola):
    # path exists
  f = open("demofile2.txt", "w")
  f.write(str(number+1))
  f.close()
else:

#open and read the file after the appending:
  f = open("demofile2.txt", "r")
  print(f.read())

