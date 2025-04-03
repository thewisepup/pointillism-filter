import numpy as np
from configs.config import PointillismConfig
from models.dot_cluster import DotCluster


class ColorTransformer:

    def __init__(self, config: PointillismConfig = None):
        self.config = config or PointillismConfig()

    def transform(self, img: np.ndarray, color_palette: np.ndarray):
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

        # TODO: get Intensity map from inverse grayscale map and add it to list comprehnsion
        I = 1.8
        dot_clusters = [
            DotCluster((x, y), pixel, color, self.config.intensity_alpha, I)
            for (x, y), pixel, color in zip(coordinates, pixels, selected_colors)
        ]
        for cluster in dot_clusters:
            print(cluster)
        if self.config.debug_mode:
            print("--Finished transforming image to dot clusters--")
        return dot_clusters

    def _select_dot_cluster_colors(self, pixel: np.ndarray, color_palette: np.ndarray):
        # Convert RGB pixel to HSV
        pixel_hsv = self._rgb_to_hsv(pixel)

        # Calculate distances between pixel and all colors in palette
        distances = np.array(
            [self._hsv_distance(pixel_hsv, color) for color in color_palette]
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

    def _rgb_to_hsv(self, rgb: np.ndarray) -> np.ndarray:
        """Convert RGB color to HSV color space."""
        rgb = rgb.astype(float) / 255.0
        r, g, b = rgb

        max_val = max(r, g, b)
        min_val = min(r, g, b)
        diff = max_val - min_val

        if diff == 0:
            h = 0
        elif max_val == r:
            h = (60 * ((g - b) / diff) + 360) % 360
        elif max_val == g:
            h = (60 * ((b - r) / diff) + 120) % 360
        else:
            h = (60 * ((r - g) / diff) + 240) % 360

        s = 0 if max_val == 0 else diff / max_val
        v = max_val

        return np.array([h / 360, s, v])

    def _hsv_distance(self, hsv1: np.ndarray, hsv2: np.ndarray) -> float:
        """Calculate distance between two HSV colors."""
        # Convert to numpy arrays if not already
        hsv1 = np.array(hsv1)
        hsv2 = np.array(hsv2)

        # Calculate circular distance for hue
        h_diff = min(abs(hsv1[0] - hsv2[0]), 1 - abs(hsv1[0] - hsv2[0]))

        # Calculate Euclidean distance for saturation and value
        s_diff = hsv1[1] - hsv2[1]
        v_diff = hsv1[2] - hsv2[2]

        # WARN double check if we want this: Weighted distance (giving more importance to hue)
        return np.sqrt(2 * h_diff**2 + s_diff**2 + v_diff**2)
