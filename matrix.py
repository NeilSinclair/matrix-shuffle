"""Script for shuffling a matrix"""
from __future__ import annotations
import numpy as np
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class Node:
  def __init__(self, coordinates: tuple, connections: list[Node] | None = None, id: int | None = None):
    self.connections: list[Node] = [] if connections is None else list(connections)
    self.coordinates = coordinates
    self.id = id

  def add_connection(self, other: Node) -> None:
    if other is self:
      return
    if other not in self.connections:
      self.connections.append(other)

  def __repr__(self):
    neighbours = [n.coordinates for n in self.connections]
    return f"Node(pos={self.coordinates}, deg={len(self.connections)}, neighbours={neighbours})"

class Matrix:
  def __init__(self, size: tuple[int, int]):
    self.nodes: list[Node] = []
    self.dimensions = list(size)
    self.matrix_map: dict[tuple, Node] = {}
    
    self.create_matrix()

  def create_matrix(self):
    c = 0
    for i in range(self.dimensions[0]):
      for j in range(self.dimensions[1]):
        c+=1
        self.add_node(Node(connections=[], coordinates=(i, j), id=c))

    self.insert_connections()

  def add_node(self, node: Node):
    self.nodes.append(node) 
    self.matrix_map[node.coordinates] = node

    # Keep track of the size of the matrix; matrix coordinatess are 0-based
    self.dimensions[0] = max(node.coordinates[0] + 1, self.dimensions[0])
    self.dimensions[1] = max(node.coordinates[1] + 1, self.dimensions[1])

  def __repr__(self):
    return f"{self.dimensions[0]} x {self.dimensions[1]} Matrix\n{self.nodes}"
  
  def display_matrix(self):
    arr = np.zeros((self.dimensions[0], self.dimensions[1]))
    for (i,j), node in self.matrix_map.items():
      arr[i,j] = node.id
    
    print(arr)
      

  def insert_connections(self, node: Node | None = None) -> None:
    """Funciton which adds in all of the connections to a Node.
    
    Logic: Add all of the other nodes which are a distance of 1 - up down or diagonally - away from a specific node. Nodes cannot be
    connected to another nodes with which are in a coordinatesc i,j < 0 or i, j > m,n 
    
    Args: 
      node (Node | None): node to update; updates all nodes if None

    Returns:
      The matrix with the connections added to the nodes
    """
    # Matrix for calculating shifted coordinates
    shift_matrix = np.array([
          (-1,1),  (0,1),  (1,1),
          (-1,0),          (1,0),
          (-1,-1), (0,-1), (1,-1)
        ], dtype=int
      )

    m,n = self.dimensions

    if node is None:
      mapped_nodes = self.matrix_map.items()
    else:
      mapped_nodes = zip((node.coordinates), node)

    for (i,j), node in mapped_nodes:
      neighbours = shift_matrix + np.array([i,j])

      mask = (
        (neighbours[:, 0] >= 0) & (neighbours[:, 0] < m) &
        (neighbours[:, 1] >= 0) & (neighbours[:, 1] < n)
      )
      
      for x, y in neighbours[mask]:
        other = self.matrix_map.get((x, y)) 
        if other is None:
            continue
        node.add_connection(other)
        other.add_connection(node)

  def clear_connections(self):
    for (i,j), node in self.matrix_map.items():
      node.connections = []
   

