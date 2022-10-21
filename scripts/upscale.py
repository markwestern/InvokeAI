import argparse
import subprocess
from os import path, walk

from gooey import Gooey
from PIL import Image
from PIL.PngImagePlugin import PngInfo

from get_image_dict import get_image_dict

img_path = 'G:\\Git\\InvokeAI\\outputs\\img-samples\\'
upscale_path = 'G:\\Git\\InvokeAI\\outputs\\upscaled\\'
superscale_path = 'G:\\Git\\InvokeAI\\outputs\\superscale\\'


class Options:
    img: str
    model: str


@Gooey
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--superscale",
        dest='superscale',
        action='store_true',
        help="superscale upscaled images?"
    )
    parser.add_argument(
        "--img_list",
        type=list,
        nargs="?",
        help="images to upscale"
    )
    parser.add_argument(
        "--model",
        type=str,
        nargs="?",
        help="realesrgan model: realesr-animevideov3-x2 | realesr-animevideov3-x3 | realesrgan-x4plus-anime | realesrgan-x4plus",
        default="realesrgan-x4plus"
    )
    opt = parser.parse_args()

    img_pre_list = []
    opt.img_list = []
    from_path = upscale_path if opt.superscale else img_path
    for (dirpath, dirnames, filenames) in walk(from_path):
        img_pre_list.extend(filenames)
        break
    for img in img_pre_list:
        if ".png" in img:
            opt.img_list.append(img)

        print(opt.img_list)

    realesrgan2x(opt)


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


def realesrgan2x(opt: Options):
    img_list = opt.img_list

    from_path = upscale_path if opt.superscale else img_path
    to_path = superscale_path if opt.superscale else upscale_path

    for img in img_list:
        input = from_path + img
        output = to_path + img.replace('.png', 'u.png')

        if not path.exists(output):
            process = subprocess.Popen([
                "realesrgan-ncnn-vulkan/realesrgan-ncnn-vulkan.exe",
                '-i',
                input,
                '-o',
                output,
                '-n',
                opt.model
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


if __name__ == "__main__":
    main()
