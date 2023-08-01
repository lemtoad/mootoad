import tkinter as tk
from gui import LembotGUI

def main():
    root = tk.Tk()
    app = LembotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
