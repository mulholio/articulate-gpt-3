import os
from enum import Enum
import openai
import fire

openai.api_key = "YOUR KEY"

restart_sequence = "\n"

class Mode(Enum):
    """Possible game modes"""
    GUESS = 1
    DESCRIBE = 2
    NONE = 3

class InputException(Exception):
    pass

class Articulator():
    # guess or describe
    mode = Mode.NONE

    def choose_mode(self, inputed_mode):
        inputed_mode = inputed_mode.lower()
        if inputed_mode == 'guess':
            self.mode = Mode.GUESS
        elif inputed_mode == 'describe':
            self.mode = Mode.DESCRIBE
        else:
            raise InputException("Please enter 'guess' or 'describe'")

    def articulate(self):
        if self.mode == Mode.NONE:
            mode = input("Choose a mode (guess|describe): ")
            self.choose_mode(mode)

        if self.mode == Mode.GUESS:
            description = input("Describe the word for GPT-3: ")
            prompt = self._make_guess_prompt_from_description(description)
        elif self.mode == Mode.DESCRIBE:
            word = input("Write a word for GPT-3 to guess: ")
            prompt = self._make_describe_prompt_from_word(word)

        text = self._get_response(prompt)

        print(text)

    def _make_guess_prompt_from_description(self, description):
        return f"We're going to play a game of Articulate. Articulate is a party-game where you must describe a series of words without mentioning the target word itself. Below are some examples of how we play a round of Articulate.\n\nDescription: A scary water-based animal with very sharp teeth. Star of the film Jaws. Varities include: great white, basking, hammerhead and tiger.\nWord: Shark\n###\nDescription: You use this to put fluids on plants. Usually made of plastic. Not a hose.\nWord: Watering can\n###\nDescription: Small brass instrument. Used to play 'The Last Post' and jazz. Miles Davis loved it.\nWord: Trumpet\n###\nDescription: Small country in Europe, I think.\nWord: ?\n###\nDescription: A large animal that produces milk. Often found in fields.\nWord: Cow\n###\nDescription: A kind of car.\nWord: ?\n###\nDescription: Someone \n###\nDescription: Thing you read. Made of paper. Loved by nerds.\nWord: Book\n###\nDescription: The kind of meat that comes from a pig and would be used in a loin.\nWord: Pork\n###\nDescription: King who had six wives and beheaded some of them.\nWord: Henry VIII\n###\nDescription: A thing you watch films and programmes on. Used to be black and white but now comes in colour.\nWord: Television\n###\nDescription: {description}\nWord:"

    def _make_describe_prompt_from_word(self, word):
        return f"We're going to play a game of Articulate. Articulate is a party-game where you must describe a target word without mentioning the target word itself. For example, if the target word is 'banana', you cannot say 'banana' in the description.\n\nHere are some examples of how we might play a round of Articulate.\n\n---\n\nWord: Shark\nDescription: A scary water-based animal with very sharp teeth. Star of the film Jaws. Varities include: great white, basking, hammerhead and tiger.\n\nWord: Watering can\nDescription: You use this to put fluids on plants. Usually made of plastic. Not a hose.\n\nWord: Trumpet\nDescription: Small brass instrument. Used to play 'The Last Post' and jazz. Miles Davis loved it.\n\nWord: Cow\nDescription: A large animal that produces milk. Often found in fields.\n\nWord: {word}\nDescription:"

    def _get_response(self, prompt):
        print("thinking...")
        res = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            temperature=0,
            max_tokens=45,
            top_p=0.07,
            frequency_penalty=0.6,
            presence_penalty=0.1,
            stop=["\n"],
        )
        return res.choices[0].text[1:]

if __name__ == '__main__':
  fire.Fire(Articulator)