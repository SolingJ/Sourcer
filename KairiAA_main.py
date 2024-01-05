import pygame as p
import KairiAA_engine

SQUARE_SIZE = 60

BOARD_WIDTH = 420
BOARD_HEIGHT = 480
MAX_FPS = 24

IMAGES = {}
COLORS = ["#000000", "#FFFFFF"]

def load_images():
  pieces = ["gC", "gK", "gN", "gP", "gT", "gX", "sC", "sK", "sN", "sP", "sT", "sX", "sG", "gG", "sA", "sB", "gA", "gB"]
  for piece in pieces:
    IMAGES[piece] = p.transform.scale(p.image.load('pieces/' + piece + '.png'), (SQUARE_SIZE, SQUARE_SIZE * 0.95))

def main():
  p.init()
  screen = p.display.set_mode((BOARD_WIDTH,BOARD_HEIGHT))
  clock = p.time.Clock()
  load_images()
  gs = KairiAA_engine.Game_Status()
  valid_moves = gs.get_valid_moves()

  flg_running = True

  player_click = []
  square_clicked = ''

  while(flg_running):
    for e in p.event.get():
      if e.type == p.QUIT:
        flg_running = False

      elif e.type == p.KEYDOWN:
        if e.key == p.K_s:
          gs.undo_move()
          valid_moves = gs.get_valid_moves()

      elif e.type == p. MOUSEBUTTONDOWN:
        # クリックした場所の把握
        location = p.mouse. get_pos()
        col = location[0] // SQUARE_SIZE
        row = location [1] // SQUARE_SIZE
        print (location[0], location[1], row, col)

        if square_clicked == str(row) + str(col):
          square_clicked = ''
          player_click = []

        #空白をクリック
        elif len(player_click) == 0 and gs.board[row][col][0] == 's' and not gs.sente_to_move:
          square_clicked = ''
          player_click = []
          print("gote no turn")

        elif len(player_click) == 0 and gs.board[row][col][0] == 'g' and  gs.sente_to_move:
          square_clicked = ''
          player_click = []
          print("sente no turn")


        elif len(player_click) == 0 and gs.board[row][col] == '--':
          square_clicked = ''
          player_click = []
          print("sente no turn")




        else:
          square_clicked = str(row)+str(col)
          player_click.append(square_clicked)
          print('player_click = ', player_click)

        if len(player_click) == 2:
          if(check_valid_moves(player_click[0],player_click[1], valid_moves)): #後でcheck validを実装する
            gs.make_move(player_click[0], player_click[1])
            player_click = []
            square_clicked = ''
            valid_moves = gs.get_valid_moves()

          else:
            player_click = [square_clicked]


    draw_game_status(screen, gs, valid_moves, square_clicked)

    if gs.mate:
      flg_gameover = True
      if(gs.sente_to_move):
        text = "Gote Wins!"
      else:
        text = "Sente Wins!"

      draw_message(screen, text)

    clock.tick(MAX_FPS)
    p.display.flip()

def draw_message(screen,  text):
  path = "/Users/komaiakiranozomi/Library/NXWine/prefixies/default/drive_c/Program Files/AV Voice Changer 8.0 Diamond/demo/fonts/msgothic.ttc"
  font = p.font.Font(path, 50)
  textObject = font.render(text, 0, p.Color('red'))
  x_length = BOARD_WIDTH / 2 - textObject.get_width()/2
  y_length = BOARD_HEIGHT / 2 - textObject.get_height()/2
  txtlocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(x_length, y_length)
  screen.blit(textObject, txtlocation)


def draw_game_status(screen, gs, valid_moves, square_clicked):
  draw_board(screen)
  draw_pieces(screen,gs.board)
  draw_squares_color(screen, gs, valid_moves, square_clicked)

def draw_board(screen):
  for r in range(8):
    for c in range(7):
      color =COLORS[(r+c)%2]
      p.draw.rect(screen, color, p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE,SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen, board):
  for r in range(8):
    for c in range(7):
      piece = board[r][c]
      if(piece != '--'):
        screen.blit(IMAGES[piece], p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def check_valid_moves(move_start, move_end, valid_moves):
  if not valid_moves:
    return False

  for move in valid_moves:
    if move[0] == move_start and move[1] == move_end:
      return True

  return False


def draw_squares_color(screen, gs, valid_moves, square_clicked):
  if square_clicked != '':
    row = int(square_clicked[0])
    col = int(square_clicked[1])
    if (gs.board[row][col][0] == "s" and gs.sente_to_move) or (gs.board[row][col][0] == "g" and not gs.sente_to_move):
      s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
      s.set_alpha(150)
      s.fill(p.Color('blue'))
      screen.blit(s, (480, 420))
      s.fill(p.Color("orange"))
      for move in valid_moves:
        if move[0] == square_clicked:
          col_highlight = int(move[1][1])
          row_highlight = int(move[1][0])
          screen.blit(s, (col_highlight*SQUARE_SIZE, row_highlight * SQUARE_SIZE))





if __name__ == '__main__':
  main()
