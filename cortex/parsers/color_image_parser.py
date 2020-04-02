from ..mq import subscribe, AVAILABLE_PARSERS

@subscribe('color_image')
def parse_that_fucking_image(image):
    print (AVAILABLE_PARSERS)
    print (f"color image image being parsed {image}")
