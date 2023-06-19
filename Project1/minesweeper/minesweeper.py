import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    mines = set()
    safes = set()

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return Sentence.mines & self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return Sentence.safes & self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Remove the cell from the sentence and subtract the count by 1 and add the cell in known mines set
        if cell in self.cells:
            self.cells.discard(cell)
            self.count = self.count - 1
            Sentence.mines.add(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Remove the cell from the sentence since it's not a mine and do nothing to the count. Add the cell in safe cells set
        if cell in self.cells:
            self.cells.discard(cell)
            Sentence.safes.add(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        print(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1 Marking the cell as safe and a move made
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # Getting the co-ordinates of the cell
        x = cell[0]
        y = cell[1]


        # 3 Finding the neighbours of the given cell
        neighbour_cells = set()

        for i in range(-1, 2):
            for j in range(-1, 2):
                
                # To check if the cell is an unknown cell
                if (x + i, y + j) in self.moves_made:
                    continue

                if 0 <= (x + i) < self.height and 0 <= (y + j) < self.width:
                    neighbour_cells.add((x + i, y + j))

        
        # Add the set of cells and the associated count
        self.knowledge.append(Sentence(neighbour_cells, count))

        # Check for subsets and supersets and create new inferences


        for first_sentence in self.knowledge:

            for second_sentence in self.knowledge:
                

                if first_sentence == second_sentence:
                    continue

                if first_sentence.cells > second_sentence.cells:

                    sent = Sentence(first_sentence.cells - second_sentence.cells,
                                    first_sentence.count - second_sentence.count)
                    
                    if sent not in self.knowledge:
                        self.knowledge.append(sent)


        # Mark new cells as safe or mines in  newly formed sentences

        helper = set()
        for sentence in self.knowledge:
            
            # If the number of cells equals to the number of mines present that means every cell is a mine
            if len(sentence.cells) == sentence.count:

                # Using a helper set to prevent dynamic deletion of cells from the set
                for each_cell in sentence.cells:    
                    helper.add(each_cell)
                
                self.knowledge.remove(sentence)

                
                for each_cell in helper:
                    self.mark_mine(each_cell)
                continue


            # If the count of mines in the sentence is 0 that means all the cells are safe
            if sentence.count == 0:
                
                for each_cell in sentence.cells:
                    helper.add(each_cell)
                
                self.knowledge.remove(sentence)
                
                for each_cell in helper:
                    self.mark_safe(each_cell)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        print(Sentence.safes - self.moves_made)
        for safe_move in self.safes:
            if safe_move not in self.moves_made:
                return safe_move

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        while 1:

            x = random.randint(0, self.height - 1)
            y = random.randint(0, self.width - 1)

            if (x, y) not in self.mines and (x, y) not in self.moves_made:
                return x, y
