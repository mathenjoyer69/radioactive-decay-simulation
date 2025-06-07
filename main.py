import sys

import pygame.key

from classes import *

class DecaySimulation:
    def __init__(self):
        self.selected_isotope = None
        self.atoms = []
        self.time = 0
        self.is_running = False
        self.speed = 1
        self.dragging_atom = None
        self.atom_count = 0
        self.last_update = pygame.time.get_ticks()
        self.electrons = []
        self.rb_button = Button(WIDTH - 200, 110, 180, 40, "rubidium-87", RED, dark_red)
        self.start_pause_button = Button(WIDTH - 200, 160, 180, 40, "Start", green_button, dark_green_button)
        self.reset_button = Button(WIDTH - 200, 210, 180, 40, "Reset Time", gray, dark_gray)
        self.flag = False
        self.speed_options = {
            "rubidium": [
                {"value": 365.25 * 1e8, "label": "100M years/sec"},
                {"value": 365.25 * 1e9, "label": "1B years/sec"},
                {"value": 365.25 * 1e10, "label": "10B years/sec"}
            ]
        }

        self.speed_buttons = []
        for i, option in enumerate(self.speed_options["rubidium"]):
            btn = Button(WIDTH - 200, 270 + i * 40, 180, 30, option["label"], GRAY, (150, 150, 150))
            self.speed_buttons.append(btn)

        self.basket = pygame.Rect(50, HEIGHT - 100, 250, 80)

        self.timeline = None

    def create_basket(self, isotope_type):
        self.selected_isotope = isotope_type
        self.atoms = []
        self.time = 0
        self.is_running = False

        self.rb_button.is_selected = isotope_type == "rubidium"

        self.speed_buttons = []
        y_offset = 270
        for i, option in enumerate(self.speed_options[isotope_type]):
            btn = Button(WIDTH - 200, y_offset + i * 40, 180, 30, option["label"], GRAY, (150, 150, 150))
            self.speed_buttons.append(btn)

        for i in range(10):
            x = self.basket.x + 30 + i * 20
            y = self.basket.y + 40
            atom = Atom(x, y, isotope_type, f"atom-{self.atom_count + i}")
            self.atoms.append(atom)

        half_life = isotopes[isotope_type]["half_life"]
        self.timeline = Timeline(20, 50, WIDTH - 100, 40, half_life * 4)

        self.start_pause_button.text = "Start"

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEMOTION:
            self.rb_button.is_hovered = self.rb_button.is_over(mouse_pos)
            self.start_pause_button.is_hovered = self.start_pause_button.is_over(mouse_pos)
            self.reset_button.is_hovered = self.reset_button.is_over(mouse_pos)

            for btn in self.speed_buttons:
                btn.is_hovered = btn.is_over(mouse_pos)

            if self.dragging_atom is not None:
                atom = self.atoms[self.dragging_atom]
                atom.x = mouse_pos[0]
                atom.y = mouse_pos[1]
                atom.in_basket = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.flag and self.selected_isotope:
                for atom in self.atoms:
                    atom.x = random.randint(100, 700)
                    atom.y = random.randint(100, 450)
                self.flag = True

            if self.rb_button.is_over(mouse_pos):
                self.create_basket("rubidium")
            elif self.selected_isotope and self.start_pause_button.is_over(mouse_pos):
                self.is_running = not self.is_running
                self.start_pause_button.text = "Pause" if self.is_running else "Start"
                self.start_pause_button.color = (200, 50, 50) if self.is_running else (50, 200, 50)
                self.start_pause_button.hover_color = (150, 20, 20) if self.is_running else (20, 150, 20)
                self.speed = 0
            elif self.selected_isotope and self.reset_button.is_over(mouse_pos):
                self.time = 0
                self.timeline.decay_events = []
                for atom in self.atoms:
                    atom.decayed = False

            for i, btn in enumerate(self.speed_buttons):
                if btn.is_over(mouse_pos):
                    for j, b in enumerate(self.speed_buttons):
                        b.is_selected = (i == j)
                    self.speed = self.speed_options[self.selected_isotope][i]["value"]

            if self.selected_isotope:
                for i, atom in enumerate(self.atoms):
                    if not atom.decayed and atom.is_over(mouse_pos):
                        self.dragging_atom = i
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging_atom = None

    def shoot_electron(self, x, y, direction):
        self.electrons.append(Electron(x, y, direction))

    def update(self):
        if not self.is_running or not self.selected_isotope:
            return

        current_time = pygame.time.get_ticks()
        dt = (current_time - self.last_update) / 1000.0
        self.last_update = current_time

        self.time += dt * self.speed

        for atom in self.atoms:
            if not atom.decayed and self.time >= atom.lifetime:
                atom.decayed = True
                self.shoot_electron(atom.x, atom.y, (random.uniform(-1, 1), random.uniform(-1, 1)))
                self.timeline.add_decay_event(atom.id, atom.lifetime, (atom.x, atom.y))

    def draw(self, surface):
        surface.fill(WHITE)

        self.rb_button.draw(surface)

        if self.selected_isotope:
            self.start_pause_button.draw(surface)
            self.reset_button.draw(surface)

            for btn in self.speed_buttons:
                btn.draw(surface)

            pygame.draw.rect(surface, GRAY, self.basket)
            pygame.draw.rect(surface, BLACK, self.basket, 2)
            decayed_count = sum(1 for atom in self.atoms if atom.decayed)
            self.timeline.draw(surface, self.time, isotopes[self.selected_isotope]["half_life"])
            self.timeline.draw_decay_graph(surface, self.selected_isotope, self.time)

            for atom in self.atoms:
                atom.draw(surface, self.time)

            for electron in self.electrons[:]:
                electron.update()
                electron.draw(surface)
                if electron.is_off_screen():
                    self.electrons.remove(electron)

            stats_rect = pygame.Rect(WIDTH - 200, 400, 180, 80)
            pygame.draw.rect(surface, WHITE, stats_rect)
            pygame.draw.rect(surface, BLACK, stats_rect, 1)

            time_text = f"Time: {(self.time / 365.25 / 1e9):.2f}b years"

            decay_text = f"Decayed: {decayed_count}/{len(self.atoms)}"

            time_surface = small_font.render(time_text, True, BLACK)
            decay_surface = small_font.render(decay_text, True, BLACK)

            surface.blit(time_surface, (stats_rect.x + 10, stats_rect.y + 10))
            surface.blit(decay_surface, (stats_rect.x + 10, stats_rect.y + 40))
        else:
            text = "select an isotope to begin the simulation"
            text_surface = font.render(text, True, BLACK)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            surface.blit(text_surface, text_rect)

def main():
    clock = pygame.time.Clock()
    simulation = DecaySimulation()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            simulation.handle_event(event)
        simulation.update()
        simulation.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


main()
