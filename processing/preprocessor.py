import cv2
import numpy as np
from configs.config import PointillismConfig
from PIL import Image


class PreProcessor:

    def __init__(self, config: PointillismConfig = None):
        self.config = config or PointillismConfig()

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocesses input image by applying Gaussian filtering and downsampling.

        Args:
            img: Input image as numpy array (height, width, channels)
        Returns:
            Processed image as numpy array
        """
        if self.config.debug_mode:
            print("--Starting image preprocessing--")

        # create image copy
        preprocessed_image = image.copy()
        preprocessed_image = self._apply_low_pass_filter(preprocessed_image)
        preprocessed_image = self._downsample_image(preprocessed_image)

        if self.config.debug_mode:
            print("--Finished image preprocessing--")

        return preprocessed_image

    def _apply_low_pass_filter(self, image: np.ndarray):
        if self.config.kernel_size <= 0 or self.config.kernel_size % 2 == 0:
            raise ValueError("Kernel size must be a positive odd integer.")

        if self.config.debug_mode:
            print(
                f"Applying low pass filter with kernel size: {self.config.kernel_size}"
            )

        bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        bgr_blurred_image = cv2.GaussianBlur(
            bgr_image, (self.config.kernel_size, self.config.kernel_size), 0
        )
        rgb_blurred_image = cv2.cvtColor(bgr_blurred_image, cv2.COLOR_BGR2RGB)

        if self.config.debug_mode:
            debug_image = Image.fromarray(rgb_blurred_image, "RGB")
            debug_image.save("images/output/low_pass_filter.jpg")
        return rgb_blurred_image

    def _downsample_image(self, image: np.ndarray):
        if self.config.debug_mode:
            print(f"Downsampling image with factor: {self.config.cluster_distance}")

        height, width = image.shape[:2]
        new_width = int(width // self.config.cluster_distance)
        new_height = int(height // self.config.cluster_distance)

        down_sampled_image = cv2.resize(
            image, (new_width, new_height), interpolation=cv2.INTER_LINEAR
        )

        if self.config.debug_mode:
            print(
                f"Image downsampled from {(width, height)} to {(new_width, new_height)}"
            )
            debug_image = Image.fromarray(down_sampled_image, "RGB")
            debug_image.save("images/output/downsampled.jpg")
        return down_sampled_image
