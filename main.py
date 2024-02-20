from PIL import Image, ImageDraw
import numpy as np


def main(image):
    original_image = Image.open(image)
    width, height = original_image.size
    image_ratio = round(width / height, 1)

    if image_ratio == round(156 / 195, 1):
        choose_size(original_image, width, height, image, 4680, 5850, 156, 195)

    elif image_ratio == round(117 / 165, 1):
        choose_size(original_image, width, height, image, 3510, 4950, 117, 165)

    elif image_ratio == round(77 / 120, 1):
        choose_size(original_image, width, height, image, 2310, 3600, 77, 120)
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


def create_mosaic(original_image, tiles_width, tiles_height):
    count = 0
    width, height = original_image.size
    tile_size = height / tiles_height

    mosaic_image = Image.new('RGB', (width, height))

    draw = ImageDraw.Draw(mosaic_image)

    for color in [color_set_bw, color_set_disco, color_set_vintage, color_set_moonlight]:
        for y in range(tiles_height):
            for x in range(tiles_width):
                # Вырезаем кусок из исходного изображения
                box = (int(x * tile_size), int(y * tile_size), int((x + 1) * tile_size), int((y + 1) * tile_size))
                region = original_image.crop(box)

                # Получаем средний цвет этого куска
                average_color = tuple(sum(color) / len(color) for color in zip(*region.getdata()))

                # Нахождения расстояния между цветами c и average_color в пространстве цветов
                # np.array(c) и np.array(average_color) конвертируют цвета в массивы
                # np.linalg.norm() вычисляет Евклидово расстояние между ними.
                closest_color = tuple(min(color(), key=lambda c: np.linalg.norm(np.array(c) - np.array(average_color))))

                # Заполняем блок этим цветом
                draw.rectangle(box, fill=closest_color, outline="grey")

        mosaic_image.save(f'mosaic_{count}.png')
        count += 1
    # return mosaic_image


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
