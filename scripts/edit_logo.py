import sys
from PIL import Image, ImageDraw

def create_oval_logo(input_path, output_path):
    try:
        # Open the image
        img = Image.open(input_path).convert("RGBA")
        width, height = img.size
        
        # Create a mask image (L mode is 8-bit pixels, black and white)
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        
        # Draw a white ellipse on the black background
        # We'll use the entire dimension of the image if the oval fills it, 
        # or we might need a slight padding depending on the exact box
        # We can find the bounding box of non-white pixels first to be safe
        
        # Convert to RGB to find non-white pixels
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3]) # paste using alpha channel
        bg = img.convert("RGB")
        
        bbox = bg.getbbox()
        
        # Let's just create an ellipse that matches the white box dimensions closely
        # Assuming the oval is centered and touches the edges of the image (or near edges)
        
        # Define the bounding box for the ellipse (using a small margin if needed, but 0 is usually fine)
        margin = 2 # 2 pixel antialiasing margin
        draw.ellipse((margin, margin, width - margin, height - margin), fill=255)
        
        # Create a new image with transparent background
        result = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        
        # Paste the original image using the mask
        result.paste(img, (0, 0), mask=mask)
        
        # Save as PNG to support transparency
        result.save(output_path, 'PNG')
        print(f"Successfully created {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_oval_logo('static/images/logo.jpg', 'static/images/logo.png')
