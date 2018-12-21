CSC 442 Aritificial Intelligence Course Projects
===============================

Project 1: Classical Search Algorithm: Heuristic Minmax algorithm and IDS on Tic-Tac-Toe Game
---------
Back Ground:</br>

    Implement Hminmax algorithm in adversarial search problem: Tic-Tac-Toe Game
    Use a well performed evaluation(heuristic) function to estimate the final score of each node at spcific depth
    Then Use 'alpha-beta pruning to reduce number of nodes to be searched.
    There exists totally three types of Tic-Tac-Toe Game in this Project.
    1: The normal TTT game.Pawns need to be connected in horizontal, vertical or diagnoal line to get victory.
    2: Advanced normal Tic-Tac-Toe game. There are totally 9 boards in game as each board is 3x3. For example, the previous player place flag at the fifth board at position 8(5,8), then the next player must place his pawn at eighth board.
    If the next board if already full, then you could pick any board with openings.
    The requirement to win is as same as part1, if you win in one board, then you win.
    3: Cube Tic-Tac-Toe Game, extend the board(plane) to a cude(4x4x4). The requirement to win is as same as part1, but this time you could also connect 4 pawns in vertical(z direction) to get victory.
   
Project Structure:</br>

    The Project is develpoed by Java.
    Structure is as following: 
    
    
