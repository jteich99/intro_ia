from aima_libs.hanoi_states import ProblemHanoi, StatesHanoi
from aima_libs.tree_hanoi import NodeHanoi

def search_algorithm(number_disks=5) -> (NodeHanoi, dict):

    # Edite esta linea para que la list_disk use a number_disks y no quede clavado en 5
    list_disks = [i for i in range(number_disks, 0, -1)]
    initial_state = StatesHanoi(list_disks, [], [], max_disks=number_disks)
    goal_state = StatesHanoi([], [], list_disks, max_disks=number_disks)
    problem = ProblemHanoi(initial=initial_state, goal=goal_state)

    ##### EDITAR ESTA ZONA
    # Inicializamos las salidas, pero reemplazar con lo que se quiera usar.
    metrics = {
        "solution_found": False,
        "nodes_explored": None,
        "states_visited": None,
        "nodes_in_frontier": None,
        "max_depth": None,
        "cost_total": None,
        "nodes_repeated": None,
    }
    # Heuristic function 
    def heuristicFunction(node: NodeHanoi):
        value = node.path_cost
        # List to find the location of each disk
        locations = []
        stateList = node.state.get_state()
        for i in range(1,number_disks+1):
            if i in stateList[0]:
                locations.append(1)
            elif i in stateList[1]:
                locations.append(2)
            elif i in stateList[2]:
                locations.append(3)

        rodBiggestDisk = 0
        for i in range(number_disks, 0, -1):
            # Go through disks and substract from heuristic if the biggests disks are in the correct location
            criteria1 = False
            if locations[i - 1] != 3:
                criteria1 = True 
            elif criteria1:
                value -= 6 - i
                
            # Find the biggest disk out of place, and add to the heuristic all the disks in that rod
            if locations[i - 1] != 3:
                rodBiggestDisk = locations[i - 1]
                value += i
                continue
            if locations[i - 1] == rodBiggestDisk:
                value += i

        return value
    
    from queue import PriorityQueue
    frontier = PriorityQueue()
    visitedStates = [initial_state]
    root = NodeHanoi(state=initial_state)
    frontier.put((0,root))

    # Search loop
    nodesExplored = 0
    nodesRepeated = 0
    statesVisited = 1
    while not metrics["solution_found"]:
        # Expand the first node in the priority
        _, nodeToExpand = frontier.get()
        newNodes = nodeToExpand.expand(problem)
        # Consider this state visisted since it has been expanded and its children will be analyzed
        visitedStates.append(nodeToExpand.state)
        nodesExplored+= 1

        for newNode in newNodes:
            statesVisited += 1 # Since the state is checked it is considered visited
            # Enter the nodes that have a state not yet visited only
            if newNode.state not in visitedStates:
                # Test if solution
                if problem.goal_test(newNode.state):
                    solution = newNode
                    # print(f"Found solution! Path is:")
                    # for nodes in solution.path():
                    #     print(nodes.state)

                    metrics["solution_found"] = True
                    metrics["nodes_explored"] = nodesExplored
                    metrics["states_visited"] = statesVisited
                    metrics["nodes_in_frontier"] = len(frontier.queue)
                    metrics["max_depth"] = max([state.path_cost for _, state in frontier.queue])
                    metrics["cost_total"] = newNode.path_cost
                    metrics["nodes_repeated"] = nodesRepeated
                
                # If not solution: calculate heuristic function and add to frontier
                newNodePriority = heuristicFunction(newNode) 
                frontier.put((newNodePriority, newNode))
            else:
                nodesRepeated += 1
    # TODO: Completar con el algoritmo de búsqueda que desees implementar
    #####

    return solution, metrics

import time
from matplotlib import pyplot as plt

elapsedTimes = []
disksRange = range(3, 15, 1)
for i in disksRange:
    start_time = time.time()  # Record the start time
    # Your code block to be timed
    solution, metrics = search_algorithm(number_disks=i)
    end_time = time.time()    # Record the end time
    print(solution, metrics)

    elapsed_time = end_time - start_time
    elapsedTimes.append(elapsed_time)
    print(f"Elapsed time: {elapsed_time:.4f} seconds for {i} disks") 

plt.plot(disksRange, elapsedTimes, marker="x")
plt.xlabel("Cantidad de discos")
plt.ylabel("Tiempo de cómputo [s]")
plt.xticks(disksRange)
plt.xlim([min(disksRange), max(disksRange)])
plt.grid(which='major')
plt.yscale('log')
plt.savefig("searchAlgorithm.png")
