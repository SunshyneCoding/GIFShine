# GIFshine 

A powerful tool to manipulate and split GIF files into beautiful circular chunks!

## Features
- Interactive preview window with real-time feedback
- Resize and move selection with mouse controls
- Grid-based GIF splitting with customizable rows and columns
- Maintain aspect ratio option
- Smart size optimization
- Circular cropping option
- Output resizing capabilities
- Both GUI and CLI interfaces available

## Requirements
- Python 3.10 or higher
- Pillow 10.1.0 or higher (for image processing)
- tkinter (usually comes with Python)

## Installation
```bash
pip install -r requirements.txt
```

## Usage
### GUI Mode
```bash
python gifsplit_gui.py
```

#### GUI Interface Guide
1. **Input Selection**
   - Click "Select File" to choose your GIF
   - A preview window will automatically open

2. **Output Settings**
   - Default output directory is "gifsplit" in the input file's folder
   - Use "Browse" to choose a different location

3. **Preview Window Controls**
   - Click and drag to create/move selection
   - Grab edges/corners to resize selection
   - Selection maintains aspect ratio by default
   - Close and reopen preview with "Toggle Preview"

4. **Dimensions**
   - Adjust X, Y, Width, Height manually
   - "Maintain Ratio" keeps proportions locked
   - Set grid rows/columns for splitting
   - Enable "Circular Crop" for round outputs

5. **Options**
   - Set maximum size (KB) for optimization
   - Enable/disable optimization
   - Configure output dimensions

6. **Processing**
   - Click "Process GIF" to generate outputs
   - Progress bar shows operation status
   - Results saved to chosen output directory

### CLI Mode
```bash
python gifsplit_cli.py input.gif output_dir [options]

Options:
  --rows N        Number of rows to split into (default: 1)
  --cols N        Number of columns to split into (default: 1)
  --width N       Width of each output GIF (default: 200)
  --height N      Height of each output GIF (default: 200)
  --left N        Left position of the crop area (default: 0)
  --top N         Top position of the crop area (default: 0)
  --circular      Make the output GIFs circular
  --max-size N    Maximum size per chunk in KB (default: 500)
```

## Dependencies and Licenses
This project uses the following open-source libraries:

- **Pillow (PIL Fork)** - [Python Imaging Library](https://python-pillow.org/)
  - License: [HPND License](https://github.com/python-pillow/Pillow/blob/main/LICENSE)
  - Used for image processing and GIF manipulation

- **tkinter** - [Python's Standard GUI Library](https://docs.python.org/3/library/tkinter.html)
  - License: [Python Software Foundation License](https://docs.python.org/3/license.html)
  - Used for the graphical user interface

## License
GIFshine is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Copyright
GIFshine by SunshyneCoding 2025
