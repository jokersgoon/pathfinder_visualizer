import tkinter as tk
from tkinter import ttk
import heapq
import queue
import random

class PathfindingGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Pathfinding Algorithm")

        self.columns = 20
        self.rows = 20
        self.cell_size = 25

        # Add a speed control slider
        # Add a speed control entry
        self.speed_label = tk.Label(self.master, text="Speed (ms):")
        self.speed_label.pack()
        self.speed_entry = tk.Entry(self.master)
        self.speed_entry.insert(0, "100")  # default value
        self.speed_entry.pack()

        self.canvas = tk.Canvas(self.master, width=self.columns * self.cell_size, height=self.rows * self.cell_size)
        self.canvas.pack()

        self.start_node = None
        self.end_node = None

        self.algorithm = tk.StringVar(self.master)
        self.algorithm.set("A*")  # default value

        self.dropdown = ttk.Combobox(self.master, textvariable=self.algorithm, values=["A*", "Dijkstra", "BFS"])
        self.dropdown.pack()

        self.button = tk.Button(self.master, text="Run Algorithm", command=self.run_algorithm)
        self.button.pack()

        # Add a reset button
        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset)
        self.reset_button.pack()

        # Add a reset terrain button
        self.reset_terrain_button = tk.Button(self.master, text="Reset Terrain", command=self.reset_terrain)
        self.reset_terrain_button.pack()

        self.terrain = [[random.choice([0, 1]) if random.random() < 0.2 else 0 for _ in range(self.columns)] for _ in range(self.rows)]

        self.draw_grid()
        self.canvas.bind("<Button-1>", self.place_node)

    def reset(self):
        self.start_node = None
        self.end_node = None
        self.draw_grid()

    def reset_terrain(self):
        self.terrain = [[random.choice([0, 1]) if random.random() < 0.2 else 0 for _ in range(self.columns)] for _ in range(self.rows)]
        self.reset()

    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(self.columns):
            for j in range(self.rows):
                color = "black" if self.terrain[j][i] == 1 else "white"
                self.canvas.create_rectangle(i * self.cell_size, j * self.cell_size, 
                                             (i + 1) * self.cell_size, (j + 1) * self.cell_size, 
                                             outline="gray", fill=color)
    def get_speed(self):
        try:
            speed = float(self.speed_entry.get())
            if speed < 1:
                speed = 1
        except ValueError:
            speed = 100  # default value if input is invalid
        return int(speed)

    def place_node(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size

        if self.start_node is None:
            self.start_node = (x, y)
            self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size, 
                                         (x + 1) * self.cell_size, (y + 1) * self.cell_size, 
                                         fill="green")
        elif self.end_node is None:
            self.end_node = (x, y)
            self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size, 
                                         (x + 1) * self.cell_size, (y + 1) * self.cell_size, 
                                         fill="red")

    def run_algorithm(self):
        if self.start_node and self.end_node:
            algorithm = self.algorithm.get()
            if algorithm == "A*":
                path = self.a_star_search()
            elif algorithm == "Dijkstra":
                path = self.dijkstra_search()
            elif algorithm == "BFS":
                path = self.bfs_search()
            self.draw_path(path)

    def draw_path(self, path):
        for (x, y) in path:
            self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size, 
                                         (x + 1) * self.cell_size, (y + 1) * self.cell_size, 
                                         fill="blue")

    def a_star_search(self):
        open_set = []
        heapq.heappush(open_set, (0, self.start_node))
        came_from = {}
        g_score = {self.start_node: 0}
        f_score = {self.start_node: self.heuristic(self.start_node, self.end_node)}

        def search_step():
            if open_set:
                current = heapq.heappop(open_set)[1]

                if current == self.end_node:
                    path = self.reconstruct_path(came_from, current)
                    self.draw_path(path)
                    return

                for neighbor in self.get_neighbors(current):
                    tentative_g_score = g_score[current] + 1

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, self.end_node)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

                # Visualize the current node
                x, y = current
                self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size, 
                                            (x + 1) * self.cell_size, (y + 1) * self.cell_size, 
                                            fill="yellow")

                # Schedule the next step
                self.master.after(self.get_speed(), search_step)
            else:
                print("No path found")

        # Start the search
        search_step()

    def dijkstra_search(self):
        open_set = []
        heapq.heappush(open_set, (0, self.start_node))
        came_from = {}
        cost_so_far = {self.start_node: 0}

        def search_step():
            if open_set:
                current = heapq.heappop(open_set)[1]

                if current == self.end_node:
                    path = self.reconstruct_path(came_from, current)
                    self.draw_path(path)
                    return

                for neighbor in self.get_neighbors(current):
                    new_cost = cost_so_far[current] + 1

                    if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                        came_from[neighbor] = current
                        cost_so_far[neighbor] = new_cost
                        heapq.heappush(open_set, (new_cost, neighbor))

                # Visualize the current node
                x, y = current
                self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size, 
                                            (x + 1) * self.cell_size, (y + 1) * self.cell_size, 
                                            fill="yellow")

                # Schedule the next step
                self.master.after(self.get_speed(), search_step)
            else:
                print("No path found")

        # Start the search
        search_step()

    def bfs_search(self):
        queue = [(self.start_node, [self.start_node])]
        visited = set()

        def search_step():
            if queue:
                (current, path) = queue.pop(0)

                if current in visited:
                    self.master.after(int(float(self.speed_entry.get())), search_step)
                    return

                visited.add(current)

                if current == self.end_node:
                    self.draw_path(path)
                    return

                for neighbor in self.get_neighbors(current):
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))

                # Visualize the current node
                x, y = current
                self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size, 
                                            (x + 1) * self.cell_size, (y + 1) * self.cell_size, 
                                            fill="yellow")

                # Schedule the next step
                self.master.after(self.get_speed(), search_step)
            else:
                print("No path found")

        # Start the search
        search_step()

    def get_neighbors(self, node):
        x, y = node
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        valid_neighbors = []

        for nx, ny in neighbors:
            if 0 <= nx < self.columns and 0 <= ny < self.rows and self.terrain[ny][nx] == 0:
                valid_neighbors.append((nx, ny))

        return valid_neighbors

    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

if __name__ == "__main__":
    root = tk.Tk()
    gui = PathfindingGUI(root)
    root.mainloop()