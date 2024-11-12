import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Sort Visualizer")

# Colors
BACKGROUND_COLOR = (30, 30, 30)
BAR_COLOR = (70, 130, 180)
HIGHLIGHT_COLOR = (220, 20, 60)
COMPARISON_COLOR = (34, 139, 34)
SWAP_COLOR = (255, 165, 0)
TEXT_COLOR = (255, 255, 255)

# Fonts
FONT = pygame.font.SysFont('Arial', 16)

# Sorting Variables
array_size = 10
max_value = 100

# Generate a random array
def generate_array():
    return [random.randint(10, max_value) for _ in range(array_size)]

# Draw the bars
def draw_bars(array, x_offset, y_offset, width, height, indices, highlight_color):
    bar_width = width // len(array)
    max_array_value = max(array)
    for idx, val in enumerate(array):
        x = x_offset + idx * bar_width
        bar_height = int((val / max_array_value) * (height - 50))
        y = y_offset + (height - bar_height)
        color = BAR_COLOR

        # Highlight bars being compared or swapped
        if idx in indices:
            color = highlight_color

        pygame.draw.rect(WINDOW, color, (x, y, bar_width - 2, bar_height))
        # Draw value below bar
        text = FONT.render(str(val), True, TEXT_COLOR)
        text_rect = text.get_rect(center=(x + bar_width // 2, y + bar_height + 15))
        WINDOW.blit(text, text_rect)

# Draw comparison text
def draw_comparison(val1, val2, result, x_center, y):
    comparison_text = f"{val1} < {val2}"
    color = COMPARISON_COLOR if result else HIGHLIGHT_COLOR
    text = FONT.render(comparison_text, True, color)
    text_rect = text.get_rect(center=(x_center, y))
    WINDOW.blit(text, text_rect)
    # Underline the text
    pygame.draw.line(WINDOW, color, (text_rect.left, text_rect.bottom), (text_rect.right, text_rect.bottom), 2)

# Bubble Sort Implementations
class BubbleSortVisualizer:
    def __init__(self, array, x_offset, y_offset, width, height, implementation):
        self.original_array = array.copy()
        self.array = array.copy()
        self.steps = []
        self.current_step = -1
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.width = width
        self.height = height
        self.finished = False
        self.highlight_indices = []
        self.highlight_color = BAR_COLOR
        self.comparison_result = None
        self.implementation = implementation
        self.generate_steps()

    def generate_steps(self):
        arr = self.array.copy()
        n = len(arr)
        steps = []

        if self.implementation == 1:
            # First Bubble Sort implementation
            for i in range(n):
                for j in range(n - i - 1):
                    steps.append(('compare', j, j+1))
                    if arr[j] > arr[j+1]:
                        arr[j], arr[j+1] = arr[j+1], arr[j]
                        steps.append(('swap', j, j+1, arr.copy()))
        else:
            # Second Bubble Sort implementation
            for i in range(n - 1):
                for j in range(i + 1, n):
                    steps.append(('compare', i, j))
                    if arr[i] > arr[j]:
                        arr[i], arr[j] = arr[j], arr[i]
                        steps.append(('swap', i, j, arr.copy()))
        self.steps = steps

    def next_step(self):
        if self.current_step + 1 < len(self.steps):
            self.current_step += 1
            action = self.steps[self.current_step]
            if action[0] == 'compare':
                self.highlight_indices = [action[1], action[2]]
                self.highlight_color = COMPARISON_COLOR
                val1 = self.array[action[1]]
                val2 = self.array[action[2]]
                self.comparison_result = val1 < val2
            elif action[0] == 'swap':
                self.highlight_indices = [action[1], action[2]]
                self.highlight_color = SWAP_COLOR
                self.array = action[3]
                self.comparison_result = None
        else:
            self.finished = True
            self.highlight_indices = []
            self.comparison_result = None

    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            # Rebuild array from initial state up to current step
            self.array = self.original_array.copy()
            for i in range(self.current_step + 1):
                action = self.steps[i]
                if action[0] == 'swap':
                    self.array = action[3]
            action = self.steps[self.current_step]
            if action[0] == 'compare':
                self.highlight_indices = [action[1], action[2]]
                self.highlight_color = COMPARISON_COLOR
                val1 = self.array[action[1]]
                val2 = self.array[action[2]]
                self.comparison_result = val1 < val2
            elif action[0] == 'swap':
                self.highlight_indices = [action[1], action[2]]
                self.highlight_color = SWAP_COLOR
                self.comparison_result = None
            self.finished = False
        elif self.current_step == 0:
            self.reset()

    def draw(self):
        draw_bars(self.array, self.x_offset, self.y_offset, self.width, self.height, self.highlight_indices, self.highlight_color)
        if self.comparison_result is not None:
            idx1, idx2 = self.highlight_indices
            val1 = self.array[idx1]
            val2 = self.array[idx2]
            x_center = self.x_offset + self.width // 2
            y = self.y_offset + self.height - 30
            draw_comparison(val1, val2, self.comparison_result, x_center, y)

    def reset(self):
        self.current_step = -1
        self.array = self.original_array.copy()
        self.finished = False
        self.highlight_indices = []
        self.highlight_color = BAR_COLOR
        self.comparison_result = None

# Main Loop
def main():
    global array
    array = generate_array()
    left_visualizer = BubbleSortVisualizer(array, 50, 50, WIDTH // 2 - 100, HEIGHT - 100, implementation=1)
    right_visualizer = BubbleSortVisualizer(array, WIDTH // 2 + 50, 50, WIDTH // 2 - 100, HEIGHT - 100, implementation=2)

    # Buttons
    button_width = 80
    button_height = 30
    left_next_button = pygame.Rect(150, HEIGHT - 40, button_width, button_height)
    left_back_button = pygame.Rect(50, HEIGHT - 40, button_width, button_height)
    right_next_button = pygame.Rect(WIDTH - 150 - button_width, HEIGHT - 40, button_width, button_height)
    right_back_button = pygame.Rect(WIDTH - 50 - button_width, HEIGHT - 40, button_width, button_height)
    reset_button = pygame.Rect(WIDTH // 2 - 40, HEIGHT - 40, 80, 30)

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        WINDOW.fill(BACKGROUND_COLOR)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if left_next_button.collidepoint(event.pos):
                    left_visualizer.next_step()
                if left_back_button.collidepoint(event.pos):
                    left_visualizer.previous_step()
                if right_next_button.collidepoint(event.pos):
                    right_visualizer.next_step()
                if right_back_button.collidepoint(event.pos):
                    right_visualizer.previous_step()
                if reset_button.collidepoint(event.pos):
                    array = generate_array()
                    left_visualizer = BubbleSortVisualizer(array, 50, 50, WIDTH // 2 - 100, HEIGHT - 100, implementation=1)
                    right_visualizer = BubbleSortVisualizer(array, WIDTH // 2 + 50, 50, WIDTH // 2 - 100, HEIGHT - 100, implementation=2)

        # Draw Visualizations
        left_visualizer.draw()
        right_visualizer.draw()

        # Draw Buttons
        pygame.draw.rect(WINDOW, COMPARISON_COLOR, left_next_button)
        pygame.draw.rect(WINDOW, HIGHLIGHT_COLOR, left_back_button)
        pygame.draw.rect(WINDOW, COMPARISON_COLOR, right_next_button)
        pygame.draw.rect(WINDOW, HIGHLIGHT_COLOR, right_back_button)
        pygame.draw.rect(WINDOW, SWAP_COLOR, reset_button)

        # Button Text
        next_text = FONT.render('Next', True, TEXT_COLOR)
        back_text = FONT.render('Back', True, TEXT_COLOR)
        reset_text = FONT.render('Reset', True, TEXT_COLOR)

        WINDOW.blit(next_text, (left_next_button.x + 20, left_next_button.y + 5))
        WINDOW.blit(back_text, (left_back_button.x + 20, left_back_button.y + 5))
        WINDOW.blit(next_text, (right_next_button.x + 20, right_next_button.y + 5))
        WINDOW.blit(back_text, (right_back_button.x + 20, right_back_button.y + 5))
        WINDOW.blit(reset_text, (reset_button.x + 15, reset_button.y + 5))

        # Titles
        title_font = pygame.font.SysFont('Arial', 20)
        left_title = title_font.render('Implementation 1', True, TEXT_COLOR)
        right_title = title_font.render('Implementation 2', True, TEXT_COLOR)
        WINDOW.blit(left_title, (left_visualizer.x_offset + left_visualizer.width // 2 - left_title.get_width() // 2, 15))
        WINDOW.blit(right_title, (right_visualizer.x_offset + right_visualizer.width // 2 - right_title.get_width() // 2, 15))

        pygame.display.update()

if __name__ == '__main__':
    main()