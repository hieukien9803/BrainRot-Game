import pygame
import random

class Card:
    # this is an abstract class bruh
    def __init__(self, n, d, h, t):
        self.n = n
        self.d = d
        self.h = h
        self.t = t

    def skill(self):
        raise NotImplemented

    def __str__(self):
        return str(self.n)

class Player:
    def __init__(self, card):
        self.health = 10
        self.cards = card

    def __str__(self):
        return str(self.cards)


# create game object bruhh
shower_card = Card("shower", 10, 0, "damage")
touchgrass_card = Card("touchgrass", 1, 0, "damage")
deodorant_card = Card("deodorant", 2, 0, "damage")
gpt_card = Card("gpt", 2, 0, "damage")
light_mode_card = Card("lightmode", 1, 0, "damage")
talktowoman_card = Card("talktowoman", 4, 0, "damage")
if_card = Card("if", 1, 0, "damage")
timecomplex_card = Card("timecomplex", 3, 0, "damage")
failunittest_card = Card("failunittest", 3, 0, "damage")
centerdiv_card = Card("centerdiv", 3, 0,"damage")
# support card
darkmode_card = Card("darkmode", 0, 4, "heal")
python_card = Card("python", 0, 6, "heal")
energydrink_card = Card("energydrink", 0, 2, "heal")

deck = [shower_card, touchgrass_card, deodorant_card, gpt_card, light_mode_card,
        talktowoman_card, if_card, timecomplex_card, failunittest_card,
        centerdiv_card,
        darkmode_card, python_card, energydrink_card]
# set up players
you_nerd = Player(card=random.sample(deck, 6))
bot_chad = Player(card=random.sample(deck, 13))
player_cards_played = []
bot_cards_played = []

# Initialize pygame
pygame.init()

# LOAD SOUND
pygame.mixer.init()
button_sound = pygame.mixer.Sound("asset/audio/button.wav")
drawcard_sound = pygame.mixer.Sound("asset/audio/drawcard.wav")
placingcard_sound = pygame.mixer.Sound("asset/audio/placingcard.wav")
end_sound = pygame.mixer.Sound("asset/audio/sunshine.wav")
drinking_sound = pygame.mixer.Sound("asset/audio/drink.wav")
end_sound.set_volume(1.0)

# Constants
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
CARD_WIDTH, CARD_HEIGHT = 100, 150
MARGIN = 20
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)

DRAW_BUTTON_WIDTH, DRAW_BUTTON_HEIGHT = 150, 50
DRAW_BUTTON_COLOR = (200, 200, 0)
DRAW_BUTTON_HOVER_COLOR = (255, 255, 0)

delay_duration = random.randint(1000, 3000)  # Random delay in milliseconds
start_time = pygame.time.get_ticks()

# Load images for the cards
card_images = {
    "shower_card": "asset/card/shower_card.png",
    "touchgrass_card": "asset/card/touchgrass_card.png",
    "deodorant_card": "asset/card/deodorant_card.png",
    "gpt_card": "asset/card/gpt_card.png",
    "lightmode_card": "asset/card/lightmode_card.png",
    "talktowoman_card": "asset/card/talktowoman_card.png",
    "if_card": "asset/card/if_card.png",
    "timecomplex_card": "asset/card/timecomplex_card.png",
    "failunittest_card": "asset/card/failunittest_card.png",
    "centerdiv_card": "asset/card/centerdiv_card.png",
    "darkmode_card": "asset/card/darkmode_card.png",
    "python_card": "asset/card/python_card.png",
    "energydrink_card": "asset/card/energydrink_card.png"
}

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Turn-Based Card Game")
lebron = pygame.image.load("asset/lebron.png")
lebron = pygame.transform.scale(lebron, (WIDTH, HEIGHT))  # Scale to fit screen

# Create a surface for fading
fade_surface = pygame.Surface((WIDTH, HEIGHT))
fade_surface.set_alpha(0)  # Initial transparency

# Fade duration (in seconds)
fade_duration = 10
alpha = 0  # Transparency level (0-255)
fade_speed = 255 / (fade_duration * 60)
start_ticks = pygame.time.get_ticks()
# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 48)

# Clock
clock = pygame.time.Clock()
# Load background image for the menu
menu_background = pygame.image.load("asset/background.png")
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))


def draw_menu():
    """Draw the start menu."""
    # Blit the background image
    screen.blit(menu_background, (0, 0))

    # Add menu text on top of the image
    title_text = big_font.render("BRAIN ROT Game", True, BLACK)
    start_text = font.render("Click to Start", True, BLACK)
    screen.blit(title_text,
                (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(start_text,
                (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 20))
    pygame.display.flip()


# Add this variable to track the selected card
selected_card = None

def draw_ui():
    """Draw the game UI with hover effect and card click details."""
    global selected_card
    screen.fill((0, 0, 0))

    # Draw health
    player_health_text = big_font.render(f"Player Health: {you_nerd.health}", True, BLUE)
    bot_health_text = big_font.render(f"Bot Health: {bot_chad.health}", True, RED)
    screen.blit(player_health_text, (MARGIN, HEIGHT - 80))
    screen.blit(bot_health_text, (MARGIN, 20))

    # Display turn info
    if player_turn:
        turn_text = big_font.render("Your Turn", True, BLACK)
    else:
        turn_text = big_font.render("Bot's Turn", True, BLACK)
    screen.blit(turn_text, (WIDTH // 2 - turn_text.get_width() // 2, HEIGHT // 2 - 100))

    # If a card is selected, show the image of the card
    if selected_card:
        # Display the card image in the center
        card_image_path = card_images.get(selected_card.n, None)
        if card_image_path:
            card_image = pygame.image.load(card_image_path)
            card_image = pygame.transform.scale(card_image, (CARD_WIDTH * 2, CARD_HEIGHT * 2))  # Scale the image
            screen.blit(card_image, (WIDTH // 2 - CARD_WIDTH, HEIGHT // 2 - CARD_HEIGHT))
            return  # Skip drawing the cards if one is selected to show the image

    # Draw player cards with hover effect
    y = HEIGHT - CARD_HEIGHT - 100
    for i, card in enumerate(you_nerd.cards):
        x = MARGIN + i * (CARD_WIDTH + MARGIN)
        mouse_pos = pygame.mouse.get_pos()

        # Check if the mouse is hovering over the card
        if x < mouse_pos[0] < x + CARD_WIDTH and y < mouse_pos[1] < y + CARD_HEIGHT:
            # Apply a small vertical offset for hover effect
            offset_y = -10
        else:
            offset_y = 0

        # Draw the card with the hover effect
        pygame.draw.rect(screen, BLUE, (x, y + offset_y, CARD_WIDTH, CARD_HEIGHT))
        card_text = font.render(str(card), True, WHITE)
        screen.blit(card_text, (x + 10, y + CARD_HEIGHT // 2 - 10 + offset_y))

    # Draw played cards
    y = HEIGHT // 2 - CARD_HEIGHT // 2
    for i, card in enumerate(player_cards_played):
        x = WIDTH // 2 - len(player_cards_played) * (CARD_WIDTH + MARGIN) // 2 + i * (CARD_WIDTH + MARGIN)
        pygame.draw.rect(screen, BLUE, (x, y, CARD_WIDTH, CARD_HEIGHT))
        card_text = font.render(str(card.n), True, WHITE)
        screen.blit(card_text, (x + 10, y + CARD_HEIGHT // 2 - 10))

    for i, card in enumerate(bot_cards_played):
        x = WIDTH // 2 - len(bot_cards_played) * (CARD_WIDTH + MARGIN) // 2 + i * (CARD_WIDTH + MARGIN)
        y = HEIGHT // 2 - CARD_HEIGHT - MARGIN * 2
        pygame.draw.rect(screen, RED, (x, y, CARD_WIDTH, CARD_HEIGHT))
        card_text = font.render(str(card), True, WHITE)
        screen.blit(card_text, (x + 10, y + CARD_HEIGHT // 2 - 10))

    # Draw the Draw Card button
    draw_button_rect = pygame.Rect(WIDTH - DRAW_BUTTON_WIDTH - MARGIN, HEIGHT - DRAW_BUTTON_HEIGHT - MARGIN, DRAW_BUTTON_WIDTH, DRAW_BUTTON_HEIGHT)
    mouse_pos = pygame.mouse.get_pos()
    if draw_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, DRAW_BUTTON_HOVER_COLOR, draw_button_rect)
    else:
        pygame.draw.rect(screen, DRAW_BUTTON_COLOR, draw_button_rect)
    button_text = font.render("Draw Card", True, BLACK)
    screen.blit(button_text, (draw_button_rect.x + 10, draw_button_rect.y + 10))

    return draw_button_rect

def handle_draw_card():
    """Handle the draw card action and immediately update the screen."""
    global player_turn
    if len(deck) > 0:
        new_card = random.choice(deck)
        you_nerd.cards.append(new_card)
        deck.remove(new_card)  # Remove drawn card from deck
    pygame.mixer.Sound.play(drawcard_sound)
    draw_ui()  # Redraw UI immediately after drawing a card
    pygame.display.flip()
    player_turn = False

def play_card(card):
    """Function to simulate playing a card and updating the screen."""
    global player_turn
    if card in you_nerd.cards:
        pygame.mixer.Sound.play(placingcard_sound)
        player_cards_played.append(card)
        you_nerd.cards.remove(card)  # Remove card from player's hand
        if card.t == "damage":
            bot_chad.health -= card.d
        elif card.t == "heal":
            you_nerd.health = min(10, you_nerd.health + card.h)
            if card.n == "energydrink":
                pygame.mixer.Sound.play(drinking_sound)

        draw_ui()  # Redraw UI immediately after playing a card
        pygame.display.flip()
        player_turn = False

import time

def handle_bot_turn():
    """Handle the bot's turn with a random delay."""
    global player_turn
    time.sleep(random.randint(1, 3))  # Random delay between 1 to 3 seconds

    if len(bot_chad.cards) > 0:
        card = random.choice(bot_chad.cards)
        pygame.mixer.Sound.play(placingcard_sound)
        bot_cards_played.append(card)
        bot_chad.cards.remove(card)
        if card.t == "damage":
            you_nerd.health -= card.d
        elif card.t == "heal":
            bot_chad.health = min(10, bot_chad.health + card.h)
    draw_ui()  # Redraw UI immediately after bot's action
    pygame.display.flip()
    player_turn = True

def display_card_details(card):
    """Render the card image on top of the gameplay and return to the game on any click."""
    card_image_path = card_images.get(f"{card.n}_card", None)
    if card_image_path:
        try:
            # Load and scale the card image
            card_image = pygame.image.load(card_image_path)
            card_image = pygame.transform.scale(card_image, (CARD_WIDTH * 3.4, CARD_HEIGHT * 3.4))  # Scale the image

            # Calculate position to center the image on the screen
            x = 620
            y = 100

            # Render the card image on top of the gameplay screen
            screen.blit(card_image, (x, y))
            pygame.display.flip()  # Update the screen with the card image

            # Wait for any mouse click to return to the game
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:  # Exit on any mouse click
                        return  # Exit the function and resume gameplay
        except pygame.error as e:
            print(f"Error loading or displaying image: {e}")
    else:
        print(f"No image found for card: {card.n}")


def handle_card_hover(pos):
    """Handle mouse hover over a card."""
    y = HEIGHT - CARD_HEIGHT - 100
    for i, card in enumerate(you_nerd.cards):
        x = MARGIN + i * (CARD_WIDTH + MARGIN)
        if x < pos[0] < x + CARD_WIDTH and y < pos[1] < y + CARD_HEIGHT:
            return card
    return None


def handle_card_click(pos):
    """
    Handle clicking on a card and return the card being clicked (selected).

    Args:
        pos (tuple): The (x, y) position of the mouse click.

    Returns:
        Card: The selected card if a card is clicked, otherwise None.
    """
    # Define the y-coordinate range for the player's cards
    y_start = HEIGHT - CARD_HEIGHT - 100
    y_end = y_start + CARD_HEIGHT

    # Iterate through the player's cards to check if the click is within a card's bounds
    for i, card in enumerate(you_nerd.cards):
        x_start = MARGIN + i * (CARD_WIDTH + MARGIN)
        x_end = x_start + CARD_WIDTH

        # Check if the click position is within the current card's bounds
        if x_start <= pos[0] <= x_end and y_start <= pos[1] <= y_end:
            return card  # Return the clicked card

    # If no card is clicked, return None
    return None


########################
game_running = False
player_turn = True
game_over = False  # New state to handle the fade effect
hovered_card = None
clicked_card = None  # Track the clicked card to display details
bot_action_ready = False


while True:
    if not game_running and not game_over:
        # Main menu logic
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_running = True

    elif game_running and not game_over:
        # Main game logic
        mouse_pos = pygame.mouse.get_pos()
        hovered_card = handle_card_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                draw_button_rect = draw_ui()
                if player_turn:
                    if draw_button_rect.collidepoint(event.pos):
                        handle_draw_card()
                        draw_ui()  # Update the UI immediately after drawing a card
                        pygame.display.flip()
                    else:
                        if event.button == 1:  # Left click
                            print("LEFT CLICKED")
                            clicked_card = handle_card_click(event.pos)
                            play_card(clicked_card)
                        if event.button == 3:  # Right click
                            print("RIGHT CLICKED")
                            clicked_card = handle_card_click(event.pos)
                            if clicked_card:
                                # print(clicked_card.n)
                                display_card_details(clicked_card)

        if not player_turn:
            handle_bot_turn()

        # Check if the game ends
        if you_nerd.health <= 0 or bot_chad.health <= 0:
            game_over = True
            start_ticks = pygame.time.get_ticks()  # Record the fade start time
            end_sound.play()

        # If there's a hovered card, display a tooltip
        if hovered_card:
            pygame.draw.rect(screen, BLACK, (mouse_pos[0] + 10, mouse_pos[1] + 10, 120, 60))
            pygame.draw.rect(screen, WHITE, (mouse_pos[0] + 12, mouse_pos[1] + 12, 116, 56))
            card_name_text = font.render(hovered_card.n, True, BLACK)
            screen.blit(card_name_text, (mouse_pos[0] + 15, mouse_pos[1] + 15))
        draw_ui()
        pygame.display.flip()
        clock.tick(FPS)

    elif game_over:
        # Render the fade effect and end screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if alpha < 255:
            alpha += fade_speed  # Increment alpha based on fade speed
            if alpha > 255:
                alpha = 255
            fade_surface.set_alpha(int(alpha))
            fade_surface.blit(lebron, (0, 0))
            screen.blit(fade_surface, (0, 0))
        else:
            # Once fully faded in, just draw the image directly
            screen.blit(lebron, (0, 0))

        # Stop sound after 10 seconds
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        if elapsed_time >= fade_duration:
            end_sound.stop()

        pygame.display.flip()
        clock.tick(60)  # Limit frame rate


