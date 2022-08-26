"""
OPAL
Optimising Protected Areas (w)ith Love.

Optimises land selection to select the "best" areas of land to purchase on a budget
"""

from cells import *
from data_loader import *

if __name__ == "__main__":
    testcollection = csv_to_collection("testdata/test.csv")
    for cell in testcollection.get_adjacents(testcollection.get_cells()[12]):
        print(cell.get_x(), cell.get_y(), cell.get_composition())