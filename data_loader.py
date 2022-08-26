"""
Data loading functionality for OPAL.
"""

from cells import *
import csv

def csv_to_collection(filepath: str) -> CellCollection:
    """Reads a csv file and converts it to a CellCollection
    
    Parameters:
        filepath (str): location of csv file to convert
        species_name (List[str]): list of species names

    Returns:
        (CellCollection): CellCollection containing all the cells in csv file
        """
    collection = CellCollection()
    with open(filepath, "r", newline="") as csvfile:
        species_names = []
        fileiter = csv.DictReader(csvfile)
        #get species names from fieldnames
        for fname in fileiter.fieldnames:
            if fname not in ["x", "y", "cost", "slope", "fertility"]:
                species_names.append(fname)

        for row in fileiter:
            #make composition dictionary
            composition = {name: float(row[name]) for name in species_names}
            #add the cell!
            collection.add_cell(Cell(int(row["x"]), int(row["y"]),
                                     float(row["cost"]), float(row["slope"]),
                                     float(row["fertility"]), composition))
    
    return collection
