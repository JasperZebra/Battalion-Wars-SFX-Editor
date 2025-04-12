import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import re
import os
from PIL import Image, ImageTk
import tkinter.colorchooser as colorchooser

from theme_manager import ThemeManager
from utils import create_military_background

class ParticleEffectEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Battalion Wars SFX Editor | Made By: Jasper_Zebra | Version 1.0")
        self.root.geometry("1100x850")
        
        # Set application icon
        self.set_app_icon()
        
        # Apply Battalion Wars 2 theme
        theme_manager = ThemeManager(root)
        self.style, self.colors = theme_manager.setup_theme()
        
        self.file_path = None
        self.file_content = None
        self.editable_values = {}  # Store editable values
        
        # Create background
        self.bg_image = create_military_background(950, 700)
        self.bg_label = tk.Label(root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.setup_ui()
    
    def set_app_icon(self):
        """Set the application icon"""
        try:
            # Look for the icon in the assets folder
            icon_path = os.path.join("assets", "sfx_editor_icon.png")
            
            # Check if the icon file exists
            if os.path.exists(icon_path):
                # Load the icon with PIL and set it as the window icon
                icon = Image.open(icon_path)
                photo_icon = ImageTk.PhotoImage(icon)
                self.root.iconphoto(True, photo_icon)
                self.update_status("ICON LOADED SUCCESSFULLY")
            else:
                self.update_status("WARNING: ICON FILE NOT FOUND")
                print(f"Icon file not found at {icon_path}")
        except Exception as e:
            self.update_status("WARNING: FAILED TO LOAD ICON")
            print(f"Failed to set application icon: {str(e)}")
    
    def update_status(self, message):
        """Update status bar message - used before status_var is initialized"""
        if hasattr(self, 'status_var'):
            self.status_var.set(message)
        else:
            # Store for later when status_var is created
            self._pending_status = message
            
    def setup_ui(self):
        """Setup the user interface components"""
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10", style="Military.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Title with military stencil style
        title_frame = ttk.Frame(main_frame, style="TitleBG.TFrame")
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(title_frame, text="BATTALION WARS SFX EDITOR", style='Title.TLabel')
        title_label.pack(fill=tk.X, pady=10)
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="MISSION FILE", padding="5", style="Military.TLabelframe")
        file_frame.pack(fill=tk.X, pady=5)
        
        self.file_label = ttk.Label(file_frame, text="No file selected", style="FileText.TLabel")
        self.file_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.browse_button = ttk.Button(file_frame, text="SELECT", command=self.browse_file, style="Military.TButton")
        self.browse_button.pack(side=tk.RIGHT, padx=5)
        
        # Create a PanedWindow to split the file viewer and color editor
        paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Left panel - File viewer
        self.setup_file_viewer(paned_window)
        
        # Right panel - Color editor
        self.setup_color_editor(paned_window)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame, style="Military.TFrame")
        button_frame.pack(fill=tk.X, pady=10)
        
        self.apply_button = ttk.Button(button_frame, text="APPLY CHANGES", command=self.apply_changes, style="Deploy.TButton")
        self.apply_button.pack(side=tk.RIGHT, padx=5)
        
        # Status bar - military-style
        status_frame = ttk.Frame(self.root, style="Status.TFrame")
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar(value="SYSTEM READY")
        if hasattr(self, '_pending_status'):
            self.status_var.set(self._pending_status)
            delattr(self, '_pending_status')
            
        self.status_bar = ttk.Label(status_frame, textvariable=self.status_var, style="Status.TLabel")
        self.status_bar.pack(fill=tk.X)
    
    def setup_file_viewer(self, parent):
        """Setup the file viewer panel"""
        file_viewer_frame = ttk.LabelFrame(parent, text="FILE CONTENTS", padding="5", style="Military.TLabelframe")
        
        # Create a Text widget for viewing the file
        self.file_viewer = scrolledtext.ScrolledText(
            file_viewer_frame, 
            wrap=tk.WORD,
            width=50,
            height=25,
            font=("Courier New", 9),
            bg=self.colors['input_bg'],
            fg=self.colors['foreground'],
            insertbackground=self.colors['foreground']
        )
        self.file_viewer.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure tags for highlighting
        self.file_viewer.tag_configure("red_value", foreground=self.colors['accent1'], background="#401010")
        self.file_viewer.tag_configure("green_value", foreground=self.colors['accent3'], background="#104010")
        self.file_viewer.tag_configure("blue_value", foreground=self.colors['accent4'], background="#102040")
        self.file_viewer.tag_configure("alpha_value", foreground="#FFFFFF", background="#404040")
        self.file_viewer.tag_configure("editable", background="#303030")
        
        # Make the text read-only
        self.file_viewer.config(state=tk.DISABLED)
        
        # Add the frame to the parent paned window
        parent.add(file_viewer_frame, weight=2)
        
    def setup_color_editor(self, parent):
        """Setup the color editor panel"""
        color_editor_frame = ttk.Frame(parent)
        parent.add(color_editor_frame, weight=1)
        
        # Color editor
        color_frame = ttk.LabelFrame(color_editor_frame, text="ORDNANCE COLOR", padding="5", style="Military.TLabelframe")
        color_frame.pack(fill=tk.BOTH, expand=True)
        
        # Current values display
        self.setup_current_values(color_frame)
        
        # Color picker
        self.setup_color_pickers(color_frame)
        
        # RGB sliders
        self.setup_rgb_sliders(color_frame)
        
        # Color preview
        self.setup_color_preview(color_frame)
        
        # Description
        self.setup_description(color_frame)
    
    def setup_current_values(self, parent):
        """Setup the current values display"""
        self.current_values_frame = ttk.LabelFrame(parent, text="CURRENT VALUES", padding="5", style="Military.TLabelframe")
        self.current_values_frame.pack(fill=tk.X, pady=5)
        
        # Create a grid for current values
        current_grid = ttk.Frame(self.current_values_frame, style="Military.TFrame")
        current_grid.pack(fill=tk.X, pady=5, padx=5)
        
        # Headers
        ttk.Label(current_grid, text="TYPE", style="ValueHeader.TLabel").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        ttk.Label(current_grid, text="START", style="ValueHeader.TLabel").grid(row=0, column=1, padx=5, pady=2)
        ttk.Label(current_grid, text="END", style="ValueHeader.TLabel").grid(row=0, column=2, padx=5, pady=2)
        ttk.Label(current_grid, text="TRANS", style="ValueHeader.TLabel").grid(row=0, column=3, padx=5, pady=2)
        
        # RED values
        red_label = ttk.Label(current_grid, text="RED", foreground=self.colors['accent1'], style="Military.TLabel")
        red_label.grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        
        self.red_start_val = ttk.Label(current_grid, text="-", style="Value.TLabel")
        self.red_start_val.grid(row=1, column=1, padx=5, pady=2)
        
        self.red_end_val = ttk.Label(current_grid, text="-", style="Value.TLabel")
        self.red_end_val.grid(row=1, column=2, padx=5, pady=2)
        
        self.red_trans_val = ttk.Label(current_grid, text="-", style="Value.TLabel")
        self.red_trans_val.grid(row=1, column=3, padx=5, pady=2)
        
        # GREEN values
        green_label = ttk.Label(current_grid, text="GREEN", foreground=self.colors['accent3'], style="Military.TLabel")
        green_label.grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
        
        self.green_start_val = ttk.Label(current_grid, text="-", style="Value.TLabel")
        self.green_start_val.grid(row=2, column=1, padx=5, pady=2)
        
        self.green_end_val = ttk.Label(current_grid, text="-", style="Value.TLabel")
        self.green_end_val.grid(row=2, column=2, padx=5, pady=2)
        
        self.green_trans_val = ttk.Label(current_grid, text="-", style="Value.TLabel")
        self.green_trans_val.grid(row=2, column=3, padx=5, pady=2)
        
        # BLUE values
        blue_label = ttk.Label(current_grid, text="BLUE", foreground=self.colors['accent4'], style="Military.TLabel")
        blue_label.grid(row=3, column=0, padx=5, pady=2, sticky=tk.W)
        
        self.blue_start_val = ttk.Label(current_grid, text="-", style="Value.TLabel")
        self.blue_start_val.grid(row=3, column=1, padx=5, pady=2)
        
        self.blue_end_val = ttk.Label(current_grid, text="-", style="Value.TLabel")
        self.blue_end_val.grid(row=3, column=2, padx=5, pady=2)
        
        self.blue_trans_val = ttk.Label(current_grid, text="-", style="Value.TLabel")
        self.blue_trans_val.grid(row=3, column=3, padx=5, pady=2)
        
        # ALPHA values
        alpha_label = ttk.Label(current_grid, text="OPACITY", style="Military.TLabel")
        alpha_label.grid(row=4, column=0, padx=5, pady=2, sticky=tk.W)
        
        self.alpha_start_val = ttk.Label(current_grid, text="-", style="Value.TLabel")
        self.alpha_start_val.grid(row=4, column=1, padx=5, pady=2)
        
        self.alpha_end_val = ttk.Label(current_grid, text="-", style="Value.TLabel")
        self.alpha_end_val.grid(row=4, column=2, padx=5, pady=2)
        
        self.alpha_trans_val = ttk.Label(current_grid, text="-", style="Value.TLabel")
        self.alpha_trans_val.grid(row=4, column=3, padx=5, pady=2)
    
    def setup_color_pickers(self, parent):
        """Setup color picker buttons"""
        preset_frame = ttk.Frame(parent, style="Military.TFrame")
        preset_frame.pack(fill=tk.X, pady=5)

        ttk.Label(preset_frame, text="COLOR SELECTION:", style="Military.TLabel").pack(side=tk.LEFT, padx=5)

        self.color_picker_button = ttk.Button(
            preset_frame, 
            text="CUSTOM COLOR", 
            command=self.open_color_picker, 
            style="Military.TButton"
        )
        self.color_picker_button.pack(side=tk.LEFT, padx=5)
    
    def setup_rgb_sliders(self, parent):
        """Setup RGB and Alpha sliders"""
        rgb_frame = ttk.Frame(parent, style="Military.TFrame")
        rgb_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Red slider
        red_label_frame = ttk.Frame(rgb_frame, style="RedLabel.TFrame")
        red_label_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(red_label_frame, text="RED:", style="Military.TLabel").pack(padx=3, pady=2)
        
        self.red_var = tk.DoubleVar(value=0.7)
        self.red_slider = ttk.Scale(rgb_frame, from_=0.0, to=1.0, variable=self.red_var, orient=tk.HORIZONTAL, style="Red.Horizontal.TScale")
        self.red_slider.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        self.red_value = ttk.Label(rgb_frame, text="0.700", style='Value.TLabel')
        self.red_value.grid(row=0, column=2, padx=5, pady=5)
        self.red_slider.bind("<Motion>", lambda e: self.update_value_label(self.red_var, self.red_value))
        
        # Green slider
        green_label_frame = ttk.Frame(rgb_frame, style="GreenLabel.TFrame")
        green_label_frame.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(green_label_frame, text="GREEN:", style="Military.TLabel").pack(padx=3, pady=2)
        
        self.green_var = tk.DoubleVar(value=0.3)
        self.green_slider = ttk.Scale(rgb_frame, from_=0.0, to=1.0, variable=self.green_var, orient=tk.HORIZONTAL, style="Green.Horizontal.TScale")
        self.green_slider.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        self.green_value = ttk.Label(rgb_frame, text="0.300", style='Value.TLabel')
        self.green_value.grid(row=1, column=2, padx=5, pady=5)
        self.green_slider.bind("<Motion>", lambda e: self.update_value_label(self.green_var, self.green_value))
        
        # Blue slider
        blue_label_frame = ttk.Frame(rgb_frame, style="BlueLabel.TFrame")
        blue_label_frame.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(blue_label_frame, text="BLUE:", style="Military.TLabel").pack(padx=3, pady=2)
        
        self.blue_var = tk.DoubleVar(value=0.5)
        self.blue_slider = ttk.Scale(rgb_frame, from_=0.0, to=1.0, variable=self.blue_var, orient=tk.HORIZONTAL, style="Blue.Horizontal.TScale")
        self.blue_slider.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
        
        self.blue_value = ttk.Label(rgb_frame, text="0.500", style='Value.TLabel')
        self.blue_value.grid(row=2, column=2, padx=5, pady=5)
        self.blue_slider.bind("<Motion>", lambda e: self.update_value_label(self.blue_var, self.blue_value))
        
        # Alpha slider
        alpha_label_frame = ttk.Frame(rgb_frame, style="AlphaLabel.TFrame")
        alpha_label_frame.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(alpha_label_frame, text="OPACITY:", style="Military.TLabel").pack(padx=3, pady=2)
        
        self.alpha_var = tk.DoubleVar(value=1.0)
        self.alpha_slider = ttk.Scale(rgb_frame, from_=0.0, to=1.0, variable=self.alpha_var, orient=tk.HORIZONTAL, style="Alpha.Horizontal.TScale")
        self.alpha_slider.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)
        
        self.alpha_value = ttk.Label(rgb_frame, text="1.000", style='Value.TLabel')
        self.alpha_value.grid(row=3, column=2, padx=5, pady=5)
        self.alpha_slider.bind("<Motion>", lambda e: self.update_value_label(self.alpha_var, self.alpha_value))
        
        rgb_frame.columnconfigure(1, weight=1)
    
    def setup_color_preview(self, parent):
        """Setup color preview area"""
        preview_frame = ttk.Frame(parent, style="Preview.TFrame")
        preview_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(preview_frame, text="VISUAL REPORT:", style="Military.TLabel").pack(side=tk.LEFT, padx=5)
        
        # Canvas for color preview with military-style border
        preview_container = ttk.Frame(preview_frame, style="PreviewBorder.TFrame")
        preview_container.pack(side=tk.LEFT, padx=10)
        
        self.color_preview = tk.Canvas(preview_container, width=120, height=40, bg="#B34D80", highlightthickness=0)
        self.color_preview.pack(padx=2, pady=2)
        
        # Hex color display
        self.hex_color = ttk.Label(preview_frame, text="#B34D80", style='Value.TLabel')
        self.hex_color.pack(side=tk.LEFT, padx=10)
        
        self.update_preview()
        
        # Bind slider movement to update preview
        self.red_slider.bind("<B1-Motion>", lambda e: self.update_preview())
        self.green_slider.bind("<B1-Motion>", lambda e: self.update_preview())
        self.blue_slider.bind("<B1-Motion>", lambda e: self.update_preview())
    
    def setup_description(self, parent):
        """Setup description text"""
        desc_frame = ttk.Frame(parent, style="Military.TFrame")
        desc_frame.pack(fill=tk.X, pady=5)
        
        desc_text = ttk.Label(
            desc_frame, 
            text="Modify the RGB and Opacity values using the sliders above.\nAny highlighted values in the file will be updated when you apply changes.",
            style="Desc.TLabel",
            justify=tk.LEFT
        )
        desc_text.pack(padx=5, pady=5, anchor=tk.W)
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Particle Effect File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.file_path = file_path
            self.file_label.config(text=os.path.basename(file_path))
            
            try:
                with open(file_path, 'r') as file:
                    self.file_content = file.read()
                    
                self.display_file_content()
                self.extract_editable_values()
                self.status_var.set(f"LOADED: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def display_file_content(self):
        """Display file content in the viewer with highlighted editable parts"""
        self.file_viewer.config(state=tk.NORMAL)
        self.file_viewer.delete(1.0, tk.END)
        self.file_viewer.insert(tk.END, self.file_content)
        
        # Highlight the editable values (color values)
        self.highlight_color_values()
        
        self.file_viewer.config(state=tk.DISABLED)
    
    def highlight_color_values(self):
        """Highlight all the color values in the file viewer"""
        # Find and highlight Start_Red values
        pattern_start_red = r'(Start_Red NUMBER_VERSION_2\n\*\*\*\*1: )(\d+\.\d+)'
        for match in re.finditer(pattern_start_red, self.file_content):
            start_idx = f"1.0+{match.start(2)}c"
            end_idx = f"1.0+{match.end(2)}c"
            self.file_viewer.tag_add("red_value", start_idx, end_idx)
            self.file_viewer.tag_add("editable", start_idx, end_idx)
        
        # Find and highlight Start_Green values
        pattern_start_green = r'(Start_Green NUMBER_VERSION_2\n\*\*\*\*1: )(\d+\.\d+)'
        for match in re.finditer(pattern_start_green, self.file_content):
            start_idx = f"1.0+{match.start(2)}c"
            end_idx = f"1.0+{match.end(2)}c"
            self.file_viewer.tag_add("green_value", start_idx, end_idx)
            self.file_viewer.tag_add("editable", start_idx, end_idx)
        
        # Find and highlight Start_Blue values
        pattern_start_blue = r'(Start_Blue NUMBER_VERSION_2\n\*\*\*\*1: )(\d+\.\d+)'
        for match in re.finditer(pattern_start_blue, self.file_content):
            start_idx = f"1.0+{match.start(2)}c"
            end_idx = f"1.0+{match.end(2)}c"
            self.file_viewer.tag_add("blue_value", start_idx, end_idx)
            self.file_viewer.tag_add("editable", start_idx, end_idx)
        
        # Find and highlight Start_Alpha values
        pattern_start_alpha = r'(Start_Alpha NUMBER_VERSION_2\n\*\*\*\*1: )(\d+\.\d+)'
        for match in re.finditer(pattern_start_alpha, self.file_content):
            start_idx = f"1.0+{match.start(2)}c"
            end_idx = f"1.0+{match.end(2)}c"
            self.file_viewer.tag_add("alpha_value", start_idx, end_idx)
            self.file_viewer.tag_add("editable", start_idx, end_idx)
            
        # Find and highlight End values and Transition values too
        for color, tag in [
            ("End_Red", "red_value"), 
            ("End_Green", "green_value"), 
            ("End_Blue", "blue_value"),
            ("End_Alpha", "alpha_value"),
            ("Transition_Red", "red_value"),
            ("Transition_Green", "green_value"),
            ("Transition_Blue", "blue_value"),
            ("Transition_Alpha", "alpha_value")
        ]:
            pattern = fr'({color} NUMBER_VERSION_2\n\*\*\*\*1: )(\d+\.\d+)'
            for match in re.finditer(pattern, self.file_content):
                start_idx = f"1.0+{match.start(2)}c"
                end_idx = f"1.0+{match.end(2)}c"
                self.file_viewer.tag_add(tag, start_idx, end_idx)
                self.file_viewer.tag_add("editable", start_idx, end_idx)
    
    def open_color_picker(self):
        # Get current RGB values from sliders
        r = int(self.red_var.get() * 255)
        g = int(self.green_var.get() * 255)
        b = int(self.blue_var.get() * 255)
        current_color = f"#{r:02x}{g:02x}{b:02x}"
        
        # Open color chooser dialog
        color_result = colorchooser.askcolor(
            color=current_color,
            title="CUSTOM COLOR SELECTION"
        )
        
        # If a color was selected (not cancelled)
        if color_result[1]:
            # color_result is a tuple: ((r, g, b), hex_string)
            r, g, b = color_result[0]
            
            # Update slider values (0-1 range)
            self.red_var.set(r / 255)
            self.green_var.set(g / 255)
            self.blue_var.set(b / 255)
            
            # Update value labels
            self.update_value_label(self.red_var, self.red_value)
            self.update_value_label(self.green_var, self.green_value)
            self.update_value_label(self.blue_var, self.blue_value)
            
            # Update color preview
            self.update_preview()

    def extract_editable_values(self):
        """Extract editable values from the file content"""
        self.editable_values = {}
        
        # Get current values for Start_Red, End_Red, etc.
        for color_type in ["Red", "Green", "Blue", "Alpha"]:
            # Get Start values
            pattern_start = fr'Start_{color_type} NUMBER_VERSION_2\n\*\*\*\*1: (\d+\.\d+)'
            match = re.search(pattern_start, self.file_content)
            if match:
                self.editable_values[f"Start_{color_type}"] = float(match.group(1))
            
            # Get End values
            pattern_end = fr'End_{color_type} NUMBER_VERSION_2\n\*\*\*\*1: (\d+\.\d+)'
            match = re.search(pattern_end, self.file_content)
            if match:
                self.editable_values[f"End_{color_type}"] = float(match.group(1))
            
            # Get Transition values
            pattern_trans = fr'Transition_{color_type} NUMBER_VERSION_2\n\*\*\*\*1: (\d+\.\d+)'
            match = re.search(pattern_trans, self.file_content)
            if match:
                self.editable_values[f"Transition_{color_type}"] = float(match.group(1))
        
        # Update the current values display
        self.update_current_values_display()
        
        # Set the sliders to match the first Start values found
        if "Start_Red" in self.editable_values:
            self.red_var.set(self.editable_values["Start_Red"])
        if "Start_Green" in self.editable_values:
            self.green_var.set(self.editable_values["Start_Green"])
        if "Start_Blue" in self.editable_values:
            self.blue_var.set(self.editable_values["Start_Blue"])
        if "Start_Alpha" in self.editable_values:
            self.alpha_var.set(self.editable_values["Start_Alpha"])
        
        # Update slider value labels
        self.update_value_label(self.red_var, self.red_value)
        self.update_value_label(self.green_var, self.green_value)
        self.update_value_label(self.blue_var, self.blue_value)
        self.update_value_label(self.alpha_var, self.alpha_value)
        
        # Update the color preview
        self.update_preview()
    
    def update_current_values_display(self):
        """Update the display of current values"""
        # Update RED values
        if "Start_Red" in self.editable_values:
            self.red_start_val.config(text=f"{self.editable_values['Start_Red']:.3f}")
        if "End_Red" in self.editable_values:
            self.red_end_val.config(text=f"{self.editable_values['End_Red']:.3f}")
        if "Transition_Red" in self.editable_values:
            self.red_trans_val.config(text=f"{self.editable_values['Transition_Red']:.3f}")
        
        # Update GREEN values
        if "Start_Green" in self.editable_values:
            self.green_start_val.config(text=f"{self.editable_values['Start_Green']:.3f}")
        if "End_Green" in self.editable_values:
            self.green_end_val.config(text=f"{self.editable_values['End_Green']:.3f}")
        if "Transition_Green" in self.editable_values:
            self.green_trans_val.config(text=f"{self.editable_values['Transition_Green']:.3f}")
        
        # Update BLUE values
        if "Start_Blue" in self.editable_values:
            self.blue_start_val.config(text=f"{self.editable_values['Start_Blue']:.3f}")
        if "End_Blue" in self.editable_values:
            self.blue_end_val.config(text=f"{self.editable_values['End_Blue']:.3f}")
        if "Transition_Blue" in self.editable_values:
            self.blue_trans_val.config(text=f"{self.editable_values['Transition_Blue']:.3f}")
        
        # Update ALPHA values
        if "Start_Alpha" in self.editable_values:
            self.alpha_start_val.config(text=f"{self.editable_values['Start_Alpha']:.3f}")
        if "End_Alpha" in self.editable_values:
            self.alpha_end_val.config(text=f"{self.editable_values['End_Alpha']:.3f}")
        if "Transition_Alpha" in self.editable_values:
            self.alpha_trans_val.config(text=f"{self.editable_values['Transition_Alpha']:.3f}")
    
    def update_value_label(self, var, label):
        label.config(text=f"{var.get():.3f}")
        self.update_preview()
    
    def update_preview(self):
        r = int(self.red_var.get() * 255)
        g = int(self.green_var.get() * 255)
        b = int(self.blue_var.get() * 255)
        color = f"#{r:02x}{g:02x}{b:02x}"
        self.color_preview.config(bg=color)
        self.hex_color.config(text=color.upper())
    
    def apply_pink(self):
        self.red_var.set(0.7)
        self.green_var.set(0.3)
        self.blue_var.set(0.5)
        self.update_preview()
        self.update_value_label(self.red_var, self.red_value)
        self.update_value_label(self.green_var, self.green_value)
        self.update_value_label(self.blue_var, self.blue_value)
    
    def apply_blue(self):
        self.red_var.set(0.2)
        self.green_var.set(0.3)
        self.blue_var.set(0.8)
        self.update_preview()
        self.update_value_label(self.red_var, self.red_value)
        self.update_value_label(self.green_var, self.green_value)
        self.update_value_label(self.blue_var, self.blue_value)
    
    def apply_green(self):
        self.red_var.set(0.3)
        self.green_var.set(0.7)
        self.blue_var.set(0.3)
        self.update_preview()
        self.update_value_label(self.red_var, self.red_value)
        self.update_value_label(self.green_var, self.green_value)
        self.update_value_label(self.blue_var, self.blue_value)
    
    def apply_red(self):
        self.red_var.set(0.8)
        self.green_var.set(0.2)
        self.blue_var.set(0.2)
        self.update_preview()
        self.update_value_label(self.red_var, self.red_value)
        self.update_value_label(self.green_var, self.green_value)
        self.update_value_label(self.blue_var, self.blue_value)
    
    def apply_changes(self):
        if not self.file_path or not self.file_content:
            messagebox.showerror("Error", "No file loaded")
            return
        
        # Get RGB values
        red = f"{self.red_var.get():.6f}"
        green = f"{self.green_var.get():.6f}"
        blue = f"{self.blue_var.get():.6f}"
        alpha = f"{self.alpha_var.get():.6f}"
        
        # Create modified content with regex replacements
        modified_content = self.file_content
        
        # Replace Red values
        modified_content = re.sub(
            r'(Start_Red NUMBER_VERSION_2\n\*\*\*\*1: )\d+\.\d+',
            r'\g<1>' + red,
            modified_content
        )
        
        # Replace Green values
        modified_content = re.sub(
            r'(Start_Green NUMBER_VERSION_2\n\*\*\*\*1: )\d+\.\d+',
            r'\g<1>' + green,
            modified_content
        )
        
        # Replace Blue values
        modified_content = re.sub(
            r'(Start_Blue NUMBER_VERSION_2\n\*\*\*\*1: )\d+\.\d+',
            r'\g<1>' + blue,
            modified_content
        )
        
        # Replace Alpha values (if the user wants to change opacity)
        modified_content = re.sub(
            r'(Start_Alpha NUMBER_VERSION_2\n\*\*\*\*1: )\d+\.\d+',
            r'\g<1>' + alpha,
            modified_content
        )
        
        # Also update End values
        modified_content = re.sub(
            r'(End_Red NUMBER_VERSION_2\n\*\*\*\*1: )\d+\.\d+',
            r'\g<1>' + red,
            modified_content
        )
        
        modified_content = re.sub(
            r'(End_Green NUMBER_VERSION_2\n\*\*\*\*1: )\d+\.\d+',
            r'\g<1>' + green,
            modified_content
        )
        
        modified_content = re.sub(
            r'(End_Blue NUMBER_VERSION_2\n\*\*\*\*1: )\d+\.\d+',
            r'\g<1>' + blue,
            modified_content
        )
        
        modified_content = re.sub(
            r'(End_Alpha NUMBER_VERSION_2\n\*\*\*\*1: )\d+\.\d+',
            r'\g<1>' + alpha,
            modified_content
        )
        
        # Also update Transition values
        modified_content = re.sub(
            r'(Transition_Red NUMBER_VERSION_2\n\*\*\*\*1: )\d+\.\d+',
            r'\g<1>' + red,
            modified_content
        )
        
        modified_content = re.sub(
            r'(Transition_Green NUMBER_VERSION_2\n\*\*\*\*1: )\d+\.\d+',
            r'\g<1>' + green,
            modified_content
        )
        
        modified_content = re.sub(
            r'(Transition_Blue NUMBER_VERSION_2\n\*\*\*\*1: )\d+\.\d+',
            r'\g<1>' + blue,
            modified_content
        )
        
        modified_content = re.sub(
            r'(Transition_Alpha NUMBER_VERSION_2\n\*\*\*\*1: )\d+\.\d+',
            r'\g<1>' + alpha,
            modified_content
        )
        
        # Save the modified content
        try:
            with open(self.file_path, 'w') as file:
                file.write(modified_content)
            
            # Update the displayed file content
            self.file_content = modified_content
            self.display_file_content()
            self.extract_editable_values()
            
            messagebox.showinfo("SUCCESS", f"Changes deployed to {os.path.basename(self.file_path)}")
            self.status_var.set(f"MISSION COMPLETE: {os.path.basename(self.file_path)} UPDATED")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply changes: {str(e)}")