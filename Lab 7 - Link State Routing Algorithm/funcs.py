import addresses
import socket
import json
import heapq
import graph
import time
import random

def broadcast(message:bytes,neighbors: list[str]):
    for neighbor in neighbors:
        addr = addresses.address[neighbor]
        client_sock = socket.socket()
        try:
            client_sock.connect(addr)
            client_sock.send(message)
        except:
            print(f'Message failed to be sent to {neighbor}')


def encode_message(router_id:str,serial:int,adj:dict[str,dict[str,int]],ttl=32) -> bytes:
    return json.dumps({
        'id':f'{router_id}{serial}',
        'ttl':ttl,
        'data':adj

    }).encode()

def decode_message(message:bytes):
    data = message.decode()

    # received_messages.add(id)
    return json.loads(data)


def handle_client(client_sock:socket.socket,adj,messages_received,source,neighbors):
    packet = client_sock.recv(1024)
    packet = decode_message(packet)
    if packet:
        for src,links in packet['data'].items():
            if src not in adj.keys():
                adj[src]={}
            for dest,weight in links.items():
                if dest not in adj.keys():
                    adj[dest]={}
                adj[src][dest]=weight
                adj[dest][src]=weight
    print(adj)
    print(packet['ttl'])
    packet['ttl']-=1
    send_packet = encode_message(packet['id'][0],int(packet['id'][1:]),packet['data'],packet['ttl'])
    if packet['id'] not in messages_received and packet['ttl']>0:
        messages_received.add(packet['id'])
        broadcast(send_packet,neighbors)
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
            if distances.get(neighbor) and distance < distances[neighbor]:
                distances[neighbor] = distance
                parents[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    return distances, parents

def shortest_path(parents, start, target):
    path = [target]
    while parents.get(path[-1]) is not None and path[-1] != start:
        path.append(parents[path[-1]])
    path.reverse()
    return path

def print_all_shortest_paths(distances, parents, start):
    print('Printing shortest paths')
    print(graph.adj.keys())
    for target in graph.adj.keys():
        path = shortest_path(parents, start, target)
        print(f"Shortest path from {start} to {target}: {path} with distance {distances.get(target)}")
    

def get_adj(router_id):
    if router_id in graph.adj.keys():
        return {
            router_id: graph.adj[router_id]
        }
    return None


        
        

        