import numpy as np
from configs.config import PointillismConfig
from models.dot_cluster import DotCluster
from utils.rgb_hsv_utils import hsv_distance, rgb_to_hsv


class ColorTransformer:

    def __init__(self, config: PointillismConfig = None):
        self.config = config or PointillismConfig()

    def transform(self, img: np.ndarray, color_palette: np.ndarray):
        """Transform an input image into a collection of dot clusters using a specified color palette.

        Args:
            img (np.ndarray): Input RGB image of shape (height, width, 3)
            color_palette (np.ndarray): Array of RGB colors to use for the dot clusters, shape (n, 3)

        Returns:
            list[DotCluster]: List of dot clusters, where each cluster contains:
                - Position (x, y) coordinates
                - Original pixel color
                - Selected colors from palette
                - Intensity value based on inverted grayscale
        """
        if self.config.debug_mode:
            print("--Transforming image to dot clusters--")

        # Get all pixels at once and reshape to 2D array of pixels
        pixels = img.reshape(-1, 3)

        # Get coordinates for all pixels
        y_coords, x_coords = np.unravel_index(np.arange(pixels.shape[0]), img.shape[:2])
        coordinates = np.column_stack((x_coords, y_coords))

        if self.config.debug_mode:
            print("creating selected clusters")
        # Vectorized color selection for all pixels at once
        selected_colors = np.array(
            [self._select_dot_cluster_colors(pixel, color_palette) for pixel in pixels]
        )

        if self.config.debug_mode:
            print("creating dot clusters")

        inversed_grayscale_image = self._convert_image_to_inversed_grayscale(img)
        inversed_grayscale_image = inversed_grayscale_image.reshape(-1, 1)
        dot_clusters = [
            DotCluster((x, y), pixel, color, self.config.intensity_alpha, intensity)
            for (x, y), pixel, color, intensity in zip(
                coordinates, pixels, selected_colors, inversed_grayscale_image
            )
        ]
        # for cluster in dot_clusters:
        #     print(cluster)
        if self.config.debug_mode:
            print("--Finished transforming image to dot clusters--")
        return dot_clusters

    def _convert_image_to_inversed_grayscale(self, img: np.ndarray):
        """Convert an RGB image to an inverted grayscale intensity map with gamma correction.

        This method creates an intensity map that will be used to determine dot sizes in the
        pointillism effect. Darker areas in the original image will result in larger dots,
        while lighter areas will result in smaller dots.

        The process involves:
        1. Converting the image to grayscale by taking the mean of RGB channels
        2. Inverting the grayscale values (255 - grayscale)
        3. Normalizing values to [0,1] range
        4. Applying gamma correction using the configured gamma_distortion value
        5. Converting back to [0,255] range as uint8

        Args:
            img (np.ndarray): Input RGB image of shape (height, width, 3)

        Returns:
            np.ndarray: Inverted grayscale intensity map of shape (height, width) with values in [0,255]
        """
        # Convert to grayscale and invert
        grayscale = 255 - np.mean(img, axis=2)
        # Normalize to [0,1] range
        normalized = grayscale / 255.0
        # Apply gamma correction
        gamma_corrected = np.power(normalized, self.config.gamma_distortion)
        # Convert back to [0,255] range and uint8
        inversed_grayscale_image = (gamma_corrected * 255).astype(np.uint8)
        return inversed_grayscale_image

    def _select_dot_cluster_colors(self, pixel: np.ndarray, color_palette: np.ndarray):
        """Select colors for a dot cluster based on the input pixel and color palette.

        This method selects three colors for each dot cluster:
        1. The two closest colors from the palette to the input pixel
        2. One random color from the remaining colors in the palette

        The color selection is based on HSV color space distance to ensure
        perceptually meaningful color matches.

        Args:
            pixel (np.ndarray): Input RGB pixel of shape (3,)
            color_palette (np.ndarray): Array of RGB colors to choose from, shape (n, 3)

        Returns:
            list: List of three RGB colors, where the first two are the closest matches
                  and the third is a random color from the remaining palette
        """
        # Convert RGB pixel to HSV
        pixel_hsv = rgb_to_hsv(pixel)

        # Calculate distances between pixel and all colors in palette
        distances = np.array(
            [hsv_distance(pixel_hsv, color) for color in color_palette]
        )

        # Get indices of 2 closest colors
        closest_indices = np.argsort(distances)[:2]
        closest_colors = color_palette[closest_indices].tolist()

        # Get remaining colors (excluding the 2 closest)
        remaining_indices = np.setdiff1d(np.arange(len(color_palette)), closest_indices)
        remaining_colors = color_palette[remaining_indices]

        # Select 1 random color from remaining colors
        random_color = remaining_colors[
            np.random.randint(len(remaining_colors))
        ].tolist()

        # Combine closest colors and random color
        return closest_colors + [random_color]


"""
TODO: color pallete needs to return RGB not HSV
TOOD: _select_dot_cluster_colors needs to return RGB colors
TODO: dot clusters need to use rgb values
"""
