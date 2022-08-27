""" 
Optimising Algorithm for OPAL
"""

from cells import *
import math
import multiprocessing as mp

MAX_PROCESSES = 0

class Optimiser(object):
    """
    Object that handles OPAL's optimisation algorithm
    """
    def __init__(self, all_cells: CellCollection, budget: float,
        frugality: float, adj_weights: float) -> None:
        self.ambient_collection = all_cells

        self.total_cost = 0
        self.total_opp_cost = 0
        for cell in all_cells.get_cells():
            self.total_cost += cell.get_cost()
            self.total_opp_cost += cell.get_opportunity_cost()

        #Eval Parameters
        self.budget = budget
        self.frugality = frugality
        self.adj_weights = adj_weights

        #caching variables below
        self.collection_scores = {}
    
    def evaluate_cell_collection(self, collection: CellCollection):
        """
        Evaluates a given cell collection according to this optimisers internal
        parameters
        """
        if self.collection_scores.get(collection, -1) != -1:
            return self.collection_scores.get(collection)
        
        composition_score = 0
        coll_adjacency = 0
        ambient_adjacency = 0
        total_cost = 0
        total_opp_cost = 0

        for cell in collection.get_cells():
            #get the product of the population levels -> encourages diversity
            product = 1
            for population in cell.get_composition().values():
                product *= population
            composition_score += product

            #get clumpedness level
            coll_adjacency += len(collection.get_adjacents(cell))
            ambient_adjacency += len(self.ambient_collection.get_adjacents(cell))

            total_cost += cell.get_cost()
            total_opp_cost += cell.get_opportunity_cost()

        cost_score = self.total_cost / self.budget
        opp_score = total_opp_cost / self.total_opp_cost
        adj_score = coll_adjacency / ambient_adjacency

        score = (composition_score + self.adj_weight * adj_score 
            - (self.frugality * (opp_score + cost_score)))
        self.collection_scores[collection] = score
        return score

    
                
