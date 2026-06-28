import simple_pdf_to_png
import white_bg_crop
from PIL import Image
import os

"""
Step of conversion

[x] Convert pdf to jpg

[x] Make a new blank with a4 size paper 

Place some margin (~5mm)
[x] Place front_photo on the left and back on the right (with size less than 65x95 mm)

[x] Place 4 images one below the other (margin of ~5mm before each one)

[] Save this file as pdf
"""

"""
1in = 2.54cm x 10 (*because there is 10mm in 1cm)
1in = 25.4mm
96px = 25.4mm
1mm = 96px / 25.4
Millimeters to Pixels Formula:
pixels = millimeters * ( PPI / 25.4 )
"""

# Ensure all required folders exist before doing anything else.
# os.makedirs(..., exist_ok=True) creates the folder if missing,
# and does nothing (no error) if it already exists.
for folder in ("pdf-files", "png-files", "cropped-pngs", "joined-file"):
    os.makedirs(folder, exist_ok=True)

for filename in os.listdir("cropped-pngs"):
    os.remove(os.path.join("cropped-pngs", filename))

for filename in os.listdir("png-files"):
    os.remove(os.path.join("png-files", filename))

## mm to pixels conversion (at a given ppi)
def mm_to_pixel(mm: float):
    ppi = 300  # ppi (pixels per inch) is same as dpi (dots per inch)
    mm_in_1_inch = 25.4  # 1 inch = 25.4 mm
    mm_to_pixel_conversion_rate = ppi / mm_in_1_inch
    pixels = int(round(mm * (ppi / mm_in_1_inch)))
    return pixels


if not os.path.isfile("blank_image.png"):
    print("Creating blank image")
    import numpy as np
    import cv2

    height = mm_to_pixel(297)
    width = mm_to_pixel(210)
    channels = 3
    img = np.full((height, width, channels), 255, dtype=np.uint8)
    cv2.imwrite("blank_image.png", img)

simple_pdf_to_png.convert_pdf_to_png("pdf-files", "png-files")
white_bg_crop.crop_out_white_pixels("png-files", "cropped-pngs")

# TODO: Convert simple pdf_to_pngs to tansparent pngs
print()


bg_image = Image.open(r"blank_image.png")

# Adding vertical and horizontal lines (every virtual 10 mm)

# Lines on top

# width_generated = 1
# height_generated = 20
# vertical_line_pil = Image.new(mode="RGB", size=(width_generated, height_generated))
# pixels_of_generated_pil_image = vertical_line_pil.load()

# for i in range(width_generated):
#     for j in range(height_generated):
#         pixels_of_generated_pil_image[i, j] = (0, 0, 0)

# for i in range(22):
#     bg_image.paste(
#         vertical_line_pil,
#         (mm_to_pixel(i * 10), mm_to_pixel(2.5)),
#     )
# # Lines on the left
# width_generated = 20
# height_generated = 1
# horizontal_line_pil = Image.new(mode="RGB", size=(width_generated, height_generated))
# pixels_of_generated_pil_image = horizontal_line_pil.load()

# for i in range(width_generated):
#     for j in range(height_generated):
#         pixels_of_generated_pil_image[i, j] = (0, 0, 0)

# for i in range(30):
#     bg_image.paste(
#         horizontal_line_pil,
#         (mm_to_pixel(2.5), mm_to_pixel(i * 10)),
#     )


# Adding files on lined canvas
png_files = os.listdir("cropped-pngs/")
if len(png_files) > 4:
    print("More than 4 pages in total all pdfs combined, adding first 4")
for i in range(len(png_files)):
    if i >= 4:
        break
    path_to_file = os.path.join("cropped-pngs", png_files[i])
    file_to_paste = Image.open(path_to_file)

    new_height = mm_to_pixel(50)
    print(new_height)
    width, height = file_to_paste.size
    new_width = int(round(new_height * width / height))
    # print(new_height)
    file_to_paste = file_to_paste.resize((new_width, new_height))

    bg_image.paste(
        file_to_paste, box=(mm_to_pixel(7), mm_to_pixel(i * 70 + 5)), mask=file_to_paste
    )
    print(f"Added '{png_files[i]}' in final the output")


if not os.path.exists("joined-file"):
    os.makedirs("joined-file")
bg_image.save("joined-file/output.png")


# TODO: Delete intermediate png files


# os.remove("cropped-pngs")
# os.remove("png-files")

# TODO: convert png to pdf for printing


# pasted_img1 = Image.open(r"png-files/MATHURALAL copy 1.png")
# print(pasted_img1.size)

# width, height = pasted_img1.size
# new_height = mm_to_pixel(350)
# new_width = int(round(new_height * width / height))
# print(new_height)
# pasted_img1 = pasted_img1.resize((new_width, new_height))

# bg_image.paste(pasted_img1, box=(mm_to_pixel(7), mm_to_pixel(4*70+5)))

# pasted_img2 = Image.open(r"png-files/MATHURALAL copy 2.png")
# pasted_img3 = Image.open(r"png-files/MATHURALAL copy 3.png")
# pasted_img4 = Image.open(r"png-files/MATHURALAL copy 4.png")

# pasted_img2 = pasted_img2.resize((new_width, new_height))
# bg_image.paste(pasted_img2, box=(mm_to_pixel(7), mm_to_pixel(1*70+5)))
# pasted_img3 = pasted_img3.resize((new_width, new_height))
# bg_image.paste(pasted_img2, box=(mm_to_pixel(7), mm_to_pixel(2*70+5)))
# pasted_img4 = pasted_img4.resize((new_width, new_height))
# bg_image.paste(pasted_img3, box=(mm_to_pixel(7), mm_to_pixel(3*70+5)))
