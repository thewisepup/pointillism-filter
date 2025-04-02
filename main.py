from configs.config import PointillismConfig
from models.dot_cluster import DotCluster
from processing import PreProcessor, ImageGenerator, ColorTransformer, ColorPalette


def main():
    # Initialize configuration
    config = PointillismConfig()

    # Initialize all required classes
    dot_cluster = DotCluster()
    preprocessor = PreProcessor()
    image_generator = ImageGenerator()
    color_transformer = ColorTransformer()
    color_palette = ColorPalette()

    print("All components initialized successfully!")


if __name__ == "__main__":
    main()
