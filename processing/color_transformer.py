import numpy as np
from configs.config import PointillismConfig
from models.dot_cluster import DotCluster


class ColorTransformer:

    def __init__(self, config: PointillismConfig = None):
        self.config = config or PointillismConfig()

    def transform(self, img: np.ndarray, color_palette: np.ndarray):
        if self.config.debug_mode:
            print("--Transforming image to dot clusters--")

        dot_clusters = []
        height, width, _ = img.shape

        for y in range(height):
            for x in range(width):
                pixel = img[y, x]
                selected_color = self._select_dot_cluster_colors(pixel, color_palette)
                dot_cluster = DotCluster((x, y), pixel, selected_color)
                dot_clusters.append(dot_cluster)
        print(len(dot_clusters))

    def _select_dot_cluster_colors(self, pixel: np.ndarray, color_palette: np.ndarray):
        # TODO: return 2 closest colors to pixel color + 1 random color
        return [0.231, 0.432, 0.432]
