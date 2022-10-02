import argparse
import subprocess
from os import path, walk

from gooey import Gooey
from PIL import Image

img_path = 'G:\\Git\\InvokeAI\\outputs\\img-samples\\'
upscale_path = 'G:\\Git\\InvokeAI\\outputs\\upscaled\\'

class Options:
    img: str
    model: str

@Gooey
def main():
    parser = argparse.ArgumentParser()
  
    parser.add_argument(
        "--img",
        type=str,
        nargs="?",
        help="image to upscale"
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

    if opt.img is None:
        img_pre_list = []
        opt.img_list = []
        for (dirpath, dirnames, filenames) in walk(img_path):
            img_pre_list.extend(filenames)
            break
        for img in img_pre_list:
            if ".png" in img and "u.png" not in img:
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
    if opt.img is not None:
        img_list = [opt.img]
    else:
        img_list = opt.img_list

    for img in img_list:
        input = img_path + img
        output = upscale_path + img.replace('.png','u.png')    
    
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

            final_output = Image.open(output)
            final_output = final_output.resize((int(final_output.size[0] / 2), int(final_output.size[1] / 2)), get_resampling_mode())
            final_output.save(output)

if __name__ == "__main__":
    main()
