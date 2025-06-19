from PIL import Image

def get_dominant_color(image: Image.Image, resize=100):
    img = image.copy()
    img = img.resize((resize, resize))

    pixels = img.getcolors(resize * resize)

    dominant_color = max(pixels, key=lambda item: item[0])[1]
    return dominant_color

def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0

    cmax = max(r, g, b)
    cmin = min(r, g, b)
    diff = cmax-cmin

    if cmax == cmin: 
        h = 0
    
    elif cmax == r: 
        h = (60 * ((g - b) / diff) + 360) % 360

    elif cmax == g:
        h = (60 * ((b - r) / diff) + 120) % 360

    elif cmax == b:
        h = (60 * ((r - g) / diff) + 240) % 360

    if cmax == 0:
        s = 0
    else:
        s = (diff / cmax) * 100

    v = cmax * 100
    return round(h), round(s), round(v)
