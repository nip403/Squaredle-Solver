import numpy as np
import os

__FP__ = os.path.dirname(__file__)

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
            out += "\n" + str(child) # str call is recursive
            
        return out.replace("\n\n", "\n") # needed for some unintended behaviour from the ternary statement and not worth properly fixing 
    
    def alphabetise(self) -> None:
        for child in self.children.values(): # reordeer to sort words by letter
            child.alphabetise()
            
        self.children = dict(sorted(self.children.items(), key=lambda i: ord(i[0])))
        
    def search(self, term: str) -> bool:
        if not isinstance(term, str):
            return False 
        
        if not len(term) and self.endNode:
            return True
        
        elif len(term):
            if term[0] in self.children.keys():
                return self.children[term[0]].search(term[1:])
            
        return False
    
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
        
    def solve(self) -> list[str]:
        for y, row in enumerate(self.rows):
            for x, letter in enumerate(row):
                if letter:
                    self.dfs()
                    
                    self.valid += self.dfs([y, x])
                    
                    
                    ###### testing a only
                    return "done a"
        
    def dfs(self, start: list[int]): # depth first search
        seen = np.zeros(self.rows.shape)
        neighbours = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dy or dx]
        stack = [start]
         = ""
        
        #note to self: arr[row, col]
            # gen valid neighbours
            # visit and update seen
            # check valid word
            # neighbours
            # visit update seen 
        
        while len(stack):
            current = stack.pop()
            seen[*current] = 1
            word
            
            print(current, self.rows[*current]) ######### 
            
            # check valid neighbours and push
            for n in neighbours:
                y, x = np.add(current, n)
                
                if not (0 <= x < len(seen[0]) and 0 <= y < len(seen)) or not self.rows[y, x]:
                    continue
                
                stack.append()
                
                
                # ensure word min 4 length to begin checking
                    
        
        return []
    
    def clear(self) -> None:
        self.valid = []
    
def build_trie(words: list[str]) -> Trie:
    root = Trie("")
    
    for i in words:
        root.insert(i.lower())
        
    root.alphabetise()
    
    return root        

def parse_input(trie: Trie) -> list[str]:
    while True:
        grid = input("""Enter squaredle grid:

    -> Separate rows by "-"
    -> Denote greyed out cells with a space " "
    -> e.g. June 15 Squaredle: a p n-ml so-rsioi-od zt-n e a

Grid: """).lower().split("-")
        
        print("\nInput Squaredle:\n")
        
        for i in grid:
            print(f'    | {" ".join(list(i))} |')
            
        cont = input("\nENTER to continue, anything else to retry: ")
        
        if not cont:
            break
    
    print()
    
    return Squaredle(
        squaredle=grid, 
        wordlist=trie
    )

def main() -> None:
    with open(__FP__ + "\\words.txt", "r+") as f:
        wordlist = f.read()
        
        for i in ("'", ' ', '\n'):
            wordlist = wordlist.replace(i, "")
            
    trie = build_trie(wordlist)
    squaredle = parse_input(trie)
    
    print(squaredle.solve())

if __name__ == "__main__":
    main()
   