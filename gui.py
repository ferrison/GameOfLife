import tkinter

blank_image = tkinter.PhotoImage()
button_common_settings = {
    'image': blank_image,
    'bd': 0,
    'relief': tkinter.FLAT
}


class Cell:
    mem_colors = {
        True: '#008A00',
        False: '#6FF07C',
    }

    inter_colors = {
        True: '#0050EF',
        False: '#A6CAFF',
    }

    logic_colors = {
        True: '#A20025',
        False: '#FFA6BB',
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

        for column, row in (
                (1, 1),
                (3, 0),
                (5, 1),
                (0, 3),
                (6, 3),
                (1, 5),
                (3, 6),
                (5, 5),
        ):

            inter_buttons.append(tkinter.Button(self.cell, text="ЛЭ", fg="white", compound="center", width=self.button_size, height=self.button_size, **button_common_settings))
            inter_buttons[-1].grid(column=column, row=row)

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
        self.widget = widget

        self.frame = tkinter.Frame(widget, bd=5)
        self.frame.pack()

        self.yscrollbar = tkinter.Scrollbar(self.frame, orient=tkinter.VERTICAL)
        self.yscrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y, expand=True)

        self.canvas = tkinter.Canvas(self.frame, bd=1, highlightthickness=0, height=800, yscrollcommand=self.yscrollbar.set)
        self.canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        self.yscrollbar.config(command=self.canvas.yview)

        self.grid = tkinter.Frame(widget)
        self.grid.pack()

        self.grid_id = self.canvas.create_window((0, 0), window=self.grid, anchor=tkinter.NW)


        def _configure_widget(event):
            self.canvas.config(height=self.widget.winfo_height()-74)

        self.widget.bind('<Configure>', _configure_widget)

        def _configure_grid(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (self.grid.winfo_reqwidth(), self.grid.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if self.grid.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                self.canvas.config(width=self.grid.winfo_reqwidth())

        self.grid.bind('<Configure>', _configure_grid)

        def _configure_canvas(event):
            if self.grid.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                self.canvas.itemconfigure(self.grid_id, width=self.canvas.winfo_width())

        self.canvas.bind('<Configure>', _configure_canvas)

        self.highlight_only_mem = False
        self.cells = []

        for y, row in enumerate(gol_grid.grid):
            for x, gol_cell in enumerate(row):
                self.cells.append(Cell(self.grid, x, y, gol_cell, self))

    def update(self):
        for cell in self.cells:
            cell.update(self.highlight_only_mem)
