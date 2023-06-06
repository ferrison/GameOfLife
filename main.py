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


def map_booleans(value):
    if not isinstance(value, dict):
        if value=='True':
            return True
        if value=='False':
            return False
        return value
    res = {}
    for k, v in value.items():
        res[map_booleans(k)] = map_booleans(v)
    return res


def load_config():
    import gui
    config = json.loads(pathlib.Path('config.json').read_text())
    for k, v in config.items():
        setattr(gui.Cell, map_booleans(k), map_booleans(v))


def main():
    root = tkinter.Tk()
    root.geometry("1000x1000")
    root.title("Игра жизнь")

    game_running = False
    speed = SPEED_MIN

    gol_grid = game_of_life.Grid(GRID_HEIGHT, GRID_WIDTH)
    load_rules(gol_grid)

    import gui
    load_config()
    grid = gui.Grid(root, gol_grid)
    grid.update()

    command_frame = tkinter.Frame(root, borderwidth=10)
    command_frame.pack(side=tkinter.BOTTOM, fill=tkinter.X)

    step_label = tkinter.Label(command_frame, text="Текущий шаг: 0")
    step_label.grid(row=0, column=1, padx=20)

    def step():
        if not game_running:
            gol_grid.next_step()
            grid.update()
            step_label.configure(text=f"Текущий шаг: {gol_grid.current_step}")
    step_button = tkinter.Button(
        command_frame,
        text='Шаг',
        command=step
    )
    step_button.grid(row=0, column=2)

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
    continue_button.grid(row=0, column=3)

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
    highlight_button.grid(row=0, column=4)

    def reset():
        gol_grid.reset()
        load_rules(gol_grid)
        grid.update()
        step_label.configure(text=f"Текущий шаг: 0")
    reset_button = tkinter.Button(
        command_frame,
        text='Сброс',
        command=reset
    )
    reset_button.grid(row=0, column=5)

    def set_speed(new_speed):
        nonlocal speed
        speed = int(new_speed)
    speed_scale = tkinter.Scale(
        command_frame,
        from_=SPEED_MIN,
        to=SPEED_MAX,
        orient=tkinter.HORIZONTAL,
        command=set_speed
    )
    speed_scale.grid(row=0, column=6, padx=40)

    command_frame.columnconfigure(0, weight=1)
    command_frame.columnconfigure(7, weight=1)

    def game_runner():
        root.after(1000 // speed, game_runner)
        if game_running:
            gol_grid.next_step()
            grid.update()
            step_label.configure(text=f"Текущий шаг: {gol_grid.current_step}")
    game_runner()

    root.mainloop()


if __name__ == "__main__":
    main()
