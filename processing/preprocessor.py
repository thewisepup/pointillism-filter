import numpy as np


class PreProcessor:

    def __init__(self):
        print("init preprocessor")

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocesses input image by applying Gaussian filtering and downsampling.

        Args:
            img: Input image as numpy array (height, width, channels)
        Returns:
            Processed image as numpy array
        """
        print("preprocess_image")
