import java.util.ArrayList;
import java.util.List;

// auxiliary Node for Advanced 3T Game
public class AdvanNode {
    private static final int firstWin = 1000;
    private static final int secondWin = -firstWin;
    private final int boardSize;
    private int turn;
    private int preBoard;  // from 1 to 9 , when use as index plz minus 1
    private List<AdvanNode> successors = new ArrayList<>();
    private boolean isTerminal = false;
    private int utility;
    private List<int[]> actions = new ArrayList<>();
    private List<char[]> lines = new ArrayList<>();
    private int size;
    TTTNode[] stateNode;
    int nextBoard; // from 1 to 9 , when use as index plz minus 1

    // the constructor for initial state
    public AdvanNode(TTTNode[] nodes, int turn, int preBoard, int nextBoard) {
        size = nodes[0].size();
        boardSize = size * size;
        stateNode = new TTTNode[boardSize];
        // create
        for (int i = 0; i < boardSize; i++) {
            TTTNode tempNode = nodes[i];
            stateNode[i] = new TTTNode(tempNode.state(), GameParameters.defaultTurn, GameParameters.classicSize);
        }
        this.turn = turn;
        this.preBoard = preBoard;
        this.nextBoard = nextBoard;
        initialActions();
        checkIsTerminal();
    }

    // return if the node is terminal
    public boolean isTerminal() {
        return isTerminal;
    }

    // check if this node is a terminal node
    private void checkIsTerminal() {
        // one player wins
        for (TTTNode node : stateNode) {
            if (node.terminates()) { // not a draw
                if (node.utility() != 0) {
                    isTerminal = true;
                    utility = node.utility() > 0 ? firstWin : secondWin;
                    return;
                }
            }
        }
        // the draw situation, all node is draw(empty position > 0)
        if (actions.size() == 0) {
            utility = 0;
            isTerminal = true;
        }
    }

    // validate the position for updating
    public boolean validateMove(int position, int board) {
        return stateNode[board - 1].validMove(position);
    }

    // validate the board for update
    public boolean validateBoard(int board) {
        if (board < 1 || board > boardSize) {
            return false;
        }
        if (nextBoard != GameParameters.defaultTurn) {
            // if the board player choose is not nextBoard, check if nextBoard is Full and not terminates
            if (board != nextBoard) {
                TTTNode nextNode = stateNode[nextBoard - 1];
                boolean flag = nextNode.emptyNumber() == 0 && !nextNode.terminates();
                if (!flag) {
                    System.out.println("You must choose the board in prompt");
                }
                return flag; // next board is in a draw situation
            } else { // check if nextBoard has empty positions
                TTTNode nextNode = stateNode[nextBoard - 1];
                boolean flag = nextNode.emptyNumber() > 0;
                if (!flag) {
                    System.out.println("The board you choose is also full! Plz Choose another board");
                }
                return flag;
            }
        }
        return true;
    }

    // show the current world state
    public void showState() {
        for (int i = 0; i < boardSize; i++) {
            System.out.println(rowState(i));
        }
    }

    // return the row i of showState
    private String rowState(int row) {
        StringBuilder builder = new StringBuilder();
        int initial = (row / 3) * 3;
        for (int i = initial; i <= initial + 2; i++) {
            builder.append(rowBoard(row % 3, i));
        }
        return builder.toString();
    }

    // return the row i of a board in worldstate
    private String rowBoard(int row, int board) {
        TTTNode node = stateNode[board];
        StringBuilder builder = new StringBuilder();
        String showstate = node.state();
        for (int i = row * 3; i <= row * 3 + 2; i++) {
            builder.append(showstate.charAt(i));
        }
        builder.append(" ");
        return builder.toString();
    }

    // initializing the actions that current board could take
    private void initialActions() {
        if (preBoard == GameParameters.defaultTurn) {
            for (int i = 0; i < boardSize; i++) {
                for (int position : stateNode[i].actions()) {
                    actions.add(new int[]{i + 1, position + 1});
                }
            }
        } else if (stateNode[nextBoard - 1].emptyNumber() == 0) {
            for (int i = 0; i < boardSize; i++) {
                if (i != nextBoard - 1) {
                    for (int position : stateNode[i].actions()) {
                        actions.add(new int[]{i + 1, position + 1});
                    }
                }
            }
        } else {
            for (int position : stateNode[nextBoard - 1].actions()) {
                actions.add(new int[]{nextBoard, position + 1});
            }
        }
    }

    // transition mode
    public AdvanNode transit(int board, int position) {
        // abstract the String for new Node
        TTTNode tempNode = stateNode[board - 1];
        TTTNode newNode = tempNode.transition(position - 1, GameParameters.currentFlag(turn()));
        stateNode[board - 1] = newNode;
        AdvanNode newAdvanNode = new AdvanNode(stateNode, GameParameters.changeTurn(turn()), board, position);
        stateNode[board - 1] = tempNode;
        return newAdvanNode;
    }

    // return successor nodes
    public List<AdvanNode> successors() {
        if (successors.size() > 0) {
            return successors;
        }
        for (int[] positions : actions) {
            // abstract the board and position info
            int board = positions[0];
            int position = positions[1];
            // add new Node
            successors.add(transit(board, position));
        }
        return successors;
    }

    // return the utility value if this is a terminal node
    public int utility() {
        if (!isTerminal()) {
            throw new IllegalArgumentException("Not a terminal state");
        }
        return utility;
    }

    // return the available actions
    public List<int[]> actions() {
        if (actions.size() == 0) {
            initialActions();
        }
        return actions;
    }

    // return the turn of current node
    public int turn() {
        return turn;
    }

    // return lines of AdvanNode
    public List<char[]> lines() {
        if (lines.size() == 0) {
            for (TTTNode node : stateNode) {
                lines.addAll(node.lines());
            }
        }
        return lines;
    }

    // return basicsize of node
    public int size() {
        return size;
    }

    public static void main(String[] args) {
        Advanced3TGame game = new Advanced3TGame(GameParameters.classicSize);
        game.GameStart();
    }
}

