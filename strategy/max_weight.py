def assign_tasks_max_weight(vehicles, tasks, graph):
    assignment = [] 

    task_sorted = sorted(tasks, key = lambda t: t.weight, reverse = True)

    for task in task_sorted:
        if task.completed or task.assigned:
            continue

        for v in vehicles:
            if v.status == "idle":
                assignment.append((v, task))

            v.status = "busy"
            v.task = task
            task.assigned =True

            break 
    return assignment