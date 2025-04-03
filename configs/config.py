from dataclasses import dataclass


@dataclass
class PointillismConfig:
    # Preprocessing parameters
    kernel_size: int = 15
    downsample_factor: float = 0.5
    cluster_distance: int = 10
    intensity_alpha: int = 100

    # Debug mode
    debug_mode: bool = False
