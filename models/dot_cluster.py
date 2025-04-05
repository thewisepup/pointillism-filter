import numpy as np


class DotCluster:

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
        Compute the weights (Q) for each selected color to use for the pixel dot cluster.
        Solves the equation Q = C^-1 · P where:
        - C is a 3x3 matrix containing the RGB values of the three selected colors
        - P is a 3x1 matrix containing the RGB values of the original pixel
        - Q is a 3x1 matrix of weights for each selected color

        Returns:
            np.ndarray: A flattened array of weights for each selected color
        """
        # TODO: double check math

        C = np.array(self.selected_colors)
        P = np.array(self.pixel_color).reshape(3, 1)
        C_inv = np.linalg.pinv(C)
        Q = C_inv @ P  # Matrix multiplication

        return Q.flatten()  # Return as a flat array

    def _compute_color_dot_counts(self):
        """
        Compute the weights for each selected_color to use for the pixel dot cluster

        Args:
            pixel_rgb: rgb value of input pixel to generate dot cluster for
            selected_colors: list of (3) colors to generate dot cluster

        Returns:
            weights: np.ndarray shape(3,)
        """
        # TODO: double check
        dot_counts = self.color_weights * (
            (self.alpha * self.intensity) // 100
        )  # TODO: do sum of weights instead of 100
        return dot_counts
