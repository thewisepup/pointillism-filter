import random
from typing import List
import numpy as np
from configs.config import PointillismConfig
from models.dot_cluster import DotCluster
from PIL import Image


class ImageGenerator:
    def __init__(self, config: PointillismConfig = None):
        self.config = config or PointillismConfig()

    def generate(self, dot_clusters: List[DotCluster], preprocessed_image: np.ndarray):
        self._validate_cluster_and_image(dot_clusters, preprocessed_image)

        height, width, channels = preprocessed_image.shape
        print(preprocessed_image.shape)
        scaled_height = self.config.cluster_distance * height
        scaled_width = self.config.cluster_distance * width

        # Create a white canvas with the scaled dimensions
        canvas = np.full(
            (int(scaled_height), int(scaled_width), 3), 255, dtype=np.uint8
        )
        print(canvas.shape)
        for cluster in dot_clusters:
            self._draw_cluster(canvas, cluster)
        if self.config.debug_mode:
            debug_image = Image.fromarray(canvas, "RGB")
            debug_image.save("images/output/canvas.jpg")

        print(canvas)
        return canvas

    def _draw_cluster(self, canvas: np.ndarray, cluster: DotCluster):
        center_x = int(cluster.position[0] * self.config.cluster_distance)
        center_y = int(cluster.position[1] * self.config.cluster_distance)

        # Fill the cluster area with black
        canvas[center_y, center_x] = [0, 0, 0]

    def _validate_cluster_and_image(
        self, dot_clusters: List[DotCluster], preprocessed_image: np.ndarray
    ):
        row, col, _ = preprocessed_image.shape
        assert row * col == len(dot_clusters)

        for cluster in dot_clusters:
            x, y = cluster.position[0], cluster.position[1]
            assert 0 <= x < col
            assert 0 <= y < row
