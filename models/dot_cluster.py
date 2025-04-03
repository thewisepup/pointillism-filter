class DotCluster:
    def __init__(self, position, pixel_color, selected_colors):
        self.position = position
        self.pixel_color = pixel_color
        self.selected_colors = selected_colors

    def __str__(self):
        return f"DotCluster(pos={self.position}, pixel_color={self.pixel_color}, selected_colors={self.selected_colors})"
