import os
import re
import shutil
from powi.equipment import path_maker

def folder_path_handler():
    """This function handles where the folder path should be used"""
    global folder_path

    change_folder = input("Do you want to change the default folder? (y/n) ").lower()
    if change_folder == 'y':
        folder_path = None
    else:
        folder_path = None
        try:
            with open("last_folder.txt", "r") as f:
                folder_path = f.read()
        except FileNotFoundError:
            pass

    if not folder_path or not os.path.exists(folder_path):
        folder_path = input("Enter folder path: ")
        with open("last_folder.txt", "w") as f:
            f.write(folder_path)
    else:
        print(f"Searching in folder: {folder_path}")

def file_sorter():
    filelist = os.listdir(folder_path)

    for file in filelist:
        if re.search('USDT', file):
            print(file)
            file_source = folder_path + "/" + file
            file_destination_folder = folder_path + "/trades/"
            path_maker(file_destination_folder)
            file_destination = file_destination_folder + file
            print(file_destination)
            # input()
            shutil.move(file_source, file_destination)

def file_desorter():
	print()
	desorter_counter = 0
	total_desorter_counter = 0

	filelist = os.listdir(folder_path)
	# print(filelist)

	for file in filelist:
		
		filename, extension = os.path.splitext(file)
		src = folder_path + '/' + file
		
		if len(extension) == 0:

			srclist = os.listdir(src) # list of files inside the secondary folder_path
			print(srclist)
			
			for f in srclist:
				# define the location of every file in the secondary folder_path
				new_src = src + '/' + f
				dest = folder_path
				file_loc = dest + '/' + f

				if (f in filelist):
					new_src_file_size = os.stat(new_src).st_size
					file_size = os.stat(file_loc).st_size

					print('new_src_file_size: ' + str(new_src_file_size*1e-6) + 'MB')
					print('dest file size: ' + str(file_size*1e-6) + 'MB')

					if new_src_file_size == file_size:
						print('same')
						shutil.move(os.path.join(src, f), os.path.join(dest, f))
						print(f + ' was moved.')
						desorter_counter += 1
						total_desorter_counter += 1
				else:
					shutil.move(new_src, dest)
					print(f + ' was moved to:' + dest)
					desorter_counter += 1
					total_desorter_counter += 1		
	a = 0
	while(desorter_counter > 0):
		
		# folder_path = os.getcwd()
		filelist = os.listdir(folder_path)
		print(filelist)

		for file in filelist:
			
			filename, extension = os.path.splitext(file)
			src = folder_path + '/' + file
			
			if len(extension) == 0:

				srclist = os.listdir(src) # list of files inside the secondary directory
				
				for f in srclist:
					# define the location of every file in the secondary directory
					new_src = src + '/' + f
					dest = folder_path
					file_loc = dest + '/' + f

					if (f in filelist):
						new_src_file_size = os.stat(new_src).st_size
						file_size = os.stat(file_loc).st_size

						print('new_src_file_size: ' + str(new_src_file_size*1e-6) + 'MB')
						print('dest file size: ' + str(file_size*1e-6) + 'MB')

						if new_src_file_size == file_size:
							print('same')
							shutil.move(os.path.join(src, f), os.path.join(dest, f))
							print(f + ' was moved.')
							desorter_counter -= 1
							total_desorter_counter += 1
					else:
						shutil.move(new_src, dest)
						print(f + ' was moved to:' + dest)
						desorter_counter -= 1
						total_desorter_counter += 1
		a += 1
		if a == 10:
			break
	print()
	print( 'total files desorted: ' + str(total_desorter_counter))

if __name__ == '__main__':
    folder_path_handler()

    
    file_desorter()
    # file_sorter()
