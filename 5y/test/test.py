file = request.files['demofile2.txt']

def check_and_rename(file, add=0):
    original_file = file
    if add != 0:
        split = file.split(".")
        part_1 = split[0] + "_" + str(add)
        file = ".".join([part1, split[1]])
    if not os.path.isfile(file):
        # save here
    else:
        check_and_rename(original_file, add+=1)
