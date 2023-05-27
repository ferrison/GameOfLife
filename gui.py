import tkinter

blank_image = tkinter.PhotoImage()
button_common_settings = {
    'image': blank_image,
    'bd': 0,
    'relief': tkinter.FLAT
}


class Cell:
    mem_colors = {
        False: '#FFB2B8',
        True: 'red',
    }

    inter_colors = {
        False: '#9B9BFF',
        True: 'blue',
    }

    logic_colors = {
        False: '#BAFFBA',
        True: 'green',
    }

    button_size = 20

    def __init__(self, widget, x, y, gol_cell, grid):
        self.gol_cell = gol_cell
        self.grid = grid

        self.cell = tkinter.Frame(widget, pady=4, padx=4)
        self.cell.grid(row=y, column=x)

        self.mem_button = tkinter.Button(self.cell, command=self.flip_gol_cell, width=self.button_size*2+4, height=self.button_size*2, **button_common_settings)
        self.mem_button.grid(column=2, row=2, columnspan=2, rowspan=2)

        self.inter_buttons = self.init_inter_buttons()
        self.logic_buttons = self.init_logic_buttons()

    def flip_gol_cell(self):
        self.gol_cell.is_alive = not self.gol_cell.is_alive
        self.grid.update()

    def init_inter_buttons(self):
        inter_buttons = []

        for column, row, columnspan, rowspan in (
                (0, 0, 2, 1),
                (2, 0, 2, 1),
                (4, 0, 2, 1),
                (0, 1, 2, 4),
                (4, 1, 2, 4),
                (0, 5, 2, 1),
                (2, 5, 2, 1),
                (4, 5, 2, 1),
        ):

            inter_buttons.append(tkinter.Button(self.cell, state=tkinter.DISABLED, width=self.button_size*columnspan, height=self.button_size*rowspan, **button_common_settings))
            inter_buttons[-1].grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan)

        return inter_buttons

    def init_logic_buttons(self):
        logic_buttons = []

        for column, row in (
                (2, 1),
                (3, 1),
                (2, 4),
                (3, 4),
        ):

            logic_buttons.append(tkinter.Button(self.cell, state=tkinter.DISABLED, width=self.button_size, height=self.button_size, **button_common_settings))
            logic_buttons[-1].grid(column=column, row=row)

        return logic_buttons

    def update(self):
        self.mem_button.configure(bg=self.mem_colors[self.gol_cell.is_alive])

        for i in range(8):
            self.inter_buttons[i].configure(bg=self.inter_colors[self.gol_cell.neighbors[i].is_alive])

        for logic_button in self.logic_buttons:
            logic_button.configure(bg=self.logic_colors[False])


class Grid:
    def __init__(self, widget, gol_grid):
        self.grid = tkinter.Frame(widget)
        self.grid.pack()
        self.cells = []

        for y, row in enumerate(gol_grid.grid):
            for x, gol_cell in enumerate(row):
                self.cells.append(Cell(self.grid, x, y, gol_cell, self))

    def update(self):
        for cell in self.cells:
            cell.update()
