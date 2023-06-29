from objects import Grid, TriGrid, HexGrid
from alphabet import mask_word
from maze_generation import *


def get_response(message: str) -> str:
  p_message = message.lower()

  if p_message == 'hello' or p_message == 'hi':
    return f"```\n{mask_word('hi')}```"

  if p_message[:8] == '!message':
    return f"```\n{mask_word(p_message[8:])}```"

  if p_message == '!help':
    return 'This is a help message'

  return 'I didn\'t understand what you wrote. Try typing "!help"'
