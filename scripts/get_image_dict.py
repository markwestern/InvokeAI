import os
import re
import json

dirname = os.path.dirname(__file__)
cli_filename = os.path.join(dirname, '../outputs/img-samples/dream_log.txt')
web_filename = os.path.join(dirname, '../outputs/img-samples/dream_web_log.txt')

filename_re = r'.*\\([0-9\.]*png)\:'
token_re = r'.*"(?P<description>.*)"\s\-s(?P<steps>[0-9]*)\s\-W(?P<width>[0-9]*)\s\-H(?P<height>[0-9]*)\s\-C(?P<cfg_scale>[0-9]*).*\-A(?P<sampler_name>[a-z0-9_]*).*\-\-(?P<seamless>seamless).*\-S(?P<seed>[0-9]*)'
json_re = r'.*png:\s(\{.*\})'


def get_image_dict(img_name):
    with open(cli_filename) as f:
        lines = f.readlines()
        for line in lines:
            image_match = re.match(filename_re, line)

            if image_match and image_match.group(1) == img_name:
                match = re.match(token_re, line)

                if match:
                   return match.groupdict()

    with open(web_filename) as f:
        lines = f.readlines()
        for line in lines:
            image_match = re.match(filename_re, line)

            if image_match and image_match.group(1) == img_name:
                match = re.match(json_re, line)

                if match:
                    json_dict = json.loads(match.group(1))
                    image_dict = {}
                    
                    for key in json_dict:
                        if json_dict[key] != '':
                            image_dict[key] = str(json_dict[key])

                    return image_dict


    # token_list = []
    # for description in tokens:
    #     for token in re.split('\,|\.', description):
    #         token_list.append(token.strip())

    # tokens = list(set(token_list))

