import socket

HOST = "127.0.0.1"
PORT = 7878

board = """
_ _ _
_ _ _
_ _ _"""


def print_current_board():
    print(board)


def get_users_move():
    move = int(input("Enter your move : "))
    return move


def update_game_state(player, move, w):
    global board
    i = (move - 1) * 2 + 1
    board = board[:i] + w + board[i + 1 :]
    print(player + " played move:", move)


def has_game_ended(b):
    def i(x):
        return (x - 1) * 2 + 1

    if (
        b[i(1)] == b[i(2)] == b[i(3)] != "_"
        or b[i(4)] == b[(5)] == b[i(6)] != "_"
        or b[i(7)] == b[i(8)] == b[i(9)] != "_"
    ):
        return True
    elif (
        b[i(1)] == b[i(4)] == b[i(7)] != "_"
        or b[i(2)] == b[i(5)] == b[i(8)] != "_"
        or b[i(3)] == b[i(6)] == b[i(9)] != "_"
    ):
        return True
    elif b[i(1)] == b[i(5)] == b[i(9)] != "_" or b[i(7)] == b[i(5)] == b[i(3)] != "_":
        return True
    return False


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print("Waiting for players to connect...")
    conn, addr = server_socket.accept()

    print("Connected by", addr)
    print_current_board()
    with conn:
        while True:
            opp_move = int(conn.recv(1024).decode())
            print("opponent played : ")
            update_game_state("opp", opp_move, "O")
            print_current_board()
            if not opp_move:
                break
            if has_game_ended(board):
                print("\nopp has won")
                break

            print("\nYour Chance")
            move = get_users_move()

            update_game_state("user", move, "X")
            print_current_board()
            move = str(move)
            conn.send(move.encode())
            if has_game_ended(board):
                print("\nyou have won")
                break

    print("Game ended")
