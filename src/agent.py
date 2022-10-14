class agent:
    def __init__(self, start_pos) -> None:
        agent.pos = start_pos

    def get_pos(self):
        return agent.pos

    def change_pos(self, new_pos):
        agent.pos = new_pos
