import numpy as np


def rgb_to_hsv(rgb: np.ndarray) -> np.ndarray:
    """Convert RGB color to HSV color space."""
    rgb = rgb.astype(float) / 255.0
    r, g, b = rgb

    max_val = max(r, g, b)
    min_val = min(r, g, b)
    diff = max_val - min_val

    if diff == 0:
        h = 0
    elif max_val == r:
        h = (60 * ((g - b) / diff) + 360) % 360
    elif max_val == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    else:
        h = (60 * ((r - g) / diff) + 240) % 360

    s = 0 if max_val == 0 else diff / max_val
    v = max_val

    return np.array([h / 360, s, v])


def hsv_distance(hsv1: np.ndarray, hsv2: np.ndarray) -> float:
    """Calculate distance between two HSV colors."""
    # Convert to numpy arrays if not already
    hsv1 = np.array(hsv1)
    hsv2 = np.array(hsv2)

    # Calculate circular distance for hue
    h_diff = min(abs(hsv1[0] - hsv2[0]), 1 - abs(hsv1[0] - hsv2[0]))

    # Calculate Euclidean distance for saturation and value
    s_diff = hsv1[1] - hsv2[1]
    v_diff = hsv1[2] - hsv2[2]

    # Weighted distance (giving more importance to hue)
    return np.sqrt(2 * h_diff**2 + s_diff**2 + v_diff**2)
