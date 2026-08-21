from PIL import Image
from vision import analyze_image

image = Image.open("sample.jpg")

response = analyze_image(
    "Describe this image in detail.",
    image
)

print(response)