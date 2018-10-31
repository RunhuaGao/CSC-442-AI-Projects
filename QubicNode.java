import java.security.cert.TrustAnchor;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;

// Node for part 3
// QubicNode, basic size equals 4
public class QubicNode {
    private final TTTNode[] board = new TTTNode[GameParameters.qubicSize]; // the current board
    private final int turn; // current node's turn
    private boolean isTerminal;
    private int utility = GameParameters.defaultTurn;
    private List<char[]> lines = new ArrayList<>();
    private List<int[]> actions = new ArrayList<>();

    public QubicNode(TTTNode[] nodes, int turn) {
        this.turn = turn;
        for (int i = 0; i < basicSize(); i++) {
            board[i] = new TTTNode(nodes[i].state(), GameParameters.defaultTurn, basicSize());
            // construct board with  TTTNode array, but do not give it a turn as the whole turn is decided by the Game
        }
        checkIsTerminal();
    }

    // return utility value if this is a terminal Node
    public int utility() {
        if (!isTerminal()) {
            throw new IllegalArgumentException("Not a terminal Node");
        }
        return utility;
    }

    // return if current Node is a Terminal node
    public boolean isTerminal() {
        return isTerminal;
    }

    // return basic size of current node
    private int basicSize() {
        return board.length;
    }

    // return the lines(potential for victory)
    public List<char[]> lines() {
        if (lines.size() > 0) {
            return lines;
        }
        for (TTTNode node : board) {
            lines.addAll(node.lines());
        }
        getTerminalDDirectionPlane();
        getTerminalXDirectionPlane();
        getTerminalYDirectionPlane();
        getTerminalVerticalLines();
        return lines;
    }

    // check the terminal status of this node
    private void checkIsTerminal() {
        checkTerminalHorizontalLines();
        if (isTerminal()) {
            return;
        }
        // the lines in board of horizontal plane have already been check, no need to check it again
        HashSet<char[]> checkLines = new HashSet<>();
        for (TTTNode node : board) {
            checkLines.addAll(node.lines());
        }
        for (char[] array : lines()) {
            if (isTerminal() || checkLines.contains(array)) {
                continue;
            }
            setUtility(array);
        }
        checkTerminalDraw();
    }

    // check if this QubicNode is a Terminal Node
    private void checkTerminalHorizontalLines() {
        // check 40 lines, in horizontal planes
        for (TTTNode node : board) {
            if (node.terminates()) {
                isTerminal = true;
                utility = node.utility(); // the node self could Give an utility value
                return;
            }
        }
    }

    // check if any vertical Lines is of victory
    private void getTerminalVerticalLines() {
        if (isTerminal) {
            return;
        }
        // initializing all String representation
        String[] states = new String[basicSize()];
        for (int i = 0; i < basicSize(); i++) {
            states[i] = board[i].state();
        }
        // check each Vertical Line
        int length = basicSize() * basicSize();
        for (int i = 0; i < length; i++) {
            // Get any Vertical Line
            char[] array = new char[basicSize()];
            for (int v = 0; v < basicSize(); v++) {
                array[v] = states[v].charAt(i);
            }
            lines.add(array);
        }
    }

    // make sure the utility value through an array
    // the array if the result array
    private void setUtility(char[] array) {
        assert array.length == basicSize();
        if (TTTNode.checkSameLine(array)) {
            isTerminal = true;
            utility = array[0] == GameParameters.x ? GameParameters.xWin : GameParameters.oWin;
        }
    }

    // check the dia lines of a plane
    private void getTerminalVerticalPlaneDia(char[][] plane) {
        if (isTerminal) {
            return;
        }
        // make sure the plane is of right size
        assert plane.length == basicSize() && plane[0].length == basicSize();
        char[] dia1 = new char[basicSize()];
        char[] dia2 = new char[basicSize()];
        for (int i = 0; i < basicSize(); i++) {
            for (int v = 0; v < basicSize(); v++) {
                if (i == v) {
                    dia1[i] = plane[i][v];
                } else if (i + v == basicSize() - 1) {
                    dia2[i] = plane[i][v];
                }
            }
        }
        lines.add(dia1);
        lines.add(dia2);
    }

    // get the column char array from a TTTNode
    private char[] getColPlane(TTTNode node, int col) {
        char[] array = new char[basicSize()];
        String state = node.state();
        int addIndex = 0;
        for (int i = 0; i < state.length(); i++) {
            if (i % node.size() == col) {
                array[addIndex] = state.charAt(i);
                addIndex++;
            }
        }
        return array;
    }

    // get the row char array from a TTTNode
    private char[] getRowPlane(TTTNode node, int row) {
        char[] array = new char[basicSize()];
        String state = node.state();
        int addIndex = 0;
        for (int i = 0; i < state.length(); i++) {
            if (i / basicSize() == row) {
                array[addIndex] = state.charAt(i);
                addIndex++;
            }
        }
        return array;
    }

    // the dia line from a TTTNode,including two lines
    // First line including the element as x==y
    // Second line including the element as x+y==basicSize-1
    private char[][] getDiaPlane(TTTNode node) {
        char[][] dias = new char[2][basicSize()];
        char[] dia1 = new char[basicSize()];
        char[] dia2 = new char[basicSize()];
        String state = node.state();
        for (int i = 0; i < state.length(); i++) {
            int row = i / basicSize();
            int col = i % basicSize();
            if (row == col) {
                dia1[row] = state.charAt(i);
            }
            if (row + col == basicSize() - 1) {
                dia2[row] = state.charAt(i);
            }
        }
        dias[0] = dia1;
        dias[1] = dia2;
        return dias;
    }

    // the plane comes from the col of each basic plane
    private void getTerminalXDirectionPlane() {
        for (int i = 0; i < basicSize(); i++) {
            // initializing the plane
            char[][] plane = new char[basicSize()][basicSize()];
            for (int v = 0; v < basicSize(); v++) {
                plane[v] = getColPlane(board[v], i);// v is the index of which basic plane
            }
            getTerminalVerticalPlaneDia(plane);

        }
    }

    // the plane comes from the row of each basic plane
    private void getTerminalYDirectionPlane() {
        for (int i = 0; i < basicSize(); i++) {
            // initializing the plane
            char[][] plane = new char[basicSize()][basicSize()];
            for (int v = 0; v < basicSize(); v++) {
                plane[v] = getRowPlane(board[v], i);// v is the index of which basic plane
            }
            getTerminalVerticalPlaneDia(plane);
        }
    }

    // the plane comes from the dia line of each basic plane
    private void getTerminalDDirectionPlane() {
        char[][] diaPlane1 = new char[basicSize()][basicSize()];
        char[][] diaPlane2 = new char[basicSize()][basicSize()];
        for (int i = 0; i < basicSize(); i++) {
            char[][] dias = getDiaPlane(board[i]);
            diaPlane1[i] = dias[0];
            diaPlane2[i] = dias[1];
        }
        getTerminalVerticalPlaneDia(diaPlane1);
        getTerminalVerticalPlaneDia(diaPlane2);
    }

    // check if this is a draw
    private void checkTerminalDraw() {
        if (isTerminal()) {
            return;
        }
        for (TTTNode node : board) {
            if (node.emptyNumber() > 0) {
                return;
            }
        }
        isTerminal = true;
        utility = GameParameters.draw;
    }

    // return the node's empty position
    public List<int[]> actions() {
        if (actions.size() == 0) {
            for (int i = 0; i < basicSize(); i++) {
                for (int action : board[i].actions()) {
                    actions.add(new int[]{i + 1, action + 1});
                }
            }
        }
        return actions;
    }

    // show current node in format of String
    public void showState() {
        for (TTTNode node : board) {
            System.out.println(node.showState());
            System.out.println();
        }
    }

    // return the current turn of node
    public int turn() {
        return turn;
    }

    // the Qubic node's transition model
    public QubicNode transition(int plane, int position) {
        //board,position start from 1
        TTTNode tempNode = board[plane - 1];
        TTTNode newNode = tempNode.transition(position - 1, GameParameters.currentFlag(turn()));
        board[plane - 1] = newNode;
        QubicNode newqnode = new QubicNode(board, GameParameters.changeTurn(turn()));
        board[plane - 1] = tempNode;
        return newqnode;
    }



    public static void main(String[] args) {
        TTTNode[] board = GameParameters.emptyBoard(4);
        for (int i = 0; i < 4; i++) {
            board[i] = board[i].transition((3 - i) * 4 + 1, GameParameters.x);
        }
        QubicNode node = new QubicNode(board, GameParameters.firstMove);
//        System.out.println(node.isTerminal());
//        System.out.println(node.utility());
//        List<char[]> lines = node.lines();
//        List<int[]> actions = node.actions();
        node.showState();

    }
}
