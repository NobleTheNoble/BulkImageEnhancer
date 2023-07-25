import os
import random
import multiprocessing
import threading
import time
import glob
from PIL import ImageEnhance
from PIL import Image
from argparse import ArgumentParser
from time import sleep

def init_images(source):
    
    _list = []
    #return list(range(10))
    for img in glob.glob(source + "/*.png"):
        _list.append(os.path.basename(img)) 
    
    for img in glob.glob(source + "/*.jpeg"):
        _list.append(os.path.basename(img)) 
    
    for img in glob.glob(source + "/*.jpg"):
        _list.append(os.path.basename(img))        

    return _list

def process(path, source, output, brightness, contrast, sharpness):
    print(f"starting with image {path} in folder {source}")
    #sleep(random.randint(1, 3))
    
    img = Image.open(f"{source}/{path}")

    # enhance brightness...
    brightness_enhancer = ImageEnhance.Brightness(img)
    img = brightness_enhancer.enhance(brightness)
    
    sharpness_enhancer = ImageEnhance.Sharpness(img)
    img = sharpness_enhancer.enhance(sharpness)
    
    contrast_enhancer = ImageEnhance.Contrast(img)
    img = contrast_enhancer.enhance(contrast)
    
    img.save(f"{output}/{path}")
    
    print(f"done with image {path}")
    

def multiprocess(source, output, time, brightness, contrast, sharpness, threads):
    
    if os.path.exists(source):
        paths = init_images(source)

        with multiprocessing.Pool(threads) as pool:
            for path in paths:
                result = pool.apply_async(func=process, args=[path, source, output, brightness, contrast, sharpness])
            
            timer = threading.Timer(time * 60, pool.terminate)
            timer.start()
            timer.join()
        
            pool.join()
    
        

if __name__ == '__main__':
    
    parser = ArgumentParser(description="Bulk Image Enhancer using PIL", epilog="PIL Source code for enhancements can be found at: https://pillow.readthedocs.io/en/stable/_modules/PIL/ImageEnhance.html")

    #required
    parser.add_argument('source', help='Image Folder to enhance')
    parser.add_argument('output', help='Folder for the finished images')
    parser.add_argument('time', type=float, help='Enhancing time in minutes')

    #optional 
    parser.add_argument('-c','--contrast', type=float, help='Adjust image contrast. 0.0 gives a solid grey image, 1.0 retains the original.', default=1.0)
    parser.add_argument('-b', '--brightness', type=float, help='Adjust image brightness. 0.0 gives a black image, 1.0 retains the original.', default=1.0)
    parser.add_argument('-s', '--sharpness', type=float, help='Adjust image sharpness. 0.0 gives a blurred image, 1.0 retains the original.', default=1.0)

    parser.add_argument('-t', '--threads', type=int, help='Number of threads to use.', default=4)


    args = parser.parse_args()
    
    multiprocess(args.source, args.output, args.time, args.brightness, args.contrast, args.sharpness, args.threads)
    
   
        
    