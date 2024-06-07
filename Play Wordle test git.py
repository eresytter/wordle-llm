import getpass
import os
import argparse
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
import random

# Environment setup
os.environ["LANGCHAIN_TRACING_V2"] = "true"
if "LANGCHAIN_API_KEY" not in os.environ:
    os.environ["LANGCHAIN_API_KEY"] = getpass.getpass("langchain api key")

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass.getpass("open ai api key")

llm = ChatOpenAI(
    model = "gpt-3.5-turbo-0125",
    temperature = 0.1,
    max_tokens = 256
)

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
You are playing a game of Wordle. The target word is {target_word}.
Try to guess the word in as few attempts as possible. After each guess, I will provide feedback indicating how many letters are correct and in the correct position (green), how many letters are correct but in the wrong position (yellow), and how many letters are incorrect (gray). Keep guessing until you find the word.
Instructions for Wordle:
Wordle is such a simple game that there are hardly any rules. But here you go:
You have to guess the Wordle in six goes or less
Every word you enter must be in the word list. There are more than 10,000 words in this list, but only 2,309 (at the time of writing) are answers to a specific puzzle
A correct letter in the correct position provides the feedback green
A correct letter in the wrong position provides the feedback yellow
An incorrect letter or letter that is not in the word provides the feedback gray
Letters can be used more than once but you cannot use the same word more than once per game
Answers are never plurals
Each guess must be a valid five-letter word.
The color of a tile will change to show you how close your guess was.

Tips: use words that have different letters to see if they are in the word

Example of a game:
I: Play Wordle 5 times provide your chain of thought.
O: Stair.
I: 'S', 't', 'i', and 'r' are grey, and 'a' is yellow.
O: Beast.
I: 'B', 's', and 't' are grey, and 'e' and 'a' are yellow.
O: Eager.
I: 'r' and the second 'e' are grey, and 'e', 'a', and 'g' are yellow.
O: Eagle.
I: Correct

Top 5 most common letters for the first position:
first
s    1565
c     922
b     909
p     859
t     815

Top 5 most common letters for the second position:
second
a    2263
o    2096
e    1628
i    1383
u    1187

Top 5 most common letters for the third position:
third
a    1236
r    1198
i    1051
o     993
n     964

Top 5 most common letters for the fourth position:
fourth
e    2327
a    1074
t     898
i     880
n     788

Top 5 most common letters for the fifth position:
fifth
s    3958
e    1522
y    1301
d     823
t     727
Context: {context}

Guess: {guess}

Feedback: {feedback}

Make your next guess:
"""

def load_documents(file_path):
    with open(file_path, 'r') as file:
        words = [line.strip() for line in file]
    return words


def play_wordle(db, word):
    print(f"Playing Wordle for the word: {word}")
    feedback = ""
    guess = ""
    attempts = 0

    # Mask the word in the prompt template
    masked_word = '*' * len(word)

    # Search the DB for relevant context
    db_results = db.similarity_search_with_relevance_scores(word, k=3)
    if len(db_results) == 0 or db_results[0][1] < 0.7:
        print(f"Unable to find matching results.")
        return False

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in db_results])

    while guess.lower() != word.lower() and attempts < 6:
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        # Pass the masked word to the prompt template
        prompt = prompt_template.format(target_word=masked_word, context=context_text, guess=guess, feedback=feedback)
        print(prompt)
        response = llm.invoke(prompt)
        print(f"LLM's Response: {response.content}")

        # Extract the guess from the response content
        guess_lines = response.content.strip().split("\n")
        guess = guess_lines[0].strip().replace('Guess: ', '')
        print(f"LLM's Guess: {guess}")

        # Remove any extra messages from the guess
        if "Congratulations" in guess:
            guess = word

        # Provide feedback based on the presence of letters in the word
        feedback = provide_feedback_presence(word, guess)
        print(f"Feedback: {feedback}")

        attempts += 1

    if guess.lower() == word.lower():
        return True
    else:
        return False

def provide_feedback_presence(target_word, guess):
    feedback = []
    for i, letter in enumerate(guess):
        if letter == target_word[i]:
            feedback.append("green")  # Letter is in the correct position
        elif letter in target_word and letter != target_word[i]:
            feedback.append("yellow")  # Letter is present in the word but not in the correct position
        else:
            feedback.append("gray")    # Letter is not present in the word
    return ", ".join(feedback)




def main():
    # Load the target words from the text file
    file_path = r"path to previous_words.txt"
    words = load_documents(file_path)

    # Prepare the DB
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    successful_games = 0
    attempts = 0

    while successful_games < 6 and attempts < 6:  # Limiting the total number of games to 6
        word = random.choice(words)  # Select a random word from the list
        print(f"Playing Wordle for the word: {word}")
        result = play_wordle(db, word)
        attempts += 1

        if result:
            print(f"Successfully guessed the word '{word}' in {attempts} attempts.")
            successful_games += 1
            attempts = 0  # Reset attempts for the next word
        else:
            print(f"Failed to guess the word '{word}' in 6 attempts. Moving to the next word.")

    print(f"Game finished: {successful_games} successful guesses out of {attempts*6} attempts.")  # Corrected the print statement




if __name__ == "__main__":
    main()