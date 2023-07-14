import random
from PIL import Image, ImageTk
import tkinter as tk

# Create a list of image filenames for the memory game
image_filenames = [
    "durga.jpg",
    "mahishasura.jpg",
    "ganesha.jpg",
    "kartikeya.jpg",
    "lakshmi.jpg",
    "saraswati.jpg"
]

# Duplicate the image filenames to create pairs
card_images = image_filenames + image_filenames

# Shuffle the card images
random.shuffle(card_images)

# Initialize the Tkinter window
window = tk.Tk()
window.title("Durga Puja Memory Match")
window.geometry("600x600")

# Load the card images for the front side and back side
front_images = []
back_image = Image.open("back.jpg")  # Replace "back.jpg" with the filename of your blank card image
back_image = back_image.resize((100, 100))  # Adjust the image size as per your requirement
back_card = ImageTk.PhotoImage(back_image)

# Create a list to hold references to the front card images
for filename in card_images:
    image = Image.open(filename)
    image = image.resize((100, 100))  # Adjust the image size as per your requirement
    card_image = ImageTk.PhotoImage(image)
    front_images.append(card_image)

# Create a board with hidden cards
board = [None] * len(card_images)

# Function to display the current state of the board
def display_board():
    for i, card in enumerate(board):
        if card is None:
            button = tk.Button(window, image=back_card, command=lambda idx=i: flip_card(idx))
            button.grid(row=i // 4, column=i % 4)
        else:
            label = tk.Label(window, image=card)
            label.grid(row=i // 4, column=i % 4)

# Function to handle card flipping
def flip_card(index):
    global first_card_index
    global matched_pairs

    # Check if the card is already matched or flipped
    if board[index] is not None:
        return

    # Flip the card
    board[index] = front_images[index]
    display_board()

    # Check if it's the first card in a pair
    if first_card_index is None:
        first_card_index = index
    else:
        # Check if the cards match
        if card_images[first_card_index] == card_images[index]:
            print("Match!")
            matched_pairs += 1
            if matched_pairs == len(image_filenames):
                print("Congratulations! You've matched all the pairs!")
                window.destroy()
        else:
            print("No match!")
            # Flip back the cards after a short delay
            window.after(1000, lambda idx1=first_card_index, idx2=index: flip_back_cards(idx1, idx2))

        # Reset the first card index
        first_card_index = None

# Function to flip back unmatched cards
def flip_back_cards(index1, index2):
    board[index1] = None
    board[index2] = None
    display_board()

# Initialize variables
first_card_index = None
matched_pairs = 0

# Display the initial board
display_board()

# Start the Tkinter event loop
window.mainloop()
