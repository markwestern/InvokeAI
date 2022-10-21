import os
import re
from os import path
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import json

dirname = os.path.dirname(__file__)
cli_filename = os.path.join(dirname, '../outputs/img-samples/dream_log.txt')
web_filename = os.path.join(dirname, '../outputs/img-samples/dream_web_log.txt')
upscale_path = 'G:\\Git\\InvokeAI\\outputs\\upscaled\\'

filename_re = r'.*\\([0-9\.]*png)\:'
token_re = r'.*"(?P<prompt>.*)"\s\-s(?P<steps>[0-9]*)\s\-W(?P<width>[0-9]*)\s\-H(?P<height>[0-9]*)\s\-C(?P<cfg_scale>[0-9]*).*\-A(?P<sampler_name>[a-z0-9_]*).*\-\-(?P<seamless>seamless).*\-S(?P<seed>[0-9]*)'
json_re = r'.*png:\s(\{.*\})'

def add_metadata(image_dict, output):
    metadata = PngInfo()
    for key in image_dict:
        metadata.add_text(key, image_dict[key])

    final_output = Image.open(output)

    if not final_output.text:
        print(image_dict)
        final_output.save(output, pnginfo=metadata)



def main():
    with open(cli_filename) as f:
        lines = f.readlines()
        for line in lines:
            image_match = re.match(filename_re, line)

            if image_match:
                image_name = image_match.group(1)
                output = upscale_path + image_name.replace('.png','u.png') 

                if path.exists(output):
                    print('cli ' + image_name)
                    match = re.match(token_re, line)

                    if match:                    
                        image_dict = match.groupdict()
                        image_dict.pop('image_name', None)    

                        if image_dict:
                            add_metadata(image_dict, output)       
    
    with open(web_filename) as f:
        lines = f.readlines()
        for line in lines:
            image_match = re.match(filename_re, line)

            if image_match:
                image_name = image_match.group(1)
                output = upscale_path + image_name.replace('.png','u.png') 

                if path.exists(output):
                    print('web ' + image_name)
                    match = re.match(json_re, line)

                    if match:                    
                        json_dict = json.loads(match.group(1))
                        image_dict = {}
                        for key in json_dict:
                            if json_dict[key] != '':
                                image_dict[key] = str(json_dict[key])

                        if image_dict:
                            add_metadata(image_dict, output)   
                    


if __name__ == "__main__":
    main()
