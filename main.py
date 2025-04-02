from configs import PointillismConfig
from models import DotCluster
from processing import PreProcessor, ImageGenerator, ColorTransformer, ColorPalette
from PIL import Image

import numpy as np

from processing.processor import Processor


def main():
    # Initialize configuration
    config = PointillismConfig()

    # Initialize all required classes
    processor = Processor()

    # Load and convert image to numpy array
    image = Image.open("images/Brandon.jpg")
    numpy_array = np.array(image)

    processor.apply_pointillism(numpy_array)


if __name__ == "__main__":
    main()
