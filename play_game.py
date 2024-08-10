import tkinter as tk
import math
import sys
from constants import *
from environment import Environment
from environment import *
from tkinter import messagebox

"""
play_game.py

Running this file launches an interactive environment simulation. Becoming familiar with the environment mechanics may
be helpful in designing your solution.

The script takes 1 argument, input_filename, which must be a valid testcase file (e.g. one of the provided files in the
testcases directory). 

When prompted for an action, press W to move the BEE forward, S to move the BEE in reverse, A to turn the BEE
left (counterclockwise) and D to turn the BEE right (clockwise). Use Q to exit the simulation, and R to reset the
environment to the initial configuration.

COMP3702 2024 Assignment 1 Support Code
"""

class GUI:
    TILE_SIZE = 40 # Tile size
    SQRT3 = math.sqrt(3)

    def __init__(self, game_env):
        self.game_env = game_env
        self.state = game_env.get_init_state()
        self.total_cost = 0

        self.hex_width = 2 * GUI.TILE_SIZE
        self.hex_height = math.sqrt(3) * GUI.TILE_SIZE
        self.y_offset = self.hex_height * 0.75

        self.canvas_width = (self.game_env.n_cols + 4) * (GUI.TILE_SIZE * 1.5)
        self.canvas_height = (self.game_env.n_rows + 4) * (GUI.SQRT3 * GUI.TILE_SIZE)

        self.window = tk.Tk()
        self.window.title("BeeBot")
        self.canvas = tk.Canvas(self.window, bg="#ffd79c", width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(fill="both", expand=True)

        # Color
        self.colors = {
            'obstacle': '#000000',
            'target': '#ff9623',
            'BEE_body': '#3d405b',
            'background': '#feb825',
            'widget': '#8d4200'
        }

        # Bee orientations
        self.BEE_images = {
            BEE_UP: tk.PhotoImage(file="gui_assets/bee_up.png"),
            BEE_DOWN: tk.PhotoImage(file="gui_assets/bee_down.png"),
            BEE_UP_LEFT: tk.PhotoImage(file="gui_assets/bee_top_left.png"),
            BEE_UP_RIGHT: tk.PhotoImage(file="gui_assets/bee_top_right.png"),
            BEE_DOWN_LEFT: tk.PhotoImage(file="gui_assets/bee_bottom_left.png"),
            BEE_DOWN_RIGHT: tk.PhotoImage(file="gui_assets/bee_bottom_right.png")
        }

        self.draw_hexagonal_grid()
        self.draw_environment()
        self.update_status_bar()

        # Bind key events
        self.window.bind('<w>', self.move_forward)
        self.window.bind('<s>', self.move_reverse)
        self.window.bind('<a>', self.turn_left)
        self.window.bind('<d>', self.turn_right)
        self.window.bind('<q>', self.quit)
        self.window.bind('<r>', self.reset)

    def draw_hex(self, x, y, color):
        """ Draw a flat-top hexagon centered at (x, y) with a given color. """
        points = []
        for i in range(6):
            angle = math.pi / 3 * i
            px = x + GUI.TILE_SIZE * math.cos(angle)
            py = y + GUI.TILE_SIZE * math.sin(angle)
            points.extend([px, py])
        self.canvas.create_polygon(points, outline="black", fill=color, width=2)

    def draw_hexagonal_grid(self):
        """ Draw a centered hexagonal grid. """
        dx = GUI.TILE_SIZE * 1.5
        dy = GUI.SQRT3 * GUI.TILE_SIZE
        self.hexagon_positions = {}
        # Calculate offset to center the grid
        offset_x = (self.canvas_width - (self.game_env.n_cols * dx + GUI.TILE_SIZE)) / 2
        offset_y = (self.canvas_height - (self.game_env.n_rows * dy + GUI.SQRT3 * GUI.TILE_SIZE / 2)) / 2

        # Draw hexagons
        for i in range(self.game_env.n_rows):
            for j in range(self.game_env.n_cols):
                x = offset_x + j * dx
                y = offset_y + i * dy + (GUI.SQRT3 * GUI.TILE_SIZE / 2) * (j % 2)
                # Store the position and dimensions of each hexagon
                self.hexagon_positions[(i, j)] = (x, y)
                # Draw the background hexagon
                self.draw_hex(x, y, self.colors['background'])

    def draw_environment(self):
        """ Draw the specific environment elements on top of the hexagonal grid. """
        dx = GUI.TILE_SIZE * 1.5
        dy = GUI.SQRT3 * GUI.TILE_SIZE

        # Draw obstacles
        for i in range(self.game_env.n_rows):
            for j in range(self.game_env.n_cols):
                if self.game_env.obstacle_map[i][j]:
                    x, y = self.hexagon_positions[(i, j)]
                    self.draw_hex(x, y, self.colors['obstacle'])

        # Draw targets
        for tgt in self.game_env.target_list:
            ti, tj = tgt
            x, y = self.hexagon_positions[(ti, tj)]
            self.draw_hex(x, y, self.colors['target'])

            # Calculate positions for 't', 'g', and 't' inside the hexagon
            char_offset = 5  # Adjust this value as needed to place characters correctly
            self.canvas.create_text(x - char_offset, y, text='t', fill='black')
            self.canvas.create_text(x, y, text='g', fill='black')
            self.canvas.create_text(x + char_offset, y, text='t', fill='black')

        # Draw widgets
        for w in range(self.game_env.n_widgets):
            w_letter_lc = string.ascii_lowercase[w]
            w_letter_uc = string.ascii_uppercase[w]
            w_cells = widget_get_occupied_cells(self.game_env.widget_types[w], self.state.widget_centres[w],
                                                self.state.widget_orients[w])
            for wi, wj in w_cells:
                x = self.hexagon_positions[(wi, wj)][0]
                y = self.hexagon_positions[(wi, wj)][1]
                self.draw_hex(x, y, self.colors['widget'])

                # Determine if the current cell is the center of the widget
                if (wi, wj) == self.state.widget_centres[w]:
                    text = f"({w_letter_uc})"
                else:
                    text = f"({w_letter_lc})"

                self.canvas.create_text(x, y, text=text, fill='black')

        # Draw bee with orientations
        ri, rj = self.state.BEE_posit
        x, y = self.hexagon_positions[(ri, rj)]


        if hasattr(self, 'BEE_image_id'):
            self.canvas.delete(self.BEE_image_id)

        # Display the BEE image
        orientation = self.state.BEE_orient
        image = self.BEE_images.get(orientation)
        if image:
            self.BEE_image_id = self.canvas.create_image(x, y, image=image)

    def update_status_bar(self):
        if hasattr(self, 'status_bar'):
            self.status_bar.destroy()
        self.status_bar = tk.Label(self.window, text=f"Total Cost: {self.total_cost}", bg="lightgray")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def move_forward(self, event):
        self.perform_action(FORWARD)

    def move_reverse(self, event):
        self.perform_action(REVERSE)

    def turn_left(self, event):
        self.perform_action(SPIN_LEFT)

    def turn_right(self, event):
        self.perform_action(SPIN_RIGHT)

    def perform_action(self, action):
        success, cost, new_state = self.game_env.perform_action(self.state, action)
        if success:
            self.total_cost += cost
            self.state = new_state
            if self.game_env.is_solved(self.state):
                self.draw_hexagonal_grid()
                self.draw_environment()
                self.update_status_bar()
                messagebox.showinfo("Game Over",
                                    f"Environment solved with a total cost of {round(self.total_cost, 1)}!")
                self.window.quit()
        else:
            messagebox.showwarning("Warning", "Action resulted in collision. Please select a different action.")
        self.draw_hexagonal_grid()
        self.draw_environment()
        self.update_status_bar()

    def reset(self, event):
        self.state = self.game_env.get_init_state()
        self.total_cost = 0
        self.draw_hexagonal_grid()
        self.draw_environment()
        self.update_status_bar()

    def quit(self, event):
        self.window.quit()

    def render(self, action):
        success, cost, new_state = self.game_env.perform_action(self.state, action)
        
        if success:
            self.total_cost += cost
            self.state = new_state
            
            if self.game_env.is_solved(self.state):
                self.draw_hexagonal_grid()
                self.draw_environment()
                self.update_status_bar()
                tk.messagebox.showinfo("Game Over",
                                    f"Environment solved with a total cost of {round(self.total_cost, 1)}!")
                self.window.quit()
            else:
                self.draw_hexagonal_grid()
                self.draw_environment()
                self.update_status_bar()
        else:
            tk.messagebox.showwarning("Warning", "Action resulted in collision. Please select a different action.")
        
        self.window.update()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: play.py [input_filename]")
        sys.exit(1)

    input_file = sys.argv[1]
    env = Environment(input_file)
    gui = GUI(env)
    gui.window.mainloop()
