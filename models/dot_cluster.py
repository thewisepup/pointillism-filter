import numpy as np


class DotCluster:

    # TODO: pass in configs that will be used to generate weights and counts
    def __init__(self, position, pixel_color, selected_colors, alpha, I):
        self.position = position
        self.pixel_color = pixel_color
        self.selected_colors = selected_colors
        self.alpha = alpha
        self.intensity = I
        self.color_weights = self._compute_color_weights()
        self.dot_counts = self._compute_color_dot_counts()

    def __str__(self):
        return f"DotCluster(pos={self.position}, pixel_color={self.pixel_color}, selected_colors={self.selected_colors}, color_weights={self.color_weights})"

    def _compute_color_weights(self) -> np.ndarray:
        """
        Compute the weights for each selected_color to use for the pixel dot cluster

        Args:
            pixel_rgb: rgb value of input pixel to generate dot cluster for
            selected_colors: list of (3) colors to generate dot cluster

        Returns:
            weights: np.ndarray shape(3,)
        """
        # TODO: convert HSV to RGB
        # TODO: implement equations to compute color weights
        lhs = np.linalg.pinv(np.array(self.selected_colors))
        rhs = self.pixel_color.T
        return lhs * rhs

    def _compute_color_dot_counts(self):
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
