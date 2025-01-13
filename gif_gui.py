"""
GIFshine GUI Application
A happy little tool for splitting animated GIFs into grids with advanced cropping and optimization options.

Main Features:
- Interactive preview window with resize/move capabilities
- Grid-based GIF splitting
- Aspect ratio maintenance
- Size optimization
- Circular cropping option
- Output resizing
"""

import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os
from gif_processor import GifProcessor

class Main(tk.Tk):
    """Main application window for GIFshine."""
    def __init__(self):
        super().__init__()
        self.update_from_ui = False
        self.title("GIFshine")
        self.geometry("400x600")
        self.resizable(False, False)  # Fix window size
        
        # Create main container
        main_container = ttk.Frame(self)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Input file selection
        input_frame = ttk.LabelFrame(main_container, text="Input GIF", padding=5)
        input_frame.pack(fill='x', pady=(0, 10))
        
        self.file_label = ttk.Label(input_frame, text="No file selected")
        self.file_label.pack(side='left', fill='x', expand=True, padx=5)
        
        self.select_button = ttk.Button(
            input_frame,
            text="Select File",
            command=self.select_file
        )
        self.select_button.pack(side='right', padx=5)
        
        # Output directory selection
        output_frame = ttk.LabelFrame(main_container, text="Output Directory", padding=5)
        output_frame.pack(fill='x', pady=(0, 10))
        
        self.output_var = tk.StringVar()
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_var)
        self.output_entry.pack(side='left', fill='x', expand=True, padx=5)
        
        self.output_button = ttk.Button(
            output_frame,
            text="Browse",
            command=self.select_output_dir
        )
        self.output_button.pack(side='right', padx=5)
        
        # Preview button
        self.preview_button = ttk.Button(main_container, text="Toggle Preview", command=self.toggle_preview, state='disabled')
        self.preview_button.pack(fill='x', pady=(0, 10))
        
        # Dimensions frame (combines position and grid)
        pos_frame = ttk.LabelFrame(main_container, text="Dimensions", padding="5")
        pos_frame.pack(fill='x', pady=(0, 10))
        
        ## Position inputs
        ttk.Label(pos_frame, text="Selection:").grid(row=0, column=0, columnspan=4, sticky='w', pady=(0))
        
        ttk.Label(pos_frame, text="X:").grid(row=1, column=0, padx=5)
        self.x_var = tk.IntVar(value=0)
        self.x_spin = ttk.Spinbox(pos_frame, from_=0, to=10000, width=5, textvariable=self.x_var)
        self.x_spin.grid(row=1, column=1, padx=5)
        self.x_var.trace_add('write', lambda *args: self.update_selection_from_inputs('x'))
        
        ttk.Label(pos_frame, text="Y:").grid(row=2, column=0, padx=5)
        self.y_var = tk.IntVar(value=0)
        self.y_spin = ttk.Spinbox(pos_frame, from_=0, to=10000, width=5, textvariable=self.y_var)
        self.y_spin.grid(row=2, column=1, padx=5)
        self.y_var.trace_add('write', lambda *args: self.update_selection_from_inputs('y'))
        
        ttk.Label(pos_frame, text="Width:").grid(row=1, column=2, padx=5, pady=5)
        self.width_var = tk.IntVar(value=100)
        self.width_spin = ttk.Spinbox(pos_frame, from_=1, to=10000, width=5, textvariable=self.width_var)
        self.width_spin.grid(row=1, column=3, padx=5)
        self.width_var.trace_add('write', lambda *args: self.update_selection_from_inputs('width'))
        
        ttk.Label(pos_frame, text="Height:").grid(row=2, column=2, padx=5)
        self.height_var = tk.IntVar(value=100)
        self.height_spin = ttk.Spinbox(pos_frame, from_=1, to=10000, width=5, textvariable=self.height_var)
        self.height_spin.grid(row=2, column=3, padx=5)
        self.height_var.trace_add('write', lambda *args: self.update_selection_from_inputs('height'))
        
        ## Maintain ratio checkbox
        self.maintain_ratio_var = tk.BooleanVar(value=True)
        self.aspect_ratio = 1.0
        self.maintain_ratio_var.trace_add('write', lambda * args: self.update_selection_from_inputs('aspect_ratio'))
        ttk.Checkbutton(pos_frame, text="Maintain Ratio", variable=self.maintain_ratio_var).grid(row=3, column=0, columnspan=3, pady=5)
        
        self.circular_var = tk.BooleanVar(value=False)
        self.circular_var.trace_add('write', lambda * args: self.update_selection_from_inputs('circular'))
        ttk.Checkbutton(pos_frame, text="Circular Crop", variable=self.circular_var).grid(row=3, column=4, columnspan=3, pady=5)
        

        ## Grid settings
        ttk.Label(pos_frame, text="Grid:").grid(row=0, column=4, columnspan=4, sticky='w', pady=(5, 5))
        
        ttk.Label(pos_frame, text="Rows:").grid(row=1, column=4, padx=(20, 5))
        self.rows_var = tk.IntVar(value=2)
        self.rows_spin = ttk.Spinbox(pos_frame, from_=1, to=10, width=5, textvariable=self.rows_var)
        self.rows_spin.grid(row=1, column=5, padx=5)
        self.rows_var.trace_add('write', lambda *args: self.update_grid())
        
        ttk.Label(pos_frame, text="Cols:").grid(row=2, column=4, padx=(20, 5))
        self.cols_var = tk.IntVar(value=2)
        self.cols_spin = ttk.Spinbox(pos_frame, from_=1, to=10, width=5, textvariable=self.cols_var)
        self.cols_spin.grid(row=2, column=5, padx=(5))
        self.cols_var.trace_add('write', lambda *args: self.update_grid())
        
        # Options frame
        options_frame = ttk.LabelFrame(main_container, text="Options", padding="5")
        options_frame.pack(fill='x', pady=(0, 10))

        ## Optimize Options
        
    
        ttk.Label(options_frame, text="Optimize:").grid(row=0, column=0, padx=5, pady=5)
        self.optimize_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, variable=self.optimize_var).grid(row=0, column=1)
        self.optimize_var.trace_add('write', lambda *args: self.update_optimize())

        ttk.Label(options_frame, text="Max Size (KB):").grid(row=1, column=0, padx=5)
        self.max_size_var = tk.IntVar(value=500)
        self.max_size_spin = ttk.Spinbox(options_frame, from_=1, to=10000, width=5, textvariable=self.max_size_var)
        self.max_size_spin.grid(row=1, column=1, padx=5)
        
        self.update_optimize()
        
        ## Resize Options

        ttk.Label(options_frame, text="Resize:").grid(row=0, column=3, padx=5, pady=5)
        self.resize_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, variable=self.resize_var).grid(row=0, column=4)
        self.resize_var.trace_add('write', lambda *args: self.update_resize())

        ttk.Label(options_frame, text="Width:").grid(row=0, column=5, padx=5, pady=5)
        self.output_width_var = tk.IntVar(value=100)
        self.output_width_spin = ttk.Spinbox(options_frame, from_=1, to=10000, width=5, textvariable=self.output_width_var)
        self.output_width_spin.grid(row=0, column=6, padx=5)

        ttk.Label(options_frame, text="Height:").grid(row=1, column=5, padx=5)
        self.output_height_var = tk.IntVar(value=100)
        self.output_height_spin = ttk.Spinbox(options_frame, from_=1, to=10000, width=5, textvariable=self.output_height_var)
        self.output_height_spin.grid(row=1, column=6, padx=5)

        self.update_resize()

        # Process button and progress
        self.process_button = ttk.Button(main_container, text="Process GIF", command=self.process_gif, state='disabled')
        self.process_button.pack(fill='x', pady=(0, 10))
        
        self.progress = ttk.Progressbar(main_container, mode='indeterminate')
        self.progress.pack(fill='x', pady=(0, 10))
        
        self.status_label = ttk.Label(main_container, text="")
        self.status_label.pack(fill='x')
        
        # Copyright footer
        footer_style = ttk.Style()
        footer_style.configure('Footer.TLabel', foreground='gray')
        footer_label = ttk.Label(main_container, text="GIFshine by SunshyneCoding 2025", style='Footer.TLabel')
        footer_label.pack(fill='x', pady=(10, 0))
        
        # Initialize variables
        self.preview_window = None
        self.selected_file = None
        
    def select_file(self):
        """Open file dialog for selecting a GIF file."""
        filename = filedialog.askopenfilename(
            filetypes=[("GIF files", "*.gif")]
        )
        if filename:
            self.selected_file = filename
            # Truncate filename if too long
            basename = os.path.basename(filename)
            if len(basename) > 27:
                display_name = basename[:24] + "..."
            else:
                display_name = basename
            self.file_label.config(text=display_name)
            
            # Set default output directory
            parent_dir = os.path.dirname(filename)
            default_output = os.path.join(parent_dir, "gifsplit")
            self.output_var.set(default_output)
            
            # Enable buttons
            self.preview_button.config(state='normal')
            self.process_button.config(state='normal')
            
            # Automatically show preview
            self.toggle_preview()
            
    def select_output_dir(self):
        """Open directory dialog for selecting an output directory."""
        current_dir = self.output_var.get() or os.path.dirname(self.selected_file) if hasattr(self, 'selected_file') else ""
        dirname = filedialog.askdirectory(initialdir=current_dir)
        if dirname:
            self.output_var.set(dirname)
            
    def toggle_preview(self):
        """Toggle the preview window."""
        if not self.selected_file:
            return
            
        if not hasattr(self, 'preview_window') or self.preview_window is None:
            self.preview_window = PreviewWindow(self)
            self.preview_window.set_gif(self.selected_file)
        else:
            self.preview_window.on_closing()
            
    def update_spinboxes(self, coords):
        """Update spinbox values based on selection coordinates."""
        if coords:
            self.update_from_ui = True
            self.x_var.set(int(coords[0]))
            self.y_var.set(int(coords[1]))
            self.width_var.set(int(coords[2] - coords[0]))
            self.height_var.set(int(coords[3] - coords[1]))
            self.update_from_ui = False
            

    def update_resize(self):
        """Enable/disable resize input fields based on checkbox state."""
        if self.resize_var.get():
            self.output_height_spin.config(state='normal')
            self.output_width_spin.config(state='normal')
        else:
            self.output_height_spin.config(state='disabled')
            self.output_width_spin.config(state='disabled')

    def update_optimize(self):
        """Enable/disable optimization input fields based on checkbox state."""
        if self.optimize_var.get():
            self.max_size_spin.config(state='normal')
        else:
            self.max_size_spin.config(state='disabled')

    def update_grid(self):
        """Update the grid overlay in the preview window."""
        if self.preview_window:
            self.preview_window.draw_grid()
            
    def update_selection(self):
        """Update the selection rectangle in the preview window."""
        if self.preview_window:
            self.preview_window.draw_selection()
            
    def update_selection_from_inputs(self, source, *args):
        """Update the selection rectangle based on input field changes.
        
        Args:
            source: The input field that triggered the update
            *args: Additional arguments from tkinter trace
        """
        if self.update_from_ui:
            return
        try:
            width = self.width_var.get()
            height = self.height_var.get()
            if source == 'aspect' and self.maintain_ratio_var.get():
                self.aspect_ratio = width / height
                return
                
            x = self.x_var.get()
            y = self.y_var.get()
            
            # Maintain aspect ratio if checked
            if self.maintain_ratio_var.get():
                if source == 'width':
                    height = width * self.aspect_ratio
                    self.height_var.set(height)
                if source == 'height':
                    width = height / self.aspect_ratio
                    self.width_var.set(width)

            if self.preview_window and self.preview_window.crop_rect:   
                # Update the selection
                self.preview_window.canvas.coords(
                    self.preview_window.crop_rect,
                    x, y, x + width, y + height
                )
                self.preview_window.draw_selection()
        except tk.TclError:
            # This happens when the input is empty or invalid
            pass
            
    def process_gif(self):
        """Process the GIF with current settings and save the results."""
        if not self.selected_file:
            return
            
        self.progress.start()
        self.status_label.config(text="Processing...")
        self.process_button.config(state='disabled')
        
        try:
            processor = GifProcessor(self.selected_file)
            
            # Crop
            processor.crop_to_rect(
                self.x_var.get(),
                self.y_var.get(),
                self.width_var.get(),
                self.height_var.get()
            )

            # Resize
            if self.resize_var.get():
                processor.resize(self.output_width_var.get(), self.output_height_var.get())
                
            # Circelify
            if self.circular_var.get():
                processor.crop_circle()
            

            # Split and process
            chunks = processor.split_gif(self.rows_var.get(), self.cols_var.get())
            chunks = processor.optimize_chunks(chunks, self.max_size_var.get())
            
            # Save
            output_dir = self.output_var.get()
            processor.save_chunks(chunks, output_dir)
            
            self.status_label.config(text=f"Done! Files saved to: {output_dir}")
            
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            
        finally:
            self.progress.stop()
            self.process_button.config(state='normal')


class PreviewWindow(tk.Toplevel):
    """Preview window for GIF manipulation with interactive selection."""
    
    def __init__(self, parent=None):
        """Initialize the preview window.
        
        Args:
            parent: Parent window reference
        """
        super().__init__(parent)
        self.title("Preview")
        self.base_size = 300
        self.max_size = 800
        
        # Make window non-resizable
        self.resizable(False, False)
        
        # Keep window on top but non-modal
        self.transient(parent)
        
        # Bind close event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Preview canvas
        self.canvas = tk.Canvas(self, width=self.base_size, height=self.base_size)
        self.canvas.pack(expand=True, fill='both')
        
        # Bind mouse events
        self.canvas.bind('<Motion>', self.on_motion)
        self.canvas.bind('<ButtonPress-1>', self.on_left_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        
        self.movie = None
        self.photo = None
        self.frames = []
        self.current_frame = 0
        self.crop_rect = None
        self.dragging = False
        self.moving = False
        self.start_pos = None

    def check_resize_edge(self, event, coords):
        """Check which edges or corners are being clicked for resizing.
        
        Args:
            event: Mouse event containing coordinates
            coords: Current selection rectangle coordinates
            
        Returns:
            tuple: (is_left, is_right, is_top, is_bottom) edge detection flags
        """
        edge_threshold = 10
        
        # Check edges
        near_left = abs(event.x - coords[0]) < edge_threshold
        near_right = abs(event.x - coords[2]) < edge_threshold
        near_top = abs(event.y - coords[1]) < edge_threshold
        near_bottom = abs(event.y - coords[3]) < edge_threshold
        
        # Also check if we're within the vertical/horizontal bounds
        in_vertical_bound = coords[1] - edge_threshold <= event.y <= coords[3] + edge_threshold
        in_horizontal_bound = coords[0] - edge_threshold <= event.x <= coords[2] + edge_threshold
        
        # Combine the checks
        is_left = near_left and in_vertical_bound
        is_right = near_right and in_vertical_bound
        is_top = near_top and in_horizontal_bound
        is_bottom = near_bottom and in_horizontal_bound
        
        return is_left, is_right, is_top, is_bottom
        
    def on_motion(self, event):
        """Handle mouse motion for cursor changes and dragging operations."""
        if not self.crop_rect:
            return
            
        coords = self.canvas.coords(self.crop_rect)
        if coords == []:
            return

        is_left, is_right, is_top, is_bottom = self.check_resize_edge(event, coords)
        
        # Set appropriate cursor
        if (is_left and is_top) or (is_right and is_bottom):
            self.canvas.config(cursor='size_nw_se')
        elif (is_right and is_top) or (is_left and is_bottom):
            self.canvas.config(cursor='size_ne_sw')
        elif is_left or is_right:
            self.canvas.config(cursor='size_we')
        elif is_top or is_bottom:
            self.canvas.config(cursor='size_ns')
        elif coords[0] <= event.x <= coords[2] and coords[1] <= event.y <= coords[3]:
            self.canvas.config(cursor='fleur')  # Move cursor
        else:
            self.canvas.config(cursor='')  # Default cursor
            
    def on_left_press(self, event):
        """Handle left mouse button press for selection creation/modification."""
        if not self.crop_rect:
            # Create new selection
            self.dragging = True
            self.start_pos = (event.x, event.y)
            self.crop_rect = self.canvas.create_rectangle(
                event.x, event.y, event.x, event.y,
                outline='red', width=2
            )
            return
            
        coords = self.canvas.coords(self.crop_rect)
        is_left, is_right, is_top, is_bottom = self.check_resize_edge(event, coords)
        
        if is_left or is_right or is_top or is_bottom:
            self.dragging = True
            self.resize_edges = {
                'left': is_left,
                'right': is_right,
                'top': is_top,
                'bottom': is_bottom
            }
            self.start_pos = (event.x, event.y)
            self.original_coords = coords
        elif coords[0] <= event.x <= coords[2] and coords[1] <= event.y <= coords[3]:
            # Click inside selection - move it
            self.moving = True
            self.dragging = False  # Make sure we're not in dragging mode
            self.start_pos = (event.x, event.y)
            self.original_coords = coords

    def on_drag(self, event):
        """Handle dragging operations for selection resizing/moving."""
        if self.dragging and self.start_pos:
            if hasattr(self, 'resize_edges'):  # Resizing existing selection
                coords = list(self.original_coords)
                min_size = 10  # Minimum size to prevent selection from disappearing
                
                # Calculate deltas
                dx = event.x - self.start_pos[0]
                dy = event.y - self.start_pos[1]
                
                # Store original width and height
                orig_width = self.original_coords[2] - self.original_coords[0]
                orig_height = self.original_coords[3] - self.original_coords[1]

                # Update coordinates based on which edges are being dragged
                if self.resize_edges['left']:
                    coords[0] = min(self.original_coords[2] - min_size, self.original_coords[0] + dx)
                if self.resize_edges['right']:
                    coords[2] = max(self.original_coords[0] + min_size, self.original_coords[2] + dx)
                if self.resize_edges['top']:
                    coords[1] = min(self.original_coords[3] - min_size, self.original_coords[1] + dy)
                if self.resize_edges['bottom']:
                    coords[3] = max(self.original_coords[1] + min_size, self.original_coords[3] + dy)
                
                # Maintain aspect ratio if needed
                if self.master.maintain_ratio_var.get():
                    new_width = abs(coords[2] - coords[0])
                    new_height = abs(coords[3] - coords[1])
                    aspect_ratio = orig_width / orig_height
                    
                    if self.resize_edges['left'] or self.resize_edges['right']:
                        # Width is controlling dimension
                        target_height = new_width / aspect_ratio
                        if self.resize_edges['top']:
                            coords[1] = coords[3] - target_height
                        else:
                            coords[3] = coords[1] + target_height
                    else:
                        # Height is controlling dimension
                        target_width = new_height * aspect_ratio
                        if self.resize_edges['left']:
                            coords[0] = coords[2] - target_width
                        else:
                            coords[2] = coords[0] + target_width
                
                # Ensure the selection stays within canvas bounds
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
                
                coords[0] = max(0, min(coords[0], canvas_width - min_size))
                coords[1] = max(0, min(coords[1], canvas_height - min_size))
                coords[2] = max(min_size, min(coords[2], canvas_width))
                coords[3] = max(min_size, min(coords[3], canvas_height))
                
                # Update selection
                self.canvas.coords(self.crop_rect, *coords)
                self.master.update_spinboxes(coords)
                self.draw_selection()
            else:  # Drawing new selection
                width = abs(event.x - self.start_pos[0])
                height = abs(event.y - self.start_pos[1])
                
                # Maintain aspect ratio if checked
                if self.master.maintain_ratio_var.get():
                    if width > height:
                        height = width
                    else:
                        width = height
                
                # Calculate coordinates based on drag direction
                x1 = min(self.start_pos[0], self.start_pos[0] + (width if event.x > self.start_pos[0] else -width))
                y1 = min(self.start_pos[1], self.start_pos[1] + (height if event.y > self.start_pos[1] else -height))
                x2 = max(self.start_pos[0], self.start_pos[0] + (width if event.x > self.start_pos[0] else -width))
                y2 = max(self.start_pos[1], self.start_pos[1] + (height if event.y > self.start_pos[1] else -height))
                
                # Update selection
                self.canvas.coords(self.crop_rect, x1, y1, x2, y2)
                self.master.update_spinboxes([x1, y1, x2, y2])
                self.draw_selection()
        elif self.moving and self.start_pos:  # Moving the selection
            dx = event.x - self.start_pos[0]
            dy = event.y - self.start_pos[1]
            
            # Calculate new positions based on original coords and delta
            new_x1 = max(0, min(self.original_coords[0] + dx, self.canvas.winfo_width() - (self.original_coords[2] - self.original_coords[0])))
            new_y1 = max(0, min(self.original_coords[1] + dy, self.canvas.winfo_height() - (self.original_coords[3] - self.original_coords[1])))
            new_x2 = new_x1 + (self.original_coords[2] - self.original_coords[0])
            new_y2 = new_y1 + (self.original_coords[3] - self.original_coords[1])
            
            # Update selection
            self.canvas.coords(self.crop_rect, new_x1, new_y1, new_x2, new_y2)
            self.master.update_spinboxes([new_x1, new_y1, new_x2, new_y2])
            self.draw_selection()
            
    def on_release(self, event):
        """Handle mouse button release events."""
        if self.crop_rect:
            coords = self.canvas.coords(self.crop_rect)
            self.master.update_spinboxes(coords)
        self.dragging = False
        self.moving = False
        self.start_pos = None
        if hasattr(self, 'resize_edges'):
            delattr(self, 'resize_edges')
        if hasattr(self, 'original_coords'):
            delattr(self, 'original_coords')
        
    def show_frame(self):
        """Show the current frame of the GIF."""
        if self.frames:
            self.canvas.delete("gif")
            # Draw image with lower z-order
            self.canvas.create_image(0, 0, anchor='nw', image=self.frames[self.current_frame], tags="gif")
            # Make sure selection is always on top
            if self.crop_rect:
                self.draw_selection()
            
    def draw_selection(self):
        """Draw the selection rectangle and grid overlay."""
        if not self.crop_rect:
            return
            
        # Get the current coordinates
        coords = self.canvas.coords(self.crop_rect)
        # Delete old selection
        self.canvas.delete(self.crop_rect)
        
        if self.master.circular_var.get():
            # Create oval for circular selection
            self.crop_rect = self.canvas.create_oval(
                coords[0], coords[1], coords[2], coords[3],
                outline='red', width=2
            )
        else:
            # Create rectangle for normal selection
            self.crop_rect = self.canvas.create_rectangle(
                coords[0], coords[1], coords[2], coords[3],
                outline='red', width=2
            )
        
        self.canvas.tag_raise(self.crop_rect)
        self.draw_grid()

    def draw_grid(self):
        """Draw the grid overlay based on current row/column settings."""
        if not self.crop_rect:
            return
            
        coords = self.canvas.coords(self.crop_rect)
        rows = self.master.rows_var.get()
        cols = self.master.cols_var.get()
        
        # Remove old grid lines
        self.canvas.delete("grid")
        
        # Draw vertical grid lines
        cell_width = (coords[2] - coords[0]) / cols
        for i in range(1, cols):
            x = coords[0] + (cell_width * i)
            self.canvas.create_line(
                x, coords[1], x, coords[3],
                fill='red', width=1, tags="grid"
            )
        
        # Draw horizontal grid lines
        cell_height = (coords[3] - coords[1]) / rows
        for i in range(1, rows):
            y = coords[1] + (cell_height * i)
            self.canvas.create_line(
                coords[0], y, coords[2], y,
                fill='red', width=1, tags="grid"
            )

    def animate(self):
        """Animate the GIF by updating the current frame."""
        if self.frames:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.show_frame()
            self.after(100, self.animate)
            
    def set_gif(self, gif_path):
        """Load and display a GIF file.
        
        Args:
            gif_path: Path to the GIF file to load
        """
        self.gif = Image.open(gif_path)
        self.frames = []
        try:
            while True:
                frame = self.gif.copy()
                # Resize frame maintaining aspect ratio
                new_width = frame.size[0]
                new_height = frame.size[1]
                photo = ImageTk.PhotoImage(frame)
                self.frames.append(photo)
                self.gif.seek(self.gif.tell() + 1)
        except EOFError:
            pass
        
        self.geometry(f"{int(new_width)}x{int(new_height)}")
        self.canvas.config(width=new_width, height=new_height)
        self.show_frame()
        self.animate()
        
        # Create initial selection
        self.create_initial_selection()
        
    def create_initial_selection(self):
        """Create the initial selection rectangle centered in the preview."""
        if self.frames:
            # Get canvas dimensions
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            
            # Create selection in the center with default size
            sel_width = min(200, width - 20)  # Default width or smaller if canvas is small
            sel_height = min(200, height - 20)  # Default height or smaller if canvas is small
            
            # Calculate centered position
            x = (width - sel_width) // 2
            y = (height - sel_height) // 2
            
            # Create the selection rectangle
            self.crop_rect = self.canvas.create_rectangle(
                x, y, x + sel_width, y + sel_height,
                outline='red', width=2
            )
            self.master.update_selection_from_inputs('ui')

    def on_closing(self):
        """Handle window closing events."""
        self.master.preview_window = None
        self.destroy()

if __name__ == '__main__':
    app = Main()
    app.mainloop()
