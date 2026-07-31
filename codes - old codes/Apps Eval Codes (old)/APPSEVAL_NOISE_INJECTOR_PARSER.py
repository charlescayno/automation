import os

filelist = os.listdir(os.getcwd())

# # with noise injector
# for file in filelist:
#     filename, extension = os.path.splitext(file)
#     if extension == '.png':
#         temp = filename.split(', ')
#         iout = temp[-1].strip('mA')
#         vout = temp[-2].strip('V')
#         load = temp[0]
#         vin = temp[1]
#         noise = temp[2]
#         resistor_load = temp[3]
#         scope = temp[4]
#         if temp[4] == 'scope1':
#             output_list = [load, vin, noise, resistor_load, vout, iout]
#             print(','.join(output_list))

# without noise injector
for file in filelist:
    filename, extension = os.path.splitext(file)
    if extension == '.png':
        temp = filename.split(', ')
        iout = temp[-1].strip('mA')
        vout = temp[-2].strip('V')
        load = temp[0]
        vin = temp[1]
        # noise = temp[2]
        # resistor_load = temp[3]
        scope = temp[2]
        if temp[2] == 'scope1':
            output_list = [load, vin, vout, iout]
            print(','.join(output_list))