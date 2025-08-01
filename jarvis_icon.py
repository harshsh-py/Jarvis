from PIL import Image, ImageDraw

def create_jarvis_icon():
    # Create a new image with a blue background
    size = (64, 64)
    icon = Image.new('RGB', size, color='#007ACC')
    
    # Create a drawing object
    draw = ImageDraw.Draw(icon)
    
    # Draw a white circle (representing a minimalist robot head)
    margin = 10
    draw.ellipse([margin, margin, size[0]-margin, size[1]-margin], fill='white')
    
    # Draw "eyes" - two small blue rectangles
    eye_color = '#007ACC'
    eye_width = 8
    eye_height = 12
    eye_y = 25
    # Left eye
    draw.rectangle([20, eye_y, 20+eye_width, eye_y+eye_height], fill=eye_color)
    # Right eye
    draw.rectangle([36, eye_y, 36+eye_width, eye_y+eye_height], fill=eye_color)
    
    # Save the icon
    icon.save('jarvis_icon.png')

if __name__ == "__main__":
    create_jarvis_icon()
