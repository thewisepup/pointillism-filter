import random
from typing import List
import cv2
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

        return canvas

    def _draw_cluster(self, canvas: np.ndarray, cluster: DotCluster):
        center_x = int(cluster.position[0] * self.config.cluster_distance)
        center_y = int(cluster.position[1] * self.config.cluster_distance)
        center = (center_x, center_y)

        # Create a temporary layer for all dots
        temp_layer = np.zeros_like(canvas)

        # Generate points for all three colors
        color1_points = self._generate_dot_points(center, int(cluster.dot_counts[0]))
        color2_points = self._generate_dot_points(center, int(cluster.dot_counts[1]))
        color3_points = self._generate_dot_points(center, int(cluster.dot_counts[2]))

        # Draw all dots for each color
        for x, y in color1_points:
            cv2.circle(
                canvas,
                (int(x), int(y)),
                self.config.brushstroke_radius,
                tuple(map(int, cluster.selected_colors[0][::-1])),
                -1,
            )

        for x, y in color2_points:
            cv2.circle(
                canvas,
                (int(x), int(y)),
                self.config.brushstroke_radius,
                tuple(map(int, cluster.selected_colors[1][::-1])),
                -1,
            )

        for x, y in color3_points:
            cv2.circle(
                canvas,
                (int(x), int(y)),
                self.config.brushstroke_radius,
                tuple(map(int, cluster.selected_colors[2][::-1])),
                -1,
            )

    def _generate_dot_points(self, center, num_dots: int):
        """
        Generate a dot cluster around a center point.
        Each dot is positioned by sampling from a Gaussian distribution.
        """
        if num_dots <= 0:
            return []
        dots = []
        x_offsets = np.random.normal(
            loc=self.config.scatter_distribution_mean,
            scale=self.config.scatter_distribution_std,
            size=num_dots,
        )
        y_offsets = np.random.normal(
            loc=self.config.scatter_distribution_mean,
            scale=self.config.scatter_distribution_std,
            size=num_dots,
        )
        dots = np.stack((center[0] + x_offsets, center[1] + y_offsets), axis=-1)
        return dots

    def _validate_cluster_and_image(
        self, dot_clusters: List[DotCluster], preprocessed_image: np.ndarray
    ):
        row, col, _ = preprocessed_image.shape
        assert row * col == len(dot_clusters)

        for cluster in dot_clusters:
            x, y = cluster.position[0], cluster.position[1]
            assert 0 <= x < col
            assert 0 <= y < row
