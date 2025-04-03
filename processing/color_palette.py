import colorsys
from typing import List, Tuple
import cv2
import numpy as np
from configs.config import PointillismConfig
from PIL import Image


class ColorPalette:

    def __init__(self, config: PointillismConfig = None):
        self.config = config or PointillismConfig()

    def compute_pointillism_color_palette(self, img: np.ndarray) -> np.ndarray:
        """
        Select color palette for pointillism image by applying k-means clustering, color transformation, and adding complementary colors
        Args:
            img: Input image as numpy array (height, width, channels)

        Returns:
            List of 16 colors
        """
        if self.config.debug_mode:
            print("--Generating Color Palette--")
        primary_colors = self._compute_primary_colors(img)
        enhanced_hsv_primary_colors = self._enhance_color_palette(primary_colors)

    def _compute_primary_colors(self, img: np.ndarray) -> np.ndarray:
        """Apply k-means clustering to extract num_colors primary colors
        Args:
            img: Input image as numpy array (height, width, channels)

        Returns:
            List of num_colors primary colors
        """
        if self.config.debug_mode:
            print("Computing primary colors")
        flattened_img = img.reshape((-1, 3))  # reshape pixels to a (h*w,3) shape
        flattened_img = np.float32(flattened_img)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, centers = cv2.kmeans(
            flattened_img, 8, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
        )
        primary_colors = np.uint8(centers)
        return np.uint8(primary_colors)

    def _enhance_color_palette(self, rgb_colors: np.ndarray) -> np.ndarray:
        """
        Convert RGB color to HSV and apply color enhancements. (Hard code saturation and brightness boost for now)
        Args:
            img: Input image as numpy array (height, width, channels)

        Returns:
            List of num_colors enhanced color palette in HSV
        """
        if self.config.debug_mode:
            print("Computing HSV colors and applying color saturation")
        # Convert RGB colors to HSV
        normalized_rgb = rgb_colors.astype(float) / 255.0
        hsv_colors = np.array(
            [colorsys.rgb_to_hsv(r, g, b) for r, g, b in normalized_rgb]
        )
        # Apply saturation Snew = (S)^.75 + .05
        hsv_colors[:, 1] = np.power(hsv_colors[:, 1], 0.75) + 0.05
        # Apply saturation Vnew = (V)^.75 + .05
        hsv_colors[:, 2] = np.power(hsv_colors[:, 2], 0.75) + 0.05
        return hsv_colors

    def _compute_complementary_colors(
        self, primary_colors: List[np.ndarray]
    ) -> List[np.ndarray]:
        """
        Generate a list of 8 complementary colors given a list of 8 primary_colors
        Args:
            primary_colors: List of 8 HSV primary colors

        Returns:
            List of 8 complementary_colors
        """
        pass
