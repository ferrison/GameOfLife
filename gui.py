import tkinter

blank_image = tkinter.PhotoImage()
button_common_settings = {
    'image': blank_image,
    'bd': 0,
    'relief': tkinter.FLAT
}


class Cell:
    mem_colors = {
        True: '#60A917',
        False: '#008A00',
    }

    inter_colors = {
        True: '#1BA1E2',
        False: '#0050EF',
    }

    logic_colors = {
        True: '#D80073',
        False: '#A20025',
    }

    button_size = 20

    def __init__(self, widget, x, y, gol_cell, grid):
        self.gol_cell = gol_cell
        self.grid = grid

        self.cell = tkinter.Frame(widget, pady=10, padx=10, bg='black', highlightbackground="white", highlightthickness=2)
        self.cell.grid(row=y, column=x)

        self.mem_button = tkinter.Button(self.cell, text="ЭП", fg="white", compound="center", command=self.flip_gol_cell, width=self.button_size, height=self.button_size, **button_common_settings)
        self.mem_button.grid(column=3, row=3)

        self.inter_buttons = self.init_inter_buttons()
        self.logic_buttons = self.init_logic_buttons()

    def flip_gol_cell(self):
        self.gol_cell.is_alive = not self.gol_cell.is_alive
        self.grid.update()

    def init_inter_buttons(self):
        inter_buttons = []

        for column, row, columnspan, rowspan in (
                (1, 1, 1, 1),
                (3, 0, 1, 1),
                (5, 1, 1, 1),
                (0, 3, 1, 1),
                (6, 3, 1, 1),
                (1, 5, 1, 1),
                (3, 6, 1, 1),
                (5, 5, 1, 1),
        ):

            inter_buttons.append(tkinter.Button(self.cell, text="ЛЭ", fg="white", compound="center", width=self.button_size, height=self.button_size, **button_common_settings))
            inter_buttons[-1].grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan)

        return inter_buttons

    def init_logic_buttons(self):
        logic_buttons = []

        for column, row in (
                (3, 2),
                (2, 3),
                (4, 3),
                (3, 4),
        ):

            logic_buttons.append(tkinter.Button(self.cell, text="ЭВЗ", fg="white", compound="center", width=self.button_size, height=self.button_size, **button_common_settings))
            logic_buttons[-1].grid(column=column, row=row)

        return logic_buttons

    def update(self, highlight_only_mem):
        self.mem_button.configure(bg=self.mem_colors[self.gol_cell.is_alive])

        if highlight_only_mem:
            for i in range(8):
                self.inter_buttons[i].configure(bg=self.inter_colors[False])

            self.logic_buttons[0].configure(bg=self.logic_colors[False])
            self.logic_buttons[1].configure(bg=self.logic_colors[False])
            self.logic_buttons[2].configure(bg=self.logic_colors[False])
            self.logic_buttons[3].configure(bg=self.logic_colors[False])

            return

        for i in range(8):
            self.inter_buttons[i].configure(bg=self.inter_colors[self.gol_cell.neighbors[i].is_alive])

        self.logic_buttons[0].configure(bg=self.logic_colors[self.gol_cell.neighbors[1].is_alive or self.gol_cell.neighbors[2].is_alive])
        self.logic_buttons[1].configure(bg=self.logic_colors[self.gol_cell.neighbors[0].is_alive or self.gol_cell.neighbors[3].is_alive])
        self.logic_buttons[2].configure(bg=self.logic_colors[self.gol_cell.neighbors[4].is_alive or self.gol_cell.neighbors[7].is_alive])
        self.logic_buttons[3].configure(bg=self.logic_colors[self.gol_cell.neighbors[5].is_alive or self.gol_cell.neighbors[6].is_alive])


class Grid:
    def __init__(self, widget, gol_grid):
        self.grid = tkinter.Frame(widget)
        self.highlight_only_mem = False
        self.grid.pack()
        self.cells = []

        for y, row in enumerate(gol_grid.grid):
            for x, gol_cell in enumerate(row):
                self.cells.append(Cell(self.grid, x, y, gol_cell, self))

    def update(self):
        for cell in self.cells:
            cell.update(self.highlight_only_mem)
