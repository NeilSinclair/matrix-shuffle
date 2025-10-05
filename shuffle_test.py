"""Module which tests the shuffle"""
from matrix import Matrix, Node
import copy
from shuffle_matrix import swap_shuffle, training

def basic_test(): 
  matrix = Matrix(size=(3,3))
  matrix, score = swap_shuffle(matrix)
  print(f"Score: {score:.2f}")

def training_test():
  matrix = Matrix((5,5))
  matrix.display_matrix()
  matrix = training(matrix, copy.deepcopy(matrix), n_steps=50000, alpha=0.9999, T=1.0, debug_steps=1999)
  # print(matrix)
  matrix.display_matrix()

if __name__ == "__main__":
  training_test()
