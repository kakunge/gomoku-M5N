import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QLabel, QGraphicsEllipseItem, QMessageBox, QVBoxLayout, QPushButton, QDialog
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPoint

NONE = 0
WHITE = 1
BLACK = 2

COLOUR = 0
COORD = 1

my_map = [[0]*15,[0]*15,[0]*15,[0]*15,[0]*15,[0]*15,[0]*15,[0]*15,[0]*15,[0]*15,[0]*15,[0]*15,[0]*15,[0]*15,[0]*15]
my_colour = NONE

def view_map():
    global my_map
    global board

    xOffset = 50
    yOffset = 50

    for y in range(15):
        for x in range(15):
            color = Qt.transparent

            if board.stones[x][y] is None:
                if my_map[x][y] == WHITE:
                    color = Qt.white
                elif my_map[x][y] == BLACK:
                    color = Qt.black
                else:
                    continue

                stone = GomokuStone(y, x, xOffset, yOffset, 50, color)
                board.scene.addItem(stone)
                board.stones[x][y] = stone

    board.viewport().repaint()

def set_colour(colour):
    print("set_colour:", colour)

    global my_colour
    global board

    my_colour = colour
    board.setColorLabel(my_colour)
    view_map()

def set_stone(x, y, colour):
    print("set_stone:", x, y, colour)

    global board
    global my_map

    board.turnNumber += 1    
    board.setTurnNumberLabel()

    my_map[x][y] = colour
    view_map()

def choose_colour():
    print("select_colour")
    window = ColorWindow()
    window.show()
    window.exec_()

    if (window.decision == 1):
        print("WHITE")
    elif (window.decision == 2):
        print("BLACK")

    return window.decision

def place_stone():
    print("place_stone")

    global board

    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = board
    window.show()
    app.exec_()

    if window.selected_cell is not None:
        row, col = window.selected_cell
        view_map()
        window.selected_cell = None
        return col, row


def make_decision():
    print("make_decision")
    window = DecisionWindow()
    window.show()
    window.exec_()

    if (window.decision == 0):
        print("COLOUR")
    elif (window.decision == 1):
        print("COORD")
    
    return window.decision

def victory():
    print("victory")

    global board
    global my_colour

    board.endGame(1 if my_colour == BLACK else 0)

    QMessageBox.information(None, "Game Over", "Win!")

def defeat():
    print("defeat")

    global board
    global my_colour

    board.endGame(0 if my_colour == BLACK else 1)

    QMessageBox.information(None, "Game Over", "Lose...")

class DecisionWindow(QDialog):
    def __init__(self):
        super().__init__(None, Qt.WindowTitleHint)

        self.setWindowTitle("Make Decision")

        layout = QVBoxLayout()

        self.colorButton = QPushButton("COLOUR")
        self.coordButton = QPushButton("COORD")

        self.colorButton.clicked.connect(self.handleColorButtonClicked)
        self.coordButton.clicked.connect(self.handleCoordButtonClicked)

        layout.addWidget(self.colorButton)
        layout.addWidget(self.coordButton)

        self.setLayout(layout)

        self.decision = None
        
    def handleColorButtonClicked(self):
        self.decision = COLOUR
        self.hide()

    def handleCoordButtonClicked(self):
        self.decision = COORD
        self.hide()

class ColorWindow(QDialog):
    def __init__(self):
        super().__init__(None, Qt.WindowTitleHint)

        self.setWindowTitle("Make Decision")

        layout = QVBoxLayout()

        self.blackButton = QPushButton("BLACK")
        self.whiteButton = QPushButton("WHITE")

        self.blackButton.clicked.connect(self.handleBlackButtonClicked)
        self.whiteButton.clicked.connect(self.handleWhiteButtonClicked)

        layout.addWidget(self.blackButton)
        layout.addWidget(self.whiteButton)

        self.setLayout(layout)

        self.decision = None

    def handleBlackButtonClicked(self):
        self.decision = BLACK
        self.hide()

    def handleWhiteButtonClicked(self):
        self.decision = WHITE
        self.hide()


class GomokuStone(QGraphicsEllipseItem):
    def __init__(self, row, col, xOffset, yOffset, size, color):
        super().__init__(col * size - 25 + xOffset, row * size - 25 + yOffset, 50, 50)
        self.row = row
        self.col = col
        self.size = size
        self.setBrush(QBrush(color))
        self.show()
        self.update()

    def getRow(self):
        return self.row

    def getCol(self):
        return self.col

class GomokuBoard(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setFixedSize(1200, 800)
        self.setSceneRect(0, 0, 1200, 800)
        self.setBackgroundBrush(QColor("#a87532"))

        self.numRows = 15
        self.numCols = 15
        self.cellSize = 50
        self.stones = [[None for _ in range(self.numCols)] for _ in range(self.numRows)]
        self.isBlackTurn = True

        self.colorLabel = QLabel("Color : ", self)
        self.colorLabel.move(800, 50)
        self.colorLabel.setStyleSheet("color: black; font-size: 20px; font-family: Arial;")
        self.colorLabel.show()

        self.turnNumber = 1
        self.turnNumberLabel = QLabel("1 Turn", self)
        self.turnNumberLabel.move(800, 90)
        self.turnNumberLabel.setStyleSheet("color: black; font-size: 20px; font-family: Arial;")
        self.turnNumberLabel.show()

        self.selected_cell = None

        self.drawBoard()
        self.show()
        self.update()
    
    def mousePressEvent(self, event):
        point = self.mapToScene(event.pos())
        xOffset = 50
        yOffset = 50
        row = int((point.y() - yOffset + self.cellSize / 2) / self.cellSize)
        col = int((point.x() - xOffset + self.cellSize / 2) / self.cellSize)

        if 0 <= row < self.numRows and 0 <= col < self.numCols and not self.stones[row][col]:
            print(row, col)
            self.selected_cell = (row, col)
            QApplication.exit(0)

    def checkWin(self, row, col):
        currentColor = self.stones[row][col].brush().color()

        dx = [1, 0, 1, 1]
        dy = [0, 1, 1, -1]

        for i in range(4):
            count = 1
            for d in [-1, 1]:
                nx = row + dx[i] * d
                ny = col + dy[i] * d
                while 0 <= nx < self.numRows and 0 <= ny < self.numCols and self.stones[nx][ny] and self.stones[nx][ny].brush().color() == currentColor:
                    count += 1
                    nx += dx[i] * d
                    ny += dy[i] * d

            if count >= 5:
                return True

        return False
    
    def setTurnNumberLabel(self):
        self.turnNumberLabel.setText("{} Turn".format(self.turnNumber))
        self.turnNumberLabel.adjustSize()

    def setColorLabel(self, color):
        if (color == WHITE):
            self.colorLabel.setText("Color : WHITE")
            self.colorLabel.adjustSize()
        else:
            self.colorLabel.setText("Color : BLACK")
            self.colorLabel.adjustSize()

    def endGame(self, isBlackWin):
        self.setEnabled(False)
        winColor = Qt.black if isBlackWin else Qt.white
        winStones = []

        for i in range(self.numRows):
            for j in range(self.numCols):
                if self.stones[i][j] and self.stones[i][j].brush().color() == winColor:
                    if self.checkWin(i, j):
                        winStones.append(QPoint(i, j))

        for point in winStones:
            row, col = point.x(), point.y()
            self.stones[row][col].setBrush(Qt.yellow)

    def drawBoard(self):
        xOffset, yOffset = 50, 50

        for i in range(self.numRows):
            self.scene.addLine(xOffset, yOffset + i * self.cellSize, xOffset + (self.numCols - 1) * self.cellSize, yOffset + i * self.cellSize, QPen(Qt.gray))

        for j in range(self.numCols):
            self.scene.addLine(xOffset + j * self.cellSize, yOffset, xOffset + j * self.cellSize, yOffset + (self.numRows - 1) * self.cellSize, QPen(Qt.gray))

app = QApplication(sys.argv)
board = GomokuBoard()
board.show()

if __name__ == "__main__":
    sys.exit(app.exec_())
