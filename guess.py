import random

def decimalToBinary(n,size): 
    return bin(n).replace("0b", "").zfill(size) # converts decimal to binary and fills "0" upto binary size of Max limit

def binaryToDecimal(n):
    return int(n,2) # converts binary to decimal

def printNumbers(numList,N): # print the numbers from the given list

    display = ""
    ele = 0

    while ele < len(numList): # traverse list
        i = 0

        while i < 5 and ele < len(numList): # to print numbers in box format of width 5

            if numList[ele] > N: # if number exceeds Max number
                return # then stop
            
            num = str(numList[ele]).zfill(len(str(N))-1)
            display = display + f"{num}    " # displaying
            ele = ele + 1
            i = i + 1

        display = display + "\n" # line break
	
    #print(display) # print
    return display # return

def generateNumbers(i,N,size): # genrates the numbers to display based on the "i" input

    numList = [] # declaring

    for j in range(1,N+1): # from 1 to Max limit

        if int(decimalToBinary(j,size)[-i]): # if i'th charcter from reverse in binary is 1?
            numList.append(j) # then append to the list
            
    return printNumbers(numList,N) # calling print list


def finalize(binary,N): # does the final job

    binary = binary[::-1][:-1] # reversing the string and removing the first character
    number = binaryToDecimal(binary) # getting final decimal number from binary

    if number == 0 or number > N:
        #print(f"\t\tI said in between 1 - {N}\n") # number not in the list
        return 0
    else:
        #print("\t\tYour number is",number,"\n") # final answer
        return number
    

def main(): # main function
    
    N = input("Enter the Upper Limit 1 - ? ") # MAX number

    while (not N.isnumeric()) or (int(N) < 1):
        print("\nWrong Input, Enter only Positve non-zero Number")
        N = input("Enter the Upper Limit 1 - ? ")

    N = int(N)
    size = len(bin(N).replace("0b", "")) # getting the size of Max number

    print(f"Take a Number between 0 - {N}, and i will guess it in {size} steps")
    input("Ready ? press Enter to continue... ")
    print("\n")

    binarylist = ["0"] * int(size+1) # declaring list of Max number size

    nlist = list(range(1,size+1)) # genrating list of 1 to Max size
    random.shuffle(nlist) # randomizing it

    for i in nlist:
        generateNumbers(i,N,size) # calling generate function
        print("\n") 

        take = input("is your number in this list? 0 for No & 1 for Yes : ") # taking input
        while not (take == "0" or take == "1"):
            print("\nWrong Input, Enter Input Again")
            take = input("is your number in this list? 0 for No & 1 for Yes : ")
            
        binarylist[i] = take # adding to the list
        print("\n")

    binary = "" # decalring
    for ele in binarylist: 
        binary = binary + ele # converting list into string

    return finalize(binary,N) # calling the final function


#############################################################################################

from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton

def Ggame(app,call):
	app.answer_callback_query(call.id)
	call.data = call.data[2:]

    # not callback
	if call.data == "not":
		app.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'**OK, No Problem.**')

    # game start callback
	elif call.data == "ready":
		N = int(call.message.text.split(" - ")[1].split("\n")[0])
		size = len(bin(N).replace("0b", ""))
		binary = "0".zfill(size+1)
		
		nlist = list(range(0,size))
		random.shuffle(nlist)
		slist = ""
		for ele in nlist:
			slist = slist + str(ele)
		
		text = generateNumbers(int(slist[0])+1, N, size)
		ydata = f'{N} {binary} {slist} 1'
		ndata = f'{N} {binary} {slist} 0'
		
		app.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'**{text}**\n__is your number there ?__ **(1 / {size})**',
        reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton( text='Yes', callback_data=f'G {ydata}'),
                        InlineKeyboardButton( text='No', callback_data=f'G {ndata}')
                    ]]))
    
    # game callback
	else:
		data = call.data.split(" ")
		N = int(data[0])
		size = len(bin(N).replace("0b", ""))
		binary = data[1]
		slist = data[2]
		res = data[3]
		
		pos = int(slist[0])+1
		slist = slist[1:]
		binary = list(binary)
		binary[pos] = res
		binary = "".join(binary)
		
		if len(slist) != 0:
			text = generateNumbers(int(slist[0])+1, N, size)
			ydata = f'{N} {binary} {slist} 1'
			ndata = f'{N} {binary} {slist} 0'
			
			app.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'**{text}**\n__is your number there ?__ **({size-len(slist)+1} / {size})**',
                    reply_markup=InlineKeyboardMarkup(
                            [[
                                InlineKeyboardButton( text='Yes', callback_data=f'G {ydata}'),
                                InlineKeyboardButton( text='No', callback_data=f'G {ndata}')
                            ]]))
						
		else:
			number = finalize(binary,N)
			if number == 0:
				app.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'__I said in between__ **1 - {N}**')
			else:
				app.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'__Your number is__ **{number}**')

################################################################################################
