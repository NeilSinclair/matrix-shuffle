"""Module that shuffles and scores a move"""
import random 
import itertools
from matrix import Matrix, Node


def swap_shuffle(matrix: Matrix) -> tuple[Matrix, float]:
  """Function which shuffles a matrix and returns a new one.
  
  Logic: randomly selects 2 nodes in the matrix and swaps them.
  """
  old_matrix = matrix
  m,n = matrix.dimensions
  coords = list(itertools.product(range(m), range(n)))
  p1, p2 = random.sample(coords, k=2)

  node1_old = matrix.matrix_map[p1]
  node2_old = matrix.matrix_map[p2]

  matrix.matrix_map[p1] = matrix.matrix_map[p2]
  matrix.matrix_map[p2] = node1_old

  # TODO: this should really just do this for the nodes being swapped
  matrix.clear_connections()
  matrix.insert_connections()

  score1 = score_node(node1_old, matrix.matrix_map[p1])
  score2 = score_node(node2_old, matrix.matrix_map[p2])

  score = (score1 + score2) / 2

  return matrix, score


def score_node(old_node: Node, new_node: Node) -> float:
  """Function which returns the score for shuffling a Node.
  
  Logic: return the proportion of connections from the old_node that are still in the new node. For example
  if the connections are: old_node = [A,B,C] and new_node = [C,D,E] then the score should be 
  1 / len(new_node.connections)

  Args:
    old_node (Node): the node before it was moved
    new_node (Node): the node after it was moved

  Returns:
    float: the overlap score

  """
  old_node_connections = set([n.coordinates for n in old_node.connections])
  new_node_connections = set([n.coordinates for n in new_node.connections])

  # print(f"------\nold_node_connections: {old_node_connections}")
  # print(f"new_node_connections: {new_node_connections}")
  # print(f"intersection: {old_node_connections.intersection(new_node_connections)}\n------")

  score = len(old_node_connections.intersection(new_node_connections)) / len(new_node_connections)

  return score

def score_matrix(old_matrix: Matrix, new_matrix: Matrix) -> float:
  """Function that scores the overall change in the overlap based on move of n-points"""
  score = 0
  for (i,j), node in old_matrix.matrix_map.items():
    score += score_node(node, new_matrix.matrix_map[(i,j)])

  return score / (old_matrix.dimensions[0] * old_matrix.dimensions[1])

def training(matrix: Matrix, n_steps: int, p_explore: float, threshold: float=0.5, debug: bool=False) -> None:
  """Function which makes the swaps and calculates the score.
  
  If the score from a swap leads to a decrease below a threshold, this move will be kept with p_explore
  """
  old_matrix = matrix
  for i in range(n_steps):
    new_matrix, score = swap_shuffle(old_matrix)
    # If the score benefit is less than we want (i.e. too many overlaps), we only update the matrix based on a random factor
    if score > threshold:
      if random.uniform(0, 1) < p_explore:
        old_matrix = new_matrix
    # If the score is less than the threshold (i.e. good), we update the matrix
    else:
      old_matrix = new_matrix
    
    print(f"Score on iteration {i+1} = {score:.2f}")

