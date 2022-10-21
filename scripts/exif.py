from PIL import Image
from PIL.PngImagePlugin import PngInfo

targetImage = Image.open("G:\\Git\\InvokeAI\\outputs\\upscaled\\000007.1323613031u.png")

print(targetImage.text)