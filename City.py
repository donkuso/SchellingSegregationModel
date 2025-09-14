# City function manages 
#   creating the grid, 
#   placing agent and empty cells, 
#   checking neighbors, 
#   and moving unsatisfied agents

import random
from Agent import Agent

class City:
    def __init__(self, width, height, rounds):
        """
        width: number of columns
        height: number of rows
        rounds: number of stimulation rounds
        """
        self.width = width
        self.height = height
        self.rounds = rounds
        self.grid = []
        self.set_up()
    
    def __str__(self):
        """Returns string representation of the grid"""
        rows = []
        for r in self.grid:
            row_str = "|"
            for c in r:
                if c is None:
                    row_str += "_|"
                else:
                    row_str += str(c) + "|"
            rows.append(row_str)
        return "\n".join(rows)

    def set_up(self):
        self.grid = []
        for r in range(self.height):
            row = []
            for c in range(self.width):
                roll = random.random()
                if roll < 1/3:
                    row.append(Agent("X"))
                elif roll < 2/3:
                    row.append(Agent("0"))
                else: 
                    row.append(None)
            self.grid.append(row)

    def get_neighbors(self, x, y):
        neighbors = []
        for r in range(y-1, y+2):
            for c in range(x-1, x+2):
                if r == y and c == x: 
                    continue
                if 0 <= r < self.height and 0 <= c < self.width:
                    neighbors.append(self.grid[r][c])
        return neighbors

    def move_agent(self, x, y):
        """Move agent at (x,y) to a random empty cell in the grid."""
        agent = self.grid[y][x]
        if agent is None:
            return  
        empties = [(r, c) for r in range(self.height) 
                          for c in range(self.width) 
                          if self.grid[r][c] is None]
        if not empties:
            return  
        new_r, new_c = random.choice(empties)
        self.grid[new_r][new_c] = agent
        self.grid[y][x] = None

    def simulate(self):
        """Run the simulation for the set number of rounds."""
        for round_num in range(self.rounds):
            unsatisfied = []
            for r in range(self.height):
                for c in range(self.width):
                    agent = self.grid[r][c]
                    if agent is not None:
                        neighbors = self.get_neighbors(c, r)
                        if not agent.is_satisfied(neighbors):
                            unsatisfied.append((c, r))

            # move unsatisfied agents
            for (x, y) in unsatisfied:
                self.move_agent(x, y)

            print(f"--- Round {round_num+1} ---")
            print(self)
            print()