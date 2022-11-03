from get_image_dict import get_image_dict
from PIL.PngImagePlugin import PngInfo
import argparse
import subprocess
from os import path, walk

from gooey import Gooey
from PIL import Image
Image.MAX_IMAGE_PIXELS = 1866240000


img_path = 'G:\\Git\\InvokeAI\\outputs\\img-samples\\'
upscale_path = 'G:\\Git\\InvokeAI\\outputs\\upscaled\\'
superscale_path = 'G:\\Git\\InvokeAI\\outputs\\superscale\\'


class Options:
    img: str
    model: str


models = ["realesr-animevideov3-x2", "realesr-animevideov3-x3",
          "realesrgan-x4plus-anime", "realesrgan-x4plus"]


@Gooey
def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--image",
        dest='image'
    )
    parser.add_argument(
        "--model",
        dest='model',
        choices=models,
        metavar='model',
        default='realesrgan-x4plus',
        help=f'realesrgan model: {", ".join(models)}'
    )
    opt = parser.parse_args()

    realesrgan2x(True, opt.model, opt.image)


def get_resampling_mode():
    try:
        from PIL import Image, __version__
        major_ver = int(__version__.split('.')[0])
        if major_ver >= 9:
            return Image.Resampling.LANCZOS
        else:
            return Image.LANCZOS
    except Exception as ex:
        return 1  # 'Lanczos' irrespective of version.


def get_filelist(from_path):
    img_pre_list = []
    img_list = []
    for (dirpath, dirnames, filenames) in walk(from_path):
        img_pre_list.extend(filenames)
        break
    for img in img_pre_list:
        if ".png" in img:
            img_list.append(img)

    return img_list


def realesrgan2x(superscale, model, image):
    from_path = upscale_path if superscale else img_path
    to_path = superscale_path if superscale else upscale_path

    img_list = [image] if image else get_filelist(from_path)

    for img in img_list:
        print(img)
        input = from_path + img
        output = to_path + img.replace('.png', 'u.png')

        if not path.exists(output):
            process = subprocess.Popen([
                "realesrgan-ncnn-vulkan/realesrgan-ncnn-vulkan.exe",
                '-i', input,
                '-o', output,
                '-n', model
            ])
            process.wait()

            metadata = PngInfo()
            image_dict = get_image_dict(img)
            if image_dict:
                for key in image_dict:
                    metadata.add_text(key, image_dict[key])

            final_output = Image.open(output)
            final_output = final_output.resize(
                (int(final_output.size[0] / 2), int(final_output.size[1] / 2)), get_resampling_mode())

            final_output.save(output, pnginfo=metadata)

    if not superscale:
        realesrgan2x(True, model, img.replace('.png', 'u.png'))


if __name__ == "__main__":
    main()
