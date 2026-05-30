from PIL import Image
import os

input_path = r"C:\Users\NEC-PCuser\Downloads\Gemini_Generated_Image_vgcl3vgcl3vgcl3v.png"
output_dir = r"c:\Users\NEC-PCuser\Documents\kazu_midnight_fortress\ainhit\assets"
output_path = os.path.join(output_dir, "logo.png")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Open image
img = Image.open(input_path).convert("RGBA")

# Extract luminance/grayscale to use as alpha
gray = img.convert("L")
pixels = gray.load()
width, height = gray.size

# Create a new alpha channel
new_alpha = Image.new("L", (width, height))
alpha_pixels = new_alpha.load()

# Process pixels to remove the carbon fiber background texture and extract white logo elements
for y in range(height):
    for x in range(width):
        val = pixels[x, y]
        # Clean thresholding to completely eliminate background mesh patterns (which are dark gray)
        # and preserve anti-aliasing on the edges of the logo white strokes
        if val < 60:
            alpha_pixels[x, y] = 0
        elif val > 180:
            alpha_pixels[x, y] = 255
        else:
            # Linear mapping for smooth anti-aliased boundaries
            alpha_pixels[x, y] = int((val - 60) * (255 / 120))

# Create pure white image with processed transparent alpha
white_img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
white_img.putalpha(new_alpha)

# Save high quality transparent PNG
white_img.save(output_path, "PNG")
print(f"Successfully extracted logo. Transparent white logo saved to: {output_path}")
