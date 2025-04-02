# Implementation Plan

## Overview
We want to create a program that takes in an image and configuration parameters and 
return a resulting output image where pointillism is applied to the image.

1. Preprocess Image
2. Color Selection
3. Color Transformation
4. Image Generation


## Section Descriptions
### 0. Configs

We want to create a PointillismConfig class that will contain custom configs for the program. 


### 1. Preprocessing
        a. Low Pass Filtering
        b. Down sampling

We want to preprocess the image to reduce the number of computations our algorithm needs to perform. 
We first want apply a low pass filter (Gaussian filter) to reduce aliasing. 
We then want to resize the images using sub sampling. 
We can additionally add additional filters to the preprocessing step.

### 2. Color Selection
        a. k means clustering
        b. convert rgb colors to hsv
        c. color saturation and brightness boosting
        d. add complement colors
We want to select the colors we want to use for out pointillism image. 
We will select 8 primary colors, convert the 8 colors to HSV, apply color saturation 
and brightness boosting, then add 8 more complementary colors.

### 3. Color Transformation
        a. select 3 colors for dot cluster
        b. compute weights for each color in dot cluster
        c. computer number of dots per dot cluster
For each pixel, we want to generate a dot cluster. 
A dot cluster is a number of dots using 3 colors to represent 1 pixel in the input image.



### 4. Image Generation
[Simple explanation of the final image generation process]

## Function Specifications


### Classes

class PointillismConfig:
    def __init__(self,
                 preprocessing_config=None,
                 color_palette_config=None,
                 color_transformer_config=None,
                 image_generator_config=None):
        self.preprocessing_config = preprocessing_config or PreprocessingConfig()
        self.color_palette_config = color_palette_config or ColorPaletteConfig()
        self.color_transformer_config = color_transformer_config or ColorTransformerConfig()
        self.image_generator_config = image_generator_config or ImageGeneratorConfig()
        
class PointillismProcessor:
    def __init__(self, config: PointillismConfig):
    #init all sub classes and processors
        self.preprocessor = PointillsimPreProcessor()
        self.colorpalette = ColorPalette()
        self.colortransformer = ColorTransformer()
        self.imagegenerator = ImageGenerator()

    def apply_pointillism(image):
        self.preprocessor.preprocess_image()
        self.colorpalette.generate_color_palette()
        self.colortransformer.generate_dot_clusters
        self.imagegenerator.generate_image()
        pass



### Preprocessing Functions
class PreprocessingConfig:
    ...add configs here

class PointillismPreProcessor:

    def __init__(configs)
        #init configs

    def preprocess_image(img: np.ndarray, cluster_distance: float) -> np.ndarray:
        """
        Preprocesses input image by applying Gaussian filtering and downsampling.
        
        Args:
            img: Input image as numpy array (height, width, channels)
            cluster_distance: Distance threshold that determines kernel size for Gaussian filter
            
        Returns:
            Processed image as numpy array
        """


    def __apply_gaussian_blur(img: np.ndarray, kernel_size: int) -> np.ndarray:
        """
        Applies Gaussian blur to the input image.
        
        Args:
            img: Input image as numpy array (height, width, channels)
            kernel_size: Size of the Gaussian kernel (must be odd)
            
        Returns:
            Blurred image as numpy array
        """

    def __downsample_image(img: np.ndarray, scale: float) -> np.ndarray:
        """
        Downsamples the input image by the specified scale factor.
        
        Args:
            img: Input image as numpy array (height, width, channels)
            scale: Scale factor between 0.1 and 1.0
            
        Returns:
            Downsampled image as numpy array
        """



### Color Selection Functions
class ColorPalette:

    def __init__(image):
        #init

    def compute_pointillism_color_palette(img: np.ndarray, intensity_alpha: float = 100.0) -> List[np.ndarray]
        """
        Select color palette for pointillism image by applying k-means clustering, color transformation, and adding complementary colors
        Args:
            img: Input image as numpy array (height, width, channels)
            
        Returns:
            List of 16 colors
        """

    def compute_primary_colors(img: np.ndarray, num_colors: int = 8) -> List[np.ndarray]
        """
        Apply k-means clustering to extarct num_colors primary colors
        Args:
            img: Input image as numpy array (height, width, channels)
            
        Returns:
            List of num_colors primary colors
        """

    def enhance_color_palette(colors: List[np.ndarray]) -> List[np.ndarray]
        """
        Convert RGB color to HSV and apply color enhancements. (Hard code saturation and brightness boost for now)
        Args:
            img: Input image as numpy array (height, width, channels)

        Returns:
            List of num_colors enhanced color palette
        """

    def compute_complementary_colors(primary_colors: List[np.ndarray]) -> List[np.ndarray]
        """
        Generate a list of 8 complementary colors given a list of 8 primary_colors
        Args:
            primary_colors: List of 8 HSV primary colors

        Returns:
            List of 8 complementary_colors
        """


### Color Transformation Functions

class ColorTransformers:

    def __init__(configs):
        #init configs

    def transform(image:List[np.ndarray], color_palette: List[np.ndarray]): -> dot_clusters List[DotCluster]
        """
        Generate a of dot clusters
        Args:
            image: preprocessed input image
            color_palatte: input color_palatte

        Returns:
            dot_clusters: List[DotCluster]
        """
        //pseudo code for generating dot_clusters
        for pixel in image:
            selected_colors = select_colors(pixel, color_palette)
            dot_clusters.add(DotCluster(position, pixel_color, selected_colors, config))
        return dot_clusters

class DotCluster:

    def __init__(self, position, pixel_color, selected_colors, config):
        self.position = position
        self.pixel_color = pixel_color
        self.selected_colors = selected_colors
        self.weights = self._compute_weights(pixel_color, selected_colors)
        self.dot_counts = self._compute_dot_counts(self.weights, config)

    def compute_color_weights(pixel_rgb shape (3,), selected_colors np.ndarry shape (3,3)) -> weights: np.ndarray shape(3,)
        """
        Compute the weights for each selected_color to use for the pixel dot cluster

        Args:
            pixel_rgb: rgb value of input pixel to generate dot cluster for
            selected_colors: list of (3) colors to generate dot cluster

        Returns:
            weights: np.ndarray shape(3,)
        """

    def compute_color_dot_count(weights, alpha, intensity):
        """
        Compute the weights for each selected_color to use for the pixel dot cluster

        Args:
            pixel_rgb: rgb value of input pixel to generate dot cluster for
            selected_colors: list of (3) colors to generate dot cluster

        Returns:
            weights: np.ndarray shape(3,)
        """


### Image Generation Functions

class ImageGenerator:

    def __init__():
        #init configs

    def generate(dot_clusters, configs):
        image = np.like(...)
        for cluster in dot_clusters:
            _draw_cluster(image, cluster, configs)
        return image

    def _draw_cluster(self, canvas, cluster):
        # Implementation of drawing a dot cluster on the canvas
        # Use cluster.position, cluster.selected_colors, and cluster.dot_counts
        pass


## Configuration Parameters
1. intensity_alpha (α) = 100.0
2. cluster_distance (d) = 25
3. scatter distribution std. (σ) 25.0 
4. scatter distribution mean (μ) 10.0
5. brushstroke radius (r) 6.0
6. brushstroke transparency 0.4
