import math
from collections import deque
from queue import PriorityQueue
import heapq
from queue import heappush
from queue import heappop
city_coordinates = {
    'Manchester': [53.48, -2.25],
    'Liverpool': [53.41, -2.99],
    'York': [53.96, -1.08],
    'Carlisle': [54.89, -2.94],
    'Newcastle': [54.97, -1.61],
    'Glasgow': [55.86, -4.25],
    'Edinburgh': [55.95, -3.19],
    'Oban': [56.42, -5.47],
    'Aberdeen': [57.15, -2.09],
    'Holyhead': [53.31, -4.63],
    'Inverness': [57.48, -4.23],
}
distances = {
    'Manchester': {'Holyhead': 119.79, 'Liverpool': 34, 'York': 57.49 },
    'Holyhead': {'Manchester': 120.5, 'Carlisle': 223 },
    'Liverpool': {'Manchester': 34.29, 'Carlisle': 123.69, 'York': 101.15},
    'York': {'Manchester': 72.53, 'Liverpool': 102.19 , 'Newcastle': 119.13, 'Carlisle': 116.72},
    'Carlisle': {'Holyhead': 223.28, 'Liverpool': 123.89, 'York': 116.72, 'Newcastle': 157.33, 'Glasgow': 96.02},
    'Newcastle': {'York': 117.16, 'Carlisle': 157.73, 'Edinburgh': 256.14},
    'Glasgow': {'Carlisle': 96.24, 'Oban': 96.9 , 'Edinburgh': 46.8 },
    'Edinburgh': {'Newcastle': 249.48, 'Glasgow': 46, 'Oban': 121.75, 'Aberdeen': 120.82, 'Inverness': 157.39},
    'Oban': {'Glasgow': 96.48, 'Edinburgh': 122.62, 'Aberdeen': 173.76 },
    'Aberdeen': {'Edinburgh': 120.73, 'Oban': 174, 'Inverness': 104.28},
    'Inverness': {'Edinburgh': 157.58, 'Aberdeen': 104.3},
}
def euclidean_distance(coord1, coord2):
    return math.dist(coord1, coord2)
def astar(distances, start, end):
    # Create a priority queue for A*
    queue = PriorityQueue()
    
    # Set to keep track of visited cities
    visited = set()
    
    # Initialize the start city
    queue.put((0, start, [start]))
    
    while not queue.empty():
        # Dequeue a city and its path
        _, city, path = queue.get()
        
        # Check if the city has been visited before
        if city in visited:
            continue
        
        # Mark the city as visited
        visited.add(city)
        
        # Check if the current city is the end city
        if city == end:
            cost = sum(distances[path[i]][path[i+1]] for i in range(len(path)-1))

            return path, cost
        
        # Enqueue all unvisited cities adjacent to the current city
        for neighbor, cost in distances[city].items():
            if neighbor not in visited:
                # Calculate the heuristic cost to the neighbor city
                heuristic = math.dist(city_coordinates[neighbor], city_coordinates[end])
                total_cost = cost + heuristic
                
                # Add the neighbor city to the priority queue
                queue.put((total_cost, neighbor, path + [neighbor]))
    
    # No path exists between the start and end cities
    return None, None 


start = input("Enter start:")
end = input("Enter end point:")

# Validate the input
while start not in distances or end not in distances:
    print("Invalid input, please enter valid start and end points.")
    start = input("Enter start:")
    end = input("Enter end point:")
path, cost = astar(distances, start, end)

# Print the shortest path
if path:
    print("Path:", path)
    print("Total distance:", cost, 'miles')
else:
    print("No path exists between the start and end cities.")