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
    optim = Optimiser(testcollection, 501, 100, 10000)
    best = optim.run(10)
    for cell in best.get_cells():
        print(f"{cell.get_x()}, {cell.get_y()}")