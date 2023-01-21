from PIL import Image

# Open the image
try:
    image = Image.open("image.png")
except FileNotFoundError:
    print("image.png not found, please provide the correct path")
    exit()

# Open the watermark image
try:
    watermark = Image.open("watermark.png")
except FileNotFoundError:
    print("watermark.png not found, please provide the correct path")
    exit()

# Resize the watermark
watermark_width, watermark_height = watermark.size
image_width, image_height = image.size

if watermark_width > image_width or watermark_height > image_height:
    print("Watermark is larger than the image.")
    print("Please provide a watermark with smaller size or resize the current watermark before.")
    exit()

watermark = watermark.resize((image_width // 4, image_height // 4))

# Create an RGBA image with an alpha layer the same size as the original image
watermarked = Image.new("RGBA", image.size)

# Set the watermark's transparency
watermark = watermark.convert("RGBA")
watermark_pixel = watermark.load()
for i in range(watermark.width):
    for j in range(watermark.height):
        r, g, b, a = watermark_pixel[i, j]
        watermark_pixel[i, j] = (r, g, b, int(a * 0.8))

# Position of the watermark (x, y)
watermarked.paste(watermark, (int(image_width*0.6),int(image.height*0.75)), watermark)

# Create a composite image using the alpha layer
output = Image.composite(watermarked, image, watermarked)

# Save the output
output.save("output.png")
