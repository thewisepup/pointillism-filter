from configs import PointillismConfig
from PIL import Image
import numpy as np
from processing.processor import Processor


def main():
    # Initialize configuration
    config = PointillismConfig(debug_mode=True, kernel_size=15)

    # Initialize all required classes
    processor = Processor(config)

    # Load and convert image to numpy array
    beach = "images/beach.jpg"
    brandon = "images/brandon.png"
    coffee = "images/coffee.jpeg"
    forest = "images/forest.jpeg"
    group = "images/group.JPG"

    image = Image.open(brandon)
    print("Original pillow size:", image.size)

    numpy_array = np.array(image)
    print("Original numpy shape:", numpy_array.shape)

    # Save the image
    if config.debug_mode:
        img = Image.fromarray(numpy_array)
        print("after pillow size:", img.size)
        img.save("images/output/initial.jpg")

    processor.apply_pointillism(numpy_array)


if __name__ == "__main__":
    main()
