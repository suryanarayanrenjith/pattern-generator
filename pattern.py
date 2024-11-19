import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk
import random
import math
import threading

class RangoliSensoryBoard:
    def __init__(self, master):
        self.master = master
        self.master.title("Pattern Generator")
        
        # Initialize attributes
        self.templates = self.create_templates()
        self.colors = self.load_colors("colors.txt")
        self.current_pattern = None
        self.img = None
        self.tk_img = None
        
        self.canvas = tk.Canvas(self.master, width=800, height=800)
        self.canvas.pack()
        
        self.run()
        
        threading.Thread(target=self.console_input, daemon=True).start()

    def load_colors(self, filename):
        colors = {}
        with open(filename, 'r') as file:
            for line in file:
                name, value = line.strip().split(':')
                colors[name.strip()] = tuple(map(int, value.split(',')))
        return colors

    def create_templates(self):
        templates = {
            "lotus_flower": ["flower", "circle", "petal", "star"],
            "symmetrical_star": ["star", "circle", "hexagon", "triangle"],
            "floral_mandala": ["flower", "circle", "hexagon", "spiral"],
            "geometric_rangoli": ["hexagon", "triangle", "square", "circle"],
            "peacock_feather": ["feather", "circle", "arc", "nested"]
        }
        return templates

    def select_template(self, template_name):
        if template_name in self.templates:
            self.current_pattern = self.templates[template_name]
        else:
            print(f"Template '{template_name}' not found.")
    
    def customize_pattern(self):
        pattern = []
        for shape in self.current_pattern:
            element = {
                "shape": shape,
                "color": random.choice(list(self.colors.keys())),
                "rotation": random.randint(0, 360),
                "size_variation": random.uniform(0.7, 1.3), to maintain pattern symmetry
            }
            pattern.append(element)
        return pattern
    
    def draw_star(self, draw, center, size, color, rotation):
        points = []
        for i in range(5):
            angle = i * (2 * math.pi / 5) - math.pi / 2 + math.radians(rotation)
            x = center[0] + size * math.cos(angle)
            y = center[1] + size * math.sin(angle)
            points.append((x, y))
        draw.polygon(points, fill=color)

    def draw_flower(self, draw, center, size, color, rotation):
        for i in range(6):
            angle = i * (2 * math.pi / 6) + math.radians(rotation)
            x = center[0] + size * math.cos(angle)
            y = center[1] + size * math.sin(angle)
            draw.ellipse([
                (x - size / 3, y - size / 3),
                (x + size / 3, y + size / 3)
            ], fill=color)

    def draw_hexagon(self, draw, center, size, color, rotation):
        points = []
        for i in range(6):
            angle = i * (2 * math.pi / 6) - math.pi / 2 + math.radians(rotation)
            x = center[0] + size * math.cos(angle)
            y = center[1] + size * math.sin(angle)
            points.append((x, y))
        draw.polygon(points, fill=color)
    
    def draw_concentric_circles(self, draw, center, size, color):
        for i in range(5, 0, -1):
            draw.ellipse([
                (center[0] - size * i / 5, center[1] - size * i / 5),
                (center[0] + size * i / 5, center[1] + size * i / 5)
            ], outline=color)

    def create_image(self, pattern):
        img_size = 800
        self.img = Image.new('RGB', (img_size, img_size), (255, 255, 255))
        draw = ImageDraw.Draw(self.img)
        
        center = (img_size // 2, img_size // 2)

        max_radius = 200
        step = max_radius // len(pattern)
        radius = max_radius

        for element in pattern:
            color = self.colors[element['color']]
            shape = element['shape']
            rotation = element['rotation']
            size_variation = element['size_variation']
            adjusted_radius = radius * size_variation

            if shape == "circle":
                draw.ellipse([
                    (center[0] - adjusted_radius, center[1] - adjusted_radius),
                    (center[0] + adjusted_radius, center[1] + adjusted_radius)
                ], outline=color, fill=color)

            elif shape == "star":
                self.draw_star(draw, center, adjusted_radius, color, rotation)

            elif shape == "flower":
                self.draw_flower(draw, center, adjusted_radius, color, rotation)

            elif shape == "hexagon":
                self.draw_hexagon(draw, center, adjusted_radius, color, rotation)

            elif shape == "concentric":
                self.draw_concentric_circles(draw, center, adjusted_radius, color)

            radius -= step
        
        self.tk_img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)

    def save_image(self):
        if self.img:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                self.img.save(file_path)
                print(f"Image saved as {file_path}")

    def console_input(self):
        while True:
            print("\nOptions:")
            print("1. Download Image")
            print("2. Rerun Code to Generate New Pattern")
            print("3. Exit")
            choice = input("Enter your choice (1, 2, or 3): ").strip()

            if choice == "1":
                self.save_image()
            elif choice == "2":
                self.run()
            elif choice == "3":
                print("Exiting the program. Goodbye!")
                self.master.quit()
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

    def run(self):
        template_name = random.choice(list(self.templates.keys()))
        self.select_template(template_name)
        pattern = self.customize_pattern()

        self.create_image(pattern)

if __name__ == "__main__":
    root = tk.Tk()
    app = RangoliSensoryBoard(root)
    root.mainloop()
