from dataclasses import dataclass


@dataclass
class PointillismConfig:
    # Preprocessing parameters
    kernel_size: int = 15
    downsample_factor: float = 0.5
    cluster_distance: int = 6
    intensity_alpha: int = 100
    gamma_distortion: float = 1.8
    scatter_distribution_mean = 6  # mu
    scatter_distribution_std = 6  # sigma
    brushstroke_radius = 2
    opacity = 0.5
    # Debug mode
    debug_mode: bool = False
