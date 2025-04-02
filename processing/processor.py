import numpy as np
from configs.config import PointillismConfig
from .preprocessor import PreProcessor


class Processor:
    def __init__(self):
        # init all sub classes and processors
        self.preprocessor = PreProcessor()

    def apply_pointillism(self, image: np.ndarray) -> np.ndarray:
        """Applies the pointillism effect to the input image.

        Args:
            image: A NumPy array of shape (height, width, 3) representing
                   an RGB image, with pixel values in the range [0, 255]
                   and data type `np.uint8`.

        Returns:
            A NumPy array representing the pointillism-rendered image.

        Raises:
            ValueError: If the input image is not a valid NumPy array
                        in the expected format.
        """
        print("apply_pointillism")
        self._validate_image_input(image)
        self.preprocessor.preprocess_image(image)

    def _validate_image_input(self, image: np.ndarray):
        print("_validate_image_input")
        if not isinstance(image, np.ndarray):
            raise ValueError("Input image must be a NumPy array.")
        if image.ndim != 3 or image.shape[2] != 3:
            raise ValueError("Input image must have shape (height, width, 3).")
        if image.dtype != np.uint8:
            raise ValueError("Input image must have data type np.uint8.")
        if np.any(image < 0) or np.any(image > 255):
            raise ValueError("Pixel values must be in the range [0, 255].")
