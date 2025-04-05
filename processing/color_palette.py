import colorsys
from typing import List, Tuple
import cv2
import numpy as np
from configs.config import PointillismConfig
from PIL import Image


class ColorPalette:
    COLOR_PALETTE_LENGTH = 16  # 8 primary colors + 8 complementary colors

    def __init__(self, config: PointillismConfig = None):
        self.config = config or PointillismConfig()

    def compute_pointillism_color_palette(self, img: np.ndarray) -> np.ndarray:
        """
        Select color palette for pointillism image by applying k-means clustering, color transformation, and adding complementary colors
        Args:
            img: Input image as numpy array (height, width, channels)

        Returns:
            List of 16 colors (8 primary + 8 complementary)
        """
        if self.config.debug_mode:
            print("--Generating Color Palette--")
        primary_colors = self._compute_primary_colors(img)
        enhanced_primary_colors = self._enhance_color_palette(primary_colors)
        complementary_colors = self._compute_complementary_colors(
            enhanced_primary_colors
        )
        print(np.vstack((enhanced_primary_colors, complementary_colors)))
        if self.config.debug_mode:
            print("--Finished Generating Color Palette--")
        # Combine primary and complementary colors into a single list
        color_palette = np.vstack((enhanced_primary_colors, complementary_colors))
        self.validate_color_palette(color_palette)
        return np.vstack((enhanced_primary_colors, complementary_colors))

    def _compute_primary_colors(self, img: np.ndarray) -> np.ndarray:
        """Apply k-means clustering to extract num_colors primary colors
        Args:
            img: Input image as numpy array (height, width, channels)

        Returns:
            List of num_colors RGB primary colors
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
            List of num_colors enhanced color palette in RGB
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

        # TODO: double check this
        # Convert HSV back to RGB
        rgb_colors = np.array(
            [colorsys.hsv_to_rgb(h, s, v) for h, s, v in hsv_colors]
        )  # Scale back to 0-255 range
        rgb_colors = np.uint8(rgb_colors * 255)
        return rgb_colors

    def _compute_complementary_colors(self, primary_colors: np.ndarray) -> np.ndarray:
        """Generate a list of 8 complementary colors given a list of 8 primary_colors
        Args:
            primary_colors: List of 8 RGB primary colors

        Returns:
            List of 8 complementary_colors
        """
        if self.config.debug_mode:
            print("Computing complementary colors")

        complementary_colors = primary_colors.copy()
        # Convert RGB colors to HSV
        normalized_rgb = complementary_colors.astype(float) / 255.0
        complementary_colors = np.array(
            [colorsys.rgb_to_hsv(r, g, b) for r, g, b in normalized_rgb]
        )
        # Generate random shifts between 0 and 180 degrees
        random_shifts = np.random.uniform(0, 180, size=len(primary_colors))
        # Shift the hue values by the random amounts
        # Hue values in HSV are in range [0, 1], so we divide by 360
        complementary_colors[:, 0] = (
            complementary_colors[:, 0] + random_shifts / 360.0
        ) % 1.0

        # Convert HSV back to RGB
        rgb_colors = np.array(
            [colorsys.hsv_to_rgb(h, s, v) for h, s, v in complementary_colors]
        )
        # Scale back to 0-255 range
        complementary_colors = np.uint8(rgb_colors * 255)

        return complementary_colors

    def validate_color_palette(self, color_palette: np.ndarray):
        """Validates that the color palette meets requirements.

        Args:
            color_palette: Array of RGB colors

        Raises:
            ValueError: If color palette is invalid
        """
        if not isinstance(color_palette, np.ndarray):
            raise ValueError("Color palette must be a NumPy array")

        if color_palette.shape != (self.COLOR_PALETTE_LENGTH, 3):
            raise ValueError("Color palette must contain exactly 16 RGB colors")

        if color_palette.dtype != np.uint8:
            raise ValueError("Color values must be uint8 (0-255)")

        if np.any(color_palette < 0) or np.any(color_palette > 255):
            raise ValueError("RGB values must be in range 0-255")
