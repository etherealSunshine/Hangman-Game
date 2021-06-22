from typing import TypeVar
from typing import List, Tuple
import streamlit as st
from PIL import Image

StateT = TypeVar('StateT')

MIN_LENGTH = 5
MAX_LENGTH = 8

def get_image():
	image = [Image.open('image0.jpg')]
	image.append(Image.open('image1.jpg'))
	image.append(Image.open('image2.jpg'))
	image.append(Image.open('image3.jpg'))
	image.append(Image.open('image4.jpg'))
	image.append(Image.open('image5n.jpg'))
	image.append(Image.open('image6n.jpg'))
	image.append(Image.open('image7n.jpg'))
	return image

def persistent_game_state(initial_state: StateT) -> StateT:
    session_id = st.report_thread.get_report_ctx().session_id
    session = st.server.server.Server.get_current()._get_session_info(session_id).session
    if not hasattr(session, '_gamestate'):
        setattr(session, '_gamestate', initial_state)
    return session._gamestate

def get_words() -> List[str]:
    with open('words1000.txt') as f:
        words = [line.strip() for line in f]

    words = [w for w in words if MIN_LENGTH <= len(w) <= MAX_LENGTH]
    words = [w for w in words if all('a' <= c <= 'z' for c in w)]

    return words

def display(is_image,input='',image=[],wrong_guesses=0):
    col1, col2 = st.beta_columns(2)
    
    if is_image == False:
        col1.text(input)
    else:
	    col2.image(image[wrong_guesses],width=230)

@st.cache	
class GameState:

	def __init__(self,game_number: int,word : str,guessed : str = '',step: int=0, game_over: bool=False):
		self.game_number = game_number
		self.word = word
		self.guessed = guessed
		self.step = step
		self.game_over = game_over
		
def push_state(state,guessed,wrong_guesses,game_number,word,game_over):
	state.guessed = guessed
	state.step = wrong_guesses
	state.game_number = game_number
	state.word = word
	state.game_over = game_over
