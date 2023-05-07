#### I've done the extra credit ####

from typing import Dict
from typing import List
from typing import Optional

import rubik

# ---------------------------------------------------------------------------------------------------------
# My problem is set up with a list used as a queue containing tuples composed of a position and a list of strings representing all permutations leading it for each node
    # a node is visited when popped from the front of the queue

# Maintainance at each iteration the number of nodes left to visit decrements, and the length of our paths get closer to the maximum length possible (14 perms)

## at every depth visited we have all the possible paths (list of permutations) of length equal to that depth

# The 2-ways BFS terminates when there is a common node visited by both tree or when all nodes of our trees of height 7 are visited on each tree and the path length exceeds 14

## For every common node there is a valid path from the start configuration to the end configuration with a length equal to the total height of both threes combined
    ## by which we can reach the end configuration from the start configuration and vise-versa  
# ---------------------------------------------------------------------------------------------------------

def shortest_path(start: rubik.Position, end: rubik.Position) -> Optional[List[rubik.Permutation]]:
    """
    Using 2-way BFS, finds the shortest path from start to end.
    Returns a list of Permutations representing that shortest path.
    If there is no path to be found, return None instead of a list.
    """
    if start == end: return []

    start_queue: list[tuple[rubik.Position, list]] = [ ( (start), [] ) ]
    end_queue: list[tuple[rubik.Position, list]] = [ ( (end), [] ) ]

    counter_twists: Dict[str, str] = {'F': 'Fi', 'L': 'Li', 'U': 'Ui', 'Fi': 'F', 'Li': 'L', 'Ui': 'U'}
    visited = 0
    leaves = [1, 7, 37, 187, 937, 4687, 23437]
    epopped = []
    spopped = []
    str_to_perm = { value: key for key, value in rubik.quarter_twists_names.items() }

    while visited < 23437:
        visit_node_append_children(start_queue, end_queue, spopped, epopped, counter_twists)
        visited += 1
        
        if visited != leaves[0]: continue 
        else: leaves.pop(0)

        start_tree_leaves: Dict[rubik.Position, list[str]] = dict(start_queue + spopped)
        end_tree_nodes: Dict[rubik.Position, list[str]] = dict(end_queue + epopped)
        
        common_positions = list(set(start_tree_leaves.keys()) & set(end_tree_nodes.keys()))

        if not common_positions: continue
        return compare_valid_paths(str_to_perm, common_positions, start_tree_leaves, end_tree_nodes)
        
    return None

def compare_valid_paths(str_to_perm: dict[str, rubik.Permutation], common_positions: list[rubik.Position], start_tree_leaves, end_tree_nodes):
    """
    takes a list of common positions and compare their path lengths
    return the shortest path
    """
    short_path = common_positions[0]

    for pos in common_positions:
        path_perms = list(map(str_to_perm.get, start_tree_leaves[pos] + end_tree_nodes[pos]))
        if len(path_perms) < len(short_path): 
            short_path = path_perms

    return short_path

def visit_node_append_children(start_queue: list[tuple[rubik.Position, list]], end_queue: list[tuple[rubik.Position, list]], spopped, epopped, counter_twists):
    """
    visit a node on each tree and append its children to its respective queue
    """
    snode = start_queue.pop(0)
    enode = end_queue.pop(0)
    epopped.append(enode)
    spopped.append(snode)
    for move in rubik.quarter_twists:
        mv_str = rubik.quarter_twists_names[move]

        if snode[1]:
            if snode[1][-1] == counter_twists[mv_str]: continue

        spos = rubik.perm_apply(move, snode[0])
        epos = rubik.perm_apply(move, enode[0])
        
        start_queue.append( (spos, snode[1] + [mv_str]) )
        end_queue.append( (epos, [counter_twists[mv_str]] + enode[1]) )
    
# O(|E|+ |V|) with |V| and |E| is the total cardinality of set of vertices and edges respectively of both threes combined. E = Estart + Eend  V = Vstart + Vend
# The closer the common position between our trees is to our start and end possitions the quicker the running time is. So the shortest the path is between start and end the quicker the algorithm is