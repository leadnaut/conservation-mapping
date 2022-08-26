"""
Base classes for Untitled Conservation Tool
"""

from typing import Dict


class Cell(object):
    def __init__(self, x: int, y: int, species: Dict[str, float]) -> None:
        self.x = x
        self.y = y
        self.species = Dict
    
    def getX(self) -> int:
        """ Get the cell's x-coordinate
        
        Returns:
            (int): This cell's x-coordinate
        """
        return self.x
    
    def getY(self) -> int:
        """ Get the cell's y-coordinate
        
        Returns:
            (int): This cell's y-coordinate
        """
        return self.y
    
    def getSpecies(self) -> Dict[str, float]:
        """ Get a shallow copy of the cell's species population dictionary
        
        Returns:
            (Dict[str, int]): This cell's species population dictionary
        """
        return self.species.copy()
    
    def getSpeciesAmount(self, species: str) -> float:
        """ Get the current population of a particular species in the cell 
        
        Parameters:
            species (str): the species to get amount of
        Returns:
            (float): The current population of the species parameter in this 
            cell
        Raises:
            KeyError: if specified species not in dictionary
        """
        return self.getSpecies[species]
    

