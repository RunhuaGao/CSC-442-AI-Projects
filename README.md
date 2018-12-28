CSC 442 Aritificial Intelligence Course Projects
===============================

### Project 1: Classical Search Algorithm: Heuristic Minmax algorithm and IDS on Tic-Tac-Toe Game
__Project Description:__</br>
Implement __Hminmax algorithm__ in adversarial search problem: Tic-Tac-Toe Game</br>
Use a well performed __evaluation(heuristic) function__ to estimate the final score of each node at spcific depth</br>
Perform __alpha-beta pruning__ to reduce number of nodes to be searched.</br></br>
__Game Rules:__ There are 3 types of TTT games in this Project</br>
>>1: The normal TTT game.Pawns need to be connected in horizontal, vertical or diagnoal line to get victory.</br></br>
>>2: Advanced normal Tic-Tac-Toe game. There are totally 9 boards in game as each board is 3x3.</br> 
    For example, the previous player place flag at the fifth board at position 8(5,8),</br>
    then the next player must place his pawn at eighth board.</br>
    If the next board if already full, then you could pick any board with openings.</br>
    The requirement to win is as same as part1, if you win in one board, then you win.</br></br>
>>3: Cube Tic-Tac-Toe Game, extend the board(plane) to a cude(4x4x4). 
    The requirement to win is as same as part1, 
    but this time you could also connect 4 pawns in vertical(z direction) to get victory.</br></br>

__Data structure:__</br>
__Game1__: 
