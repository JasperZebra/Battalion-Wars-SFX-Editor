import tkinter as tk
from tkinter import ttk

class ThemeManager:
    def __init__(self, root):
        self.root = root
        self.colors = self.define_colors()
    
    def define_colors(self):
        """Define a color palette inspired by Battalion Wars 2"""
        return {
            'background': '#2A2C2E',       # Dark gray background
            'foreground': '#FFFFFF',       # White text
            'accent1': '#D82800',          # Red accent (for buttons, highlights)
            'accent2': '#FFB300',          # Yellow accent (for titles, important elements)
            'accent3': '#45A018',          # Green accent
            'accent4': '#2F95D8',          # Blue accent
            'border': '#000000',           # Black borders
            'input_bg': '#3A3C3E',         # Slightly lighter gray for inputs
            'button_bg': '#D82800',        # Red buttons
            'button_fg': '#FFFFFF',        # White text on buttons
            'button_pressed': '#A01800',   # Darker red when pressed
            'title_bg': '#3F3F3F',         # Title background
            'status_bg': '#333537',        # Status bar background
        }
    
    def setup_theme(self):
        """Configure Battalion Wars 2 inspired styling for the application"""
        # Create a style object
        style = ttk.Style()
        
        # Use clam theme as base
        style.theme_use('clam')

        # GLOBAL STYLE CONFIGURATION
        style.configure('.',
            background=self.colors['background'],
            foreground=self.colors['foreground'],
            fieldbackground=self.colors['input_bg'],
            troughcolor=self.colors['background'],
            borderwidth=2,
            font=('Arial Black', 10)  # Bold, military-like font
        )

        # FRAME STYLING
        style.configure('Military.TFrame',
            background=self.colors['background']
        )
        
        style.configure('TitleBG.TFrame',
            background=self.colors['title_bg']
        )
        
        style.configure('Preview.TFrame',
            background=self.colors['background']
        )
        
        style.configure('PreviewBorder.TFrame',
            background=self.colors['accent2'],
            borderwidth=2,
            relief='solid'
        )
        
        # Colored label frames for RGB sliders
        style.configure('RedLabel.TFrame',
            background=self.colors['accent1'],
            borderwidth=2,
            relief='solid'
        )
        
        style.configure('GreenLabel.TFrame',
            background=self.colors['accent3'],
            borderwidth=2,
            relief='solid'
        )
        
        style.configure('BlueLabel.TFrame',
            background=self.colors['accent4'],
            borderwidth=2,
            relief='solid'
        )
        
        style.configure('AlphaLabel.TFrame',
            background='#8F8F8F',
            borderwidth=2,
            relief='solid'
        )

        # LABEL FRAME STYLING
        style.configure('Military.TLabelframe',
            background=self.colors['background'],
            bordercolor=self.colors['accent2'],
            borderwidth=3
        )
        style.configure('Military.TLabelframe.Label',
            background=self.colors['background'],
            foreground=self.colors['accent2'],
            font=('Arial Black', 11)
        )

        # BUTTON STYLING - Military style
        style.configure('Military.TButton',
            background=self.colors['button_bg'],
            foreground=self.colors['button_fg'],
            bordercolor=self.colors['border'],
            borderwidth=2,
            relief='raised',
            padding=6,
            font=('Arial Black', 9)
        )
        style.map('Military.TButton',
            background=[('pressed', self.colors['button_pressed']), ('active', self.colors['button_pressed'])],
            foreground=[('pressed', self.colors['button_fg']), ('active', self.colors['button_fg'])]
        )
        
        # "Deploy" button - special styling
        style.configure('Deploy.TButton',
            background=self.colors['accent3'],  # Green for "Deploy"
            foreground=self.colors['button_fg'],
            bordercolor=self.colors['border'],
            borderwidth=2,
            relief='raised',
            padding=6,
            font=('Arial Black', 10)
        )
        style.map('Deploy.TButton',
            background=[('pressed', '#2F7010'), ('active', '#3A8818')],
            foreground=[('pressed', self.colors['button_fg']), ('active', self.colors['button_fg'])]
        )

        # LABEL STYLING
        style.configure('Military.TLabel',
            background=self.colors['background'],
            foreground=self.colors['foreground'],
            font=('Arial Black', 9)
        )
        
        # Title style
        style.configure('Title.TLabel', 
            background=self.colors['title_bg'],
            foreground=self.colors['accent2'],
            font=('Arial Black', 16),
            anchor='center'
        )
        
        # Value label style
        style.configure('Value.TLabel', 
            background=self.colors['background'],
            foreground=self.colors['accent2'],
            font=('Arial Black', 10)
        )
        
        # Value header style
        style.configure('ValueHeader.TLabel', 
            background=self.colors['background'],
            foreground='#AAAAAA',
            font=('Arial Black', 10)
        )
        
        # Description style
        style.configure('Desc.TLabel', 
            background=self.colors['background'],
            foreground='#CCCCCC',
            font=('Arial', 9)
        )
        
        # File text label
        style.configure('FileText.TLabel', 
            background=self.colors['background'],
            foreground='#CCCCCC',
            font=('Arial', 10)
        )
        
        # Status bar styling
        style.configure('Status.TFrame',
            background=self.colors['status_bg'],
            relief='sunken'
        )
        
        style.configure('Status.TLabel', 
            background=self.colors['status_bg'],
            foreground='#AAAAAA',
            font=('Arial', 9),
            padding=3
        )

        # SCALE (SLIDER) STYLING
        style.configure('TScale',
            background=self.colors['background'],
            troughcolor=self.colors['input_bg'],
            bordercolor=self.colors['accent2'],
            lightcolor=self.colors['accent1'],
            darkcolor=self.colors['accent1']
        )
        
        # Custom slider styles for each color
        style.configure('Red.Horizontal.TScale',
            background=self.colors['background'],
            troughcolor='#401010',
            bordercolor=self.colors['accent1']
        )
        
        style.configure('Green.Horizontal.TScale',
            background=self.colors['background'],
            troughcolor='#104010',
            bordercolor=self.colors['accent3']
        )
        
        style.configure('Blue.Horizontal.TScale',
            background=self.colors['background'],
            troughcolor='#102040',
            bordercolor=self.colors['accent4']
        )
        
        style.configure('Alpha.Horizontal.TScale',
            background=self.colors['background'],
            troughcolor='#303030',
            bordercolor='#8F8F8F'
        )

        # ROOT WINDOW BACKGROUND
        self.root.configure(bg=self.colors['background'])

        return style, self.colors