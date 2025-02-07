# modified from https://github.com/Kabilan108/ipython-icat

from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.core.magic import Magics, magics_class, line_magic
from IPython.core.displayhook import DisplayHook

from subprocess import run
from io import BytesIO
import sys
import os

from matplotlib.backend_bases import _Backend, FigureManagerBase
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib import interactive, is_interactive
from matplotlib._pylab_helpers import Gcf
import matplotlib

from PIL import Image

if hasattr(sys, "ps1") or sys.flags.interactive:
    interactive(True)


def _run(*cmd):
    def f(*args, output=True, **kwargs):
        if output:
            kwargs["capture_output"] = True
            kwargs["text"] = True
        r = run(cmd + args, **kwargs)
        if output:
            return r.stdout.rstrip()

    return f


_icat = _run("kitty", "+kitten", "icat", "--align", "left")


class FigureManagerICat(FigureManagerBase):
    def show(self):
        with BytesIO() as buf:
            self.canvas.figure.savefig(buf, format="png")
            _icat(output=False, input=buf.getbuffer())


class FigureCanvasICat(FigureCanvasAgg):
    manager_class = FigureManagerICat


@_Backend.export
class _BackendICatAgg(_Backend):
    FigureCanvas = FigureCanvasICat
    FigureManager = FigureManagerICat
    mainloop = lambda: None

    @classmethod
    def draw_if_interactive(cls):
        manager = Gcf.get_active()
        if is_interactive() and manager.canvas.figure.get_axes():
            cls.show()

    @classmethod
    def show(cls, *args, **kwargs):
        _Backend.show(*args, **kwargs)
        Gcf.destroy_all()


@magics_class
class ICatMagics(Magics):
    @line_magic
    def plt_icat(self, line):
        matplotlib.use("module://icat")
        print("loaded icat backend for mpl")

    @magic_arguments()
    @argument("image", help="PIL Image object or path to image file")
    @argument("-w", "--width", type=int, help="Width to resize the image")
    @argument("-h", "--height", type=int, help="Height to resize the image")
    @line_magic
    def icat(self, line):
        args = parse_argstring(self.icat, line)
        image_arg = args.image.strip()

        # check if the input is a variable in the user's ns
        user_ns = self.shell.user_ns
        if image_arg in user_ns and isinstance(user_ns[image_arg], Image.Image):
            img = user_ns[image_arg]
        elif os.path.isfile(image_arg):
            img = Image.open(image_arg)
        else:
            print(
                f"Error: '{image_arg}' is neither a valid PIL Image nor a path to an image file."
            )
            return

        # resize the image if width or height is specified
        if args.width or args.height:
            img.thumbnail((args.width or img.width, args.height or img.height))

        # display image
        with BytesIO() as buf:
            img.save(buf, format="PNG")
            _icat(output=False, input=buf.getbuffer())

class CustomDisplayHook(DisplayHook):
    def __init__(self, shell):
        self.shell = shell

    def __call__(self, result=None):
        if result is None:
            return
        # Custom logic to handle result display
        print("Custom display:", repr(result))

def icat(img: Image.Image, width: int = None, height: int = None):
    img_ = img.copy()
    with BytesIO() as buf:
        if width or height:
            img_.thumbnail((width or img.width, height or img.height))
        img_.save(buf, format="PNG")
        _icat(output=False, input=buf.getbuffer())


def load_ipython_extension(ipython):

    hook = CustomDisplayHook(shell=ipython)

    # Obtain the current config and set the display hook class programmatically
    ipython.config.InteractiveShell.displayhook_class = hook
    # Initialize with the shell
    ipython.displayhook = CustomDisplayHook(shell=ipython)
    ipython.register_magics(ICatMagics)
