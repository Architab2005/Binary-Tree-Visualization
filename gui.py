import tkinter as tk
from tkinter import messagebox, colorchooser
from PIL import Image, ImageDraw, ImageFont  
import os
from tree import AVLTree

class UltimateTreeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌳 Ultimate AVL Tree Visualizer v3.0")
        self.root.geometry("1200x850")
        self.root.configure(bg='#1e1e1e')  # Dark default
        self.tree = AVLTree()
        self.dark_mode = True
        self.colors = {
            'bg': '#1e1e1e', 'canvas': '#2d2d2d', 'node': '#4CAF50', 'highlight': '#FFD700',
            'line': '#2196F3', 'text': '#ffffff', 'footer': '#424242'
        }
        self.setup_ui()
        self.draw_tree()

    def setup_ui(self):
        # Theme toggle + controls
        theme_frame = tk.Frame(self.root, bg=self.colors['bg'])
        theme_frame.pack(pady=10)
        
        tk.Button(theme_frame, text="🌙 Dark" if not self.dark_mode else "☀️ Light", 
                 command=self.toggle_theme, bg=self.colors['node'], fg="white",
                 font=('Arial', 11, 'bold')).pack(side=tk.LEFT, padx=10)
        tk.Button(theme_frame, text="📸 Export PNG", command=self.export_png,
                 bg="#FF5722", fg="white", font=('Arial', 11, 'bold')).pack(side=tk.LEFT, padx=10)

        control_frame = tk.Frame(self.root, bg=self.colors['bg'])
        control_frame.pack(pady=5)
        tk.Label(control_frame, text="Value:", font=('Arial', 12, 'bold'), 
                bg=self.colors['bg'], fg=self.colors['text']).pack(side=tk.LEFT)
        self.entry = tk.Entry(control_frame, width=6, font=('Arial', 12), bg='#3c3c3c', fg='white')
        self.entry.pack(side=tk.LEFT, padx=(0,10))
        self.entry.insert(0, "50")

        btn_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        btn_frame.pack(side=tk.LEFT)
        tk.Button(btn_frame, text="🔵 AVL Insert", command=self.animate_insert, 
                 bg=self.colors['node'], fg="white").pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="🔍 Animate Search", command=self.animate_search, 
                 bg="#FF9800", fg="white").pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="🎲 Random 25", command=self.random_tree, 
                 bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="♻️ Clear", command=self.clear_highlights, 
                 bg="#9E9E9E", fg="white").pack(side=tk.LEFT, padx=2)

        # Traversals
        trav_frame = tk.Frame(self.root, bg=self.colors['bg'])
        trav_frame.pack(pady=5)
        tk.Button(trav_frame, text="📊 Inorder", command=self.show_inorder, 
                 bg="#FF5722", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(trav_frame, text="📏 Height", command=self.show_height, 
                 bg="#9C27B0", fg="white").pack(side=tk.LEFT, padx=5)

        # Canvas
        self.canvas = tk.Canvas(self.root, width=1100, height=600, 
                               bg=self.colors['canvas'], relief="ridge", bd=3)
        self.canvas.pack(pady=20)

        # Footer
        footer = tk.Frame(self.root, bg=self.colors['footer'], height=60)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        footer.pack_propagate(False)
        self.footer_label = tk.Label(footer, 
            text="Binary-Tree-Visualization | 👩‍💻 Archita.B | B.TECH CSE'26 | Tech‑Driven Business Solutions", 
            bg=self.colors['footer'], fg=self.colors['text'], font=('Arial', 11, 'bold'))
        self.footer_label.pack(pady=15)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.colors = {'bg': '#1e1e1e', 'canvas': '#2d2d2d', 'node': '#4CAF50', 'highlight': '#FFD700', 'line': '#2196F3', 'text': '#ffffff', 'footer': '#424242'}
            self.root.configure(bg='#1e1e1e')
        else:
            self.colors = {'bg': '#f8f9fa', 'canvas': '#ffffff', 'node': '#e3f2fd', 'highlight': '#fff176', 'line': '#1976d2', 'text': '#212529', 'footer': '#e9ecef'}
            self.root.configure(bg='#f8f9fa')
        self.setup_ui()  # Refresh colors
        self.draw_tree()

    def animate_insert(self):
        try:
            val = int(self.entry.get())
            self.tree.insert_node(val)
            self.footer_label.config(text=f"✅ AVL Inserted {val} - Rotations Applied! | 👩‍💻 Archita.B CSE'26")
            self.draw_tree()
        except:
            messagebox.showerror("Error", "Enter integer 1-999!")

    def animate_search(self):
        try:
            val = int(self.entry.get())
            found, path = self.tree.search_node(val)
            self.draw_tree(highlight_path=path)
            status = "✅ FOUND" if found else "❌ NOT FOUND"
            self.footer_label.config(text=f"🔍 Search {val}: {status} | Path: {path} | 👩‍💻 Archita.B CSE'26")
        except:
            messagebox.showerror("Error", "Enter integer!")

    def random_tree(self):
        self.tree = AVLTree()
        self.tree.generate_random(30)
        self.footer_label.config(text="🎲 Perfect 30-node AVL Tree | Always Balanced! | 👩‍💻 Archita.B CSE'26")
        self.draw_tree()

    def clear_highlights(self):
        self.tree.clear_visited(self.tree.root)
        self.draw_tree()
        self.footer_label.config(text="♻️ Highlights cleared | 👩‍💻 Archita.B CSE'26")

    def show_inorder(self):
        trav = self.tree.inorder()
        messagebox.showinfo("Inorder", f"[{', '.join(map(str, trav[:20]))}{'...' if len(trav)>20 else ''}]")

    def show_height(self):
        h = self.tree.height()
        messagebox.showinfo("Stats", f"Height: {h}\nNodes: {len(self.tree.inorder())}\nLog(n): {round(self.tree.height() / (len(self.tree.inorder())**0.48), 2)}")

    def export_png(self):
        try:
            ps_filename = "temp_tree.eps"
            png_filename = f"avl_tree_{len(self.tree.inorder())}_nodes.png"
            
            # Canvas to PostScript
            self.canvas.postscript(file=ps_filename, colormode='color')
            
            # Convert to PNG
            from PIL import Image
            img = Image.open(ps_filename)
            img.save(png_filename, 'PNG')
            os.remove(ps_filename)
            
            self.footer_label.config(text=f"📸 Saved {png_filename} | 👩‍💻 Archita.B CSE'26")
            messagebox.showinfo("✅ Exported", f"{png_filename}\nSize: {img.size}")
        except ImportError:
            messagebox.showerror("Missing", "pip install Pillow")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed:\n{str(e)}")
            
    def draw_tree(self, highlight_path=None):
        self.canvas.delete("all")
        if not self.tree.root:
            self.canvas.create_text(550, 300, text="Empty AVL Tree\nInsert or Random!", 
                                  font=("Arial", 20), fill=self.colors['text'])
            return
        
        self._draw_recursive(self.tree.root, 550, 100, 500, highlight_path)
        self.canvas.create_text(550, 30, text="Ultimate AVL Tree v3.0 - Dark Mode + PNG Export", 
                               font=("Arial", 16, "bold"), fill=self.colors['text'])

    def _draw_recursive(self, node, x, y, spacing, highlight_path):
        if not node: return
        
        color = self.colors['highlight'] if node.val in (highlight_path or []) else self.colors['node']
        self.canvas.create_oval(x-28, y-20, x+28, y+20, fill=color, outline="#2e7d32", width=3)
        self.canvas.create_text(x, y, text=str(node.val), font=("Arial", 15, "bold"))
        
        # Balance factor
        balance = self.tree.get_balance(node)
        self.canvas.create_text(x, y+40, text=f"BF: {balance}", font=("Arial", 10), fill="#FF6B6B")
        
        # Recurse
        self._draw_recursive(node.left, x-spacing//2, y+90, spacing//2, highlight_path)
        self._draw_recursive(node.right, x+spacing//2, y+90, spacing//2, highlight_path)
        
        # Lines
        if node.left:
            self.canvas.create_line(x, y+20, x-spacing//2, y+70, fill=self.colors['line'], width=3, arrow=tk.LAST)
        if node.right:
            self.canvas.create_line(x, y+20, x+spacing//2, y+70, fill=self.colors['line'], width=3, arrow=tk.LAST)
