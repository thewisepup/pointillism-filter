import numpy as np


class DotCluster:

    # TODO: pass in configs that will be used to generate weights and counts
    def __init__(self, position, pixel_color, selected_colors):
        self.position = position
        self.pixel_color = pixel_color
        self.selected_colors = selected_colors
        self.color_weights = self._compute_color_weights()
        self.dot_counts = self._compute_color_dot_counts()

    def __str__(self):
        return f"DotCluster(pos={self.position}, pixel_color={self.pixel_color}, selected_colors={self.selected_colors})"

    def _compute_color_weights(self) -> np.ndarray:
        """
        Compute the weights for each selected_color to use for the pixel dot cluster

        Args:
            pixel_rgb: rgb value of input pixel to generate dot cluster for
            selected_colors: list of (3) colors to generate dot cluster

        Returns:
            weights: np.ndarray shape(3,)
        """
        # TODO: implement equations to compute color weights
        return [0.4, 0.4, 0.2]

    def _compute_color_dot_counts():
        """
        Compute the weights for each selected_color to use for the pixel dot cluster

        Args:
            pixel_rgb: rgb value of input pixel to generate dot cluster for
            selected_colors: list of (3) colors to generate dot cluster

        Returns:
            weights: np.ndarray shape(3,)
        """
        # TODO: implement equation to compute dot counts
        return [100, 422, 11]
