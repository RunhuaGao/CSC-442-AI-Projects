import java.util.Scanner;

public class Advanced3TGame {
    // standard variables as same as in TTTNode and TTTGame
    private final int size;
    private static final String pageLine = "_________________________ New Move!";
    private AdvanNode state;
    private int nextBoard = GameParameters.defaultTurn;
    private int player = GameParameters.defaultTurn;

    // constructor
    public Advanced3TGame(int size) {
        this.size = size;
    }

    // the Game Process
    public void GameStart() {
        state = GameParameters.emptyAdvanNode(size);
        player = GameParameters.defaultTurn;
        player = TTTGame.playerTurn();// use turn input method in TTTGame
        while (!state.isTerminal()) {
            System.out.println(pageLine);
            System.out.println();
            state.showState();
            if (state.turn() == player) {
                updateMovePlayer();
            } else {
                int[] solution = new hMinMax(state).solution;
                state = state.transit(solution[0], solution[1]);

                nextBoard = state.nextBoard;
            }
            System.out.println();
        }
        // clarify the result, who wins or it is a draw
        state.showState();
        int value = state.utility();
        if (value == 0) {
            System.out.println("This is a draw!");
        } else {
            if ((value > 0 && player == GameParameters.firstMove) || (value < 0 && player == GameParameters.secondMove)) {
                System.out.println("You Win!");
            } else {
                System.out.println("You Lose!");
            }
        }
    }

    // update state
    private void updateMovePlayer() {
        while (true) {
            System.out.println("Plz type the board you wanna mark(1-9,must be right position if it is not initial action)");
            if (nextBoard > 0) { // after initial state, print out a prompt to tell the player right board they should mark
                System.out.println("The board you may mark is: " + nextBoard);
                // prompt: player could choose another board if nextBoard is full
                System.out.println("If the board above is full, you can choose another board with empty positions");
            }
            Scanner reader = new Scanner(System.in);
            int board = reader.hasNextInt() ? reader.nextInt() : 0;
            if (!state.validateBoard(board)) {
                state.showState();
                continue;
            }
            // read position and update world state
            while (true) {
                System.out.println("Plz Choose the position of board you wanna mark");
                int position = reader.hasNextInt() ? reader.nextInt() : 0; // read the position player choose to mark
                if (!state.validateMove(position, board)) {
                    state.showState();
                    System.out.println("This position is invalid! Choose again.");
                    continue;
                }
                state = state.transit(board, position); // update world state
                nextBoard = position;
                return;
            }
        }
    }

    // a class that calculate the action te program for an AdvanNode
    // implements the hMinMax algorithm and alpha beta pruning
    private class hMinMax {
        private static final int limitDepth = 5;
        private static final int alphaDefault = Integer.MIN_VALUE;
        private static final int betaDefault = Integer.MAX_VALUE;
        private AdvanNode root;
        private int[] solution;

        public hMinMax(AdvanNode node) {
            root = node;
            calSolution();
        }

        // the HMinMax plus alpha beta pruning algorithm implementation
        private int calHMinMax(AdvanNode node, int a, int b, int depth) {
            if (node.isTerminal()) { // if it is a terminal node, return its utility function
                return node.utility();
            } else if (depth == limitDepth) {
                return new HeuristicAdvanNode(node).heuritic();
            } else {
                if (node.turn() == GameParameters.firstMove) {
                    int value = alphaDefault;
                    for (int[] action : node.actions()) {
                        int board = action[0];// from 1 to 9
                        int position = action[1]; // from 1 to 9
                        AdvanNode sucNode = node.transit(board, position);
                        value = Math.max(value, calHMinMax(sucNode, a, b, depth + 1));
                        if (value >= b) {
                            break;
                        }
                        a = Math.max(a, value);
                    }
                    return value;
                } else {
                    int value = betaDefault;
                    for (int[] action : node.actions()) {
                        int board = action[0];// from 1 to 9
                        int position = action[1]; // from 1 to 9
                        AdvanNode sucNode = node.transit(board, position);
                        value = Math.min(value, calHMinMax(sucNode, a, b, depth + 1));
                        if (value <= a) {
                            break;
                        }
                        b = Math.min(b, value);
                    }
                    return value;
                }
            }
        }

        // calculate the solution
        private void calSolution() {
            if (root.turn() == GameParameters.firstMove) {
                int value = alphaDefault;
                for (int[] action : root.actions()) {
                    AdvanNode node = root.transit(action[0], action[1]);
                    int tempValue = calHMinMax(node, alphaDefault, betaDefault, 1);
                    if (tempValue > value) {
                        value = tempValue;
                        solution = action;
                    }
                }
            } else {
                int value = betaDefault;
                for (int[] action : root.actions()) {
                    AdvanNode node = root.transit(action[0], action[1]);
                    int tempValue = calHMinMax(node, alphaDefault, betaDefault, 1);
                    if (tempValue < value) {
                        value = tempValue;
                        solution = action;
                    }
                }
            }
        }

        // return the solution of this hMinMax algorithm to update move
        private int[] solution() {
            return solution;
        }
    }

    public static void main(String[] args) {
        Advanced3TGame game = new Advanced3TGame(GameParameters.classicSize);
        game.GameStart();
    }
}
