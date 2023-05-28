import json
import pathlib
import tkinter
from time import sleep

import game_of_life
import rules

SPEED_MIN = 1
SPEED_MAX = 10
GRID_HEIGHT = GRID_WIDTH = 5


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
    grid = gui.Grid(root, gol_grid)
    grid.update()

    command_frame = tkinter.Frame(root, borderwidth=10)
    command_frame.pack(side=tkinter.TOP)

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

    speed_scale_frame = tkinter.Frame(root, borderwidth=10)
    speed_scale_frame.pack(side=tkinter.TOP)

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
        speed_scale_frame,
        from_=SPEED_MIN,
        to=SPEED_MAX,
        orient=tkinter.HORIZONTAL,
        command=set_speed
    )
    speed_scale.grid(row=0, column=0)

    def game_runner():
        root.after(1000 // speed, game_runner)
        if game_running:
            gol_grid.next_step()
            grid.update()
    game_runner()

    root.mainloop()


if __name__ == "__main__":
    main()
