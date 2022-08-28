""" 
Optimising Algorithm for OPAL
"""

from math import inf
import random as r
from cells import *
import multiprocessing as mp


class Optimiser(object):
    """
    Object that handles OPAL's optimisation algorithm
    """
    def __init__(self, all_cells: CellCollection, budget: float, adj_weight: float) -> None:
        """ Creates a new Optimiser with given parameters
        
        Parameters:
            all_cells (CellCollection): all the cells in this optimiser's space\
            budget (float): buying budget
            frugality (float): modifier to cost_score
            adj_weight (float): weight of clumpedness
        """
        self.ambient_collection = all_cells

        self.total_cost = 0
        self.max_comp_score = 0
        for cell in all_cells.get_cells():
            self.total_cost += cell.get_cost()
            prod = 1
            for pop in cell.get_composition().values():
                prod *= pop
            self.max_comp_score = prod if prod >= self.max_comp_score else self.max_comp_score

        #Eval Parameters
        self.budget = budget
        self.adj_weight = adj_weight

        #caching variables below
        self.collection_scores = {}
    
    def evaluate_cell_collection(self, collection: CellCollection) -> float:
        """
        Evaluates a given cell collection according to this optimisers internal
        parameters.

        collection (CellCollection): collection of cells to evaluate
        """
        if self.collection_scores.get(frozenset(collection.get_cells()), -1) != -1:
            return self.collection_scores.get(frozenset(collection.get_cells()))
        
        total_comps = {species : 0 for species in collection.get_cells()[0].get_composition().keys()}
        coll_adjacency = 0
        ambient_adjacency = 0
        total_cost = 0

        for cell in collection.get_cells():
            for species, population in cell.get_composition().items():
                total_comps[species] += population

            #get clumpedness level
            coll_adjacency += len(collection.get_adjacents(cell))
            ambient_adjacency += len(self.ambient_collection.get_adjacents(cell))

            total_cost += cell.get_cost()

        if total_cost > self.budget:
            return 0
        
        adj_score = coll_adjacency / ambient_adjacency

        composition_score = 1
        for pop in total_comps.values():
            composition_score *= pop

        score = (composition_score) + adj_score * self.adj_weight
        self.collection_scores[frozenset(collection.get_cells())] = score
        return score

    def run(self, gen_size: int) -> CellCollection:
        #create intitial generation (get random members until budget is reached)
        total_evals = 0

        current_gen_children = {}
        current_gen_members = []
        for i in range(gen_size):
            cost = 0
            member = CellCollection()
            while cost < self.budget:
                cell = r.choice(self.ambient_collection.get_cells())
                if not member.is_in(cell):
                    member.add_cell(cell)
                cost += cell.get_cost()
            current_gen_members.append(member)
        
        previous_gen_score = -inf
        current_gen_score = 0
        for member in current_gen_members:
            score = self.evaluate_cell_collection(member)
            total_evals += 1
            if score > current_gen_score:
                current_gen_score = score
        
        while current_gen_score > previous_gen_score:
            for member in current_gen_members:
                #generate children
                children = get_permutations(member, self.ambient_collection)
                best_child = member
                best_child_score = 0

                #evaluate each child
                for child in children:
                    score = self.evaluate_cell_collection(child)
                    total_evals += 1
                    if score > best_child_score:
                        best_child_score = score
                        best_child = child

                #build next_generation
                current_gen_children[member] = best_child
            
            #generation advancement
            current_gen_members = list(current_gen_children.values())
            previous_gen_score = current_gen_score
            current_gen_score = 0
            for member in current_gen_members:
                score = self.evaluate_cell_collection(member)
                total_evals += 1
                if score > current_gen_score:
                    current_gen_score = score
            
            print(total_evals)
        
        #return best of the best!
        best_score = 0
        best_member = None
        for member in current_gen_members:
            score = self.evaluate_cell_collection(member)
            score += 1
            if score > best_score:
                best_member = member
                best_score = score
        
        return best_member
