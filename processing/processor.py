import numpy as np
from configs.config import PointillismConfig
from processing.color_palette import ColorPalette
from processing.color_transformer import ColorTransformer
from processing.image_generator import ImageGenerator
from .preprocessor import PreProcessor
from PIL import Image


class Processor:
    def __init__(self, config: PointillismConfig = None):
        self.config = config or PointillismConfig()
        if self.config.debug_mode:
            print("Initializing PreProcessor with config:", self.config)
        self.preprocessor = PreProcessor(self.config)
        self.color_palette = ColorPalette(self.config)
        self.color_transformer = ColorTransformer(self.config)
        self.image_generator = ImageGenerator(self.config)

    def apply_pointillism(self, image: np.ndarray) -> np.ndarray:
        """Applies the pointillism effect to the input image.

        Args:
            image: A NumPy array of shape (height, width, 3) representing
                   an RGB image, with pixel values in the range [0, 255]
                   and data type `np.uint8`.

        Returns:
            A NumPy array representing the pointillism-rendered image.

        Raises:
            ValueError: If the input image is not a valid NumPy array
                        in the expected format.
        """
        if self.config.debug_mode:
            print("Starting pointillism effect application")

        self._validate_image_input(image)
        preprocessed_image = self.preprocessor.preprocess_image(image)
        self._validate_image_input(preprocessed_image)
        if self.config.debug_mode:
            debug_image = Image.fromarray(preprocessed_image, "RGB")
            debug_image.save("images/output/preprocessed_image.jpg")

        color_palette = self.color_palette.compute_pointillism_color_palette(
            preprocessed_image
        )
        assert len(color_palette) == 16
        self.visualize_color_palette(color_palette)
        dot_clusters = self.color_transformer.transform(
            preprocessed_image, color_palette
        )

        self.image_generator.generate(dot_clusters, preprocessed_image)

    def _validate_image_input(self, image: np.ndarray):
        """Validates the input image array meets the required specifications.

        Args:
            image (np.ndarray): The input image to validate.

        Raises:
            ValueError: If the image:
                - Is not a NumPy array
                - Does not have shape (height, width, 3)
                - Does not have data type np.uint8
                - Contains pixel values outside the range [0, 255]
        """
        if not isinstance(image, np.ndarray):
            raise ValueError("Input image must be a NumPy array.")
        if image.ndim != 3 or image.shape[2] != 3:
            raise ValueError("Input image must have shape (height, width, 3).")
        if image.dtype != np.uint8:
            raise ValueError("Input image must have data type np.uint8.")
        if np.any(image < 0) or np.any(image > 255):
            raise ValueError("Pixel values must be in the range [0, 255].")

    def visualize_color_palette(
        self,
        color_palette: np.ndarray,
        output_path: str = "images/output/color_palette.jpg",
    ):
        """Visualize the color palette as a grid of color swatches.

        Args:
            color_palette: Array of RGB colors of shape (16, 3)
            output_path: Path to save the visualization
        """
        # Create a 4x4 grid of color swatches
        swatch_size = 100  # Size of each color swatch in pixels
        grid_size = 4  # 4x4 grid for 16 colors
        image_size = swatch_size * grid_size

        # Create a blank image
        visualization = np.zeros((image_size, image_size, 3), dtype=np.uint8)

        # Fill in each swatch with its corresponding color
        for i in range(grid_size):
            for j in range(grid_size):
                idx = i * grid_size + j
                if idx < len(color_palette):
                    color = color_palette[idx]
                    y_start = i * swatch_size
                    y_end = (i + 1) * swatch_size
                    x_start = j * swatch_size
                    x_end = (j + 1) * swatch_size
                    visualization[y_start:y_end, x_start:x_end] = color

        # Convert to PIL Image and save
        Image.fromarray(visualization, "RGB").save(output_path)
