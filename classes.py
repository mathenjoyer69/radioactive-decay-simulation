import random
import math
from config import *

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.is_selected = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered or self.is_selected else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=5)

        text_surface = font.render(self.text, True, WHITE if self.is_hovered or self.is_selected else BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_over(self, pos):
        return self.rect.collidepoint(pos)


class Atom:
    def __init__(self, x, y, atom_type, atom_id):
        self.x = x
        self.y = y
        self.type = atom_type
        self.id = atom_id
        self.radius = 24
        self.decayed = False
        self.lifetime = -math.log(2, math.e) * isotopes[atom_type]["half_life"] / math.log(random.random())
        self.in_basket = True
        self.dragging = False
        self.vibrate_offset = (0, 0)
        self.vibrate_timer = 0

    def draw(self, surface, current_time):
        if not self.decayed:
            self.vibrate_timer += 1
            if self.vibrate_timer % 15 == 0:
                self.vibrate_offset = (random.randint(-2, 2), random.randint(-2, 2))
        else:
            self.vibrate_offset = (0, 0)

        if not self.decayed and current_time >= self.lifetime:
            self.decayed = True

        isotope = isotopes[self.type]
        color = isotope["decay_product_color"] if self.decayed else isotope["color"]
        symbol = isotope["decay_product"] if self.decayed else isotope["symbol"]

        draw_x = self.x + self.vibrate_offset[0]
        draw_y = self.y + self.vibrate_offset[1]
        pygame.draw.circle(surface, color, (draw_x, draw_y), self.radius)
        pygame.draw.circle(surface, BLACK, (draw_x, draw_y), self.radius, 2)

        text_surface = small_font.render(symbol, True, WHITE)
        text_rect = text_surface.get_rect(center=(draw_x, draw_y))
        surface.blit(text_surface, text_rect)

    def is_over(self, pos):
        return math.sqrt((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2) < self.radius


class Timeline:
    def __init__(self, x, y, width, height, max_time):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_time = max_time
        self.decay_events = []

    def add_decay_event(self, atom_id, decay_time, position):
        self.decay_events.append({
            "id": atom_id,
            "time": decay_time,
            "position": position
        })

    def draw(self, surface, current_time, half_life):
        pygame.draw.rect(surface, BLACK, self.rect, 1)

        for i in range(4):
            position = int(self.rect.x + (i * half_life / self.max_time) * self.rect.width)
            pygame.draw.line(surface, BLACK, (position, self.rect.y), (position, self.rect.y + 10), 2)
            text = f"{i}T½"
            text_surface = small_font.render(text, True, BLACK)
            surface.blit(text_surface, (position - 10, self.rect.y + 12))

        for event in self.decay_events:
            position = int(self.rect.x + (event["time"] / self.max_time) * self.rect.width)
            pygame.draw.circle(surface, RED, (position, self.rect.y + self.rect.height - 5), 3)

        time_position = min(self.rect.x + int((current_time / self.max_time) * self.rect.width), self.rect.x + self.rect.width)
        pygame.draw.line(surface, BLUE, (time_position, self.rect.y), (time_position, self.rect.y + self.rect.height), 2)

    def draw_decay_graph(self, surface, element, time):
        graph_width = WIDTH // 4
        graph_height = HEIGHT // 4
        graph_x = WIDTH - graph_width - 20
        graph_y = HEIGHT - graph_height - 30

        pygame.draw.rect(surface, (240, 240, 240), (graph_x, graph_y, graph_width, graph_height))
        pygame.draw.rect(surface, BLACK, (graph_x, graph_y, graph_width, graph_height), 1)

        is_short_half_life = (element == "polonium")
        x_label = font.render(f"Time (y)", True, BLACK)
        surface.blit(x_label, (graph_x + graph_width // 2 - x_label.get_width() // 2, graph_y + graph_height + 12))

        y_label = font.render("Nuclei Remaining", True, BLACK)
        y_label = pygame.transform.rotate(y_label, 90)
        surface.blit(y_label, (graph_x - 50, graph_y + graph_height // 2 - 2.7*y_label.get_width()))

        half_life = isotopes[element]['half_life']
        initial_nuclei = 10
        max_time = max(time, half_life * 3)

        for i in range(10):
            t = half_life * i
            if t <= max_time:
                x_pos = graph_x + (t / max_time) * graph_width
                pygame.draw.line(surface, (200, 200, 200), (x_pos, graph_y), (x_pos, graph_y + graph_height), 1)
                label = f"{t/365.25:.1f}y" if is_short_half_life else f"{t / (1e9*365.25):.1f}B y"
                t_label = font.render(label, True, BLACK)
                surface.blit(t_label, (x_pos - t_label.get_width() // 2, graph_y + graph_height))

        for i in range(0, 101, 25):
            y_pos = graph_y + graph_height - (i / 100) * graph_height
            pygame.draw.line(surface, (200, 200, 200), (graph_x, y_pos), (graph_x + graph_width, y_pos), 1)
            num_label = font.render(f"{i}%", True, BLACK)
            surface.blit(num_label, (graph_x - 35, y_pos - 10))

        points = []
        resolution = max(1, int(max_time / 100))
        t_range = range(0, int(time) + 1, resolution)
        for t_val in t_range:
            x = graph_x + (t_val / max_time) * graph_width
            remaining = initial_nuclei * (0.5 ** (t_val / half_life))
            y = graph_y + graph_height - (remaining / initial_nuclei) * graph_height
            points.append((x, y))

        if len(points) > 1:
            pygame.draw.lines(surface, BLACK, False, points, 2)
