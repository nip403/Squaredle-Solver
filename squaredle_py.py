from squaredle_utils import Trie, Squaredle
import numpy as np
import os

__FP__ = os.path.dirname(__file__)
    
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
            
    trie = build_trie(wordlist.split(","))
    squaredle = parse_input(trie)

    for i in sorted(squaredle.solve(), key=len):
        print(i)

if __name__ == "__main__":
    main()
   