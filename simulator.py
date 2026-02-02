import pygame
import sys
import math

# Initialization
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robotic Arm Simulator v0.2")
clock = pygame.time.Clock()

# Colors
BG = (20, 20, 30)
BASE_COLOR = (200, 50, 50)
LINK1_COLOR = (100, 150, 255)
LINK2_COLOR = (100, 255, 150)
TEXT_COLOR = (220, 220, 220)

# Arm parameters
base_pos = (WIDTH // 2, HEIGHT - 50)
link1_len = 150
link2_len = 120
angle1 = 45   # Shoulder joint angle
angle2 = 30   # Elbow joint angle
angle_speed = 2  # Angle change speed per frame

# Font for UI text
font = pygame.font.SysFont("Arial", 24)

# Main loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keyboard control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angle1 -= angle_speed
    if keys[pygame.K_RIGHT]:
        angle1 += angle_speed
    if keys[pygame.K_DOWN]:
        angle2 += angle_speed
    if keys[pygame.K_UP]:
        angle2 -= angle_speed

    # Angle limits to prevent unnatural poses
    angle1 = max(-180, min(180, angle1))
    angle2 = max(-180, min(180, angle2))

    # Clear screen
    screen.fill(BG)

    # Calculate joint positions using forward kinematics
    rad1 = math.radians(angle1)
    joint1_x = base_pos[0] + link1_len * math.sin(rad1)
    joint1_y = base_pos[1] - link1_len * math.cos(rad1)

    rad2 = math.radians(angle1 + angle2)
    end_x = joint1_x + link2_len * math.sin(rad2)
    end_y = joint1_y - link2_len * math.cos(rad2)

    # Draw arm
    pygame.draw.circle(screen, BASE_COLOR, base_pos, 15)  # Base
    pygame.draw.line(screen, LINK1_COLOR, base_pos, (joint1_x, joint1_y), 8)  # Link 1
    pygame.draw.line(screen, LINK2_COLOR, (joint1_x, joint1_y), (end_x, end_y), 8)  # Link 2
    pygame.draw.circle(screen, (255, 220, 0), (end_x, end_y), 10)  # End effector

    # Display current angles
    text1 = font.render(f"Shoulder angle: {angle1:.1f}°", True, TEXT_COLOR)
    text2 = font.render(f"Elbow angle: {angle2:.1f}°", True, TEXT_COLOR)
    screen.blit(text1, (20, 20))
    screen.blit(text2, (20, 50))

    # Control hint
    hint = font.render("Controls: ← → ↑ ↓", True, (150, 150, 150))
    screen.blit(hint, (WIDTH - hint.get_width() - 20, 20))

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()