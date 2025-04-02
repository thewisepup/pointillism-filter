import cv2
import numpy as np
from configs.config import PointillismConfig
from .preprocessor import PreProcessor


class Processor:
    def __init__(self, config: PointillismConfig = None):
        self.config = config or PointillismConfig()
        # init all sub classes and processors
        self.preprocessor = PreProcessor(self.config)

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
        if self.config.debug_mode:
            print("Starting pointillism effect application")

        self._validate_image_input(image)
        preprocessed_image = self.preprocessor.preprocess_image(image)

        if self.config.debug_mode:
            cv2.imwrite(
                "images/output/preprocessed_image.jpg",
                np.transpose(preprocessed_image, (1, 0, 2)),
            )
            print("Saved preprocessed image for debugging")

    def _validate_image_input(self, image: np.ndarray):
        """Validates the input image array meets the required specifications.

        Args:
            image (np.ndarray): The input image to validate.

        Raises:
            ValueError: If the image:
                - Is not a NumPy array
                - Does not have shape (height, width, 3)
                - Does not have data type np.uint8
                - Contains pixel values outside the range [0, 255]
        """
        if not isinstance(image, np.ndarray):
            raise ValueError("Input image must be a NumPy array.")
        if image.ndim != 3 or image.shape[2] != 3:
            raise ValueError("Input image must have shape (height, width, 3).")
        if image.dtype != np.uint8:
            raise ValueError("Input image must have data type np.uint8.")
        if np.any(image < 0) or np.any(image > 255):
            raise ValueError("Pixel values must be in the range [0, 255].")
