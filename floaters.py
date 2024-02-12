import tkinter as tk
import pyautogui
import ctypes
from PIL import Image, ImageTk
from ctypes import windll, wintypes

# windll.user32.SetThreadDpiAwarenessContext(wintypes.HANDLE(-2))  # Toggle ON
# windll.user32.SetThreadDpiAwarenessContext(wintypes.HANDLE(-1))  # Toggle OFF

GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080

def move_cursor_to_left_edge():
    # 0,100 - moves to left edge
    pyautogui.moveTo(0,100,duration=0.1)

def set_appwindow(root):
    hwnd = windll.user32.GetParent(root.winfo_id())
    style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW
    style = style | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
    # Re-assert the new window style
    root.wm_withdraw()
    root.after(10, lambda: root.wm_deiconify())

class DraggableWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Floating Image")

        # Remove window decorations and make it transparent
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        # Load the PNG image with alpha transparency
        self.image = Image.open("circle2x.png")
        self.photo = ImageTk.PhotoImage(self.image)

        # Create a label to display the image
        self.label = tk.Label(self, image=self.photo, bg="black")
        self.wm_attributes("-transparentcolor", "black")
        self.label.pack()

        # Bind mouse events for window dragging and click to show second circle
        self.label.bind("<ButtonPress-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.on_drag)
        self.label.bind("<ButtonRelease-1>", self.on_click)

        # Flag to track whether the second circle is visible
        self.second_circle_visible = False
        # Flag to track double/triple click
        self.click_count = 0
        self.click_time = 0

    def start_drag(self, event):
        self.x_orig = event.x_root
        self.y_orig = event.y_root
        self.x = event.x
        self.y = event.y

    def on_drag(self, event):
        x = self.winfo_x() + event.x - self.x
        y = self.winfo_y() + event.y - self.y
        self.geometry("+{}+{}".format(x, y))

    def on_click(self, event):
        dx = abs(event.x_root - self.x_orig)
        dy = abs(event.y_root - self.y_orig)
        current_time = event.time
        if dx < 5 and dy < 5:
            if current_time - self.click_time < 300:  # Within 300 ms, it's a double/triple click
                self.click_count += 1
            else:
                self.click_count = 1
            self.click_time = current_time

            if self.click_count == 3:  # If triple-click
                self.master.destroy()
            elif self.click_count == 1 and (abs(event.x - self.x) > 5 or abs(event.y - self.y) > 5):
                # If it's a single click but mouse moved significantly (indicating a drag), do nothing
                pass
            else:
                # Delay before executing the show_second_circle function
                self.after(300, self.delayed_show_second_circle)

    def delayed_show_second_circle(self):
        if self.click_count < 3:  # If it's not a triple-click
            self.show_second_circle()

    def show_second_circle(self):
        if not self.second_circle_visible:
            self.second_circle = FloatingCircle(master=self.master)
            self.second_circle.lift()
            self.second_circle.focus_set()  # Take focus
            self.second_circle_visible = True
            self.after(5000, self.destroy_second_circle)  # Destroy after 5 seconds
            set_appwindow(self.second_circle)
            move_cursor_to_left_edge()

    def destroy_second_circle(self):
        if self.second_circle_visible:
            self.second_circle.destroy()
            self.second_circle_visible = False

class FloatingCircle(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Second Circle")
        self.geometry("100x1")  # Set a small fixed size for the window

        # Add a standard title bar
        self.title_frame = tk.Frame(self, bg="lightgray", relief="raised", bd=1)
        self.title_frame.pack(fill="x")

        self.close_button = tk.Button(self.title_frame, text="X", command=self.destroy)
        self.close_button.pack(side="right")

        self.title_label = tk.Label(self.title_frame, text="Second Circle")
        self.title_label.pack(side="left", padx=5)

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def on_drag(self, event):
        x = self.winfo_x() + event.x - self.x
        y = self.winfo_y() + event.y - self.y
        self.geometry("+{}+{}".format(x, y))

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    app = DraggableWindow(root)
    # Show app in taskbar
    app.after(10, lambda: set_appwindow(app))
    app.mainloop()
