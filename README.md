# Pointillism Filter

## Overview

This project implements a digital pointillism filter that converts regular images into artwork composed of distinct dots of color. The filter creates an artistic effect by breaking down the image into small, distinct points of color that, when viewed from a distance, blend together to form the complete image.

Pointillism algorithm taken from the following Stanford research paper.

https://web.stanford.edu/class/ee368/Project_Autumn_1516/Reports/Hong_Liu.pdf

## Features

## Requirements

- Python
- NumPy
- OpenCV
- Pillow

## Installation

1. Clone the repository:
```bash
git clone https://github.com/thewisepup/pointillism-filter.git
cd pointillism-filter
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Project Structure

```
pointillism-filter/
├── configs/           # Configuration files
├── images/           # Input and output images
├── models/           # Model-related code
├── processing/       # Image processing modules
├── main.py          # Main application entry point
└── requirements.txt  # Project dependencies
```

## Configuration

The filter can be configured through the `PointillismConfig` class in the configs directory. Key parameters include:
- `debug_mode`: Enable/disable debug output (default: True)
- TODO add more configuration explanation  

