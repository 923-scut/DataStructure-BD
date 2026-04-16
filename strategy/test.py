from strategy.nearest import assign_tasks_nearest

class V:
    def __init__(self, id, pos):
        self.id = id
        self.position = pos
        self.status = "idle"
        self.task = None

class T:
    def __init__(self, id, loc):
        self.id = id
        self.location = loc
        self.completed = False
        self.assigned = False


vehicles = [V(1, 0), V(2, 10)]
tasks = [T(1, 2), T(2, 9)]

res = assign_tasks_nearest(vehicles, tasks, None)

for v, t in res:
    print(v.id, "->", t.id)