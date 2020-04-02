from .config import subscribe

@subscribe('color_image')
def parse_that_fucking_image(image):
    print (f"color image image being parsed {image}")
