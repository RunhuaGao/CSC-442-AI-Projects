// calculate the HeuristicAdvanNode's value according to its current state
public class HeuristicAdvanNode {
    //    private static final int draw = 0;
    private static final int twoPoints = 10; // a line that only has two pawns of same type
    private static final int onePoint = 1; // a line that only has one one pawn
    private static final int threePoint = 1000;//already win
    private int size = 0;
    private AdvanNode node;
    private int value = 0;

    // the constructor
    public HeuristicAdvanNode(AdvanNode advanNode) {
        this.node = advanNode;
        if (!node.isTerminal()) {
            calAdvanNodeHeuristicValue();
            size = node.size();
        } else {
            value = node.utility() > 0 ? threePoint : -threePoint;
        }
    }

    // return the a AdvanNode's heuristic value
    public int heuritic() {
        if (Math.abs(value) > threePoint) {
            return value > 0 ? threePoint : -threePoint;
        }
        return value;
    }

    // clarify an AdvanNode's value
    private void calAdvanNodeHeuristicValue() {
        for (TTTNode region : node.stateNode) {
            for (char[] line : region.lines()) {
                int[] nums = checkLine(line);
                int xNum = nums[0];
                int oNum = nums[1];
                value += calHValue(xNum, oNum);
                if (Math.abs(value) > threePoint) {
                    return;
                }
            }
        }
    }

    // calculate each Value for the xNum, oNum in an char array
    private int calHValue(int xNum, int oNum) {
        if (xNum > 0 && oNum > 0) {
            return GameParameters.draw;
        } else if (xNum == size || oNum == size) {
            return xNum == size ? threePoint : -threePoint;
        } else {
            switch (xNum + oNum) {
                case 1:
                    return xNum > 0 ? onePoint : -onePoint;
                case 2:
                    return xNum > 0 ? twoPoints : -twoPoints;
                case 3:
                    return xNum > 0 ? threePoint : -threePoint;
            }
            return GameParameters.draw;// never reached
        }
    }

    // value one line of a TTTNode
    public static int[] checkLine(char[] array) {
        // make sure the array's length equals size
        int first = 0;
        int second = 0;
        for (char k : array) {
            if (k == GameParameters.x) {
                first += 1;
            } else if (k == GameParameters.o) {
                second += 1;
            }
        }
        return new int[]{first, second};
    }

    // some test
    public static void main(String[] args) {
        char[] ar = {GameParameters.blank, GameParameters.x, GameParameters.x};
        System.out.println();
    }
}
