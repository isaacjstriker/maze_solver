from tkinter import Tk, BOTH, Canvas

# First, create the window
class Window():
    # Initialize the window
    def __init__(self, width, height, title="Test Window"):
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.title(title)
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack(fill=BOTH, expand=True)
    # Redraw the window
    def redraw(self):
        self.root.update_idletasks()
        self.root.update()
    # Wait for the window to be closed
    def wait_for_close(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()
    # Close the window
    def on_close(self):
        self.root.destroy()