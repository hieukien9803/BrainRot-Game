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
shower_card = Card("shower_card", 2, 0, "damage")
touchgrass_card = Card("touchgrass_card", 1, 0, "damage")
deodorant_card = Card("deodorant_card", 2, 0, "damage")
gpt_card = Card("gpt_card", 1, 0, "damage")
light_mode_card = Card("light_mode_card", 1, 0, "damage")
talktowoman_card = Card("talktowoman_card", 2, 0, "damage")
if_card = Card("if_card", 1, 0, "damage")
timecomplex_card = Card("timecomplex_card", 2, 0, "damage")
failunittest_card = Card("failunittest_card", 3, 0, "damage")
centerdiv_card = Card("centerdiv_card", 2, 0,"damage")
# support card
darkmode_card = Card("darkmode_card", 0, 2, "heal")
python_card = Card("python_card", 0, 3, "heal")
energydrink_card = Card("energydrink_card", 0, 2, "heal")

deck = [shower_card, touchgrass_card, deodorant_card, gpt_card, light_mode_card,
        talktowoman_card, if_card, timecomplex_card, failunittest_card,
        centerdiv_card,
        darkmode_card, python_card, energydrink_card]
# set up players
you_nerd = Player(card=random.sample(deck, 6))
bot_chad = Player(card=random.sample(deck, 6))
player_cards_played = []
bot_cards_played = []

# Initialize pygame
pygame.init()

# LOAD SOUND
pygame.mixer.init()
button_sound = pygame.mixer.Sound("asset/button.wav")
drawcard_sound = pygame.mixer.Sound("asset/drawcard.wav")
placingcard_sound = pygame.mixer.Sound("asset/placingcard.wav")
end_sound = pygame.mixer.Sound("asset/sunshine.wav")
end_sound.set_volume(1.0)

# Constants
WIDTH, HEIGHT = 1400, 800
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
# Load images for the cards

card_images = {
    "shower_card": "assets/shower_card.png",
    "touchgrass_card": "assets/touchgrass_card.png",
    "deodorant_card": "assets/deodorant_card.png",
    "gpt_card": "assets/gpt_card.png",
    "light_mode_card": "assets/light_mode_card.png",
    "talktowoman_card": "assets/talktowoman_card.png",
    "if_card": "assets/if_card.png",
    "timecomplex_card": "assets/timecomplex_card.png",
    "failunittest_card": "assets/failunittest_card.png",
    "centerdiv_card": "assets/centerdiv_card.png",
    "darkmode_card": "assets/darkmode_card.png",
    "python_card": "assets/python_card.png",
    "energydrink_card": "assets/energydrink_card.png"
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
    screen.fill(WHITE)

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
        card_text = font.render(str(card), True, WHITE)
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
    """Handle the draw card action."""
    global player_turn
    new_card = random.choice(deck)
    you_nerd.cards.append(new_card)
    pygame.mixer.Sound.play(drawcard_sound)
    player_turn = False

def handle_player_turn(pos):
    """Handle the player's turn and card click to show details."""
    global player_turn, selected_card

    y = HEIGHT - CARD_HEIGHT - 100
    for i, card in enumerate(you_nerd.cards):
        x = MARGIN + i * (CARD_WIDTH + MARGIN)
        if x < pos[0] < x + CARD_WIDTH and y < pos[1] < y + CARD_HEIGHT:
            # If a card is clicked, show its image
            selected_card = card
            return  # Exit after selecting the card to show its details

def handle_bot_turn():
    """Handle the bot's turn."""
    global player_turn

    if bot_chad.cards:
        card = random.choice(bot_chad.cards)
        bot_cards_played.append(card)
        if card.t == "damage":
            you_nerd.health -= card.d
        elif card.t == "heal":
            bot_chad.health = min(10, bot_chad.health + card.h)
        bot_chad.cards.remove(card)
    player_turn = True


def display_card_details(card):
    """Display detailed information about a card."""
    detail_width, detail_height = 300, 200
    detail_x = WIDTH // 2 - detail_width // 2
    detail_y = HEIGHT // 2 - detail_height // 2

    # Draw a background rectangle for the details
    pygame.draw.rect(screen, BLACK, (detail_x, detail_y, detail_width, detail_height))
    pygame.draw.rect(screen, WHITE, (detail_x + 5, detail_y + 5, detail_width - 10, detail_height - 10))

    # Display card details (Name, Damage, Heal, Type)
    name_text = font.render(f"Name: {card.n}", True, BLACK)
    damage_text = font.render(f"Damage: {card.d}", True, BLACK)
    heal_text = font.render(f"Heal: {card.h}", True, BLACK)
    type_text = font.render(f"Type: {card.t}", True, BLACK)

    screen.blit(name_text, (detail_x + 20, detail_y + 20))
    screen.blit(damage_text, (detail_x + 20, detail_y + 60))
    screen.blit(heal_text, (detail_x + 20, detail_y + 100))
    screen.blit(type_text, (detail_x + 20, detail_y + 140))


def handle_card_hover(pos):
    """Handle mouse hover over a card."""
    y = HEIGHT - CARD_HEIGHT - 100
    for i, card in enumerate(you_nerd.cards):
        x = MARGIN + i * (CARD_WIDTH + MARGIN)
        if x < pos[0] < x + CARD_WIDTH and y < pos[1] < y + CARD_HEIGHT:
            return card
    return None


def handle_card_click(pos):
    """Handle clicking on a card to view its details."""
    y = HEIGHT - CARD_HEIGHT - 100
    for i, card in enumerate(you_nerd.cards):
        x = MARGIN + i * (CARD_WIDTH + MARGIN)
        if x < pos[0] < x + CARD_WIDTH and y < pos[1] < y + CARD_HEIGHT:
            return card
    return None


########################
game_running = False
player_turn = True
game_over = False  # New state to handle the fade effect
hovered_card = None
clicked_card = None  # Track the clicked card to display details

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
        hovered_card = handle_card_hover(mouse_pos)  # Update hovered card

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                draw_button_rect = draw_ui()
                if player_turn:
                    if draw_button_rect.collidepoint(event.pos):
                        handle_draw_card()
                    else:
                        clicked_card = handle_card_click(event.pos)  # Set the clicked card

        if not player_turn:
            pygame.time.delay(1000)  # Simulate thinking time
            handle_bot_turn()

        # Check if the game ends
        if you_nerd.health <= 0 or bot_chad.health <= 0:
            game_over = True
            start_ticks = pygame.time.get_ticks()  # Record the fade start time
            end_sound.play()

        draw_ui()

        # If there's a hovered card, display a tooltip
        if hovered_card:
            pygame.draw.rect(screen, BLACK, (mouse_pos[0] + 10, mouse_pos[1] + 10, 120, 60))
            pygame.draw.rect(screen, WHITE, (mouse_pos[0] + 12, mouse_pos[1] + 12, 116, 56))
            card_name_text = font.render(hovered_card.n, True, BLACK)
            screen.blit(card_name_text, (mouse_pos[0] + 15, mouse_pos[1] + 15))

        # If there's a clicked card, display detailed information
        if clicked_card:
            display_card_details(clicked_card)

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
