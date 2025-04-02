import cv2
from configs import PointillismConfig
from models import DotCluster
from processing import PreProcessor, ImageGenerator, ColorTransformer, ColorPalette
from PIL import Image

import numpy as np

from processing.processor import Processor


def main():
    # Initialize configuration
    config = PointillismConfig(debug_mode=True)

    # Initialize all required classes
    processor = Processor(config)

    # Load and convert image to numpy array
    image = Image.open("images/Brandon.jpg")
    numpy_array = np.array(image)
    print("Original shape:", numpy_array.shape)  #

    # Save the image

    if config.debug_mode:
        print("Original shape:", numpy_array.shape)
        test_img = Image.fromarray(np.transpose(numpy_array, (1, 0, 2)))
        test_img.save("images/output/initial.jpg")

    processor.apply_pointillism(numpy_array)


if __name__ == "__main__":
    main()
