import os, sys
from typing import List, Text, Tuple

Line = List[int]
Layer = List[Line]
Image = List[Layer]

def parse_image(data, width, height):
    # type: (Text, int, int) -> Image
    '''
    Builds an image structure from a string.
    '''
    nb_pixels = width * height
    if len(data) % nb_pixels != 0:
        raise Exception('Image corrupted : size is not a multiple of the pixel count')
    image = []
    for i in range(0, len(data) // nb_pixels):
        image.append([])
        for y in range(0, height):
            image[i].append([])
            for x in range(0, width):
                address = i * nb_pixels + y * width + x
                image[i][y].append(int(data[address:address + 1]))
    return image


def count_in_layer(layer, value):
    # type: (Layer, int) -> int
    '''
    Counts the number of pixels for a given value in a layer.
    '''
    res = 0
    for line in layer:
        for pixel in line:
            if pixel == value:
                res += 1
    return res


def merge_layers(layer_top, layer_bottom):
    # type: (Layer, Layer) -> Layer
    '''
    Merges two layers.
    '''
    result = []
    for line_top, line_bottom in zip(layer_top, layer_bottom):
        result_line = []
        for pixel_top, pixel_bottom in zip(line_top, line_bottom):
            result_line.append(pixel_top if pixel_top != 2 else pixel_bottom)
        result.append(result_line)
    return result


def merge_image(image):
    # type: (Image) -> Layer
    '''
    Merges all the layers from an image.
    '''
    result = image[0]
    for layer in image[1:]:
        result = merge_layers(result, layer)
    return result


def display_image(image):
    # type: (Image) -> None
    '''
    Display an image in text mode.
    '''
    for line in merge_image(image):
        for pixel in line:
            if pixel == 0:
                sys.stdout.write('█')
            else:
                sys.stdout.write(' ')
        print('')


def find_layer_with_min_count(image, value):
    # type: (Image, int) -> Tuple[Layer, int]
    '''
    Finds which layer in an image has the least pixel with a given value.
    '''
    res_layer = None
    res_count = sys.maxsize
    for layer in image:
        count = count_in_layer(layer, value)
        if count < res_count:
            res_count = count
            res_layer = layer
    return res_layer, res_count

def checks_d8p2():
    assert merge_image([[[0, 2], [2, 2]], [[1, 1], [2, 2]], [[2, 2], [1, 2]], [[0, 0], [0, 0]]]) == [[0, 1], [1, 0]]

def day8_res1(image):
    layer = find_layer_with_min_count(image, 0)[0]
    return count_in_layer(layer, 1) * count_in_layer(layer, 2)

def run():
    with open(os.path.dirname(__file__) + os.sep + 'input.txt', 'r') as in_file:
        image = parse_image(in_file.read().strip(), 25, 6)

    d8p1 = day8_res1(image)
    print(f'Day 8, Part 1 : {d8p1}')  # 1792

    checks_d8p2()

    print('Day 8, Part 2 : ')  # LJECH
    display_image(image)

if __name__ == '__main__':
    run()
