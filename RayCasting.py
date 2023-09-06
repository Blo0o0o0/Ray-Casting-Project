import pygame
import math

# Example file showing a circle moving on screen
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# start with facing up
angle = 0

maze = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

# treat the maze as a 10x10 grid and each block takes up 1x1 area
player_pos = pygame.Vector2(5.5, 5.5)
player_speed = pygame.Vector2(0, 0)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    player_speed.x = 0
    player_speed.y = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_speed.x += 0.05 * math.sin(angle)
        player_speed.y -= 0.05 * math.cos(angle)
    if keys[pygame.K_s]:
        player_speed.x -= 0.05 * math.sin(angle)
        player_speed.y += 0.05 * math.cos(angle)
    if keys[pygame.K_a]:
        player_speed.x += 0.05 * math.sin(angle + math.pi * 1.5)
        player_speed.y -= 0.05 * math.cos(angle + math.pi * 1.5)
    if keys[pygame.K_d]:
        player_speed.x += 0.05 * math.sin(angle + math.pi * 0.5)
        player_speed.y -= 0.05 * math.cos(angle + math.pi * 0.5)
    if keys[pygame.K_x]:
        pygame.quit()

    # gets mouse movement
    angle += math.pi / 45 * (pygame.mouse.get_rel()[0]/50)
    angle = angle % (2 * math.pi)
    pygame.mouse.set_pos(500, 500)
    pygame.mouse.set_visible(False)

    # if moving in the y direction won't cause you to be in a wall
    if maze[math.floor(player_pos.y + player_speed.y)][math.floor(player_pos.x)] != 1:
        # move in that direction
        player_pos.y += player_speed.y
    # if moving in the x direction won't cause you to be in a wall
    if maze[math.floor(player_pos.y)][math.floor(player_pos.x + player_speed.x)] != 1:
        # move in that direction
        player_pos.x += player_speed.x

    for i in range(-45, 45):
        distance = 0
        current_angle = angle + math.radians(i)
        ray_vector = pygame.Vector2(0, 0)
        check_vector = player_pos + ray_vector
        intersected = False
        while not intersected:
            if maze[math.floor(check_vector.y)][math.floor(check_vector.x)] == 1:
                distance = ray_vector.magnitude()
                intersected = True
            else:
                ray_vector.x += 0.05 * math.sin(current_angle)
                ray_vector.y += -0.05 * (math.cos(current_angle))
                check_vector = player_pos + ray_vector

        length_of_line = screen.get_height()*2 / ((distance+1) * (distance+1))
        line_start = pygame.Vector2(screen.get_width()*0.5 + (i * 10), 0.5 * (screen.get_height() - length_of_line))
        line_end = pygame.Vector2(screen.get_width()*0.5 + (i * 10), screen.get_height() - (0.5 * (screen.get_height() - length_of_line)))
        value = 255 - distance * 30
        if value < 20:
            value = 20

        pygame.draw.line(screen, pygame.Color((value, value, value)), line_start, line_end, width=10)

    pygame.display.set_caption("angle: " + str(angle) + "position x: " + str(player_pos.x) + "position y: " + str(player_pos.y))
    # flip() the display to put your work on screen
    for i in range(10):
        for j in range(10):
            if maze[i][j] == 1:
                pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect(j * 20, i * 20, 20, 20))
    pygame.draw.circle(screen, pygame.Color("red"), player_pos*20, 5)
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
