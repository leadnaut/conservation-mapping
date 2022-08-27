"""
Base classes for OPAL
"""

from itertools import permutations
from typing import Dict, List


class Cell(object):
    """ Represents a land cell in the simulation."""
    def __init__(self, x: int, y: int, cost: float, slope: float,
        fertility: float, composition: Dict[str, float]) -> None:
        """ Creates a new cell with given parameters.

        Parameters:
            x (int): x co-ordinate of cell
            y (int): y co-ordinate of the cell
            cost (float): cost of the cell
            slope (float): slope of the cell (0 - 1)
            fertility (float): fertility of the cell (0 - 1)
            composition (Dict[str, float]): community composition of the cell
        
        Raises:
            ValueError if !(0 <= slope <= 1) || !(0 <= fertility <= 1)
        """
        self.x = x
        self.y = y
        self.cost = cost
        if not (0 <= slope <= 1) or  not (0 <= fertility <= 1):
            raise ValueError
        self.slope = slope
        self.fertility = fertility
        self.composition = composition
        self.opportunity_cost = 1 - max(slope, 1 - fertility)
    
    def get_x(self) -> int:
        """ Get the cell's x-coordinate
        
        Returns:
            (int): This cell's x-coordinate
        """
        return self.x
    
    def get_y(self) -> int:
        """ Get the cell's y-coordinate
        
        Returns:
            (int): This cell's y-coordinate
        """
        return self.y
    
    def get_cost(self) -> float:
        """ Gets the cost of the cell
        
        Returns:
            (float): This cell's cost
        """
        return self.cost
    
    def get_slope(self) -> float:
        """ Gets the slope of the cell
        
            Returns:
                (int): This cell's slope
        """
        return self.slope
    
    def get_fertility(self) -> float:
        """ Gets the fertility of the cell
        
            Returns:
                (int): This cell's fertility
        """
        return self.fertility
    
    def get_opportunity_cost(self) -> float:
        """ Gets the opportunity cost of the cell, this value is from 0 - 1 where
        1 represents a high opportunity cost and 0 represents no opportunity cost
        
        Returns:
            (float) this cell's opportunity cost
        """
        return self.opportunity_cost
    
    def get_composition(self) -> Dict[str, float]:
        """ Gets a shallow copy of the cell's community composition dictionary
        
        Returns:
            (Dict[str, int]): This cell's community composition dictionary
        """
        return self.composition.copy()
    
    def get_species_population(self, species: str) -> float:
        """ Get the current population of a particular species in the cell 
        
        Parameters:
            species (str): the species to get the population of
        Returns:
            (float): The current population of the species parameter in this cell
        Raises:
            KeyError: if specified species not in dictionary
        """
        return self.get_species[species]
    
class CellCollection(object):
    """ Represents a group of cells in the simulation. """
    def __init__(self, cells: List[Cell] = []) -> None:
        """ Create a new CellCollection with an optional list of starting cells.
        
        Parameters:
            cells (List[Cell]) (optional): starting cells
        """
        self.max_id = 0

        #Dictionary of cells and their ids
        self.cells = {}

        for cell in cells:
            self.add_cell(cell)
    
    def get_cells(self) -> List[Cell]:
        """ Get a list of the cells within the collection
        
        Returns:
            (List[Cell]): List of cells within this collection"""
        return list(self.cells.keys())
    
    def add_cell(self, cell : Cell) -> None:
        """ Adds a cell to the map
        
        Parameters:
            cell (Cell): cell to be added
        
        Raises:
            ValueError: if cell at the same (x, y) coordinates already in collection
        """
        for other_cell in self.get_cells():
            if (cell.get_x() == other_cell.get_x() and 
                cell.get_y() == other_cell.get_y()):
                raise ValueError
        else:
            self.cells[cell] = self.max_id
            self.max_id += 1
    
    def get_adjacents(self, cell: Cell) -> List[Cell]:
        """Get the cells within the collection adjacent to a given cell.
        
        Parameters:
            cell (Cell): cell to find adjacents of
        
        Returns:
            (List[Cell]): list of cells within this collection adjacent to given cell.
        """

        adjacents = []
        for other_cell in self.get_cells():
            if ((other_cell.get_x() == cell.get_x() and
                abs(other_cell.get_y() - cell.get_y()) == 1) or 
                (other_cell.get_y() == cell.get_y() and
                abs(other_cell.get_x() - cell.get_x()) == 1)):

                adjacents.append(other_cell)

        return adjacents
    
    def is_in(self, cell : Cell) -> bool:
        """ Checks if a cell is in the collection 
        
        Parameters:
            cell (Cell): cell to be checked whether in collection
        
        Returns:
            (bool): true if cell in collection false otherwise
        """
        return self.cells.get(cell, -1) != -1


def get_permutations(collection: CellCollection,
    ambient_collection: CellCollection) -> List[CellCollection]:
    """
    Gets all small permutations of a given collection, given an ambient
    collection. A permutation is defined as a collection where one element is
    removed OR one element is added OR one element is replaced.
    
    Parameters:
        collection (CellCollection): collection to permutate
        ambient_collection (CellCollection): ambient collection to add new elements
        from
    
    Returns:
        List[CellCollection]: list of permutations
    """
    removals = []
    for cell in collection.get_cells():
        removals.append(CellCollection(collection.get_cells().remove(cell)))

    substitutions = []
    for removal in removals:
        for cell in ambient_collection.get_cells():
            substitutions.append(CellCollection(removal.get_cells().append(cell)))
    
    additions = []
    for cell in ambient_collection.get_cells():
        additions.append(CellCollection(collection.get_cells().append(cell)))
    
    return removals + substitutions + additions