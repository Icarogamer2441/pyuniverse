import pygame
import sys
import math

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PyUniverse")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

G = 150
drag_force_multiplier = 0.2
mass_increase = 10
black_hole_mass = 1000
star_mass = 100  # Massa da estrela

def calculate_gravity(obj1, obj2):
    distance = max(1, math.hypot(obj2['x'] - obj1['x'], obj2['y'] - obj1['y']))
    force = G * (obj1['mass'] * obj2['mass']) / (distance ** 2)
    angle = math.atan2(obj2['y'] - obj1['y'], obj2['x'] - obj1['x'])
    force_x = force * math.cos(angle)
    force_y = force * math.sin(angle)
    return force_x, force_y

class CelestialBody:
    def __init__(self, x, y, radius, color, mass=1):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity = [0, 0]
        self.mass = mass

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def apply_force(self, force):
        acceleration_x = force[0] / self.mass
        acceleration_y = force[1] / self.mass
        self.velocity[0] += acceleration_x
        self.velocity[1] += acceleration_y

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def increase_mass(self, amount):
        self.mass += amount

# Tela inicial
font = pygame.font.Font(None, 24)
text = font.render("PyUniverse", True, white)
text_rect = text.get_rect(center=(width//2, height//2 - 100))

info_text1 = font.render("Left click to create a planet", True, white)
info_text1_rect = info_text1.get_rect(center=(width//2, height//2 - 80))  # Ajuste na coordenada y

info_text2 = font.render("Right click on a planet to increase its mass", True, white)
info_text2_rect = info_text2.get_rect(center=(width//2, height//2 - 40))  # Ajuste na coordenada y

info_text3 = font.render("Press 'B' to create a black hole at the mouse position", True, white)
info_text3_rect = info_text3.get_rect(center=(width//2, height//2 + 10))  # Ajuste na coordenada y

info_text4 = font.render("Press 'D' to delete all planets and black holes", True, white)
info_text4_rect = info_text4.get_rect(center=(width//2, height//2 + 60))  # Ajuste na coordenada y

info_text5 = font.render("Drag with left click to apply a force to the planets", True, white)
info_text5_rect = info_text5.get_rect(center=(width//2, height//2 + 110))  # Ajuste na coordenada y

info_text6 = font.render("Press 'S' to create a star", True, white)
info_text6_rect = info_text6.get_rect(center=(width//2, height//2 + 160))  # Ajuste na coordenada y

info_text7 = font.render("G: 150 (Gravitational constant)", True, white)
info_text7_rect = info_text7.get_rect(center=(width//2, height//2 + 210))  # Ajuste na coordenada y

info_text8 = font.render("Press 'P' to start playing", True, white)
info_text8_rect = info_text8.get_rect(center=(width//2, height//2 + 260))  # Ajuste na coordenada y

# Exibir tela inicial
screen.fill(black)
screen.blit(text, text_rect)
screen.blit(info_text1, info_text1_rect)
screen.blit(info_text2, info_text2_rect)
screen.blit(info_text3, info_text3_rect)
screen.blit(info_text4, info_text4_rect)
screen.blit(info_text5, info_text5_rect)
screen.blit(info_text6, info_text6_rect)
screen.blit(info_text7, info_text7_rect)
screen.blit(info_text8, info_text8_rect)
pygame.display.flip()

waiting_for_start = True

while waiting_for_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                waiting_for_start = False

# Limpar a tela inicial
screen.fill(black)
pygame.display.flip()

celestial_bodies = []  # Lista para armazenar planetas, estrelas e buracos negros

clock = pygame.time.Clock()
dragging = False
drag_start = (0, 0)
drag_force = (0, 0)

dragging_star = False
star_drag_start = (0, 0)

scroll_speed = 5
center_arrow_size = 10

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                dragging = True
                drag_start = pygame.mouse.get_pos()
            elif event.button == 3:
                for body in celestial_bodies:
                    distance = math.hypot(event.pos[0] - body.x, event.pos[1] - body.y)
                    if distance <= body.radius:
                        body.increase_mass(mass_increase)
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            new_planet = CelestialBody(event.pos[0], event.pos[1], 20, white)
            celestial_bodies.append(new_planet)
            new_planet.apply_force((drag_force[0] * drag_force_multiplier, drag_force[1] * drag_force_multiplier))
            drag_force = (0, 0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                # Cria um buraco negro nas coordenadas do mouse
                black_hole = CelestialBody(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 30, blue, black_hole_mass)
                celestial_bodies.append(black_hole)
            elif event.key == pygame.K_s:
                # Cria uma estrela nas coordenadas do mouse
                star = CelestialBody(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 50, red, star_mass)
                celestial_bodies.append(star)
            elif event.key == pygame.K_d:
                # Deleta todos os corpos celestes
                celestial_bodies = []
            elif event.key == pygame.K_LEFT:
                for body in celestial_bodies:
                    body.x += scroll_speed
            elif event.key == pygame.K_RIGHT:
                for body in celestial_bodies:
                    body.x -= scroll_speed
            elif event.key == pygame.K_UP:
                for body in celestial_bodies:
                    body.y += scroll_speed
            elif event.key == pygame.K_DOWN:
                for body in celestial_bodies:
                    body.y -= scroll_speed
            elif event.key == pygame.K_s:
                dragging_star = True
                star_drag_start = pygame.mouse.get_pos()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                dragging_star = False
                current_pos = pygame.mouse.get_pos()
                star.apply_force((current_pos[0] - star_drag_start[0], current_pos[1] - star_drag_start[1]))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        for body in celestial_bodies:
            body.x += scroll_speed
    if keys[pygame.K_RIGHT]:
        for body in celestial_bodies:
            body.x -= scroll_speed
    if keys[pygame.K_UP]:
        for body in celestial_bodies:
            body.y += scroll_speed
    if keys[pygame.K_DOWN]:
        for body in celestial_bodies:
            body.y -= scroll_speed

    screen.fill(black)

    center_x = sum(body.x for body in celestial_bodies) / len(celestial_bodies) if celestial_bodies else width / 2
    center_y = sum(body.y for body in celestial_bodies) / len(celestial_bodies) if celestial_bodies else height / 2

    if center_x != width / 2 or center_y != height / 2:
        center_arrow_angle = math.atan2(height / 2 - center_y, width / 2 - center_x)
        center_arrow_x = width / 2 + center_arrow_size * math.cos(center_arrow_angle)
        center_arrow_y = height / 2 + center_arrow_size * math.sin(center_arrow_angle)

        pygame.draw.line(screen, white, (width / 2, height / 2), (center_arrow_x, center_arrow_y), 2)
        pygame.draw.polygon(screen, white, [(width / 2 - 5, height / 2 - 15),
                                            (width / 2 + 5, height / 2 - 15),
                                            (width / 2, height / 2 - 5)])

    for i in range(len(celestial_bodies)):
        for j in range(len(celestial_bodies)):
            if i != j:
                gravity_force = calculate_gravity(celestial_bodies[i].__dict__, celestial_bodies[j].__dict__)
                celestial_bodies[i].apply_force(gravity_force)

    for body in celestial_bodies:
        body.update()
        body.draw()

    for body in celestial_bodies:
        pygame.draw.line(screen, red, (body.x, body.y), (body.x + drag_force[0], body.y + drag_force[1]), 3)

    if dragging:
        current_pos = pygame.mouse.get_pos()
        drag_force = (current_pos[0] - drag_start[0], current_pos[1] - drag_start[1])

    if dragging_star:
        current_pos = pygame.mouse.get_pos()
        star_drag_force = (current_pos[0] - star_drag_start[0], current_pos[1] - star_drag_start[1])
        star.apply_force(star_drag_force)

    pygame.display.flip()
    clock.tick(60)
