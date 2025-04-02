from configs.config import PointillismConfig
from models.dot_cluster import DotCluster
from processing.preprocessor import PreProcessor
from processing.image_generator import ImageGenerator
from processing.color_transformer import ColorTransformer
from processing.color_palette import ColorPalette


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
