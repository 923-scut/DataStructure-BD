from .nearest import assign_tasks_nearest
from .max_weight import assign_tasks_max_weight


def assign_tasks(vehicles, tasks, graph, strategy="nearest"):

    if strategy == "nearest":
        return assign_tasks_nearest(vehicles, tasks, graph)

    elif strategy == "max_weight":
        return assign_tasks_max_weight(vehicles, tasks, graph)

    else:
        raise ValueError("Unknown strategy")