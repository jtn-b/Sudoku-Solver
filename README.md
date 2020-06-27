# Sudoku-Solver
Interactive 9x9 Soduko game built using pygame module. Random games are scraped from [this site](http://www.menneske.no/sudoku/eng/random.html) at startup using python's  
BeautifulSoup module. Scraped puzzles are solved using backtracking.

## Installing & Launching
1. Make sure Python and pip are installed.
2. Navigate to the cloned directory.
2. Run ```pip install -r requirements.txt``` command to install dependencies.
3. Run ```python GUI.py``` to launch the game.

## How to play ?
1. Click on the cell to select in for input.
2. Enter a number (<kbd>1</kbd>-<kbd>9</kbd>) and press <kbd>Enter</kbd> to confirm.
3. To erase number before confirming , press <kbd>Delete</kbd>.
4. For every conflicting entry , you get a strike (displayed as '**X**' in the bottom left of the screen).
5. You lose after accumulating 3 strikes.
6. Click on the <kbd>Solution</kbd> button to display the solution.
