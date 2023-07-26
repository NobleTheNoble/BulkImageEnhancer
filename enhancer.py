import os
import multiprocessing
import glob
from PIL import ImageEnhance
from PIL import Image
from argparse import ArgumentParser
import datetime

def print_with_timestamp(message, num_images_processed=None):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%H:%M:%S.%f")
    
    if num_images_processed is not None:
        message += f" ({num_images_processed} images processed)"
    
    log_message = f"[{formatted_time}] {message}"
    print(log_message)
    with open('logs.txt', 'a') as file:
        file.write(log_message + '\n')
        file.close()

def init_images(source):
    _list = []

    for img in glob.glob(source + "/*.png"):
        _list.append(os.path.basename(img)) 
    
    for img in glob.glob(source + "/*.jpeg"):
        _list.append(os.path.basename(img)) 
    
    for img in glob.glob(source + "/*.jpg"):
        _list.append(os.path.basename(img))        

    return _list

def process(path, source, output, brightness, contrast, sharpness):
    print_with_timestamp(f"Starting with image {path} in folder {source}")
    
    img = Image.open(f"{source}/{path}")

    brightness_enhancer = ImageEnhance.Brightness(img)
    img = brightness_enhancer.enhance(brightness)
    
    sharpness_enhancer = ImageEnhance.Sharpness(img)
    img = sharpness_enhancer.enhance(sharpness)
    
    contrast_enhancer = ImageEnhance.Contrast(img)
    img = contrast_enhancer.enhance(contrast)
    
    img.save(f"{output}/{path}")
    
    print_with_timestamp(f"Done with image {path}")
    

def multiprocess(source, output, time, brightness, contrast, sharpness, threads):
    
    if os.path.exists(source):
        paths = init_images(source)
        processed_images = multiprocessing.Value('i', 0)

        def process_callback(result):
            with processed_images.get_lock():
                processed_images.value += 1

        with multiprocessing.Pool(threads) as pool:
            for path in paths:
                pool.apply_async(func=process, args=[path, source, output, brightness, contrast, sharpness], callback=process_callback)

            pool.close()
            pool.join()

            print_with_timestamp("All images processed.", processed_images.value)
    
        

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