import math
from collections import Counter
from random import random
from collections import Counter


from PIL import Image, ImageDraw
import numpy as np


def main(image):
    orig_image = Image.open(image)
    width, height = orig_image.size
    image_ratio = round(width / height, 1)

    if image_ratio == round(156 / 195, 1):
        a = choose_size(orig_image, width, height, image, 4680, 5850, 156, 195)
        # create_mosaic_filtered()
    elif image_ratio == round(117 / 165, 1):
        choose_size(orig_image, width, height, image, 3510, 4950, 117, 165)

    elif image_ratio == round(77 / 120, 1):
        choose_size(orig_image, width, height, image, 2310, 3600, 77, 120)
    else:
        print(f'not ifs {image_ratio.__round__(1)}')
        print(f'image_ratio:{(4726 / 5908).__round__(1)}')
        print(f'image_ratio:{(3532 / 4981).__round__(1)}')
        print(f'image_ratio:{(2340 / 3621).__round__(1)}')


def choose_size(original_image, original_width, original_height, new_image, new_width, new_height, tiles_width, tiles_height):
    if original_width % tiles_width == 0 and original_height % tiles_height == 0:
        create_mosaic(original_image, tiles_width, tiles_height)
    elif original_image.size > (new_width, new_height):
        create_mosaic(crop_image(new_image), tiles_width, tiles_height)
    else:
        create_mosaic(resize_image(new_image, new_width, new_height), tiles_width, tiles_height)




def calculate_color_preferences(original_image):
    color_counter = Counter(original_image.getdata())
    total_pixels = original_image.width * original_image.height

    color_preferences = {}
    for color, count in color_counter.items():
        color_preferences[color] = count / total_pixels

    return color_preferences


def create_mosaic(original_image, tiles_width, tiles_height):
    width, height = original_image.size
    tile_size = height / tiles_height
    mosaic_image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(mosaic_image)


    # ------------
    color_set = color_set_disco()

    # Словарь для отслеживания использования каждого цвета
    color_usage = {tuple(color): 0 for color in color_set}

    for y in range(tiles_height):
        for x in range(tiles_width):
            box = (int(x * tile_size), int(y * tile_size), int((x + 1) * tile_size), int((y + 1) * tile_size))
            region = original_image.crop(box)
            average_color = tuple(int(sum(color) / len(color)) for color in zip(*region.getdata()))

            closest_color = min(color_set_disco(), key=lambda c: np.linalg.norm(np.array(c) - np.array(average_color)))
            # Увеличение счетчика использования выбранного цвета на 20%
            color_usage[tuple(closest_color)] += 1

            draw.rectangle(box, fill=tuple(closest_color), outline="grey")

    # Находим цвет, который нужно увеличить на 20%
    color_to_increase = max(color_usage, key=color_usage.get)
    # Увеличиваем количество использований этого цвета на 20%
    color_usage[color_to_increase] = int(color_usage[color_to_increase] * 1)

    mosaic_image.show()
    print(color_usage)

    # Создаем мозаичное изображение, учитывая новые значения цветов
    mosaic_image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(mosaic_image)
    for y in range(tiles_height):
        for x in range(tiles_width):
            box = (int(x * tile_size), int(y * tile_size), int((x + 1) * tile_size), int((y + 1) * tile_size))
            region = original_image.crop(box)
            average_color = tuple(int(sum(color) / len(color)) for color in zip(*region.getdata()))

            closest_color = min(color_set, key=lambda c: np.linalg.norm(np.array(c) - np.array(average_color)))
            # Используем обновленное количество использований цвета
            if tuple(closest_color) == color_to_increase:
                draw.rectangle(box, fill=tuple(closest_color), outline="grey")
                color_usage[color_to_increase] -= 1
                if color_usage[color_to_increase] <= 0:
                    # Если использования закончились, удаляем цвет из набора
                    color_set_disco().remove(list(color_to_increase))

    mosaic_image.show()
    # return mosaic_image
# def create_mosaic_filtered(original_image):
#     for y in range(tiles_height):
#         for x in range(tiles_width):
#             box = (int(x * tile_size), int(y * tile_size), int((x + 1) * tile_size), int((y + 1) * tile_size))
#             original_image.crop(box)
#             # average_color = tuple(sum(color) / len(color) for color in zip(*regionn.getdata()))
#             # print(f'{average_color=}')
#             # closest_color = tuple(min(color_set_disco(), key=lambda c: np.linalg.norm(np.array(c) - np.array(average_color))))
#             # print(f'{closest_color=}')
#             a = calculate_color_preferences(mosaic_image)
#             # Определяем вероятности выбора цвета на основе предпочтений по использованию каждого цвета
#             color_probabilities = [a.get(closest_color, 0)]
#
#             # Увеличиваем долю использования первого цвета на 15%
#             if closest_color == list(a.keys())[0]:
#                 color_probabilities[0] *= 2
#
#             # Случайным образом выбираем цвет в соответствии с вероятностями
#             # chosen_color = closest_color  # В данном случае мы просто используем средний цвет блока
#             # print(f'{closest_color=}')
#             draw.rectangle(box, fill=tuple(closest_color), outline="grey")
#
#     mosaic_image.show()








# Пример использования:
# original_image = Image.open("original_image.jpg")
# create_mosaic(original_image, tiles_width, tiles_height)


def manhattan_distance(color1, color2):
    return sum(abs(c1 - c2) for c1, c2 in zip(color1, color2))


def euklid_distance(color1, color2):
    return np.linalg.norm(np.array(color1) - np.array(color2))


def cosine_distance(color1, color2):
    dot_product = color1[0] * color2[0] + color1[1] * color2[1] + color1[2] * color2[2]
    magnitude1 = math.sqrt(color1[0] ** 2 + color1[1] ** 2 + color1[2] ** 2)
    magnitude2 = math.sqrt(color2[0] ** 2 + color2[1] ** 2 + color2[2] ** 2)
    if magnitude1 == 0 or magnitude2 == 0:
        return 0  # Возвращаем 0, если одна из длин векторов равна нулю
    return dot_product / (magnitude1 * magnitude2)


def chebyshev_distance(color1, color2):
    return max(abs(color1[0] - color2[0]), abs(color1[1] - color2[1]), abs(color1[2] - color2[2]))


def color_set_disco():
    colors = [
        [254, 249, 149],  # #fef995
        [242, 181, 32],  # #f2b520
        [234, 75, 133],  # #ea4b85
        [10, 170, 226],  # #0aaae2
        [95, 72, 146],  # #5f4892
        [0, 0, 0],  # #000000
    ]
    return colors


def color_set_bw():
    colors = [
        [255, 255, 255],  # #ffffff
        [191, 191, 191],  # #bfbfbf
        [127, 127, 127],  # #7f7f7f
        [63, 63, 63],  # #3f3f3f
        [0, 0, 0],  # #000000
    ]
    return colors


def color_set_vintage():
    colors = [
        [251, 234, 189],  # #fbeabd
        [227, 178, 119],  # #e3b277
        [178, 121, 68],  # #b27944
        [160, 96, 52],  # #a06034
        [79, 45, 43],  # #4f2d2b
        [0, 0, 0],  # #000000
    ]
    return colors


def color_set_moonlight():
    colors = [
        [255, 255, 255],  # #ffffff
        [237, 242, 250],  # #edf2fa
        [170, 186, 232],  # #aabae8
        [112, 133, 215],  # #7085d7
        [54, 75, 131],  # #364b83
        [40, 43, 84],  # #282b54
        [5, 29, 46],  # #051d2e
    ]
    return colors


def crop_image(image):
    img = Image.open(image)
    width, height = img.size

    new_ratio = 4680 / 5850
    image_ratio = width / height

    if image_ratio > new_ratio:  # Изображение шире, обрезаем по вертикали

        new_width = 4680

        left = (width - new_width) / 2
        top = 0
        right = left + new_width
        bottom = height
    else:  # Изображение выше, обрезаем по горизонтали

        new_height = 5850

        left = 0
        top = (height - new_height) / 2
        right = width
        bottom = top + new_height

    return img.crop((left, top, right, bottom))


def resize_image(image, new_width, new_height):
    img = Image.open(image)
    # width, height = img.size
    resized_image = img.resize((new_width, new_height), Image.LANCZOS)  # используем метод LANCZOS для лучшего качества масштабирования

    return resized_image


# START--------------------------------------------
###################################################
for photo in [
    'cropped_image01.jpg',
    # 'cropped_image_2.jpeg',
    # 'cropped_image_3.jpeg',
]:
    # image_path = "cropped_image01.jpeg"
    main(photo)

###################################################
# FINISH--------------------------------------------
