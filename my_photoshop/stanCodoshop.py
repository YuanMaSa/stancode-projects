"""
File: stanCodoshop.py
----------------------------------------------
SC101_Assignment3
Adapted from Nick Parlante's
Ghost assignment by Jerry Liao.

-----------------------------------------------

TODO:
"""

import os
import sys
import time
from simpleimage import SimpleImage


def get_pixel_dist(pixel, red, green, blue):
    """
    Returns the color distance between pixel and mean RGB value

    Input:
        pixel (Pixel): pixel with RGB values to be compared
        red (int): average red value across all images
        green (int): average green value across all images
        blue (int): average blue value across all images

    Returns:
        dist (int): color distance between red, green, and blue pixel values

    """
    return ((red-pixel.red)**2+(green-pixel.green)**2+(blue-pixel.blue)**2)**0.5

def get_average(pixels):
    """
    Given a list of pixels, finds the average red, blue, and green values

    Input:
        pixels (List[Pixel]): list of pixels to be averaged
    Returns:
        rgb (List[int]): list of average red, green, blue values across pixels respectively

    Assumes you are returning in the order: [red, green, blue]

    """
    red_avg = sum([x.red for x in pixels])//len(pixels)
    green_avg = sum([x.green for x in pixels])//len(pixels)
    blue_avg = sum([x.blue for x in pixels])//len(pixels)
    return [red_avg, green_avg, blue_avg]

def get_best_pixel(pixels):
    """
    Given a list of pixels, returns the pixel with the smallest
    distance from the average red, green, and blue values across all pixels.

    Input:
        pixels (List[Pixel]): list of pixels to be averaged and compared
    Returns:
        best (Pixel): pixel closest to RGB averages

    """
    new_dict = {}
    avg_red = get_average(pixels)[0]
    avg_green = get_average(pixels)[1]
    avg_blue = get_average(pixels)[-1]

    for pix in pixels:
        # append key (distance in string type) and value (object) to new dictionary
        new_dict[str(get_pixel_dist(pix, avg_red, avg_green, avg_blue))] = pix
    # sort the value and retrieve the smallest one
    sorted_list = sorted(new_dict.items(), key=lambda x: float(x[0]))
    return sorted_list[0][1]


def solve(images):
    """
    Given a list of image objects, compute and display a Ghost solution image
    based on these images. There will be at least 3 images and they will all
    be the same size.

    Input:
        images (List[SimpleImage]): list of images to be processed
    """
    # print(images)
    width = images[0].width
    height = images[0].height
    result = SimpleImage.blank(width, height)
    ######## YOUR CODE STARTS HERE #########
    # Write code to populate image and create the 'ghost' effect

    for x in range(width):
        for y in range(height):
            # loop (x,y) in each image
            pixel_lst = [img.get_pixel(x, y) for img in images]
            best_pixel = get_best_pixel(pixel_lst)
            # assign new value
            result.get_pixel(x, y).red = best_pixel.red
            result.get_pixel(x, y).green = best_pixel.green
            result.get_pixel(x, y).blue = best_pixel.blue

    ######## YOUR CODE ENDS HERE ###########
    print("Displaying image!")
    result.show()
    # testing command below (for TA)
    # python3 stanCodoshop.py clock-tower    --> about 10 sec
    # python3 stanCodoshop.py hoover         --> about 8 sec
    # python3 stanCodoshop.py math-corner    --> about 20 sec
    # python3 stanCodoshop.py monster        --> about 60 sec

def jpgs_in_dir(dir):
    """
    (provided, DO NOT MODIFY)
    Given the name of a directory, returns a list of the .jpg filenames
    within it.

    Input:
        dir (string): name of directory
    Returns:
        filenames(List[string]): names of jpg files in directory
    """
    filenames = []
    for filename in os.listdir(dir):
        if filename.endswith('.jpg'):
            filenames.append(os.path.join(dir, filename))
    return filenames


def load_images(dir):
    """
    (provided, DO NOT MODIFY)
    Given a directory name, reads all the .jpg files within it into memory and
    returns them in a list. Prints the filenames out as it goes.

    Input:
        dir (string): name of directory
    Returns:
        images (List[SimpleImages]): list of images in directory
    """
    images = []
    jpgs = jpgs_in_dir(dir)
    for filename in jpgs:
        print("Loading", filename)
        image = SimpleImage(filename)
        images.append(image)
    return images


def main():
    # (provided, DO NOT MODIFY)
    args = sys.argv[1:]
    # We just take 1 argument, the folder containing all the images.
    # The load_images() capability is provided above.
    images = load_images(args[0])
    solve(images)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(
        "total running time of function : --- %s seconds ---"
        % (time.time() - start_time)
    )
