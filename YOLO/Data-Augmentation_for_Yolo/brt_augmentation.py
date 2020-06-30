# -*- coding: utf-8 -*-
import os
import imgaug as ia
from imgaug import augmenters as iaa
import scipy.misc
import shutil
import imageio

path = './highTargets'

augmentation_path = './highTargets/final/'

for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".jpg"):
            for light in range(6):
                jpg_path = path + "/" + file

                image = imageio.imread(jpg_path, as_gray=False, pilmode="RGB")

                if light < 5:
                    seq = iaa.Sequential([
                            iaa.Multiply( 1 - 0.15 * (light) )
                    ])
                else:
                    seq = iaa.Sequential([
                            iaa.Multiply( 1 + 0.3 * (light-4) )
                    ])
                    

                image_aug = seq.augment_images([image])[0]

                new_jpg_path = augmentation_path + file[:-4] + "_%d"%light + ".jpg"
            

                imageio.imsave(new_jpg_path, image_aug)          
            


