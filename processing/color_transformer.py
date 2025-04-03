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

        # Vectorized color selection for all pixels at once
        selected_colors = np.array(
            [self._select_dot_cluster_colors(pixel, color_palette) for pixel in pixels]
        )

        # Create dot clusters using list comprehension
        dot_clusters = [
            DotCluster((x, y), pixel, color)
            for (x, y), pixel, color in zip(coordinates, pixels, selected_colors)
        ]
        print(len(dot_clusters))

    def _select_dot_cluster_colors(self, pixel: np.ndarray, color_palette: np.ndarray):
        # TODO: return 2 closest colors to pixel color + 1 random color
        return [0.231, 0.432, 0.432]
