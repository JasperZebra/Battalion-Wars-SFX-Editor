import tkinter as tk
from particle_editor import ParticleEffectEditor

if __name__ == "__main__":
    root = tk.Tk()
    app = ParticleEffectEditor(root)
    root.mainloop()