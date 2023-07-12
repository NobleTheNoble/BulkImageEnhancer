import time
from time import sleep
from threading import Thread
from argparse import ArgumentParser
import random
import os
from concurrent.futures import ThreadPoolExecutor
from threading import Event
import multiprocessing

parser = ArgumentParser(description="Bulk Image Enhancer using PIL", epilog="PIL Source code for enhancements can be found at: https://pillow.readthedocs.io/en/stable/_modules/PIL/ImageEnhance.html")

parser.add_argument('source', help='Image Folder to enhance')
parser.add_argument('output', help='Folder for the finished images')
parser.add_argument('time', type=int, help='Enhancing time in minutes')

args = parser.parse_args()

def init_images():
    
    return list(range(10))
    '''
    images = []
    
    for i in range(100):
        images.append(f"image-{i}.jpg")

    return images
    '''
    
def process(i):
    print(f"starting with image {i}")
    sleep(random.randint(3, 6))
    print(f"done with image {i}")
    
if __name__ == '__main__':
    
    if os.path.exists(args.source):
        pool = multiprocessing.Pool(2)
        manager = multiprocessing.Manager()

        start_time = time.perf_counter()

        counter = 0

        for i in range(100):
            pool.apply_async(process, args=[i])

        #start timer
        while True:
            sleep(1)
            
            #enable timer
            #print(round(time.perf_counter() - start_time))
            
            if round(time.perf_counter() - start_time) == args.time * 60:
                break
            
        pool.terminate()
        pool.join()
    
        
    

    
    
    
    