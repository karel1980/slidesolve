board = [ [1,2,2,3], [1,2,2,3], [4,4,5,5], [6,7,7,8], [9,0,0,10] ]

blocks = {}

def print_board(board):
  for row in range(len(board)):
    for col in range(len(board[row])):
      n = board[row][col]
      print "%3d  "%n,

      if not blocks.has_key(n):
        blocks[n] = {'tl':(row,col),'mask':[(0,0)]}
      else:
        blocks[n]['mask'].append((row - blocks[n]['tl'][0], col - blocks[n]['tl'][1]))
      
    print

#print_board(board)
#print blocks

movelist = []
opening = blocks[0]
del blocks[0]

def solve(movelist, board, blocks):
  if solved(board,blocks):
    print_all_moves(movelist)
    return True
    
  moves = []
  for b in keys(blocks):
    check_add_move(movelist, moves, b, (-1,0))
    check_add_move(movelist, moves, b, (1,0))
    check_add_move(movelist, moves, b, (0,-1))
    check_add_move(movelist, moves, b, (0,1))

  for m in moves:
    do_move(movelist, board, blocks)
    if solve(movelist, board, blocks):
      return True
    undo_move(movelist, board, blocks)

# TODO: implement 'solved', 'print_solution', 'check_add_move', 'do_move', and  'undo_move'
