/**
 * Some Game standard parameters to be used in each Game Process and Node class
 * It is convenient to define a class to implement these things rather than copy & pasting
 */
public final class GameParameters {
    /**
     * The mark flag for player who choose firstMove
     */
    public static final char x = 'x';

    /**
     * The mark flag for player who choose secondMove
     */
    public static final char o = 'o';

    /**
     * The mark flag which represents the position is empty
     */
    public static final char blank = '-';

    /**
     * the int stands for both the turn(first) and the type flag(@char x) with it
     */
    public static final int firstMove = 0;

    /**
     * the int stands for both the turn(first) and the type flag(@char x) with it
     */
    public static final int secondMove = 1;

    /**
     * the default turn for initial state(node)
     */
    public static final int defaultTurn = -1;

    // classic Size of a TTTNode
    public static final int classicSize = 3;

    // Qubic Size
    public static final int qubicSize = 4;

    // X Win utility const Value
    public static final int xWin = 1;

    // O Wins utility const Value
    public static final int oWin = -1;

    // draw utility const Value
    public static final int draw = 0;

    // return an initial TTTNode
    public static TTTNode emptyNode(int size) {
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < size * size; i++) {
            builder.append(blank);
        }
        return new TTTNode(builder.toString(), firstMove, size);
    }

    // return an initial AdvanGameBoard
    public static TTTNode[] emptyBoard(int size) {
        TTTNode[] board = new TTTNode[size * size];
        for (int i = 0; i < size * size; i++) {
            board[i] = emptyNode(size);
        }
        return board;
    }

    // return an initial AdvanNode
    public static AdvanNode emptyAdvanNode(int size) {
        return new AdvanNode(emptyBoard(size), firstMove, defaultTurn, defaultTurn);
    }

    // change the turn according to the game or node's current turn
    public static int changeTurn(int currentTurn) {
        return currentTurn == firstMove ? secondMove : firstMove;
    }

    // return the flag that should add to the current node/Game board
    public static char currentFlag(int currentTurn) {
        return currentTurn == firstMove ? x : o;
    }
}
