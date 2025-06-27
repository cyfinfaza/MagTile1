import tkinter as tk
from tkinter import messagebox
import time
from TileController import TileController

class MagneticCoilArrayGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Magnetic Coil Array Controller")
        
        self.controller = None
        self.width = 3
        self.height = 3
        self.cell_size = 50
        self.path = []
        
        self.setup_gui()
        
    def setup_gui(self):
        self.canvas = tk.Canvas(self.master, width=self.width*self.cell_size, height=self.height*self.cell_size)
        self.canvas.pack()
        
        self.draw_grid()
        
        self.canvas.bind("<Button-1>", self.on_click)
        
        tk.Button(self.master, text="Clear Path", command=self.clear_path).pack()
        tk.Button(self.master, text="Execute Path", command=self.execute_path).pack()
        tk.Button(self.master, text="Connect to Controller", command=self.connect_controller).pack()
        
    def draw_grid(self):
        for i in range(self.width):
            for j in range(self.height):
                x1 = i * self.cell_size
                y1 = j * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
        
    def on_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if (row, col) not in self.path:
            self.path.append((row, col))
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="red")
            if len(self.path) > 1:
                prev_row, prev_col = self.path[-2]
                self.canvas.create_line(
                    (prev_col + 0.5) * self.cell_size,
                    (prev_row + 0.5) * self.cell_size,
                    (col + 0.5) * self.cell_size,
                    (row + 0.5) * self.cell_size,
                    fill="blue", width=2
                )
        
    def clear_path(self):
        self.path = []
        self.canvas.delete("all")
        self.draw_grid()
        
    def connect_controller(self):
        try:
            port = '/dev/tty.usbmodem1101'  # Replace with your Arduino port
            self.controller = TileController(port)
            self.width = self.controller.read_width()
            self.height = self.controller.read_height()
            self.canvas.config(width=self.width*self.cell_size, height=self.height*self.cell_size)
            self.clear_path()
            messagebox.showinfo("Connection", "Successfully connected to the controller!")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
        
    def execute_path(self):
        if not self.controller:
            messagebox.showerror("Error", "Please connect to the controller first.")
            return
        
        if not self.path:
            messagebox.showwarning("Warning", "No path drawn. Please draw a path first.")
            return
        
        try:
            max_power = 4095
            for row, col in self.path:
                print(f"Activating coil at ({row}, {col})")
                self.controller.set_power(row, col, max_power)
                time.sleep(0.25)
                self.controller.set_power(row, col, 0)
            messagebox.showinfo("Execution Complete", "Path execution completed successfully!")
        except Exception as e:
            messagebox.showerror("Execution Error", f"An error occurred: {str(e)}")
        finally:
            self.turn_off_all_coils()
        
    def turn_off_all_coils(self):
        if self.controller:
            for row in range(self.height):
                for col in range(self.width):
                    self.controller.set_power(row, col, 0)

if __name__ == "__main__":
    root = tk.Tk()
    app = MagneticCoilArrayGUI(root)
    root.mainloop()