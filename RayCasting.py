import pygame
import math
import random

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
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

# treat the maze as a 10x10 grid and each block takes up 1x1 area
player_pos = pygame.Vector2(5.5, 5.5)
player_speed = pygame.Vector2(0, 0)
player_vertical_speed = 0
player_vertical_height = 0
# trail[0] is always the current tile, trail[1] is the one before and etc
trail = []
# length of trail including the space the player is on
trail_length = 1
current_tile = pygame.Vector2(5,5)
trail.append(pygame.Vector2(5,5))
stuck = False
# adds a starting fuit space
valid_fruit_space = False
while not valid_fruit_space:
    randx = random.randint(1,8)
    randy = random.randint(1,8)
    # for all the places in the trail including player space
    for i in trail:
        # if it is a valid space
        if(int(i.x) != randx and int(i.y) != randy):
            valid_fruit_space = True
            maze[randy][randx] = 2

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
    if keys[pygame.K_c] and player_vertical_height == 0:
        player_vertical_speed = 3
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
    # if youre where a fruit is
    if maze[math.floor(player_pos.y)][math.floor(player_pos.x)] == 2:
        maze[math.floor(player_pos.y)][math.floor(player_pos.x)] = 0
        trail_length = trail_length + 1
        valid_fruit_space = False
        while not valid_fruit_space:
            randx = random.randint(1,8)
            randy = random.randint(1,8)
            # for all the places in the trail including player space
            for i in trail:
                # if it is a valid space
                if(int(i.x) != randx and int(i.y) != randy):
                    valid_fruit_space = True
                    maze[randy][randx] = 2
        


    
    # Trail calculations
    current_tile.x = math.floor(player_pos.x)
    current_tile.y = math.floor(player_pos.y)
    # If we have changed tiles
    if(current_tile.x != trail[0].x or current_tile.y != trail[0].y):
        trail.insert(0, pygame.Vector2(current_tile.x, current_tile.y))
        # If trail is longer than it should be
        if(len(trail) > trail_length):
            maze[int(trail[len(trail)-1].y)][int(trail[len(trail)-1].x)] = 0
            del trail[len(trail)-1]
    # Add walls in all the trail
    for i in range(1,len(trail)):
        maze[int(trail[i].y)][int(trail[i].x)] = 1
    
    if(maze[int(current_tile.y+1)][int(current_tile.x)] == 1 and maze[int(current_tile.y-1)][int(current_tile.x)] == 1 and maze[int(current_tile.y)][int(current_tile.x+1)] == 1 and maze[int(current_tile.y)][int(current_tile.x-1)] == 1):
        stuck = True


    
    # Adding the speed to the height and decreasing the speed
    player_vertical_height += player_vertical_speed
    player_vertical_speed =  player_vertical_speed - 0.2
    if player_vertical_height < 0:
        player_vertical_speed = 0
        player_vertical_height = 0

    for i in range(-45, 45):
        distance = 0
        current_angle = angle + math.radians(i)
        ray_vector = pygame.Vector2(0, 0)
        check_vector = player_pos + ray_vector
        intersected = False
        fruit = False
        while not intersected:
            # if its a wall
            if maze[math.floor(check_vector.y)][math.floor(check_vector.x)] == 1:
                distance = ray_vector.magnitude()
                intersected = True
            # if its a fruit
            elif maze[math.floor(check_vector.y)][math.floor(check_vector.x)] == 2:
                distance = ray_vector.magnitude()
                intersected = True
                fruit = True
            else:
                ray_vector.x += 0.05 * math.sin(current_angle)
                ray_vector.y += -0.05 * (math.cos(current_angle))
                check_vector = player_pos + ray_vector

        length_of_line = screen.get_height()*2 / ((distance+1) * (distance+1))
        line_start = pygame.Vector2(screen.get_width()*0.5 + (i * 10), 0.5 * (screen.get_height() - length_of_line) + player_vertical_height / distance * 7)
        line_end = pygame.Vector2(screen.get_width()*0.5 + (i * 10), screen.get_height() - (0.5 * (screen.get_height() - length_of_line)) + player_vertical_height / distance * 7)
        value = 255 - distance * 30
        if value < 20:
            value = 20

        if fruit:
            pygame.draw.line(screen, pygame.Color((value, 0, 0)), line_start, line_end, width=10)
        else:
            pygame.draw.line(screen, pygame.Color((value, value, value)), line_start, line_end, width=10)

    pygame.display.set_caption("angle: " + str(angle) + "position x: " + str(player_pos.x) + "position y: " + str(player_pos.y))
    # flip() the display to put your work on screen
    for i in range(10):
        for j in range(10):
            if maze[i][j] == 1:
                pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect(j * 20, i * 20, 20, 20))
            if maze[i][j] == 2:
                pygame.draw.rect(screen, pygame.Color("red"), pygame.Rect(j * 20, i * 20, 20, 20))
    pygame.draw.circle(screen, pygame.Color("red"), player_pos*20, 5)

    if stuck:
        font = pygame.font.SysFont("Arial", 36)
        txtsurf = font.render("You're stuck lmao haha press x to leave", True, pygame.Color("blue"))
        screen.blit(txtsurf,(screen.get_width()/2-200,screen.get_height()/2-120))

    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
