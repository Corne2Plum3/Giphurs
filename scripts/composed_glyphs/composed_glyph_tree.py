from composed_glyphs.composed_glyph import Composed_Glyph
from logger import configure_logging
import sys

sys.path.append('..')

logger = configure_logging()

class Composed_Glyph_Tree():
    def __init__(self, glyph_name: str, children: list['Composed_Glyph_Tree']):
        self.glyph_name = glyph_name
        self.children = children

    def __repr__(self) -> str:
        output: str = f'(\'{self.glyph_name}\', ['
        for i, child in enumerate(self.children):
            if i > 0:
                output += ', '
            output += child.__repr__()
        output += '])'
        return output

    def __str__(self) -> str:
        return self.__repr__()

    def print(self):
        '''Show ASCII schema of the tree on the terminal.'''

        def _print_loop(node: Composed_Glyph_Tree, prefix: str = "", is_last: bool = True):
            # 1. Print the current node with its appropriate connector
            if prefix == "":
                # Root node doesn't need a connector
                print(node.glyph_name)
            else:
                connector = "└── " if is_last else "├── "
                print(f"{prefix}{connector}{node.glyph_name}")
            
            # 2. Update the prefix for the children
            # If this node is the last child of its parent, its vertical line ends here ("    ")
            # Otherwise, the vertical line continues down ("│   ")
            new_prefix = prefix + ("    " if is_last else "│   ")
            
            # 3. Recursively print all children
            child_count = len(node.children)
            for i, child in enumerate(node.children):
                is_child_last = (i == child_count - 1)
                _print_loop(child, new_prefix, is_child_last)

        _print_loop(self)

# === INTERNAL FUNCTIONS ===

def is_composed(name: str, cg_list: list[Composed_Glyph]) -> bool:
    '''Check if the glyph is made of other glyphs.'''
    return name in [cg.name for cg in cg_list]

def get_children_from_name(name: str, cg_list: list[Composed_Glyph]) -> list[str]:
    '''Returns the list of glyphs to build the glyph with the given name.'''
    for cg in cg_list:
        if cg.name == name:
            return cg.glyphs
    return []

def get_tree_parents(glyph_name: str, tree: Composed_Glyph_Tree) -> list[str]:
    '''Returns a list of parents of the glyph with the given name. Last element is the glyph itself. Returns empty list if not found.'''
    if tree.glyph_name == glyph_name:
        return [glyph_name]
    
    for child in tree.children:
        child_path = get_tree_parents(glyph_name, child)
        if child_path:
            return [tree.glyph_name] + child_path
            
    return []

def get_subtree(name: str, tree: Composed_Glyph_Tree) -> Composed_Glyph_Tree | None:
    if name == tree.glyph_name:
        return tree
    for child in tree.children:
        subtree = get_subtree(name, child)
        if subtree is not None:
            return subtree
    return None

def build_tree_from_glyph(name: str, cg_list: list[Composed_Glyph], path: list[str] = []) -> Composed_Glyph_Tree | None:
    '''Build glyph tree for a single glyph. Returns None if an error was detected.'''
    if name in get_children_from_name(name, cg_list):  # Self-reference check
        logger.error(f'Failed to get dependencies of "{name}": the glyph is composed of itself.')
        return None

    if name in path:  # Circular reference check using the current path trace
        # Extract the loop portion from the path for the error message
        cycle_start_idx = path.index(name)
        cycle_path = path[cycle_start_idx:] + [name]

        error_msg = f'Failed to get dependencies of "{name}" circular reference '
        error_msg += " -> ".join(f'"{p}"' for p in cycle_path)
        logger.error(error_msg)
        return None

    if not is_composed(name, cg_list):  # Leaf node (base case)
        return Composed_Glyph_Tree(name, [])

    # Recursive step
    name_tree = Composed_Glyph_Tree(name, [])
    extended_path = path + [name]   # Add current node to the path before diving into children
    for child in get_children_from_name(name, cg_list):
        # Pass the extended path down to children
        subtree = build_tree_from_glyph(child, cg_list, extended_path)
        if subtree is None:  
            return None  # Propagate failure upwards
        name_tree.children.append(subtree)

    return name_tree

def build_tree_from_list(cg_list: list[Composed_Glyph]) -> Composed_Glyph_Tree | None:
    """
    Takes a list of Composed_Glyph objects and structures them into a Composed_Glyph_Tree.
    Ensures every Composed_Glyph definition is instantiated exactly once as a parent node.
    """
    # 1. Map each composed glyph name to its object for quick lookup
    cg_map: dict[str, Composed_Glyph] = {cg.name: cg for cg in cg_list}
    
    # 2. Track which composed glyphs have already been processed into the tree
    processed_composed: set[str] = set()

    def build_node(name: str, path: list[str]) -> Composed_Glyph_Tree | None:
        # Check self-reference
        if name in get_children_from_name(name, cg_list):
            logger.error(f'Failed to get dependencies of "{name}": the glyph is composed of itself.')
            return None

        # Check circular dependency using the path trace
        if name in path:
            cycle_start_idx = path.index(name)
            cycle_path = path[cycle_start_idx:] + [name]
            error_msg = f'Failed to get dependencies of "{name}" circular reference '
            error_msg += " -> ".join(f'"{p}"' for p in cycle_path)
            logger.error(error_msg)
            return None

        # Base case: If it's a leaf node (not a composed glyph definition)
        if name not in cg_map:
            return Composed_Glyph_Tree(name, [])

        # If it is a composed glyph but we already generated its definitive structural node,
        # treat it as a leaf reference here to avoid duplicating the sub-graph elements.
        if name in processed_composed:
            return Composed_Glyph_Tree(name, [])

        # Mark this composed glyph as processed
        processed_composed.add(name)

        # Recursive step for new structural nodes
        node = Composed_Glyph_Tree(name, [])
        extended_path = path + [name]
        
        for child_name in cg_map[name].glyphs:
            subtree = build_node(child_name, extended_path)
            if subtree is None:
                return None  # Propagate error upward
            node.children.append(subtree)

        return node

    # Create the top-level master root container
    root_tree: Composed_Glyph_Tree = Composed_Glyph_Tree("", [])

    # 3. First pass: Find natural root nodes (glyphs not used as components inside any other glyph)
    all_components: set[str] = set(child for cg in cg_list for child in cg.glyphs)
    natural_roots: list[str] = [cg.name for cg in cg_list if cg.name not in all_components]

    # Process natural roots first
    for root_name in natural_roots:
        subtree = build_node(root_name, [])
        if subtree:
            root_tree.children.append(subtree)

    # 4. Second pass: Pick up any orphaned loops or disconnected components 
    # ensuring every Composed_Glyph in cg_list appears exactly once in the tree structure.
    for cg in cg_list:
        if cg.name not in processed_composed:
            subtree = build_node(cg.name, [])
            if subtree:
                root_tree.children.append(subtree)

    return root_tree

def set_glyph_priorities_from_list(cg_list: list[Composed_Glyph]) -> list[Composed_Glyph]:
    '''
        Compute the priority attributes of a list of composed glyph by building a tree.
        Higher priority value should be built first. Lowest priority is 1.

        Every `Composed_Glyphs` should have an unique glyph name (NOTE: this function doesn't check this).
    
        Returns a NEW list if success ; returns empty list if there's an issue with the tree.
    '''

    new_cg_list: list[Composed_Glyph] = cg_list.copy()
    for i, _ in enumerate(new_cg_list):
        new_cg_list[i].priority = 0

    cg_map: dict[str, int] = {cg.name: i for i, cg in enumerate(new_cg_list)}  # name -> index in new_cg_list 

    # Get tree
    cg_tree: Composed_Glyph_Tree | None = build_tree_from_list(new_cg_list)
    if cg_tree is None:
        return []
    
    # Set priorities attributes
    def _read_node(tree: Composed_Glyph_Tree, depth: int = 0) -> None:
        if tree.glyph_name != '' and tree.glyph_name in cg_map.keys():
            new_cg_list[cg_map[tree.glyph_name]].priority = max(new_cg_list[cg_map[tree.glyph_name]].priority, depth)
        for child in tree.children:
            _read_node(child, depth + 1)

    _read_node(cg_tree)
    
    # Sort by priority
    new_cg_list.sort(key=lambda cg: cg.priority, reverse=True)
    logger.debug(f'Build order and priority: {[(cg.name, cg.priority) for cg in new_cg_list]}')
    return new_cg_list
