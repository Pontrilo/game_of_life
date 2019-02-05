import numpy as np
import pylab
import random
import matplotlib.pyplot as plt


class GameOfLife:
    def __init__(self, seed_grid, n=9, t=5):
        self.n = n  # The width and height of the grid
        self.t = t  # The maximum number of timesteps
        # Create two grids to hold the old and new configurations. Dead cell represented with 0, alive with 1
        self.ogrid = np.zeros(n * n, dtype='i').reshape(n, n)
        self.seed_grid = seed_grid  # Set alive cells
        self.ogrid[4:7, 4:5] = self.seed_grid  # place alive cells on the grid
        self.ngrid = np.zeros(n * n, dtype='i').reshape(n, n)

        # If preferred set up a random initial configuration for the grid instead of a seed grid
        """
        for i in range(0, self.n):
            for j in range(0, self.n):
                if random.randint(0, 100) < 15:
                    self.old_grid[i][j] = 1
                else:
                    self.old_grid[i][j] = 0
        """

    def alive_neighbours(self, i, j):
        neighbours = 0  # Set initial neighbours to zero

        for x in [i - 1, i, i + 1]:
            for y in [j - 1, j, j + 1]:
                if x == i and y == j:
                    continue  # Skip the cell itself
                if x != self.n and y != self.n:
                    neighbours += self.ogrid[x][y]  # For each cell on the grid, add the neighbours to the count
                # Elifs handle the case where the neighbour is off the grid. Grid is a toroidal array
                elif x == self.n and y != self.n:
                    neighbours += self.ogrid[0][y]
                elif x != self.n and y == self.n:
                    neighbours += self.ogrid[x][0]
                else:
                    neighbours += self.ogrid[0][0]
        return neighbours  # Return the total amount of neighbours

    def running(self):
        plt.imshow(self.ogrid, cmap='binary')  # Draw initial grid
        plt.show()  # Show grid in window

        tl = 1  # Set starting time level
        while tl <= self.t:  # If time level is below max timesteps keep playing

            # Apply Conway's rules to every cell of the grid
            for i in range(self.n):
                for j in range(self.n):
                    alive = self.alive_neighbours(i, j)  # Set total neighbours for each cell to alive
                    if self.ogrid[i][j] == 1 and alive < 2:
                        self.ngrid[i][j] = 0  # Dead from underpopulation
                    elif self.ogrid[i][j] == 1 and (alive == 2 or alive == 3):
                        self.ngrid[i][j] = 1  # Survival
                    elif self.ogrid[i][j] == 1 and alive > 3:
                        self.ngrid[i][j] = 0  # Dead from overcrowding
                    elif self.ogrid[i][j] == 0 and alive == 3:
                        self.ngrid[i][j] = 1  # The creation of life

            pylab.imshow(self.ngrid, cmap='binary')  # Draw new grid
            pylab.show()  # Show new grid

            # The new configuration becomes the old configuration for the next generation
            self.ogrid = self.ngrid.copy()

            # Move on to the next time level
            tl += 1


gameOne = GameOfLife(seed_grid=[[0], [0], [0]], n=9, t=1)  # Scenario 5, Grid with no live cells
gameTwo = GameOfLife(seed_grid=[[1], [1], [1]], n=9, t=3)  # Scenario 6, Expected outcome for seeded grid
gameOne.running()
print("game over")
gameTwo.running()
