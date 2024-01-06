class Game_Status():
  def __init__(self):
    #先手：Sente, 後手：Gote
    self.board = [
      ["gN", "gX", "gP", "gK", "gP", "gX", "gC"],
      ["--", "gC", "--", "--", "--", "gN", "--"],
      ["gT", "gT", "gT", "gT", "gT", "gT", "gT"],
      ["--", "--", "--", "--", "--", "--", "--"],
      ["--", "--", "--", "--", "--", "--", "--"],
      ["sT", "sT", "sT", "sT", "sT", "sT", "sT"],
      ["--", "sN", "--", "--", "--", "sC", "--"],
      ["sC", "sX", "sP", "sK", "sP", "sX", "sN"],
      ]
    self.senteKingLocation = "73"
    self.goteKingLocation = "03"

    self.counter = 0
    self.sente_to_move = True
    self.moveLog = []

  def make_move(self, move_start, move_end):
    start_row = int(move_start[0])
    start_col = int(move_start[1])

    end_row = int(move_end[0])
    end_col = int(move_end[1])

    piece_moved= self.board[start_row][start_col]
    piece_captured = self.board[end_row][end_col]
    self.board[start_row][start_col] = '--'
    self.board[end_row][end_col] = piece_moved
    self.sente_to_move = not self.sente_to_move

    self.moveLog.append([start_row, start_col, end_row, end_col, piece_moved, piece_captured])
    #print("The Player moved a piece from " + str(start_row) + str(start_col) +" to "+ str(end_row)+str(end_col) )

    self.counter += 1

    if(piece_moved == 'sT' and end_row == 2) or (piece_moved == 'gT' and end_row == 5) :
      self.board[end_row][end_col] = self.board[end_row][end_col][0] + "G"

    if(piece_moved == 'sC' and end_row <= 2) or (piece_moved == 'gC' and end_row >= 5) :
      self.board[end_row][end_col] = self.board[end_row][end_col][0] + "A"

    if(piece_moved == 'sX' and end_row <= 2) or (piece_moved == 'gX' and end_row >= 5) :
      self.board[end_row][end_col] = self.board[end_row][end_col][0] + "B"



    if piece_moved == "sK":
      self.senteKingLocation = str(end_row) + str(end_col)
    elif piece_moved == "gK":
      self.goteKingLocation = str(end_row) + str(end_col)


    self.mate = False




  def undo_move(self,):
    if(len(self.moveLog) != 0):
      move = self.moveLog.pop()
      self.board[move[0]][move[1]] = move[4]
      self.board[move[2]][move[3]] = move[5]
      self.sente_to_move = not self.sente_to_move
      if move[4] == "sK":
        self.senteKingLocation = str(move[0]) + str(move[1])
      elif move[4] == "gK":
        self.goteKingLocation =str(move[0]) + str(move[1])



  def get_valid_moves(self):
    moves = self.get_all_possible_moves()

    self.remove_invalid_moves(moves)

    if(len(moves) == 0):
      self.mate = True
    else:
      self.mate = False

    return moves

  def remove_invalid_moves(self, moves):
    for i in range(len(moves)-1, -1, -1):
      move = moves[i]
      self.make_move(move[0], move[1])
      self.sente_to_move = not self.sente_to_move
      if(self.confirm_check()):
        moves.remove(moves[i])
      self.sente_to_move = not self.sente_to_move
      self.undo_move()

  def confirm_check(self):
    if self.sente_to_move:
      king_location = self.senteKingLocation
    else:
      king_location = self.goteKingLocation
    return self.confirm_attack(king_location)

  def confirm_attack(self, square):
    self.sente_to_move = not self.sente_to_move
    opp_moves = self.get_all_possible_moves()
    self.sente_to_move = not self.sente_to_move
    for move in opp_moves:
      if(move[1] == square):
        return True
    return False


  def get_all_possible_moves(self):
    moves = []
    for row in range(len(self.board)):
      for col in range(len(self.board[row])):
        piece_color = self.board[row][col][0]
        piece_type = self.board[row][col][1]
        if (piece_color == "s" and  self.sente_to_move) or (piece_color == "g" and not self.sente_to_move):
          if(piece_type == "T"):
            self.get_Teng_moves(row, col, moves)
          if(piece_type == "G"):
            self.get_Gaay_moves(row, col, moves)
          if(piece_type == "C"):
            self.get_CHAA_moves(row, col, moves)
          if(piece_type == "A"):
            self.get_Ak_moves(row, col, moves)
          if(piece_type == "K"):
            self.get_Krung_moves(row, col, moves)
          if(piece_type == "N"):
            self.get_Naay_moves(row, col, moves)
          if(piece_type == "P"):
            self.get_Poi_moves(row, col, moves)
          if(piece_type == "X"):
            self.get_Xun_moves(row, col, moves)
          if(piece_type == "B"):
            self.get_Bong_moves(row, col, moves)



    return moves


  #Tengは歩に相当する駒．プロモーションゾーンに入ると候(Gaay)に強制的に成る．
  def get_Teng_moves(self, row, col, moves):
    if self.sente_to_move:
      row_adj = -1
      opp_piece = 'g'
    else:
      row_adj = 1
      opp_piece = 's'

    if row >0 and row < 7:
      end_row = row + row_adj
      end_col = col

      if(self.board[end_row][end_col][0] == opp_piece or self.board[end_row][end_col] == '--' ):
        move = (str(row)+str(col), str(end_row)+str(end_col))
        moves.append(move)

  def get_Gaay_moves(self, row, col, moves):
    if self.sente_to_move:
      row_adj = 1
      col_adj = 1
      opp_piece = 'g'
    else:
      row_adj = 1
      col_adj = 1
      opp_piece = 's'

    #前に進む場合
    if row >=0 and row < 7:
      end_row = row + row_adj
      end_col = col

      if(self.board[end_row][end_col][0] == opp_piece or self.board[end_row][end_col] == '--' ):
        move = (str(row)+str(col), str(end_row)+str(end_col))
        moves.append(move)

    #後ろに進む場合
    if row >0 and row <= 7:
      end_row = row - row_adj
      end_col = col

      if(self.board[end_row][end_col][0] == opp_piece or self.board[end_row][end_col] == '--' ):
        move = (str(row)+str(col), str(end_row)+str(end_col))
        moves.append(move)

    #右に進む場合
    if col >=0 and col < 6:
      end_row = row
      end_col = col + col_adj

      if(self.board[end_row][end_col][0] == opp_piece or self.board[end_row][end_col] == '--' ):
        move = (str(row)+str(col), str(end_row)+str(end_col))
        moves.append(move)


    #左に進む場合
    if col >0 and col <= 6:
      end_row = row
      end_col = col - col_adj

      if(self.board[end_row][end_col][0] == opp_piece or self.board[end_row][end_col] == '--' ):
        move = (str(row)+str(col), str(end_row)+str(end_col))
        moves.append(move)

  #槍．
  def get_CHAA_moves(self, row, col, moves):
    if self.sente_to_move:
      row_adj = -2
      col_adj = 2
      front = -1
      opp_piece = 'g'
    else:
      row_adj = 2
      col_adj = 2
      front = 1
      opp_piece = 's'

    #前に進む場合
    if row >= 1 and row <= 6:
      end_row = row + row_adj
      end_col = col

      if(self.board[end_row][end_col] == '--' and self.board[end_row-front][end_col] == '--'):
        move = (str(row)+str(col), str(end_row)+str(end_col))
        moves.append(move)

    #右に進む場合
    if col <= 4:
      end_row = row
      end_col = col + col_adj

      if(self.board[end_row][end_col] == '--' and self.board[end_row][col+1] == '--'):
        move = (str(row)+str(col), str(end_row)+str(end_col))
        moves.append(move)

    #左に進む場合
    if col >= 2:
      end_row = row
      end_col = col - col_adj

      if(self.board[end_row][end_col] == '--' and self.board[end_row][col-1] == '--'):
        move = (str(row)+str(col), str(end_row)+str(end_col))
        moves.append(move)

    ##前側の駒を取る場合
    if (opp_piece == 'g' and row >= 1) or (opp_piece == 's' and row <= 6):
      if(col <= 5 and self.board[row+front][col+1][0] == opp_piece):
        move = (str(row)+str(col), str(row+front)+str(col+1))
        moves.append(move)
      if(col >= 1 and self.board[row+front][col-1][0] == opp_piece):
        move = (str(row)+str(col), str(row+front)+str(col-1))
        moves.append(move)




  def get_Ak_moves(self, row, col, moves):
    if self.sente_to_move:
      row_adj = -2
      col_adj = 2
      front = -1
      opp_piece = 'g'
    else:
      row_adj = 2
      col_adj = 2
      front = 1
      opp_piece = 's'

    #前に進む場合
    if row >= 1 and row <= 6:
      end_row = row + row_adj
      end_col = col

      if(is_in_row(end_row) and self.board[end_row][end_col] == '--' and is_in_row(end_row-front) and self.board[end_row-front][end_col] == '--'):
        move = (str(row)+str(col), str(end_row)+str(end_col))
        moves.append(move)

    #右に進む場合
    if col <= 4:
      end_row = row
      end_col = col + col_adj

      if(is_in_col(end_row) and self.board[end_row][end_col] == '--' and self.board[end_row][col+1] == '--'):
        move = (str(row)+str(col), str(end_row)+str(end_col))
        moves.append(move)

    #左に進む場合
    if col >= 2:
      end_row = row
      end_col = col - col_adj

      if(self.board[end_row][end_col] == '--' and self.board[end_row][col-1] == '--'):
        move = (str(row)+str(col), str(end_row)+str(end_col))
        moves.append(move)

    ##前側の駒を取る場合
    if (opp_piece == 'g' and row >= 1) or (opp_piece == 's' and row <= 6):
      if(col <= 5 and self.board[row+front][col+1][0] == opp_piece):
        move = (str(row)+str(col), str(row+front)+str(col+1))
        moves.append(move)
      if(col >= 1 and self.board[row+front][col-1][0] == opp_piece):
        move = (str(row)+str(col), str(row+front)+str(col-1))
        moves.append(move)

    ##後ろの駒を取る場合
    if (opp_piece == 'g' and row <= 6) or (opp_piece == 's' and row >= 1):
      if(col <= 5 and self.board[row-front][col+1][0] == opp_piece):
        move = (str(row)+str(col), str(row-front)+str(col+1))
        moves.append(move)
      if(col >= 1 and self.board[row-front][col-1][0] == opp_piece):
        move = (str(row)+str(col), str(row-front)+str(col-1))
        moves.append(move)

  def get_Krung_moves(self, row, col, moves):
    if row > 0 and col > 0:
      end_row = row-1
      end_col = col-1

      if(not self.board[end_row][end_col][0] == self.board[row][col][0]):
        move = (str(row)+str(col), str(end_row)+str(end_col))
        moves.append(move)

    if row > 0:
      end_row = row-1
      end_col = col

      if(not self.board[end_row][end_col][0] == self.board[row][col][0]):
        move = (str(row)+str(col), str(end_row)+str(end_col))
        moves.append(move)

    if row > 0 and col < 6:
      end_row = row-1
      end_col = col+1

      if(not self.board[end_row][end_col][0] == self.board[row][col][0]):
        move = (str(row)+str(col), str(end_row)+str(end_col))
        moves.append(move)

    if row <7:
      end_row = row+1
      end_col = col

      if(not self.board[end_row][end_col][0] == self.board[row][col][0]):
        move = (str(row)+str(col), str(end_row)+str(end_col))
        moves.append(move)


    if row < 7 and col<6:
      end_row = row+1
      end_col = col+1

      if(not self.board[end_row][end_col][0] == self.board[row][col][0]):
        move = (str(row)+str(col), str(end_row)+str(end_col))
        moves.append(move)

    if row <7 and col > 0:
      end_row = row+1
      end_col = col-1

      if(not self.board[end_row][end_col][0] == self.board[row][col][0]):
        move = (str(row)+str(col), str(end_row)+str(end_col))
        moves.append(move)

    if col > 0:
      end_row = row
      end_col = col-1

      if(not self.board[end_row][end_col][0] == self.board[row][col][0]):
        move = (str(row)+str(col), str(end_row)+str(end_col))
        moves.append(move)

    if col < 6:
      end_row = row
      end_col = col+1

      if(not self.board[end_row][end_col][0] == self.board[row][col][0]):
        move = (str(row)+str(col), str(end_row)+str(end_col))
        moves.append(move)

  def get_Poi_moves(self, row, col, moves):
    sente_mae = -1
    gote_mae = 1
    if row > 0 and col > 0:
      end_row = row-1
      end_col = col-1

      if( self.board[row][col][0] == 's' and end_row >= 5) or( self.board[row][col][0] == 'g' and end_row <= 2):
        if(not self.board[end_row][end_col][0] == self.board[row][col][0]):
          move = (str(row)+str(col), str(end_row)+str(end_col))
          moves.append(move)

    if row > 0:
      end_row = row-1
      end_col = col
      if( self.board[row][col][0] == 's' and end_row >= 5) or( self.board[row][col][0] == 'g' and end_row <= 2):
        if(not self.board[end_row][end_col][0] == self.board[row][col][0]):
          move = (str(row)+str(col), str(end_row)+str(end_col))
          moves.append(move)

    if row > 0 and col < 6:
      end_row = row-1
      end_col = col+1
      if( self.board[row][col][0] == 's' and end_row >= 5) or( self.board[row][col][0] == 'g' and end_row <= 2):
        if(not self.board[end_row][end_col][0] == self.board[row][col][0]):
          move = (str(row)+str(col), str(end_row)+str(end_col))
          moves.append(move)

    if row <7:
      end_row = row+1
      end_col = col
      if( self.board[row][col][0] == 's' and end_row >= 5) or( self.board[row][col][0] == 'g' and end_row <= 2):
        if(not self.board[end_row][end_col][0] == self.board[row][col][0]):
          move = (str(row)+str(col), str(end_row)+str(end_col))
          moves.append(move)


    if row < 7 and col<6:
      end_row = row+1
      end_col = col+1
      if( self.board[row][col][0] == 's' and end_row >= 5) or( self.board[row][col][0] == 'g' and end_row <= 2):

        if(not self.board[end_row][end_col][0] == self.board[row][col][0]):
          move = (str(row)+str(col), str(end_row)+str(end_col))
          moves.append(move)

    if row <7 and col > 0:
      end_row = row+1
      end_col = col-1
      if( self.board[row][col][0] == 's' and end_row >= 5) or( self.board[row][col][0] == 'g' and end_row <= 2):

        if(not self.board[end_row][end_col][0] == self.board[row][col][0]):
          move = (str(row)+str(col), str(end_row)+str(end_col))
          moves.append(move)

    if col > 0:
      end_row = row
      end_col = col-1
      if( self.board[row][col][0] == 's' and end_row >= 5) or( self.board[row][col][0] == 'g' and end_row <= 2):

        if(not self.board[end_row][end_col][0] == self.board[row][col][0]):
          move = (str(row)+str(col), str(end_row)+str(end_col))
          moves.append(move)

    if col < 6:
      end_row = row
      end_col = col+1
      if( self.board[row][col][0] == 's' and end_row >= 5) or( self.board[row][col][0] == 'g' and end_row <= 2):
        if(not self.board[end_row][end_col][0] == self.board[row][col][0]):
          move = (str(row)+str(col), str(end_row)+str(end_col))
          moves.append(move)


  def get_Naay_moves(self, row, col, moves):
    for row_num in range(row-1, -1, -1):
      end_row = row_num
      end_col = col

      if self.board[end_row][end_col] == '--':
        move = (str(row)+str(col), str(end_row)+str(end_col))
        moves.append(move)
      elif self.board[end_row][end_col][0] == self.board[row][col][0]:
        break
      else:
        move = (str(row)+str(col), str(end_row)+str(end_col))
        moves.append(move)
        break

    for row_num in range(row+1, 8):
          end_row = row_num
          end_col = col

          if self.board[end_row][end_col] == '--':
            move = (str(row)+str(col), str(end_row)+str(end_col))
            moves.append(move)
          elif self.board[end_row][end_col][0] == self.board[row][col][0]:
            break
          else:
            move = (str(row)+str(col), str(end_row)+str(end_col))
            moves.append(move)
            break

    for col_num in range(col+1, 7):
          end_row = row
          end_col = col_num

          if self.board[end_row][end_col] == '--':
            move = (str(row)+str(col), str(end_row)+str(end_col))
            moves.append(move)
          elif self.board[end_row][end_col][0] == self.board[row][col][0]:
            break
          else:
            move = (str(row)+str(col), str(end_row)+str(end_col))
            moves.append(move)
            break

    for col_num in range(col-1, -1, -1):
          end_row = row
          end_col = col_num

          if self.board[end_row][end_col] == '--':
            move = (str(row)+str(col), str(end_row)+str(end_col))
            moves.append(move)
          elif self.board[end_row][end_col][0] == self.board[row][col][0]:
            break
          else:
            move = (str(row)+str(col), str(end_row)+str(end_col))
            moves.append(move)
            break

    if(self.board[row][col][0] == 's' and row <= 2) or (self.board[row][col][0] == 'g' and row >= 5) :
      self.get_bishop_moves(row, col, moves)

  def get_bishop_moves(self, row, col, moves):
    for row_num in range(row-1, -1, -1):
      if(col+row-row_num<7):
          end_row = row_num
          end_col = col+row-row_num
          if self.board[end_row][end_col] == '--':
            move = (str(row)+str(col), str(end_row)+str(end_col))
            moves.append(move)
          elif self.board[end_row][end_col][0] == self.board[row][col][0]:
            break
          else:
            move = (str(row)+str(col), str(end_row)+str(end_col))
            moves.append(move)
            break

    for row_num in range(row+1, 8):
      if(col+row-row_num>=0):
        end_row = row_num
        end_col = col+row-row_num
        if self.board[end_row][end_col] == '--':
          move = (str(row)+str(col), str(end_row)+str(end_col))
          moves.append(move)
        elif self.board[end_row][end_col][0] == self.board[row][col][0]:
          break
        else:
          move = (str(row)+str(col), str(end_row)+str(end_col))
          moves.append(move)
          break

    for row_num in range(row+1, 8):
      if(col-row+row_num<7):
          end_row = row_num
          end_col = col-row+row_num
          if self.board[end_row][end_col] == '--':
            move = (str(row)+str(col), str(end_row)+str(end_col))
            moves.append(move)
          elif self.board[end_row][end_col][0] == self.board[row][col][0]:
            break
          else:
            move = (str(row)+str(col), str(end_row)+str(end_col))
            moves.append(move)
            break

    for row_num in range(row-1, -1, -1):
      if(col-row+row_num>=0):
        end_row = row_num
        end_col = col-row+row_num
        if self.board[end_row][end_col] == '--':
          move = (str(row)+str(col), str(end_row)+str(end_col))
          moves.append(move)
        elif self.board[end_row][end_col][0] == self.board[row][col][0]:
          break
        else:
          move = (str(row)+str(col), str(end_row)+str(end_col))
          moves.append(move)
          break



  def get_Xun_moves(self, row, col, moves):
    if self.sente_to_move:
      row_adj = -2
      col_adj = 2
      front = -1
      opp_piece = 'g'
      self_piece = 's'
    else:
      row_adj = 2
      col_adj = 2
      front = 1
      opp_piece = 's'
      self_piece = 'g'

    end_row = row + row_adj
    end_col = col + 1

    if(is_in_row(end_row) and is_in_col(end_col) and self.board[end_row][end_col][0] != self_piece):
      move = (str(row)+str(col), str(end_row)+str(end_col))
      moves.append(move)

    end_row = row + row_adj
    end_col = col - 1

    if(is_in_row(end_row) and is_in_col(end_col) and self.board[end_row][end_col][0] != self_piece):
      move = (str(row)+str(col), str(end_row)+str(end_col))
      moves.append(move)


  def get_Bong_moves(self, row, col, moves):
    if self.sente_to_move:
      row_adj = -2
      col_adj = 2
      front = -1
      opp_piece = 'g'
      self_piece = 's'
    else:
      row_adj = 2
      col_adj = 2
      front = 1
      opp_piece = 's'
      self_piece = 'g'

    self.get_Xun_moves(row, col, moves)

    end_row = row + 1
    end_col = col + 2

    if(is_in_row(end_row) and is_in_col(end_col) and self.board[end_row][end_col][0] != self_piece):
      move = (str(row)+str(col), str(end_row)+str(end_col))
      moves.append(move)

    end_row = row - 1
    end_col = col + 2

    if(is_in_row(end_row) and is_in_col(end_col) and self.board[end_row][end_col][0] != self_piece):
      move = (str(row)+str(col), str(end_row)+str(end_col))
      moves.append(move)

    end_row = row + 1
    end_col = col - 2

    if(is_in_row(end_row) and is_in_col(end_col) and self.board[end_row][end_col][0] != self_piece):
      move = (str(row)+str(col), str(end_row)+str(end_col))
      moves.append(move)

    end_row = row - 1
    end_col = col - 2

    if(is_in_row(end_row) and is_in_col(end_col) and self.board[end_row][end_col][0] != self_piece):
      move = (str(row)+str(col), str(end_row)+str(end_col))
      moves.append(move)


    end_row = row - row_adj
    end_col = col - 1

    if(is_in_row(end_row) and is_in_col(end_col) and self.board[end_row][end_col][0] != self_piece):
      move = (str(row)+str(col), str(end_row)+str(end_col))
      moves.append(move)

    end_row = row - row_adj
    end_col = col + 1

    if(is_in_row(end_row) and is_in_col(end_col) and self.board[end_row][end_col][0] != self_piece):
      move = (str(row)+str(col), str(end_row)+str(end_col))
      moves.append(move)









def is_in_row(row):
  return 0 <= row and row <= 7

def is_in_col(row):
  return 0 <= row and row <= 6
