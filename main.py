# Chrome Dinosaur Game with NEAT AI
# Inspired by car_sim NEAT implementation

import pygame
import os
import random
import sys
import neat

pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))
BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

# Global variables
game_speed = 20
current_generation = 0


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

        self.alive = True
        self.distance = 0
        self.time = 0

    def update(self, action):
        """
        Update dinosaur based on AI action
        action: 0 = run, 1 = jump, 2 = duck
        """
        if self.step_index >= 10:
            self.step_index = 0

        # AI controlled actions - ONLY when not already in a jump
        if action == 1 and not self.dino_jump:  # Jump
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif action == 2 and not self.dino_jump:  # Duck
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif action == 0 and not self.dino_jump:  # Run (ONLY if not jumping!)
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

        # Handle jumping physics
        if self.dino_jump:
            # Move dinosaur based on velocity
            self.dino_rect.y -= self.jump_vel * 4
            # Apply gravity (decrease velocity)
            self.jump_vel -= 0.8

        # Update image and animation (BEFORE state changes from landing)
        if self.dino_jump:
            self.image = self.jump_img
        elif self.dino_duck:
            self.image = self.duck_img[self.step_index // 5]
            self.step_index += 1
        elif self.dino_run:
            self.image = self.run_img[self.step_index // 5]
            self.step_index += 1

        # Update rect size for collision detection
        self.dino_rect.width = self.image.get_width()
        self.dino_rect.height = self.image.get_height()

        # Always lock X position
        self.dino_rect.x = self.X_POS

        # Handle Y position and ground collision AFTER visuals are set
        if self.dino_jump:
            # Ground collision detection - prevent going below ground
            if self.dino_rect.y >= self.Y_POS:
                # Landed - snap to ground and reset jump state
                self.dino_rect.y = self.Y_POS
                self.dino_jump = False
                self.dino_run = True
                self.jump_vel = self.JUMP_VEL
            # else: Y position already set by physics above
        else:
            # Not jumping - enforce ground position
            if self.dino_duck:
                self.dino_rect.y = self.Y_POS_DUCK
            else:
                self.dino_rect.y = self.Y_POS

        # Increase distance and time
        self.distance += game_speed
        self.time += 1

    def duck(self):
        # Deprecated - keeping for compatibility but unused
        pass

    def run(self):
        # Deprecated - keeping for compatibility but unused
        pass

    def jump(self):
        # Deprecated - keeping for compatibility but unused
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def get_data(self, obstacles):
        """
        Get input data for neural network
        Returns: [dino_y, dino_ducking, obstacle_x, obstacle_y, obstacle_width, game_speed, next_obstacle_x]
        """
        if len(obstacles) > 0:
            obstacle = obstacles[0]
            obstacle_x = obstacle.rect.x
            obstacle_y = obstacle.rect.y
            obstacle_width = obstacle.rect.width

            # Check for second obstacle
            next_obstacle_x = 0
            if len(obstacles) > 1:
                next_obstacle_x = obstacles[1].rect.x
        else:
            obstacle_x = SCREEN_WIDTH
            obstacle_y = 0
            obstacle_width = 0
            next_obstacle_x = 0

        return [
            self.dino_rect.y,
            1 if self.dino_duck else 0,
            obstacle_x,
            obstacle_y,
            obstacle_width,
            game_speed,
            next_obstacle_x
        ]

    def check_collision(self, obstacles):
        """Check if dinosaur collided with any obstacle"""
        for obstacle in obstacles:
            if self.dino_rect.colliderect(obstacle.rect):
                self.alive = False
                return True
        return False

    def is_alive(self):
        return self.alive

    def get_reward(self):
        """Calculate fitness reward"""
        return self.distance / 50.0


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)

    def off_screen(self):
        return self.rect.x < -self.rect.width


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, screen):
        if self.index >= 9:
            self.index = 0
        screen.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def remove_off_screen_obstacles(obstacles):
    """Remove obstacles that are off screen"""
    return [obstacle for obstacle in obstacles if not obstacle.off_screen()]


def spawn_obstacle(obstacles):
    """Spawn new obstacles"""
    if len(obstacles) == 0:
        obstacle_type = random.randint(0, 2)
        if obstacle_type == 0:
            obstacles.append(SmallCactus(SMALL_CACTUS))
        elif obstacle_type == 1:
            obstacles.append(LargeCactus(LARGE_CACTUS))
        else:
            obstacles.append(Bird(BIRD))
    return obstacles


def run_simulation(genomes, config):
    """
    Main NEAT simulation function
    """
    global current_generation, game_speed

    # Empty collections for nets and dinosaurs
    nets = []
    dinosaurs = []

    # Initialize PyGame and the display
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # For all genomes create a new neural network
    for _, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
        dinosaurs.append(Dinosaur())

    # Initialize game variables
    clock = pygame.time.Clock()
    cloud = Cloud()
    obstacles = []
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0

    # Fonts
    generation_font = pygame.font.Font('freesansbold.ttf', 20)
    alive_font = pygame.font.Font('freesansbold.ttf', 20)
    score_font = pygame.font.Font('freesansbold.ttf', 20)

    current_generation += 1

    # Counter to limit time
    counter = 0
    max_counter = 30 * 60  # About 60 seconds at 30 FPS

    while True:
        # Exit on quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill screen
        screen.fill((255, 255, 255))

        # Update background
        image_width = BG.get_width()
        screen.blit(BG, (x_pos_bg, y_pos_bg))
        screen.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

        # Update points and game speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        # Spawn and update obstacles
        obstacles = spawn_obstacle(obstacles)
        for obstacle in obstacles:
            obstacle.update()
            obstacle.draw(screen)
        obstacles = remove_off_screen_obstacles(obstacles)

        # Update cloud
        cloud.update()
        cloud.draw(screen)

        # Process each dinosaur
        still_alive = 0
        for i, dinosaur in enumerate(dinosaurs):
            if dinosaur.is_alive():
                still_alive += 1

                # Get neural network output
                output = nets[i].activate(dinosaur.get_data(obstacles))
                choice = output.index(max(output))

                # Update dinosaur with AI action
                dinosaur.update(choice)
                dinosaur.draw(screen)

                # Check collision
                dinosaur.check_collision(obstacles)

                # Update fitness
                genomes[i][1].fitness += dinosaur.get_reward()

        # If all dinosaurs are dead, end generation
        if still_alive == 0:
            break

        counter += 1
        if counter >= max_counter:
            break

        # Display generation info
        generation_text = generation_font.render(
            f"Generation: {current_generation}", True, (0, 0, 0))
        screen.blit(generation_text, (50, 30))

        alive_text = alive_font.render(
            f"Alive: {still_alive}", True, (0, 0, 0))
        screen.blit(alive_text, (50, 60))

        score_text = score_font.render(
            f"Score: {points}", True, (0, 0, 0))
        screen.blit(score_text, (50, 90))

        pygame.display.update()
        clock.tick(30)  # 30 FPS

    # Generation completed successfully
    return


def run_neat(config_path):
    """
    Setup and run NEAT algorithm
    """
    # Load NEAT configuration
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    # Create population and add reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Run simulation for a maximum of 1000 generations
    winner = population.run(run_simulation, 1000)

    # Show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    # Path to NEAT configuration file
    config_path = "./config.txt"
    run_neat(config_path)
