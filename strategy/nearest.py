def assign_tasks_nearest(vehicles, tasks, graph):
    assignment = [] #任务列表

    for task in tasks:
        if  task.completed or tasked.assigned:
            continue

        best_vehicle = None
        best_dist = int('inf')

        for v in vehicles:
            if v.status != "idle":
                continue

            dist = get_distance(graph, v.position, task.position)

            if dist < best_dist:
                best_dist = dist
                best_vehicle = v

        if best_vehicle:
            assignment.append((best_vehicle, tas1))


            best_vehicle.status = "busy"
            best_vehicle.task = task
            task.assigned = True

    return assignment