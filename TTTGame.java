import java.util.List;
import java.util.Scanner;

public class TTTGame {
    private final int size;
    private TTTNode currentNode;

    // the constructor
    public TTTGame(int size) {
        this.size = size;
    }

    // Game process
    public void gameStart() {
        currentNode = GameParameters.emptyNode(size);
        int player = TTTGame.playerTurn();
        while (!currentNode.terminates()) {
            if (currentNode.turn() == player) {
                updateStatePlayer(playerMove(), player);
            } else {
                currentNode = new calNextMoveProgram(currentNode).solution;
            }
        }
        // clarify the winner
        int score = currentNode.utility();
        System.out.println(currentNode.showState()); // show current state
        if (score == 0) {
            System.out.println("This is a draw!");
        } else {
            if (score == 1 && player == GameParameters.firstMove) {
                System.out.println("You Win!");
            } else if (score == -1 && player == GameParameters.secondMove) {
                System.out.println("You Win");
            } else {
                System.out.println("You lose!");
            }
        }
    }

    // make sure the turn that the player want to select
    static int playerTurn() {
        while (true) {
            System.out.println("Plz select firstmove(0, with mark x) or secondmove(1,with mark o): ");
            Scanner reader = new Scanner(System.in);
            int flag = -1;
            if (reader.hasNext()) {
                flag = reader.nextInt();
            }
            if (flag != GameParameters.firstMove && flag != GameParameters.secondMove) {
                System.out.println("Invalid input, plz try again!");
                continue;
            }
            return flag;
        }
    }

    // make sure the position that player wanna drop the flag is valid
    private int playerMove() {
        while (true) {
            System.out.println("Plz choose the position you wanna select to drop your pawn");
            System.out.println(currentNode.showState());
            Scanner reader = new Scanner(System.in);
            int position = reader.nextInt();
            if (!currentNode.validMove(position)) {
                System.out.println("This Position is already filled with a pawn, Plz choose an empty position");
                continue;
            }
            return position;
        }
    }

    // calculate the utility value of a node
    private int calUtility(TTTNode node) {
        // if the node is a terminal node, directly return its score
        if (node.terminates()) {
            return node.utility();
        } else {
            if (node.turn() == GameParameters.firstMove) {
                int value = -2;
                for (TTTNode successor : node.successors()) {
                    int tempValue = calUtility(successor);// recursively calculate the score of a node
                    if (tempValue > value) {
                        value = tempValue;
                    }
                }
                return value;
            } else {
                int value = 2;
                for (TTTNode successor : node.successors()) {
                    int tempValue = calUtility(successor);// recursively calculate the score of a node
                    if (tempValue < value) {
                        value = tempValue;
                    }
                }
                return value;
            }
        }
    }

    // update current state to next state in player turn
    private void updateStatePlayer(int position, int player) {
        // make sure that the position is valid
        // already check the position in playerMove method
        currentNode = currentNode.transition(position - 1, GameParameters.currentFlag(currentNode.turn()));
    }

    // calculate optimal path for the program's turn
    private class calNextMoveProgram {
        TTTNode root;
        int turn;
        TTTNode solution;

        public calNextMoveProgram(TTTNode node) {
            this.root = node;
            this.turn = root.turn();
            calOptimalSolution();
        }

        private void calOptimalSolution() {
            List<TTTNode> nodes = root.successors();
            if (turn == GameParameters.firstMove) {
                int value = -2;
                for (TTTNode node : nodes) {
                    int tempValue = calUtility(node);// calculate each successor node's utility value
                    if (tempValue > value) {
                        value = tempValue;
                        solution = node;
                    }
                }
            } else {
                int value = 2;
                for (TTTNode node : nodes) {
                    int tempValue = calUtility(node);// calculate each successor node's utility value
                    if (tempValue < value) {
                        value = tempValue;
                        solution = node;
                    }
                }
            }
        }
    }

    public static void main(String[] args) {
        TTTGame game1 = new TTTGame(3);
        game1.gameStart();
    }
}