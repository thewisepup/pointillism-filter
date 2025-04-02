import numpy as np
from configs.config import PointillismConfig
from .preprocessor import PreProcessor


class Processor:
    def __init__(self, config: PointillismConfig):
        # init all sub classes and processors
        self.preprocessor = PreProcessor()

    def apply_pointillism(self, image: np.ndarray) -> np.ndarray:
        self.preprocessor.preprocess_image()
