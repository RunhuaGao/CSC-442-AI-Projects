public class HeuristicQubicNode {
    private static final int xWin = 8000;
    private static final int oWin = -xWin;
    private static final int onePoint = 1;
    private static final int twoPoint = 10;
    private static final int threePoint = 100; // max is 76*100 - 7600 < xWin
    private final QubicNode root;
    private int value = 0;

    public HeuristicQubicNode(QubicNode node) {
        root = node;
        if (root.isTerminal()) {
            value = root.utility() == GameParameters.xWin ? xWin : oWin;
        } else {
            calValue();
        }
    }

    // return a total heuristic value
    public int hValue() {
        if (value != GameParameters.draw) {
            if (Math.abs(value) > xWin) {
                return value > 0 ? xWin : oWin;
            }
            return value;
        }
        return GameParameters.draw;
    }

    // cal value for each line in root node
    private void calValue() {
        for (char[] array : root.lines()) {
            int[] nums = HeuristicAdvanNode.checkLine(array);
            value += calHValue(nums[0], nums[1]);
            if (Math.abs(value) > xWin) {
                return;
            }
        }
    }

    // cal heuristic value for one line of node
    private int calHValue(int xNum, int oNum) {
        if (xNum > 0 && oNum > 0) {
            return GameParameters.draw;
        }
        switch (xNum + oNum) {
            case 1:
                return xNum > 0 ? onePoint : -onePoint;
            case 2:
                return xNum > 0 ? twoPoint : -twoPoint;
            case 3:
                return xNum > 0 ? threePoint : -threePoint;
            case 4:
                return xNum > 0 ? xWin : oWin;
        }
        return GameParameters.draw;
    }
}
