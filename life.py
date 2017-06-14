import numpy as np
from matplotlib import pyplot as plt
from asciimatics.event import KeyboardEvent, MouseEvent
from asciimatics.screen import Screen


def init_board(width: int, height: int) -> np.ndarray:
    return np.random.randint(0,2, size=(width, height), dtype=np.bool_)


def evolve_board(board: np.ndarray):
    int_board = board.astype(np.int)
    neighbours = int_board[0:-2, 0:-2] + int_board[0:-2, 1:-1] + int_board[0:-2, 2:] + \
                 int_board[1:-1, 0:-2] + int_board[1:-1, 2:] + \
                 int_board[2:  , 0:-2] + int_board[2:  , 1:-1] + int_board[2:  , 2:]

    birth = (neighbours == 3) & (int_board[1:-1, 1:-1] == 0)
    survive = ((neighbours == 2) | (neighbours == 3)) & (int_board[1:-1, 1:-1] == 1)
    new_board = np.zeros_like(int_board)
    new_board[1:-1, 1:-1][birth | survive] = 1
    return new_board.astype(np.bool_)


def show_board_img(board: np.ndarray):
    size = np.array(board.shape)
    dpi = 72.0
    figsize = size[1] / float(dpi), size[0] / float(dpi)
    fig = plt.figure(figsize=figsize, dpi=dpi, facecolor="white")
    fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False)
    plt.imshow(board, interpolation='nearest', cmap=plt.cm.gray_r)
    plt.xticks([]), plt.yticks([])
    plt.show()


def show_board(board: np.ndarray, screen):
    for i, row in enumerate(board):
        screen.print_at(''.join([f"{'■' if alive else ' ': ^2}" for alive in row]), 0, i)
    screen.refresh()



from time import sleep
np.random.seed(999)

def draw(screen):
    board = init_board(64, 64)

    while True:
        sleep(0.05)
        show_board(board, screen)
        board = evolve_board(board)

        # Key
        event = screen.get_event()
        if isinstance(event, KeyboardEvent):
            if event.key_code in (ord('Q'), ord('q')):
                return

        elif isinstance(event, MouseEvent):
            if event.buttons & MouseEvent.LEFT_CLICK != 0:
                y = event.y
                x = event.x // 2
                if y in range(board.shape[0]) and x in range(board.shape[1]):
                    board[y, x]=1


if __name__ == "__main__":
    Screen.wrapper(draw)