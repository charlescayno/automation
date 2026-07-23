import os

# input_path = input(">> Import Path: ")
input_path = r"C:\Users\ccayno\Desktop\DER-991\0106\Initial Audible Noise Data 01052023\DER-991 Audible Noise\without epoxy\screenshots"

for filename in os.listdir(input_path):
    print(filename)
    f = filename.split(', .png')
    src = input_path + '/'+ filename
    dest = input_path +'/'+ f[0] + ', without epoxy.png'
    os.rename(src, dest)
    print(f)
