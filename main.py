import json
import pathlib
import tkinter

import game_of_life
import rules

SPEED_MIN = 1
SPEED_MAX = 10
GRID_HEIGHT = GRID_WIDTH = 10


def load_rules(grid):
    config = json.loads(pathlib.Path('rules.json').read_text())
    if 'each_cell' in config:
        for rule in config['each_cell']:
            grid.set_rule_to_each_cell(getattr(rules, rule["name"])(**rule["params"]))
        config.pop('each_cell')
    for cell_coords in config:
        for rule in config[cell_coords]:
            for coord in cell_coords.split(';'):
                x, y = map(int, coord.split(','))
                grid[x, y].rules.append(getattr(rules, rule["name"])(**rule["params"]))


def main():
    root = tkinter.Tk()
    root.title("Игра жизнь")

    game_running = False
    speed = SPEED_MIN

    gol_grid = game_of_life.Grid(GRID_HEIGHT, GRID_WIDTH)
    load_rules(gol_grid)

    import gui
    frame = tkinter.Frame(root, bd=5)
    frame.pack()

    scrollbar = tkinter.Scrollbar(frame, orient=tkinter.VERTICAL)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y, expand=True)

    canvas = tkinter.Canvas(frame, bd=1, highlightthickness=0, height=800, yscrollcommand=scrollbar.set)
    canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

    scrollbar.config(command=canvas.yview)

    grid = gui.Grid(root, gol_grid)
    grid_id = canvas.create_window((0, 0), window=grid.grid, anchor=tkinter.NW)
    grid.update()

    def _configure_grid(event):
        # Update the scrollbars to match the size of the inner frame.
        size = (grid.grid.winfo_reqwidth(), grid.grid.winfo_reqheight())
        canvas.config(scrollregion="0 0 %s %s" % size)
        if grid.grid.winfo_reqwidth() != canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            canvas.config(width=grid.grid.winfo_reqwidth())

    grid.grid.bind('<Configure>', _configure_grid)
    _configure_grid(None)

    def _configure_canvas(event):
        if grid.grid.winfo_reqwidth() != canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            canvas.itemconfigure(grid_id, width=canvas.winfo_width())

    canvas.bind('<Configure>', _configure_canvas)
    _configure_canvas(None)

    command_frame = tkinter.Frame(root, borderwidth=10)
    command_frame.pack(side=tkinter.BOTTOM, fill=tkinter.X)

    def step():
        if not game_running:
            gol_grid.next_step()
            grid.update()
    step_button = tkinter.Button(
        command_frame,
        text='Шаг',
        command=step
    )
    step_button.grid(row=0, column=0)

    def continue_():
        nonlocal game_running
        game_running = not game_running
        if game_running:
            continue_button.configure(text='Остановить')
        else:
            continue_button.configure(text='Продолжить')
    continue_button = tkinter.Button(
        command_frame,
        text='Продолжить',
        command=continue_
    )
    continue_button.grid(row=0, column=1)

    def highlight():
        grid.highlight_only_mem = not grid.highlight_only_mem
        grid.update()
        if grid.highlight_only_mem:
            highlight_button.configure(text='Подсвечивать все')
        else:
            highlight_button.configure(text='Подсвечивать только ЭП')
    highlight_button = tkinter.Button(
        command_frame,
        text='Подсвечивать только ЭП',
        command=highlight
    )
    highlight_button.grid(row=0, column=2)

    def reset():
        gol_grid.reset()
        load_rules(gol_grid)
        grid.update()
    reset_button = tkinter.Button(
        command_frame,
        text='Сброс',
        command=reset
    )
    reset_button.grid(row=0, column=3)

    def set_speed(new_speed):
        global speed
        speed = int(new_speed)
    speed_scale = tkinter.Scale(
        command_frame,
        from_=SPEED_MIN,
        to=SPEED_MAX,
        orient=tkinter.HORIZONTAL,
        command=set_speed
    )
    speed_scale.grid(row=0, column=4, padx=20)

    def game_runner():
        root.after(1000 // speed, game_runner)
        if game_running:
            gol_grid.next_step()
            grid.update()
    game_runner()

    root.mainloop()


if __name__ == "__main__":
    main()
