"""
OPAL
Optimising Protected Areas (w)ith Love.

Optimises land selection to select the "best" areas of land to purchase on a budget
"""

from cells import *
from data_loader import *
from optimiser import Optimiser

if __name__ == "__main__":
    testcollection = csv_to_collection("testdata/test.csv")
    optim = Optimiser(testcollection, 1000, 100)
    best = optim.run(100)
    with open("testdata/out.txt", "w") as f:
        for cell in best.get_cells():
            f.write(f"({cell.get_x()}, {cell.get_y()})\n")
    
    print(len(optim.collection_scores))