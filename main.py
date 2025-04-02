from configs import PointillismConfig
from models import DotCluster
from processing import PreProcessor, ImageGenerator, ColorTransformer, ColorPalette
import numpy as np


def main():
    # Initialize configuration
    config = PointillismConfig()

    # Initialize all required classes
    dot_cluster = DotCluster()
    preprocessor = PreProcessor()
    image_generator = ImageGenerator()
    color_transformer = ColorTransformer()
    color_palette = ColorPalette()
    # Create a 40x40 test image array
    test_image = np.zeros((40, 40), dtype=np.uint8)
    print("All components initialized successfully!")


if __name__ == "__main__":
    main()
