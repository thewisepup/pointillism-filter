from dataclasses import dataclass


@dataclass
class PointillismConfig:
    # Preprocessing parameters
    kernel_size: int = 101
    downsample_factor: float = 0.5

    # Debug mode
    debug_mode: bool = False
