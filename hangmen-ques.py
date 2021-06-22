from string import ascii_lowercase
import types
import random

import streamlit as st

from support import persistent_game_state
from support import GameState
from support import get_words
from support import push_state
from support import display
from PIL import Image


# Define a function that gets all images in a list and returns the list.

def get_image():
    image = [Image.open("image0.jpg")]
    image.append(Image.open("image1.jpg"))
    image.append(Image.open("image2.jpg"))
    image.append(Image.open("image3.jpg"))
    image.append(Image.open("image4.jpg"))
    image.append(Image.open("image5.jpg"))
    image.append(Image.open("image6.jpg"))
    image.append(Image.open("image7.jpg"))
    number = len(image)
    return image,number
	
#Call 'get_image'

image,no_of_images = get_image()

#Call the 'get_words' function to get a list of words. Use 'random.choice' to choose a random word from the list.

initial_word = random.choice(get_words())

#Declare a 'Gamestate' as imported from the support file. Initialise the game number to 0 and word to be guessed as 'initial_word'.
#Other parameters of the gamestate have been passed an initial value beforehand.

initial_gamestate = GameState(0,initial_word)

#We will be using 'persistent_game_state' function from support file to save and modify game states during execution of the game.
#Call the function and pass initial_state as 'initial_gamestate'

state = persistent_game_state(initial_state=initial_gamestate) 

#Passing class instance variables to placeholders for convenience 
guessed = state.guessed
wrong_guesses = state.step
game_number = state.game_number
word = state.word
game_over = state.game_over
#Declare a new game button, and re-initialise the current 'state' so that a fresh game can be sarted when the button is pressed.
#Assign an empty string '' to the 'guessed' parameter
#Assign wrong guesses =  0 to 'wrong_guesses' parameter
#Update the game number by incrementing it by one
#Generate a new randomly chosen word by executing 'random.choice' on the 'get_words' function
#Update the 'game_over' parameter to 'False'

if st.button("new game"):
    guessed = ''
    wrong_guesses = 0
    game_number += 1
    word = random.choice(get_words())
    game_over = False
	
	#Push the state by calling the following function
    push_state(state,guessed,wrong_guesses,game_number,word,game_over)

#Start game execution logic now. First check for the 'game_over' parameter to be False
if not game_over:

	#Declare a user input bar. Have "guess a letter" displayed as the label for the input bar. Accept only 1 character maximum
	#Since every new game needs a new key for the input bar, assign key to 'game_number'
	
    guess = st.text_input("guess a letter", max_chars = 1, key=game_number)
	
	#Check if the input was empty, if 'guess' is False, have 'please guess' displayed 
	
    if not guess:
        display(False,"please guess")
		
	#Otherwise, check if the input was in lowercase. If input is < 'a' or > 'z' display 'please enter lowercase letter'
	
    elif guess.lower() < 'a' or guess.lower() > 'z':
	    display(False,"please enter lowercase letter")
		
	#Otherwise, check if the letter has been already guessed. Display f"you already guessed {guess}" if a guess is repeated.
	
    elif guess.lower() in guessed.lower():
	    display(False,f"you already guessed {guess}")
		
	#Otherwise, check if the letter is present in the word being guessed. If not display f"the word has no {guess}".
	#If the letter is not in the word, add the letter to the 'guessed' string and increment the wrong guesses.
    elif guess not in word:
        display(False,f"the word has no {guess}")
        guessed+=guess
        wrong_guesses+=1

        #Push the state 
        push_state(state, guessed,wrong_guesses,game_number,word,game_over)
		
	#Otherwise if the letter is present in the word, have 'good guess' displayed.
	#Add the letter to the 'guessed' string.
    #Push the state
	
    else: 
        display(False,"good guess")
        guessed+=guess
        letters_guessed= letters_guessed + guess
        push_state(state, guessed,wrong_guesses,game_number,word,game_over)

#We will now build a list which has the information about how many of the letters have been guessed
# Hint : list.append(a) adds the element a at the end of the list

    letters_guessed = []
    for c in word:
        # check if the letter in word is present in the 'guessed' string
        if c in guessed:
            # If it is present append 'True' to the list
            letters_guessed.append(True)
        else:
            # If not append 'False' to the list
            letters_guessed.append(False)





#Check if the wrong guesses are equal to 'no_of_images' in image list - 1 (minus one because we started step with 0)

if wrong_guesses == no_of_images - 1:

	#If the maximum guesses are exhausted, display f"you lose, the word was {state.word}"

    display(False,f"you lose, the word was {state.word}")

	#Update the 'game_over' parameter to True and push state

    game_over=True
    push_state(state, guessed,wrong_guesses,game_number,word,game_over)
#If not check if the word has been completely guessed. Use 'all()' functionality of python on the 'letters_guessed' list

elif all(letters_guessed):
	
	#Print f"YOU WIN"
    display(False,f"YOU WIN")

	#Update 'game_over' to true and push state

    game_over=True
    push_state(state, guessed,wrong_guesses,game_number,word,game_over)











# In the intermediate stage when the game is still on, we need to display image according to current wrong number of guesses display 'image[wrong_guesses]'
# Pass the image list and current wrong guesses to the display function

display(True,'',image,wrong_guesses)

# Finally, make a list from the word where guessed characters are displayed as it is and dashes are displayed otherwise.

chars = [c if c in guessed else "_" for c in word]

#Display the list after converting it to a string using join functionality

display(False," ".join(chars))

# Show the guessed letters, again after converting it to a string by using join

display(False,f'guessed: {"".join(guessed)}')
