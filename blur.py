import os
from sys import argv
import cv2
import argparse

from numpy import double

arg_parse = argparse.ArgumentParser()
arg_parse.add_argument('--images', action='store', required=True)
arg_parse.add_argument('--labels', action='store', required=True)
arg_parse.add_argument('--blur', action='store', type=int, default=10)
args = arg_parse.parse_args()

images_path = args.images + '\\'
labels_path = args.labels + '\\'
out_path = f'{argv[0]}\\..\\out\\'

if os.path.exists(out_path) == False:
    os.mkdir(out_path)

for file in os.listdir(out_path):
    os.remove(f'{out_path}{file}')

for image_file in os.listdir(images_path):
    image_path = images_path + image_file
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    print(f'\nBLURRING: {image_file}')
    try:
        for line in open(labels_path + image_file.replace('.jpg', '.txt'), 'r').readlines():
            coords = line.split(' ')
            
            # Coordinates from labels
            x = int(double(coords[1]) * width)
            y = int(double(coords[2]) * height)
            w = int(double(coords[3])* width)
            h = int(double(coords[4])* height)
            # print(f'{x} {y} {w} {h}')
            
            x_blur_start = x-w if x-w >= 0 else 0
            y_blur_start = y-h if y-h >= 0 else 0
            x_blur_end = x+w if x+w <= width else width
            y_blur_end = y+h if y+h <= height else height
            
            lp = image[y_blur_start:y_blur_end, x_blur_start:x_blur_end]
            lp = cv2.blur(lp, (args.blur,args.blur))
            image[y_blur_start:y_blur_end, x_blur_start:x_blur_end] = lp
            #image = cv2.GaussianBlur(image, (x - w, y - h), (x + w, y + h), (0,0,0), -1)
        
        # Saving to file
        print(f'SAVING TO out\\{image_file}')
        cv2.imwrite(f'{out_path}{image_file}', image) 
    except FileNotFoundError:
        print(f'LABEL FILE NOT FOUND. SAVING WITH NO BLUR.')
        cv2.imwrite(f'{out_path}{image_file}', image) 
    #cv2.imwrite(f'out\\{image_file}', image) 
