def aliveness_rule(overpopulating, underpopulating, born, from_step=0):
    def rule(cell):
        if cell.grid.current_step >= from_step:
            alive_neighbors = len([n for n in cell.neighbors if n.is_alive])
            if cell.is_alive:
                if underpopulating < alive_neighbors < overpopulating:
                    return True
            else:
                if alive_neighbors == born:
                    return True
            return False
        return cell.is_alive_in_next_step
    return rule


def dead_rule(from_step):
    def rule(cell):
        if cell.grid.current_step >= from_step:
            return False
        return cell.is_alive_in_next_step
    return rule
