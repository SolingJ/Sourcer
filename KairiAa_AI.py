import random
import KairiAA_piece as ps


MAX_VALUE =50000
MIN_VALUE = -MAX_VALUE
DEPTH = 2
BEST_RATE = 0.95
import time


def get_AI_move(gs, valid_moves):

  score, next_move = get_Minimax_move(gs, valid_moves, DEPTH,  gs.sente_to_move)
  print("AI score: " + str(score))
  return score, next_move

  next_move = valid_moves[0]
  if(gs.sente_to_move):
    max_score = MIN_VALUE
    for move in valid_moves:
      gs.make_move(move[0], move[1])
      score,_ = get_Minimax_move(gs, valid_moves, DEPTH, True)
      if score > max_score and True_by_probability(0.9):
        max_score = score
        next_move = move
      gs.undo_move()
  else:
      min_score = MAX_VALUE
      for move in valid_moves:
        gs.make_move(move[0], move[1])
        score, _ = get_Minimax_move(gs, valid_moves, DEPTH, False)
        if score < min_score and True_by_probability(0.9):
          min_score = score
          next_move = move
        gs.undo_move()
      print('chess_ai', min_score, next_move)

  return next_move
def get_Minimax_move(gs, valid_moves, depth, sente_and_gote):

  next_move = ''
  if depth == 0:
    return get_board_score(gs)

  if len(valid_moves) == 0:
    if gs.mate:
      if gs.sente_to_move:
        return MIN_VALUE
      else:
        return MAX_VALUE

    else:
      return 0


  if(sente_and_gote):
    max_score = MIN_VALUE
    for move in valid_moves:
      gs.make_move(move[0], move[1])
      if depth > 1:
        next_moves = gs.get_valid_moves()
      else:
        next_moves = []
      score = get_Minimax_move(gs, next_moves, depth-1, False)
      if score > max_score and True_by_probability(BEST_RATE):
        max_score = score
        if(depth == DEPTH):
          next_move = move
      gs.undo_move()

    if(depth == DEPTH):
      return max_score, next_move
    else:
      return max_score


  else:
    min_score = MAX_VALUE
    for move in valid_moves:
      gs.make_move(move[0], move[1])
      if depth > 1:
        next_moves = gs.get_valid_moves()
      else:
        next_moves = []
      score = get_Minimax_move(gs, next_moves, depth-1, True)
      if score < min_score and True_by_probability(BEST_RATE):
        min_score = score
        if(depth == DEPTH):
          next_move = move
      gs.undo_move()

    if(depth == DEPTH):
        return min_score, next_move
    else:
        return min_score





PIECE_TYPE_SQUARE = {'K': 1000, 'P':6, 'N':10, 'X':6, 'B':9, 'T':1, 'A':5, 'C':3, 'G':4,}

def get_board_score_piece_count(gs):
  score_sente = 0
  score_gote = 0

  score = 0

  for row in range(len(gs.board)):
    for col in range(len(gs.board[row])):
      square = gs.board[row][col]
      if square[0] == 's':
        score += PIECE_TYPE_SQUARE[square[1]]
      elif square[0] == 'g':
        score -= PIECE_TYPE_SQUARE[square[1]]

  return score


def get_board_score(gs):

  score = 0
  for row in range(len(gs.board)):
    for col in range(len(gs.board[row])):
      square = gs.board[row][col]
      score_piece_position = 0
      if (not square[1] in ps.Sente_to_gote_ga_chigau and square[1] != '-'):
        score_piece_position = ps.scores[square[1]][row][col]
      elif ( square[1] in ps.Sente_to_gote_ga_chigau):
        score_piece_position = ps.scores[square][row][col]

      if(square[0] == 's'):
        score += score_piece_position
      elif(square[0] == 'g'):
        score -= score_piece_position

  return score

def True_by_probability(p):
  x = random.random()
  return True if (x<p) else False