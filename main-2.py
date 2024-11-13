import pygame
import sys
import random

# Initialize Pygame
pygame.init()
# Enable key repeating
pygame.key.set_repeat(200, 50)  # (delay, interval) in milliseconds

# Screen dimensions
WIDTH, HEIGHT = 1200, 750
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
TITLE_FONT = pygame.font.SysFont('Arial', 20)

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
        bar_height = int((val / max_array_value) * (height - 100))  # Adjusted height
        y = y_offset + (height - bar_height)
        color = BAR_COLOR

        # Highlight bars being compared or swapped
        if idx in indices:
            color = highlight_color

        pygame.draw.rect(WINDOW, color, (x, y, bar_width - 2, bar_height))
        # Draw value below bar
        text = FONT.render(str(val), True, TEXT_COLOR)
        text_rect = text.get_rect(center=(x + bar_width // 2, y + bar_height + 5))
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
        # Comparison text will be drawn in the main loop to avoid duplication

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
    left_visualizer = BubbleSortVisualizer(array, 50, 50, WIDTH // 2 - 100, HEIGHT - 300, implementation=1)
    right_visualizer = BubbleSortVisualizer(array, WIDTH // 2 + 50, 50, WIDTH // 2 - 100, HEIGHT - 300, implementation=2)

    # Buttons
    button_width = 80
    button_height = 30

    # Single Next and Back Buttons
    button_y = left_visualizer.y_offset + left_visualizer.height + 40  # Added more space
    next_button = pygame.Rect(WIDTH // 2 + 10, button_y, button_width, button_height)
    back_button = pygame.Rect(WIDTH // 2 - button_width - 10, button_y, button_width, button_height)
    # Reset Button
    reset_button = pygame.Rect(WIDTH // 2 - 40, HEIGHT - 50, 80, 30)

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
                if next_button.collidepoint(event.pos):
                    left_visualizer.next_step()
                    right_visualizer.next_step()
                if back_button.collidepoint(event.pos):
                    left_visualizer.previous_step()
                    right_visualizer.previous_step()
                if reset_button.collidepoint(event.pos):
                    array = generate_array()
                    left_visualizer = BubbleSortVisualizer(array, 50, 50, WIDTH // 2 - 100, HEIGHT - 300, implementation=1)
                    right_visualizer = BubbleSortVisualizer(array, WIDTH // 2 + 50, 50, WIDTH // 2 - 100, HEIGHT - 300, implementation=2)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    left_visualizer.next_step()
                    right_visualizer.next_step()
                if event.key == pygame.K_b:
                    left_visualizer.previous_step()
                    right_visualizer.previous_step()

        # Draw Visualizations
        left_visualizer.draw()
        right_visualizer.draw()

        # Draw Buttons
        pygame.draw.rect(WINDOW, COMPARISON_COLOR, next_button)
        pygame.draw.rect(WINDOW, HIGHLIGHT_COLOR, back_button)
        pygame.draw.rect(WINDOW, SWAP_COLOR, reset_button)

        # Button Text
        next_text = FONT.render('Next', True, TEXT_COLOR)
        back_text = FONT.render('Back', True, TEXT_COLOR)
        reset_text = FONT.render('Reset', True, TEXT_COLOR)

        WINDOW.blit(next_text, (next_button.x + 20, next_button.y + 5))
        WINDOW.blit(back_text, (back_button.x + 20, back_button.y + 5))
        WINDOW.blit(reset_text, (reset_button.x + 15, reset_button.y + 5))

        # Titles
        left_title = TITLE_FONT.render('Implementation 1', True, TEXT_COLOR)
        right_title = TITLE_FONT.render('Implementation 2', True, TEXT_COLOR)
        WINDOW.blit(left_title, (left_visualizer.x_offset + left_visualizer.width // 2 - left_title.get_width() // 2, 15))
        WINDOW.blit(right_title, (right_visualizer.x_offset + right_visualizer.width // 2 - right_title.get_width() // 2, 15))

        # Draw Comparison Text Below Buttons
        if left_visualizer.comparison_result is not None:
            idx1, idx2 = left_visualizer.highlight_indices
            val1 = left_visualizer.array[idx1]
            val2 = left_visualizer.array[idx2]
            x_center = left_visualizer.x_offset + left_visualizer.width // 2
            y = next_button.y + button_height + 30
            draw_comparison(val1, val2, left_visualizer.comparison_result, x_center, y)

        if right_visualizer.comparison_result is not None:
            idx1, idx2 = right_visualizer.highlight_indices
            val1 = right_visualizer.array[idx1]
            val2 = right_visualizer.array[idx2]
            x_center = right_visualizer.x_offset + right_visualizer.width // 2
            y = next_button.y + button_height + 30
            draw_comparison(val1, val2, right_visualizer.comparison_result, x_center, y)

        pygame.display.update()

if __name__ == '__main__':
    main()
