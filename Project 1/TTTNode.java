import java.util.ArrayList;
import java.util.List;

// auxiliary node for Basic TTT Game
public class TTTNode {
    private static int size;
    private static int boardLength;
    private final int turn;
    private final String state;
    private boolean isTerminate;
    private int utility = 5;
    private List<TTTNode> successors = new ArrayList<>();
    private List<Integer> actions = new ArrayList<>();
    private List<char[]> lines = new ArrayList<>();

    // the constructor
    public TTTNode(String state, int turn, int size) {
        this.state = state;
        this.turn = turn;
        this.size = size;
        boardLength = size * size;
        checkTerminal(); // terminates depends on the empty size
    }

    // return if the node is a terminal state
    public boolean terminates() {
        return isTerminate;
    }

    // check if the node is terminal
    private void checkTerminal() {
        List<char[]> arrays = lines();
        for (char[] array : arrays) {
            if (checkSameLine(array)) {
                isTerminate = true;
                utility = array[0] == GameParameters.x ? 1 : -1;
                return;
            }
        }
        if (emptyNumber() == 0) {
            isTerminate = true;
            utility = GameParameters.draw;
        }
    }

    // return possible lines for victory of current Node
    public List<char[]> lines() {
        if (lines.size() > 0) {
            return lines;
        }
        char[][] board = new char[size][size];
        for (int row = 0; row < size; row++) {
            for (int col = 0; col < size; col++) {
                board[row][col] = state.charAt(row * size + col);
            }
        }
        char[] diagonal1 = new char[size];
        char[] diagonal2 = new char[size];
        for (int i = 0; i < size; i++) {
            // check row array
            lines.add(board[i]);
            // check col line
            char[] col = new char[size];
            for (int v = 0; v < size; v++) {
                col[v] = board[v][i];
                if (i == v) {
                    diagonal1[i] = board[i][v];
                }
                if (i + v == size - 1) {
                    diagonal2[i] = board[i][v];
                }
            }
            lines.add(col);
        }
        lines.add(diagonal1);
        lines.add(diagonal2);
        return lines;
    }

    // check if an array of size is a same line(not all blank)
    public static boolean checkSameLine(char[] array) {
        if (array.length != size) {
            throw new IllegalArgumentException();
        }
        int[] nums = HeuristicAdvanNode.checkLine(array);
        return nums[0] == size || nums[1] == size;
    }

    // initialize the actions
    private void initialAction() {
        for (int i = 0; i < state.length(); i++) {
            if (state.charAt(i) == GameParameters.blank) {
                actions.add(i);
            }
        }
    }

    // show the current node's state in string
    public String showState() {
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < boardLength; i++) {
            if (i % size == 0 && i > 0) {
                builder.append('\n');
            }
            builder.append(state.charAt(i));
        }
        return builder.toString();
    }

    // return the current's state
    public String state() {
        // avoid external environment can change the internal variable
        char[] arrays = state.toCharArray();
        return new String(arrays);
    }

    // return the turn of current node
    public int turn() {
        if (terminates()) {
            throw new IllegalArgumentException("This node is at terminal state, no further move");
        }
        return turn;
    }

    // return the successor nodes of current node
    public List<TTTNode> successors() {
        if (isTerminate || successors.size() > 0) {
            return successors;
        }
        for (int i : actions) {
            successors.add(transition(i, GameParameters.currentFlag(turn)));
        }
        return successors;
    }

    // return the utility this node if it is a terminal node
    public int utility() {
        if (!terminates()) {
            throw new IllegalArgumentException("This node is not terminal node, you should recursively calculate its utility");
        }
        return utility;
    }

    // valid if it is a valid Move for current node
    public boolean validMove(int position) {
        return position >= 1 && position <= boardLength && state().charAt(position - 1) == GameParameters.blank;
    }

    // return how much empty positions current node has
    public int emptyNumber() {
        return actions().size();
    }

    // return the actions that this node have
    public List<Integer> actions() {
        if (actions.size() == 0) {
            initialAction();
        }
        return actions;
    }

    // return the basic size of this node
    public int size() {
        return size;
    }

    // update transition model
    public TTTNode transition(int action, char flag) {
        StringBuilder builder = new StringBuilder();
        builder.append(state());
        builder.setCharAt(action, flag);
        return new TTTNode(builder.toString(), GameParameters.changeTurn(turn()), size());
    }

    public static void main(String[] args) {
        String k = "xxoooxxxooxo---x";
        TTTNode node1 = new TTTNode(k, GameParameters.secondMove, GameParameters.qubicSize);
        System.out.println(node1.showState());
        System.out.print(node1.terminates());
        System.out.println(node1.utility());
//        System.out.println(node1.isTerminate);
    }
}
