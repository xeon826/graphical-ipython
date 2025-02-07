# ipython-icat

[![PyPI version](https://img.shields.io/pypi/v/ipython-icat.svg?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/ipython-icat/)

## Installation

You can install `ipython-icat` using pip:

```bash
pip install ipython-icat
```

## Requirements

- Python 3.9+
- IPython
- matplotlib
- Pillow (PIL)
- kitty terminal

## Usage

### Loading the Extension

In your IPython session, load the extension:

```python
%load_ext icat
```

### Displaying Matplotlib Plots

To use the kitty backend for matplotlib:

```python
%plt_icat
```

After running this command, any matplotlib plots you create will be displayed directly in your kitty terminal.

### Displaying Images

To display an image file or a PIL Image object:

```python
%icat path/to/your/image.jpg
```

or

```python
from PIL import Image
img = Image.open('path/to/your/image.jpg')
%icat img
```

You can also resize the image when displaying:

```python
%icat path/to/your/image.jpg -w 300 -h 200
```

## Features

- Display matplotlib plots directly in kitty terminal
- Show PIL Image objects or image files
- Resize images on display
- Seamless integration with IPython workflow

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [matplotlib-backend-kitty](https://github.com/jktr/matplotlib-backend-kitty) for the original implementation
- [matplotlib](https://github.com/matplotlib/matplotlib) and [Pillow](https://python-pillow.org/) for their excellent libraries
- [kitty terminal](https://github.com/kovidgoyal/kitty) for supporting image protocol

## Contact

If you have any questions or feedback, please open an issue on the GitHub repository.

