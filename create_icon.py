from PIL import Image, ImageDraw, ImageFont
import os

# ensure assets folder exists
os.makedirs("assets", exist_ok=True)

SIZE = 512

# Create base image
img = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 0))
draw = ImageDraw.Draw(img)

# Colors
purple = (94, 58, 170, 255)
gold = (245, 192, 60, 255)
dark = (40, 40, 40, 255)

# Draw rounded calculator body
margin = 40
draw.rounded_rectangle(
    [margin, margin, SIZE - margin, SIZE - margin],
    radius=80,
    fill=purple,
    outline=dark,
    width=12,
)

# Screen
draw.rectangle(
    [120, 110, SIZE - 120, 230],
    fill=(230, 230, 230, 255),
    outline=dark,
    width=6,
)

# Calculator buttons
button_size = 60
start_x = 150
start_y = 270

for row in range(3):
    for col in range(3):
        x = start_x + col * 100
        y = start_y + row * 100
        draw.ellipse([x, y, x + button_size, y + button_size], fill=gold, outline=dark, width=4)

# Add PF text
try:
    font = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 130)
except:
    font = ImageFont.load_default()

text = "PF"
bbox = draw.textbbox((0, 0), text, font=font)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]

draw.text(
    ((SIZE - text_w) / 2, 40),
    text,
    font=font,
    fill=gold,
)

# Save multi-resolution ICO
ico_sizes = [(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)]
img.save("assets/app.ico", sizes=ico_sizes)

print("Icon created at: assets/app.ico")