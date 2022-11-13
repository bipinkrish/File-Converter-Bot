import random

###########################################################################
# AI

# Random
def selectRandom(board):
    ln = len(board)
    r = random.randrange(0,ln)
    return board[r]

# To check if one of the following patterns are true; then the respective player has won
def win_check(board, choice):
    
    #HORIZONTAL CHECK;
    return ( 
       ( board[1] == choice and board[2] == choice and board[3] == choice )
    or ( board[4] == choice and board[5] == choice and board[6] == choice )
    or ( board[7] == choice and board[8] == choice and board[9] == choice )
    #VERTICAL CHECK;
    or ( board[1] == choice and board[4] == choice and board[7] == choice )
    or ( board[2] == choice and board[5] == choice and board[8] == choice )
    or ( board[3] == choice and board[6] == choice and board[9] == choice )
    #DIAGONAL CHECK;
    or ( board[1] == choice and board[5] == choice and board[9] == choice )
    or ( board[3] == choice and board[5] == choice and board[7] == choice )  )


# Getting Board (like keypad)
def getboard(data,order):
    board = ["N"]
    for i in range(9):
        temp = data[order[i]]
        if temp == "1":
            board.append("X")
        elif temp == "2":
            board.append("O")
        else:
            board.append(" ")
    return board

# AI Function
def CompAI(board):
    position = 0
    possibilities = [x for x, letter in enumerate(board) if letter == ' ' and x != 0]
    
    # including both X and O, since if computer will win, he will place a choice there, but if the component will win --> we have to block that move
    for let in ['O', 'X']:
        for i in possibilities:
            # Creating a copy of the board everytime, placing the move and checking if it wins;
            # Creating a copy like this  and not this boardCopy = board, since changes to boardCopy changes the original board;
            boardCopy = board[:]
            boardCopy[i] = let
            if(win_check(boardCopy, let)):
                position = i
                return position

    openCorners = [x for x in possibilities if x in [1, 3, 7, 9]]
    
    if len(openCorners) > 0:
        position = selectRandom(openCorners)
        return position

    if 5 in possibilities:
        position = 5
        return position

    openEdges = [x for x in possibilities if x in [2, 4, 6, 8]]
    
    if len(openEdges) > 0:
        position = selectRandom(openEdges)
        return position

# Managing in b/w
def getAI(data):
    order = [6,7,8,3,4,5,0,1,2]
    board = getboard(data,order)
    pos = CompAI(board)
    if pos != None:
        return order[pos-1]

###########################################################################
# Checking for Winner

# Converting String into Matrix
def convert(data):
    datalist = []
    temp = []
    for i in range(9):
        if data[i] == '1':
            temp.append("X")
        elif data[i] == "2":
            temp.append("O")
        else:
            temp.append(" ")
        
        if (i+1)%3 == 0:
            datalist.append(temp)
            temp = []
    
    return datalist

# Transposing the Matrix
def transpose(matrix):
    rows = len(matrix)
    columns = len(matrix[0])
    matrix_T = []
    for j in range(columns):
        row = []
        for i in range(rows):
           row.append(matrix[i][j])
        matrix_T.append(row)
    return matrix_T

# (part of CheckWin)
def checkRows(board):
    for row in board:
        if len(set(row)) == 1:
            return row[0]
    return 0

# (part of CheckWin)
def checkDiagonals(board):
    if len(set([board[i][i] for i in range(len(board))])) == 1:
        return board[0][0]
    if len(set([board[i][len(board)-i-1] for i in range(len(board))])) == 1:
        return board[0][len(board)-1]
    return 0

# Checking Winner
def checkWin(board):
    for newBoard in [board, transpose(board)]:
        result = checkRows(newBoard)
        if result:
            return result
    return checkDiagonals(board)

# in b/w 
def check(data):
    res = checkWin(convert(data))
    if res == " " or res == 0:
        return False,0
    else:
        if res == "X":
            return True,1
        elif res == "O":
            return True,2


###########################################################################
# TicTacToe Game

from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton

TTTlist = []
class TTTdata:
	msgid: str
	p1: str
	p2: str

def TTTgetdata(msgid):
	for ele in TTTlist:
		if ele.msgid == msgid:
			return ele
	return 0

def TTTstoredata(msgid,p1=None,p2=None):
    new = TTTgetdata(msgid)
    if new == 0:
        new = TTTdata()
        new.msgid = msgid
        TTTlist.append(new)
    if p1 != None: new.p1 = p1
    if p2 != None: new.p2 = p2

def TTTremovedata(msgid):
	for ele in TTTlist:
		if ele.msgid == msgid:
			break
	TTTlist.remove(ele)

def TTTboard(data,chance,ai,won=0):
	board = []
	temp = []
	for i,ele in enumerate(data):
		if ele == "0": t = " "
		elif ele == "1": t = "X"
		elif ele == "2": t = "O"

		if won == 0: temp.append(InlineKeyboardButton( text=t, callback_data=f"TTT {chance} {ai} {str(i+1)} {data}"))
		else: temp.append(InlineKeyboardButton( text=t, callback_data=f"TTT won {won}"))

		if (i+1)%3 == 0:
			board.append(temp)
			temp = []
	
	return InlineKeyboardMarkup(board)

def TTTdeclare(data):
	result = check(data)
	if result[0]:
		if result[1] == 1: return 1
		else: return 2
	return 0

def TTTcheck(app,data,message,p1,p2):
	res = TTTdeclare(data)
	if res:
		if res == 1: app.edit_message_text(message.chat.id, message.id,f"**{p1}** has Won (X)", reply_markup=TTTboard(data,None,None,1))
		else: app.edit_message_text(message.chat.id, message.id,f"**{p2}** has Won (O)", reply_markup=TTTboard(data,None,None,2))
		return 1
	elif "0" not in data:
		app.edit_message_text(message.chat.id, message.id,f"**Draw Match**", reply_markup=TTTboard(data,None,None,3))
		return 1
	else: return 0

def TTTgame(app,call,message,flag=0):
	if flag: calldata = "AI"
	else: calldata = call.data[4:]

	# second step
	if calldata in ["P2","AI"]:
		data = "000000000"
		chance = random.choice((0, 1))
		ai = 0

	# private chat
	if flag:
		ai = 1
		if chance: now = f'**{message.from_user.first_name} **' 
		else: now = '**🤖 AI**'
		msg = app.send_message(message.chat.id, f'__Player 1 (X) : **{message.from_user.first_name}**\nPlayer 2 (O) : **🤖 AI**\n\n{now} will make a first move__', reply_to_message_id=message.id,
		reply_markup=InlineKeyboardMarkup(
		[[ InlineKeyboardButton( text='⏳ Start the Game', callback_data=f"TTT {chance} {ai} 0 {data}")]]))
		TTTstoredata(msg.id, p1=message.from_user.id)
		return

	# p1 details
	players = TTTgetdata(message.id)
	p1 = app.get_users(players.p1)

	# clicked p2
	if calldata == "P2":
		if call.from_user.id == p1.id:
			app.answer_callback_query(call.id, "You can't be both Player 1 and 2.\nchoose v/s AI instead.", show_alert=True)
		else:
			app.answer_callback_query(call.id)
			if chance: now = f'**{p1.first_name}**' 
			else: now = f'**{call.from_user.first_name}**'
			TTTstoredata(message.id, p2=call.from_user.id)
			app.edit_message_text(message.chat.id, message.id, f'__Player 1 (X) : **{p1.first_name}**\nPlayer 2 (O) : **{call.from_user.first_name}**\n\n{now} will make a first move__',
			reply_markup=InlineKeyboardMarkup(
			[[ InlineKeyboardButton( text='⏳ Start the Game', callback_data=f"TTT {chance} {ai} 0 {data}")]]))
		return

	# clicked ai
	if calldata == "AI":
		app.answer_callback_query(call.id)
		ai = 1
		if chance: now = f'**{p1.first_name} **' 
		else: now = '**🤖 AI**'
		app.edit_message_text(message.chat.id, message.id, f'__Player 1 (X) : **{p1.first_name}**\nPlayer 2 (O) : **🤖 AI**\n\n{now} will make a first move__',
		reply_markup=InlineKeyboardMarkup(
		[[ InlineKeyboardButton( text='⏳ Start the Game', callback_data=f"TTT {chance} {ai} 0 {data}")]]))
		return

	# p2 details
	try:
		p2 = app.get_users(players.p2)
		p2name, p2id =  p2.first_name, p2.id
	except:
		p2name = "🤖 AI"
		p2id = 0
	
	# unknow user
	if call.from_user.id not in [p1.id,p2id]:
		app.answer_callback_query(call.id, "This is not your Game", show_alert=True)
		return

	# splittng
	data = calldata.split()

	# check for complete
	if data[0] == "won":
		won = data[-1]
		if won == "1": app.answer_callback_query(call.id, f"{p1.first_name} has already won (X)", show_alert=True)
		elif won == "2": app.answer_callback_query(call.id, f"{p2name} has already won (O)", show_alert=True)
		elif won == "3": app.answer_callback_query(call.id, f"Draw Match", show_alert=True)
		return

	# third step and loop
	chance = int(data[0])
	ai = int(data[1])
	pos = int(data[2]) - 1
	data = data[3]

	# not your chance
	if (pos != -1) and ((chance and (call.from_user.id != p1.id)) or ((not chance) and (call.from_user.id != p2id))):
		app.answer_callback_query(call.id, "Not your Chance", show_alert=True)
		return

	# tap on same button
	if data[pos] != "0":
		app.answer_callback_query(call.id, "Don't you know the Rules?", show_alert=True)
		return
	
	app.answer_callback_query(call.id)
	if ai:
		if not chance:
			pos = getAI(data)
			mark = "2"
			chance = 1
			data = data[:pos] + mark + data[pos+1:]
			if TTTcheck(app,data,message,p1.first_name,p2name): return
		else:
			if pos != -1:
				mark = "1"
				data = data[:pos] + mark + data[pos+1:]
				if TTTcheck(app,data,message,p1.first_name,p2name): return
				pos = getAI(data)
				mark = "2"
				data = data[:pos] + mark + data[pos+1:]
				if TTTcheck(app,data,message,p1.first_name,p2name): return

		app.edit_message_text(message.chat.id, message.id,f"**{p1.first_name}**__'s chance (X)__", reply_markup=TTTboard(data,chance,ai))

	else:
		if pos != -1:
			if chance:
				mark = "1"
				chance = 0
			else:
				mark = "2"
				chance = 1
		
			data = data[:pos] + mark + data[pos+1:]
			if TTTcheck(app,data,message,p1.first_name,p2name): return

		if chance: app.edit_message_text(message.chat.id, message.id,f"**{p1.first_name}**__'s chance (X)__", reply_markup=TTTboard(data,chance,ai))
		else: app.edit_message_text(message.chat.id, message.id,f"**{p2name}**__'s chance (O)__", reply_markup=TTTboard(data,chance,ai))

###############################################################################################
