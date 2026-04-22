from os import listdir
from os.path import isfile, join

mypath = input(">> Enter pathname: ")
fdrive_path = input(">> Enter fdrive path: ")
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# open file in write mode
with open(f'{mypath}/fdrive_link.txt', 'w') as fp:
    for i in onlyfiles:
        link = fdrive_path + '/' + i
        print(link)
        fp.write("%s\n\n" % link)
    print('Done')
