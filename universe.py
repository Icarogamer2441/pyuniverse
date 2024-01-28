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
drag_force_multiplier = 0.05
mass_increase = 10
black_hole_mass = 1000

def calculate_gravity(obj1, obj2):
    distance = max(1, math.hypot(obj2['x'] - obj1['x'], obj2['y'] - obj1['y']))
    force = G * (obj1['mass'] * obj2['mass']) / (distance ** 2)
    angle = math.atan2(obj2['y'] - obj1['y'], obj2['x'] - obj1['x'])
    force_x = force * math.cos(angle)
    force_y = force * math.sin(angle)
    return force_x, force_y

class Planet:
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

class BlackHole:
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def apply_gravity(self, other_black_hole):
        gravity_force = calculate_gravity(self.__dict__, other_black_hole.__dict__)
        other_black_hole.apply_force((-gravity_force[0], -gravity_force[1]))

    def apply_force(self, force):
        acceleration_x = force[0] / self.mass
        acceleration_y = force[1] / self.mass
        self.x += acceleration_x
        self.y += acceleration_y

# Tela inicial
font = pygame.font.Font(None, 24)
text = font.render("Gravitational Attraction", True, white)
text_rect = text.get_rect(center=(width//2, height//2 - 100))

info_text1 = font.render("Left click to create a planet", True, white)
info_text1_rect = info_text1.get_rect(center=(width//2, height//2 - 50))

info_text2 = font.render("Right click on a planet to increase its mass", True, white)
info_text2_rect = info_text2.get_rect(center=(width//2, height//2))

info_text3 = font.render("Press 'B' to create a black hole at the mouse position", True, white)
info_text3_rect = info_text3.get_rect(center=(width//2, height//2 + 50))

info_text4 = font.render("Press 'D' to delete all planets and black holes", True, white)
info_text4_rect = info_text4.get_rect(center=(width//2, height//2 + 100))

info_text5 = font.render("Drag with left click to apply a force to the planets", True, white)
info_text5_rect = info_text5.get_rect(center=(width//2, height//2 + 150))

info_text6 = font.render("G: 150 (Gravitational constant)", True, white)
info_text6_rect = info_text6.get_rect(center=(width//2, height//2 + 200))

info_text7 = font.render("Press 'P' to start playing", True, white)
info_text7_rect = info_text7.get_rect(center=(width//2, height//2 + 250))

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

planets = []
black_holes = []

clock = pygame.time.Clock()
dragging = False
drag_start = (0, 0)
drag_force = (0, 0)

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
                for planet in planets:
                    distance = math.hypot(event.pos[0] - planet.x, event.pos[1] - planet.y)
                    if distance <= planet.radius:
                        planet.increase_mass(mass_increase)
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            new_planet = Planet(event.pos[0], event.pos[1], 20, white)
            planets.append(new_planet)
            new_planet.apply_force((drag_force[0] * drag_force_multiplier, drag_force[1] * drag_force_multiplier))
            drag_force = (0, 0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                # Cria um buraco negro nas coordenadas do mouse
                black_hole = BlackHole(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 30, blue, black_hole_mass)
                black_holes.append(black_hole)
            elif event.key == pygame.K_d:
                # Deleta todos os planetas e buracos negros
                planets = []
                black_holes = []

    if dragging:
        drag_end = pygame.mouse.get_pos()
        drag_force = (drag_end[0] - drag_start[0], drag_end[1] - drag_start[1])

    screen.fill(black)

    for i in range(len(planets)):
        for j in range(len(black_holes)):
            black_holes[j].apply_gravity(planets[i])

    for i in range(len(planets)):
        for j in range(i+1, len(planets)):
            gravity_force = calculate_gravity(planets[i].__dict__, planets[j].__dict__)
            planets[i].apply_force(gravity_force)
            planets[j].apply_force((-gravity_force[0], -gravity_force[1]))

            distance = math.hypot(planets[j].x - planets[i].x, planets[j].y - planets[i].y)
            if distance < planets[i].radius + planets[j].radius:
                if planets[i].mass >= planets[j].mass:
                    planets[i].mass += planets[j].mass
                    planets.pop(j)
                else:
                    planets[j].mass += planets[i].mass
                    planets.pop(i)
                break

    for black_hole in black_holes:
        black_hole.draw()
    
    for i in range(len(black_holes)):
        for j in range(i+1, len(black_holes)):
            black_holes[i].apply_gravity(black_holes[j])

            distance = math.hypot(black_holes[j].x - black_holes[i].x, black_holes[j].y - black_holes[i].y)
            if distance < black_holes[i].radius + black_holes[j].radius:
                if black_holes[i].mass >= black_holes[j].mass:
                    black_holes[i].mass += black_holes[j].mass
                    black_holes.pop(j)
                else:
                    black_holes[j].mass += black_holes[i].mass
                    black_holes.pop(i)
                break
    
    for planet in planets:
        planet.update()
        planet.draw()

    for planet in planets:
        pygame.draw.line(screen, red, (planet.x, planet.y), (planet.x + drag_force[0], planet.y + drag_force[1]), 3)

    pygame.display.flip()
    clock.tick(60)
