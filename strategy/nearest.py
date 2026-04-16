def assign_tasks_nearest(vehicles, tasks, graph):
    assignments = [] 

    for task in tasks:
        if  task.completed or task.assigned:
            continue

        best_vehicle = None
        best_dist = float('inf')

        for v in vehicles:
            if v.status != "idle":
                continue

            dist = get_distance(graph, v.position, task.position)

            if dist < best_dist:
                best_dist = dist
                best_vehicle = v

        if best_vehicle:
            assignments.append((best_vehicle, task))


            best_vehicle.status = "busy"
            best_vehicle.task = task
            task.assigned = True

    return assignments