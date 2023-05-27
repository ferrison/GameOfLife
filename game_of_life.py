class Cell:
    def __init__(self, grid):
        self.grid = grid
        self.is_alive = False
        self.is_alive_in_next_step = None
        self.neighbors = []  # 0 это верхний левый, дальше по часовой
        self.rules = []

    def calc_next_step_state(self):
        self.is_alive_in_next_step = self.is_alive
        for rule in self.rules:
            self.is_alive_in_next_step = rule(self)

    def set_precalced_state(self):
        self.is_alive = self.is_alive_in_next_step
        self.is_alive_in_next_step = None


class Grid:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.current_step = 0
        self.grid = [[Cell(grid=self) for _ in range(width)] for _ in range(height)]

        self.init_neighbors_links()

    def __getitem__(self, item):
        x, y = item
        return self.grid[y % self.height][x % self.width]

    def init_neighbors_links(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                cell.neighbors = [
                    self[x-1, y-1], self[x, y-1], self[x+1, y-1],
                    self[x-1, y], self[x+1, y],
                    self[x-1, y+1], self[x, y+1], self[x+1, y+1],
                ]

    def set_states(self, states):
        if len(states) != len(self.grid) or len(states[0]) != len(self.grid[0]):
            raise ValueError('Не правильный размер')

        for y, row in enumerate(states):
            for x, state in enumerate(row):
                self[x, y].is_alive = state

    def get_states(self):
        states = [[None]*self.width for _ in range(self.height)]

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                states[y][x] = cell.is_alive

        return states

    def set_rule_to_each_cell(self, rule):
        for row in self.grid:
            for cell in row:
                cell.rules.append(rule)

    def next_step(self):
        for row in self.grid:
            for cell in row:
                cell.calc_next_step_state()

        for row in self.grid:
            for cell in row:
                cell.set_precalced_state()

        self.current_step += 1

        return self.get_states()
