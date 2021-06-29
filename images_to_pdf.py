import os
from PIL import Image


class Converter:

    @staticmethod
    def save_images_to_pdf(filename, image_dir, pdf_dir):
        images = []
        for image in os.listdir(image_dir):
            images.append(Image.open(image_dir + '/' + image))
        im1 = images.pop(0)
        pdf1_filename = filename + ".pdf"
        os.chdir(pdf_dir)
        im1.save(pdf1_filename, "PDF", resolution=100.0, save_all=True, append_images=images)
        print(os.getcwd() + ' 2')

    @staticmethod
    def extract_images_from_pdf():
        # TODO
        pass
