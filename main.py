from tkinter import * 
from tkinter.ttk import *

from functools import partial

import json 
import random


def draw_players(): 
    for label in player_labels: 
        label.grid_forget() 

    for index, player in enumerate(player_scores):
        player_label = Label(root, text = player + ": " + str(player_scores[player]))
        player_label.grid(row = 10, column = index)
        player_labels.append(player_label)

def create_new_player(name_input, window): 
    player_scores.update({name_input.get():0})
    window.destroy()
    draw_players()

def ask_question(category, amt, button): 
    temp = Tk()
    temp.title(category +" - $" + str(amt))
    temp.geometry("600x150")
    
    #see if its the daily double 
    global daily_double_cnt
    global questions_asked

    questions_asked += 1 

    #category_questions['category'][amt]['question']
    #category_questions[category][amt]['answer']
    question_label = Label(temp, text=category_questions[category][str(amt)]['question'])
    question_label.place(relx = 0.5, rely = 0.3, anchor = CENTER)

    dd_label = Label(temp, text="DAILY DOUBLE")

    answer_label = Label(temp, text=category_questions[category][str(amt)]['answer'])
    
    view_answer = Button(temp, text="View Answer", command= lambda: answer_label.place(relx = 0.5, rely = 0.8, anchor = CENTER))
    view_answer.place(relx = 0.3, rely = 0.7, anchor = CENTER)

    exit_btn = Button(temp, text="Go Back", command= lambda: temp.destroy())
    exit_btn.place(relx = 0.8, rely = 0.7, anchor = CENTER)

    if daily_double_cnt < 2: 
        
        upper = 25 - questions_asked 
        rand = random.randrange(0, upper)

        if rand < 2 or rand == upper: 
            dd_label.place(relx = 0.5, rely = 0.1, anchor = CENTER)
            daily_double_cnt +=1 


    button.grid_forget()

def add_player(): 
    #make temp window
    temp = Tk()
    temp.title("Add New Contestant")
    temp.geometry("150x75")
    
    #user friendly text 
    label = Label(temp, text="Player Name:", borderwidth=1).grid(row = 0, column = 1, padx=10)
    
    #user input 
    input_box = Entry(temp)
    input_box.grid(row = 1, column = 1, padx = 10)

    #button to confirm input
    button = Button(temp, text="OK!", command=partial(create_new_player, input_box, temp)).grid(row = 2, column = 1)

def update_player_scores(player_input, amount_input, window): 
    amt = int(amount_input.get())
    player = str(player_input.get())
    
    if player in player_scores:
        player_scores[player] += amt

    draw_players()
    window.destroy()

def add_score():
    temp = Tk()
    temp.title("Update Scores")
    temp.geometry("150x250")

    label = Label(temp, text="Player").grid(row = 0, column = 0)
    player_input = Entry(temp)
    player_input.grid(row = 1, column = 0, padx=10, pady=10)

    label = Label(temp, text="Amount").grid(row = 2, column = 0)
    amount_input = Entry(temp)
    amount_input.grid(row = 3, column = 0, padx=10, pady=10)

    button = Button(temp, text="OK!", command=partial(update_player_scores, player_input, amount_input, temp)).grid(row = 4, column = 0)

def change_scene(): 
    global board_multiplier
    global questions_asked
    global daily_double_cnt

    questions_asked = 0 
    daily_double_cnt = 0
	
    if board_multiplier == 0: 
        board_multiplier = 1
        make_board()
    else: 
        #final jeopardy
        pass


# show on the window
def make_board():
    #clear anything that might have been drawn first 
    for label in labels: 
        label.destroy()

    for button in buttons: 
        button.destroy()

    #make the buttons for each category 
    for c in range(len(categories[board_multiplier])): 
        label = Label(root, text=categories[board_multiplier][c], borderwidth=0)
        label.grid(row=0, column = c, padx=38)
        labels.append(label)

        for r in range(len(questions)): 
            button = Button(root, text="$"+str(questions[c]*(board_multiplier+1)))
            button.configure(command=partial(ask_question, categories[board_multiplier][r], questions[c], button))
            buttons.append(button)
            button.grid(row=c + 1, column=r)


def load_data(filename): 
    categories = []
    category_questions = {}

    with open(filename, encoding="latin1") as f: 
        data = json.load(f)
        categories = data['categories']
        category_questions = data['questions']
    
    
    return categories, category_questions

# main window object named root
root = Tk()
root.option_add('*Font', '19')
root.geometry("850x400")
root.title("Jeopardy!")

        
#add player button 
add_player = Button(root, text ="Add Player", command=add_player)
add_player.place(relx = 0.2, rely = 0.5, anchor = W)

#add score button 
add_score = Button(root, text ="Update Scores", command=add_score)
add_score.place(relx = 0.5, rely = 0.5, anchor = CENTER)

#change scene button 
change_scene = Button(root, text ="Next Board", command=change_scene)
change_scene.place(relx = 0.8, rely = 0.5, anchor = E)

categories, category_questions = load_data('./board_1.json') 
questions = [100, 200, 300, 400, 500]

board_multiplier = 0
questions_asked = 0 
daily_double_cnt = 0

player_scores = {}

player_labels = []

buttons = []
labels = []

make_board()

root.mainloop()