import numpy as np

class Trie:
    _print_words_only = True
    
    def __init__(self, label: str):
        self.label = label
        self.children = {}
        self.endNode = False
        
    def insert(self, new: str) -> None:
        """
        Recursively create a Trie (Prefix Tree) from a given string
        
        1: create/move to new child with same prefix as current word/substring
        2: assign remaining string minus prefix to new child, with key as the prefix
        3: empty string = finished word
        """
    
        if not len(new):
            self.endNode = True
            return 
        
        if not new[0] in self.children.keys(): 
            child = Trie(self.label + new[0])
            self.children[new[0]] = child
            
        self.children[new[0]].insert(new[1:])

    def __str__(self):
        out = self.label if not self._print_words_only or self.endNode else ""
           
        for child in self.children.values():
            out += "\n" + str(child) # recursive str call
            
        return out.replace("\n\n", "\n") # needed for some unintended behaviour from the ternary statement and not worth properly fixing 
    
    def alphabetise(self) -> None: # reordeer to sort words by letter
        for child in self.children.values():
            child.alphabetise()
            
        self.children = dict(sorted(self.children.items(), key=lambda i: ord(i[0])))
        
    def search(self, term: str) -> bool: # searches for a string matching and ending at a prefix endnode
        if not isinstance(term, str):
            return False 
        
        if not len(term) and self.endNode:
            return True
        
        elif len(term):
            if term[0] in self.children.keys():
                return self.children[term[0]].search(term[1:])
            
        return False
    
    def child_exists(self, sequence: str) -> bool: # checks if a given prefix/word exists in the trie
        if not len(sequence):
            return True
        
        return False if sequence[0] not in self.children.keys() else self.children[sequence[0]].child_exists(sequence[1:])
    
    def clear(self) -> None:
        self.children = {}
        
class Squaredle:
    def __init__(self, *, squaredle: list[str], wordlist: Trie, min_length: int = 4):
        if not isinstance(min_length, int) and min_length >= 1:
            raise ValueError("Parameter min_length must be a positive int.")
        
        self.rows = np.array(list(map(list, squaredle)))
        self.rows[self.rows == " "] = ""
        
        self.valid = []
        self.depth = min_length
        self.wordlist = wordlist
        self._neighbours = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dy or dx]
        
    def solve(self) -> list[str]:
        for y, row in enumerate(self.rows):
            for x, letter in enumerate(row):
                if letter:
                    self.dfs(np.array([y, x]), [], "") # dfs from each available letter in the squaredle grid
                    
        return set(self.valid) # same words can be formed from different starting points
        
    def dfs(self, pos: list[int], seen: set[tuple[int]], path: str) -> None:
        """Recursive depth first search

        Args:
            pos (list[int]): current head of search
            seen (list[list[int]]): list of nodes visited
            path (str): string/word representation of nodes visited in order
        """
        # update & check word
        path += self.rows[*pos]
        
        if not self.wordlist.child_exists(path):
            return

        if len(path) >= self.depth and self.wordlist.search(path):
            self.valid.append(path)
            
        # check neighbours and continue dfs
        for n in self._neighbours:
            new = np.add(pos, n)
        
            # invalid if: out of bounds || invalid/blanked letter || overlapping/already visited
            if not (np.all(0 <= new) and np.all(new < self.rows.shape)) or not self.rows[*new] or new.tolist() in seen:
                continue
            
            self.dfs(new, seen + [pos.tolist()], path) # tolist method shenanigans as a scuffed fix for "in" keyword
            
    def clear(self) -> None:
        self.valid = []