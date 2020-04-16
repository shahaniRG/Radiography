# Code free for public use, just acknowledge use
# Paul Chao, pchao@umich.edu
# March 18, 2020
# Data obtained at APS 2ID-BM
# Data type: tiff stack
# Quick look at radiography data. Use by providing path to the folder, folder name and number of files in folder
# Optionally, change the number of projections to increment, and the file start number (default, should be saved as 0)
# See Al-Cu Example
#
# -h result:
#   -v verbose
#   -vv extra verbose
#   -q quiet
#   --seq_frm
#   --type c,s continious or sequential
#   --save boolean, default=True
#   --overwrite boolean, default=False
#   --increment, integer, default=50 (every ten seconds)
#   --start_frame, integer, default=0 (or first file)
#   --end_frame, integer, default=num_files
#   --time, boolean, default=True
#   --track, boolean, default=False, track radiography intensity

from __future__ import print_function
import numpy as np
import os
import time
import sys
import matplotlib.pyplot as plt
from PIL import Image
from scipy import ndimage
import argparse

## --------------------------------------------------------------------------------------------------
# Read flags with argparse


parser = argparse.ArgumentParser(description='Quick python script to process radiography data',
     epilog="\n Thanks for using! Email me at pchao@umich.edu if there are issues or bugs!")


parser.add_argument("path", help="folder path containing tiffs")
group = parser.add_mutually_exclusive_group()
#group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
group.add_argument("-v", "--verbosity", action="count",  default=0,
                    help="Increase output verbosity. -v for simple. -vv for progress bar.")
parser.add_argument("--delimiter", action='store', default='_',
                    help="File name delimiter. Default _")
parser.add_argument("--file_extension", action='store', default='.tif',
                    help="File extension. Default .tif")
parser.add_argument("--seq_frames", action='store',type=int, default=5,
                    help="During sequential method, the number of frames it will divide by")
parser.add_argument("--mode", action='store', default='c',
                    help="Continious (c) or sequential (s) method")
parser.add_argument("--save", action='store_true', default=True,
                    help="Save files to new directory /path_type_start_end_increment")
#parser.add_argument("--overwrite", action='store_true',default=False,
#                    help="Don't overwrite if already exists")
parser.add_argument("--start_frame", action='store',type=int, default=argparse.SUPPRESS,
                    help="The start frame, will default to be the first file in folder")
parser.add_argument("--end_frame", action='store',type=int, default=argparse.SUPPRESS,
                    help="The end frame, will default to be the last file in the folder")
parser.add_argument("--increment_frame", action='store',type=int, default=100,
                    help="Number of frames to increment by. Default 100 frames.")
parser.add_argument("--time", action='store_true', default=True,
                    help="Time how long the program runs. Default True.")
parser.add_argument("--track", action='store_true',default=False,
                    help="Track intensity from each radiograph. Default False.")
parser.add_argument("--medfilt", action='store',type=int, default=1,
                    help="Size of median filter kernal. Default 1 (not used).")
args = parser.parse_args()

folder_path = args.path

# ----
# Check validity of inputs
if not os.path.isdir(folder_path):
    print('The path specified does not exist')
    sys.exit()

# -- folder atributes
num_files = len(os.listdir(folder_path))
first_file = os.listdir(folder_path)[0]
last_file = os.listdir(folder_path)[-1]

ff = first_file.split(args.delimiter)
ff_ending = ff[-1]
ff_digits = ff_ending.split('.')[0]
ff_num_digits = len(ff_digits)
ff_res = [int(i) for i in ff_digits.split() if i.isdigit()]

lf = last_file.split(args.delimiter)
lf_ending = lf[-1]
lf_digits = lf_ending.split('.')[0]
lf_num_digits = len(lf_digits)
lf_res = [int(i) for i in lf_digits.split() if i.isdigit()]

padding = ff_num_digits
ff_val = int(ff_res[0])
lf_val = int(lf_res[0])

#Check Math
# Do the number of files match last file-first file
if lf_val-ff_val != num_files-1:
    print('Hey, something is wrong with the number of files')
    print('num files: {} -- start file: {} -- end file: {}'.format(num_files,ff_val,lf_val))
    sys.exit()

# set defaults for start or end frame as first and last file
if hasattr(args, 'start_frame'):
    start_frame = args.start_frame
else:
    start_frame = ff_val
if hasattr(args, 'end_frame'):
    end_frame = args.end_frame
else:
    end_frame = lf_val

if end_frame > (num_files+start_frame):
    print('\n**** Turn off choose_end or choose value less than ' + str(num_files))
    sys.exit()

#Print out
if args.verbosity >= 2:
    print('** File Path:' + args.path)
    print('** Number of files: {}'.format(num_files))
    print('** Begin from file {} to {}'.format(start_frame, end_frame))
elif args.verbosity >= 1:
    print('** Begin from file {} to {}'.format(start_frame, end_frame))
else:
    print('** Begin')


#-----
# Begin

timeme = args.time
if timeme:
    start = time.time()

# Import files
print('\n**** Opening: ' + folder_path)

print('\n**** Incrementing by: ' + str(args.increment_frame) + ' projections')

not_filename_len = padding + len(args.file_extension)
filename = first_file[:-not_filename_len]

file_inc = args.increment_frame

# Progress bar
bar_length = 50
tracker = np.zeros(num_files//file_inc)

print('\n**** We will process ' + str((end_frame-start_frame)//file_inc) + ' radiographs')

# Calculate background is continious
if args.mode == 'c':
    print('\n*** in continious mode')
    print('\n*** calculating background from first image')
    selected_filename = filename + str(start_frame).zfill(padding) + args.file_extension
    im_path = os.path.join(folder_path, selected_filename)
    temp_img = Image.open(im_path)
    bkg_img = np.array(temp_img, dtype=np.double)
    if(args.medfilt > 1):
        bkg_img = ndimage.median_filter(bkg_img, args.medfilt)



# Make save directory
if(args.save):
    current_folder = os.path.dirname(folder_path)
    basename = os.path.basename(folder_path)
    folder_name = basename + '_' + args.mode + '_medfilt' + str(args.medfilt) + '_inc' + str(file_inc) + '_start' + str(start_frame) + '_end' + str(end_frame)
    if args.mode == 's':
        folder_name = folder_name + '_seq_inc' + str(args.seq_frames)
    save_folder = os.path.join(current_folder, folder_name)
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    else:
        print('WARNING: Directory already exists')

# Execute Division
#print('\n**** Dividing the {} projections from the first projection: \n'.format(int(num_files//file_inc)) )



if args.mode == 'c': #Continious
    track_count = 0
    print_status = True
    for val in range(start_frame, end_frame, file_inc): #range(start, stop. step)
      # Divide first file from all the other files
      img_filename = filename + str(val).zfill(padding) + args.file_extension
      file_path = os.path.join(folder_path, img_filename)
      img = Image.open(file_path)
      current_img = np.array(img, dtype=np.double)

      if(args.medfilt > 1):
          current_img = ndimage.median_filter(current_img, args.medfilt)

      img_diff = current_img / bkg_img

      if(args.track == True):
          mysum = np.sum(img_diff)
          tracker[track_count] = mysum
      #print(str(mysum))
      # Save results
      if(args.save):
        img_save = Image.fromarray(img_diff)
        img_save.save(save_folder + '/' + filename + 'mode_' + args.mode + '_' + str(val) + '.tiff', 'tiff')
      #print('* saved image #: ' + str(val-file_start))

      if args.verbosity >= 2:
          # Update Progress Bar
          percent = float(val-start_frame) / float(num_files)
          hashes = '#' * int(round(percent * bar_length))
          spaces = '-' * (bar_length - len(hashes))
          sys.stdout.write("\rCompleted: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
          sys.stdout.flush()
      elif args.verbosity >= 1:
        if(print_status):
            print('**** Running, please wait')
            print_status = False
      else:
        if(print_status):
            print('** Running, please wait')
            print_status = False

      track_count = track_count+1
      
elif args.mode == 's': #Sequential
    seq_inc = args.seq_frames
    track_count = 0
    print_status = True
    for val in range(start_frame+file_inc+seq_inc, end_frame, file_inc): #range(start, stop. step)
      # Divide (c)urrent file from (p)revious file
      p_img_filename = filename + str(val-seq_inc).zfill(padding) + args.file_extension
      p_file_path = os.path.join(folder_path, p_img_filename)
      p_img = Image.open(p_file_path)
      prev_img = np.array(p_img, dtype=np.double)

      c_img_filename = filename + str(val).zfill(padding) + args.file_extension
      c_file_path = os.path.join(folder_path, c_img_filename)
      c_img = Image.open(c_file_path)
      current_img = np.array(c_img, dtype=np.double)

      if(args.medfilt > 1):
          current_img = ndimage.median_filter(current_img, args.medfilt)
          prev_img = ndimage.median_filter(prev_img, args.medfilt)

      img_diff = current_img / prev_img

      if(args.track == True):
          mysum = np.sum(img_diff)
          tracker[track_count] = mysum
      #print(str(mysum))
      # Save results
      if(args.save):
        img_save = Image.fromarray(img_diff)
        img_save.save(save_folder + '/' + filename + 'mode_' + args.mode + '_' + str(val) + '.tiff', 'tiff')
      #print('* saved image #: ' + str(val-file_start))

      if args.verbosity >= 2:
          # Update Progress Bar
          percent = float(val-start_frame) / float(num_files)
          hashes = '#' * int(round(percent * bar_length))
          spaces = '-' * (bar_length - len(hashes))
          sys.stdout.write("\rCompleted: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
          sys.stdout.flush()
      elif args.verbosity >= 1:
        if(print_status):
            print('**** Running, please wait')
            print_status = False
      else:
        if(print_status):
            print('** Running, please wait')
            print_status = False

      track_count = track_count+1
else:
    print('ERROR: Please choose either c for continious or s for sequential processing')

if timeme:
    end  = time.time()
    print('\n**** done in ' + str(round((end-start)/60,2)) + ' minutes')

if(args.track == True):
    np.savetxt(save_folder + "Intensity.csv", tracker, delimiter=",")
    print('\n**** saved Intensity csv')
