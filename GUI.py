import time
import pygame
import sys
import generator
import copy
import solver
pygame.init()

board = generator.getPuzzle()
locked = copy.deepcopy(board)
solvedBoard = copy.deepcopy(board)
solvedBoard = solver.getSolve(solvedBoard)
endImg = pygame.image.load('res/game-over.png')
endImg = pygame.transform.scale(endImg, (400, 200))
winImg = pygame.image.load('res/win.png')
winImg = pygame.transform.scale(winImg, (400, 300))

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# DIMENSIONS
SCALER = 5
WIN_WIDTH = 90 * SCALER  # 450
WIN_HEIGHT = 90 * SCALER  # 450 + 50 FOR FOOTER
SQUARE_DIM = WIN_HEIGHT // 3  # 150
CELL_DIM = SQUARE_DIM // 3  # 50

# FONT SETTINGS
global FONT_SIZE, FONT
FONT_SIZE = 40
FONT = pygame.font.Font("res/OpenSans.ttf", FONT_SIZE)


# Mouse-Action Variables
MOUSE_POSX = 0
MOUSE_POSY = 0
isClicked = False


def setBoard():
    for i in range(9):
        for j in range(9):
            if board[i][j] == '0':
                locked[i][j] = 0
            else:
                locked[i][j] = 1


def DrawGrids():
    for x in range(0, WIN_WIDTH, CELL_DIM):  # draw vertical lines
        pygame.draw.line(DISPLAY, GRAY, (x, 0), (x, WIN_HEIGHT))
    for y in range(0, WIN_HEIGHT, CELL_DIM):  # draw horizontal lines
        pygame.draw.line(DISPLAY, GRAY, (0, y), (WIN_WIDTH, y))

    for x in range(0, WIN_WIDTH, SQUARE_DIM):  # draw vertical lines
        pygame.draw.line(DISPLAY, BLACK, (x, 0), (x, WIN_HEIGHT))
    for y in range(0, WIN_HEIGHT+SQUARE_DIM, SQUARE_DIM):  # draw horizontal lines
        pygame.draw.line(DISPLAY, BLACK, (0, y), (WIN_WIDTH, y))


def FillBoard(board):
    for i in range(0, 9, 1):
        for j in range(0, 9, 1):
            FillCells(board[i][j], CELL_DIM * j, CELL_DIM * i)


def FillCells(data, x, y):
    if data == '0':
        data = ' '
    cellSurf = FONT.render(" %s" % (data), True, RED)
    cellRect = pygame.Rect(0, 0, 0, 0)
    cellRect.topleft = (x + 5, y + -5)
    DISPLAY.blit(cellSurf, cellRect)


def getCoords(x, y):
    return (x // 50, y // 50)


def drawBox(x, y):
    px, py = getCoords(x, y)
    pygame.draw.rect(DISPLAY, BLUE, (px * 50, py * 50, CELL_DIM, CELL_DIM), 2)


def format_time(secs):
    sec = secs % 60
    minute = secs//60
    hour = minute//60
    mat = " " + str(minute) + ":" + str(sec)
    return mat


def refreshDisplay():
    DISPLAY.fill(WHITE)
    DrawGrids()
    FillBoard(board)


def drawFooter(strikes, time):
    DISPLAY.fill(pygame.Color("white"), (0, 452, 450, 50))
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0, 0, 0))
    textX = fnt.render("X" * strikes, 1, (0, 0, 0))
    DISPLAY.blit(textX, (0, 470))
    DISPLAY.blit(text, (300, 470))
    DISPLAY.fill(pygame.Color("blue"), (155, 470, 120, 30))
    solBtn = fnt.render("Solution", 1, pygame.Color("yellow"))
    DISPLAY.blit(solBtn, (155, 470))


def youWin():
    DISPLAY.fill(WHITE)
    DISPLAY.blit(winImg, (25, 50))
    fnt = pygame.font.SysFont("comicsans", 50)
    solBtn = fnt.render("Congratulations!", 1, pygame.Color("red"))
    DISPLAY.blit(solBtn, (80, 400))


def gameOverScreen():
    DISPLAY.fill(WHITE)
    DISPLAY.blit(endImg, (25, 50))
    DISPLAY.fill(pygame.Color("blue"), (155, 470, 120, 30))
    fnt = pygame.font.SysFont("comicsans", 40)
    solBtn = fnt.render("Solution", 1, pygame.Color("yellow"))
    DISPLAY.blit(solBtn, (155, 470))


def changeBtn():
    fnt = pygame.font.SysFont("comicsans", 40)
    DISPLAY.fill(pygame.Color("red"), (155, 470, 120, 30))
    solBtn = fnt.render("Solution", 1, pygame.Color("black"))
    DISPLAY.blit(solBtn, (155, 470))


def main():
    global DISPLAY, FPS_TICK
    setBoard()
    pygame.init()
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    FPS_TICK = pygame.time.Clock()
    FPS = 60
    start = time.time()
    DISPLAY = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT+50))
    pygame.display.set_caption("Sudoku")
    DISPLAY.fill(WHITE)
    DrawGrids()
    FillBoard(board)
    key = None
    strikes = 0
    showSoln = False
    gameOver = False
    isClicked = False
    hover = False
    tmp = [0, 0]
    # Main game loop
    while True:
        play_time = round(time.time() - start)

        if not solver.find_empty_location(board, tmp):
            youWin()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        elif showSoln:
            hover = False
            DISPLAY.fill(WHITE)
            DrawGrids()
            FillBoard(solvedBoard)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        elif gameOver:
            gameOverScreen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    MOUSE_POSX, MOUSE_POSY = event.pos
                    if MOUSE_POSX > 125 and MOUSE_POSX < 245 and MOUSE_POSY > 470:
                        hover = True
                    else:
                        hover = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    MOUSE_POSX, MOUSE_POSY = event.pos
                    if MOUSE_POSX > 125 and MOUSE_POSX < 245 and MOUSE_POSY > 470:
                        showSoln = True

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    hoverX, hoverY = event.pos
                    if hoverX > 125 and hoverX < 245 and hoverY > 470:
                        hover = True
                    else:
                        hover = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    MOUSE_POSX, MOUSE_POSY = event.pos
                    if MOUSE_POSX > 125 and MOUSE_POSX < 245 and MOUSE_POSY > 470:
                        showSoln = True
                    else:
                        isClicked = True
                elif isClicked:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            key = 1
                        if event.key == pygame.K_2:
                            key = 2
                        if event.key == pygame.K_3:
                            key = 3
                        if event.key == pygame.K_4:
                            key = 4
                        if event.key == pygame.K_5:
                            key = 5
                        if event.key == pygame.K_6:
                            key = 6
                        if event.key == pygame.K_7:
                            key = 7
                        if event.key == pygame.K_8:
                            key = 8
                        if event.key == pygame.K_9:
                            key = 9
                        if event.key == pygame.K_DELETE:
                            key = None
                        if event.key == pygame.K_RETURN:
                            if key == None:
                                pass
                            else:
                                xp, yp = getCoords(MOUSE_POSX, MOUSE_POSY)
                                if locked[yp][xp] == 1:
                                    pass
                                elif not solver.check_location_is_safe(board, yp, xp, key):
                                    strikes = strikes + 1
                                    if strikes == 3:
                                        gameOver = True
                                    isClicked = False
                                else:
                                    board[yp][xp] = str(key)
                                    FillCells(str(key), CELL_DIM *
                                              xp, CELL_DIM*yp)
                                    isClicked = False

                refreshDisplay()
                if isClicked == True:
                    drawBox(MOUSE_POSX, MOUSE_POSY)

                # drawFooter(strikes, play_time)
        if gameOver or showSoln:
            pass
        else:
            drawFooter(strikes, play_time)
        if hover:
            changeBtn()
        pygame.display.update()
        FPS_TICK.tick(FPS)


if __name__ == "__main__":
    main()
