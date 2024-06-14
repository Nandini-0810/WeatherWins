import streamlit as st
import numpy as np

# Function to check for a winner
def check_winner(board):
    for i in range(3):
        if np.all(board[i, :] == board[i, 0]) and board[i, 0] != "":
            return board[i, 0]
        if np.all(board[:, i] == board[0, i]) and board[0, i] != "":
            return board[0, i]
    if board[0, 0] == board[1, 1] == board[2, 2] != "":
        return board[0, 0]
    if board[0, 2] == board[1, 1] == board[2, 0] != "":
        return board[0, 2]
    return None



# Function to handle a player's move
def make_move(row, col):
    if st.session_state.board[row, col] == "" and st.session_state.winner is None:
        st.session_state.board[row, col] = st.session_state.current_player
        st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"
        st.session_state.winner = check_winner(st.session_state.board)

