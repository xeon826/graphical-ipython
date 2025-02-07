from base64 import b64encode
from IPython.lib.latextools import latex_to_png
from PIL import Image
from io import BytesIO

def write_chunked(cmd, data):
    """Write chunked data to kitty terminal."""
    import sys
    from base64 import b64encode

    data = b64encode(data)
    while data:
        chunk, data = data[:4096], data[4096:]
        m = 1 if data else 0
        sys.stdout.buffer.write(f"\033_G{cmd},m={m};".encode())
        sys.stdout.buffer.write(chunk + b"\033\\")
        sys.stdout.flush()

def imcat(image_data, metadata):
    print('asdf')
    """Display image data using kitty's terminal graphics protocol."""
    try:
        # Convert bytes to PIL Image if it's raw image data
        if isinstance(image_data, bytes):
            img = Image.open(BytesIO(image_data))
        elif isinstance(image_data, Image.Image):
            img = image_data
        else:
            img = Image.open(BytesIO(image_data))
        
        # Convert to PNG format in memory
        bio = BytesIO()
        img.save(bio, format='PNG')
        
        # Get the binary data
        payload = bio.getvalue()
        
        # Calculate dimensions
        width, height = img.size
        
        # Construct the command for kitty
        cmd = {
            'a': 'T',  # Temporary image
            'f': 100,  # PNG format
            's': width,
            'v': height,
        }
        
        # Convert command dict to string
        cmd_str = ','.join(f'{k}={v}' for k, v in cmd.items())
        
        # Write the image data in chunks
        write_chunked(cmd_str, payload)
        
        # Move cursor to next line
        print()
        
    except Exception as e:
        print(f"Error displaying image: {str(e)}")

def mathcat(data, meta):
    """Convert LaTeX to PNG and display it."""
    png = latex_to_png(f'$${data}$$'.replace('\displaystyle', '').replace('$$$', '$$'))
    imcat(png, meta)

def handle_matplotlib(fig, meta):
    print('matplot lib')
    """Convert matplotlib figure to image and display it."""
    bio = BytesIO()
    fig.canvas.print_figure(bio, format='png', bbox_inches='tight')
    bio.seek(0)
    imcat(bio.getvalue(), meta)

def register_mimerenderer(ipython, mime, handler):
    """Register a handler for a specific MIME type in IPython."""
    # Ensure the MIME type is in active types
    if mime not in ipython.display_formatter.active_types:
        ipython.display_formatter.active_types.append(mime)
    
    # Enable the formatter for this MIME type
    ipython.display_formatter.formatters[mime].enabled = True
    
    # Register the handler
    ipython.mime_renderers[mime] = handler

def load_ipython_extension(ipython):
    """Load the extension and register all supported MIME type handlers."""
    # Register handlers for different image types
    register_mimerenderer(ipython, 'image/png', imcat)
    register_mimerenderer(ipython, 'image/jpeg', imcat)
    register_mimerenderer(ipython, 'text/latex', mathcat)
    # register_mimerenderer(ipython, 'application/vnd.matplotlib.figure', handle_matplotlib)

    
    # Also handle PIL Image objects directly
    def _repr_png_(self):
        bio = BytesIO()
        self.save(bio, format='PNG')
        return bio.getvalue()
    
    # Add PNG representation method to PIL Image if not already present
    if not hasattr(Image.Image, '_repr_png_'):
        Image.Image._repr_png_ = _repr_png_
