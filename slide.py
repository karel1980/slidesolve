import sys, copy
board = [ [1,2,2,3], [1,2,2,3], [4,4,5,5], [6,7,7,8], [9,0,0,10] ]

solution = (2, (1, 3)) # block 2 topleft at position (1,3)

def print_board(board):
  for row in board:
    print row
  print  

def read_blocks(board):
  blocks = {}

  for row in range(len(board)):
    for col in range(len(board[row])):
      n = board[row][col]
      if not blocks.has_key(n):
        blocks[n] = { 'tl': (col,row), 'mask': [ (0,0) ] }
      else:
        blocks[n]['mask'].append((col - blocks[n]['tl'][0], row - blocks[n]['tl'][1]))

  return blocks

blocks = read_blocks(board)
boardlist = [ board ]
movelist = []
del blocks[0]

print blocks

def solve(movelist, boardlist, blocks):
  # stop loops
  if (len(boardlist) > 1):
    for b in boardlist[:-1]:
      if b == boardlist[-1]:
        #print "loopy: ", boardlist[-1]
        return False

  #print_board(boardlist[-1])
  # check solution
  if solved(boardlist[-1], blocks):
    print "solved"
    print_solution(movelist, boardlist)
    return True
    
  moves = []
  for b in blocks.keys():
    check_add_move(moves, board, blocks, b, (-1,0))
    check_add_move(moves, board, blocks, b, (1,0))
    check_add_move(moves, board, blocks, b, (0,-1))
    check_add_move(moves, board, blocks, b, (0,1))

  for m in moves:
    do_move(movelist, boardlist, blocks, m)
    if solve(movelist, boardlist, blocks):
      return True
    undo_move(movelist, boardlist, blocks)

  return False

def solved(board, blocks):
  return blocks[solution[0]]['tl'] == solution[1]

def print_solution(movelist):
  print movelist
  
def check_add_move(moves, board, blocks, b, move):
  block = blocks[b]
  # check for out-of-boundaries with other blocks
  for i in range(len(block['mask'])):
      bcell = (block['tl'][0] + block['mask'][i][0] + move[0], block['tl'][1] + block['mask'][i][1] + move[1])
      if bcell[1] not in range(len(board)):
        return
      if bcell[0] not in range(len(board[bcell[1]])):
        return
  
  # check for overlaps with other blocks
  ntl = (block['tl'][0] + move[0], block['tl'][1] + move[1])
  for o in blocks.keys():
    if o != b:
      other = blocks[o]
      #print
      #print "comparing block ", b, " with ", o,
      #print blocks[b],
      #print blocks[o],
      for bc in block['mask']:
        for oc in other['mask']:
          x1,y1 = ntl[0] + bc[0], ntl[1] + bc[1]
          x2,y2 = other['tl'][0] + oc[0], other['tl'][1] + oc[1]
          if x1 == x2 and y1 == y2:
            #print "overlap"
            return

  #print "valid move: ", (b, move)
  moves.append((b, move))

def do_move(movelist, boardlist, blocks, move):
  movelist.append(move)
  board = copy.deepcopy(boardlist[-1])

  #remove the block from the board
  for i in range(len(board)):
    for j in range(len(board[i])):
      if board[i][j] == move[0]: 
        board[i][j] = 0
  
  #update the block
  tl = blocks[move[0]]['tl']
  tl = (tl[0] + move[1][0], tl[1] + move[1][1])
  blocks[move[0]]['tl'] = tl

  #put the block back on the board
  block = blocks[move[0]]
  for cell in block['mask']:
    board[block['tl'][1] + cell[1]][block['tl'][0] + cell[0]] = move[0]
    
  boardlist.append(board)

def undo_move(movelist, boardlist, blocks):
  m = movelist[-1]
  del movelist[-1]
  del boardlist[-1]
  tl = blocks[m[0]]['tl']
  tl = tl[0] - m[1][0], tl[1] - m[1][1]
  blocks[m[0]]['tl'] = tl

solve(movelist, boardlist, blocks)
