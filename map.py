"""
Base classes for OPAL
"""

from typing import Dict


class Cell(object):
    def __init__(self, x: int, y: int, cost: float, slope: float,
        fertility: float, composition: Dict[str, float]) -> None:
        """ Creates a new cell with given parameters

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
        return self.species.copy()
    
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
    

