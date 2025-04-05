import numpy as np


class DotCluster:

    def __init__(self, position, pixel_color, selected_colors, alpha, I):
        # Validate pixel color is a valid RGB array with values between 0-255
        if not isinstance(pixel_color, np.ndarray) or pixel_color.shape != (3,):
            raise ValueError("pixel_color must be a numpy array of shape (3,)")
        if not np.issubdtype(pixel_color.dtype, np.integer):
            raise ValueError("pixel_color must contain integer values")
        if np.any(pixel_color < 0) or np.any(pixel_color > 255):
            raise ValueError("pixel_color values must be between 0 and 255")

        # Validate selected colors is a list of 3 valid RGB arrays
        if len(selected_colors) != 3:
            raise ValueError(
                "selected_colors must be a list of 3 RGB colors" + selected_colors
            )
        for color in selected_colors:
            if not isinstance(color, np.ndarray) or color.shape != (3,):
                raise ValueError(
                    "Each selected color must be a numpy array of shape (3,)"
                )
            if not np.issubdtype(color.dtype, np.integer):
                raise ValueError("Selected colors must contain integer values")
            if np.any(color < 0) or np.any(color > 255):
                raise ValueError("Selected color values must be between 0 and 255: ")

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
            np.ndarray: A 3x1 array of weights for each selected color
        """
        # TODO: Some values return negative values or grater than 1. Trust that the math is right
        C = np.array(self.selected_colors)
        P = np.array(np.array(self.pixel_color)).reshape(3, 1)
        C_inv = np.linalg.inv(C)
        Q = C_inv @ P
        return Q

    def _compute_color_dot_counts(self) -> np.ndarray:
        """
        Compute the number of dots for each selected color based on the color weights and intensity.

        Returns:
            np.ndarray: A 3x1 array containing the number of dots for each selected color
        """
        rhs = (self.alpha * self.intensity) / np.sum(self.color_weights)
        dot_counts = self.color_weights @ rhs
        return dot_counts
