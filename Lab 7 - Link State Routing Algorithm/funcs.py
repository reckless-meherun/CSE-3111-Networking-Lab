import addresses
import socket
import json
import heapq
import graph

def broadcast(message:bytes,neighbors: list[str]):
    for neighbor in neighbors:
        addr = addresses.address[neighbor]
        client_sock = socket.socket()
        try:
            client_sock.connect(addr)
            client_sock.send(message)
        except:
            print(f'Message failed to be sent to {neighbor}')


def encode_message(router_id:str,serial:int,adj:dict[str,dict[str,int]]) -> bytes:
    return f'{router_id}{serial}@{json.dumps(adj)}'.encode()

def decode_message(message:bytes,received_messages:set[str]):
    data = message.decode()
    id,data = data.split('@')

    
    # received_messages.add(id)
    return id,json.loads(data)


def handle_client(client_sock:socket.socket,addr,adj,messages_received,source,neighbors):
    packet = client_sock.recv(1024)
    id,data = decode_message(packet,messages_received)
    if data:
        for src,links in data.items():
            if src not in adj.keys():
                adj[src]={}
            for dest,weight in links.items():
                if dest not in adj.keys():
                    adj[dest]={}
                adj[src][dest]=weight
                adj[dest][src]=weight
    print(adj)
    if id not in messages_received:
        messages_received.add(id)
        broadcast(packet,neighbors)
    distances,parents = dijkstra(adj,source)
    print_all_shortest_paths(distances,parents,source)




def dijkstra(graph, start):
    # Initialize the distance dictionary with infinite distances for all nodes except the start node
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0

    # Initialize the parents dictionary
    parents = {node: None for node in graph}

    # Priority queue for the nodes to visit
    queue = [(0, start)]

    while queue:
        # Get the node with the smallest distance
        current_distance, current_node = heapq.heappop(queue)

        # If the current distance is greater than the stored distance, skip
        if current_distance > distances[current_node]:
            continue

        # Check all the neighbors
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            # If the distance is less than the currently stored distance, update the distance and add the node to the queue
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                parents[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    return distances, parents

def shortest_path(parents, start, target):
    path = [target]
    while path[-1] != start:
        path.append(parents[path[-1]])
    path.reverse()
    return path

def print_all_shortest_paths(distances, parents, start):
    for target in distances:
        path = shortest_path(parents, start, target)
        print(f"Shortest path from {start} to {target}: {path} with distance {distances[target]}")
    

def get_adj(router_id):
    if router_id in graph.adj.keys():
        return {
            router_id: graph.adj[router_id]
        }
    return None

