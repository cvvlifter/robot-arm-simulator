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
TARGET_COLOR = (255, 100, 100)      # Red target point
TARGET_COLOR_REACHABLE = (100, 255, 100)  # Green when reachable
MODE_COLOR_MANUAL = (150, 150, 255)
MODE_COLOR_AUTO = (100, 255, 150)

# Arm parameters
base_pos = (WIDTH // 2, HEIGHT - 50)
link1_len = 150
link2_len = 120
angle1 = 45   # Shoulder joint angle
angle2 = 30   # Elbow joint angle
angle_speed = 2  # Angle change speed per frame

# Control mode: "manual" (keyboard) or "auto" (mouse target)
control_mode = "manual"

# Target point (mouse position)
target_pos = (base_pos[0] + 100, base_pos[1] - 150)
is_dragging = False

# Font for UI text
font = pygame.font.SysFont("Arial", 24)


def inverse_kinematics(x, y, l1, l2):
    """
    Calculate joint angles for 2-link arm to reach (x, y).
    Our coordinate system:
      - 0° points UP (vertical)
      - Positive angles rotate clockwise (to the right)
    Returns (angle1_deg, angle2_deg) or (None, None) if unreachable.
    """
    # Vector from base to target (convert screen Y to math Y)
    dx = x - base_pos[0]
    dy = base_pos[1] - y  # Invert Y: screen down → math up

    dist = math.hypot(dx, dy)

    # Check reachability
    if dist > l1 + l2 or dist < abs(l1 - l2):
        return None, None

    # Angle from vertical (up) to target point
    phi = math.atan2(dx, dy)  # atan2(x, y) because vertical is Y-axis

    # Law of cosines: angle between l1 and line to target
    cos_beta = (l1 * l1 + dist * dist - l2 * l2) / (2 * l1 * dist)
    cos_beta = max(-1.0, min(1.0, cos_beta))  # Clamp for float safety
    beta = math.acos(cos_beta)

    # Law of cosines: internal angle at elbow
    cos_gamma = (l1 * l1 + l2 * l2 - dist * dist) / (2 * l1 * l2)
    cos_gamma = max(-1.0, min(1.0, cos_gamma))
    gamma = math.acos(cos_gamma)

    # Shoulder angle (from vertical)
    angle1_rad = phi - beta

    # Elbow angle (relative bend between links)
    # For natural "elbow down" configuration:
    angle2_rad = math.pi - gamma

    return math.degrees(angle1_rad), math.degrees(angle2_rad)

# Main loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mx, my = pygame.mouse.get_pos()
                # Check if clicked near target
                if math.hypot(mx - target_pos[0], my - target_pos[1]) < 15:
                    is_dragging = True
                else:
                    # Start dragging from current mouse position
                    is_dragging = True
                    target_pos = (mx, my)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                is_dragging = False

        if event.type == pygame.MOUSEMOTION:
            if is_dragging:
                target_pos = pygame.mouse.get_pos()

        # Toggle control mode
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                control_mode = "auto" if control_mode == "manual" else "manual"

    # Keyboard control (only in manual mode)
    if control_mode == "manual":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            angle1 -= angle_speed
        if keys[pygame.K_RIGHT]:
            angle1 += angle_speed
        if keys[pygame.K_DOWN]:
            angle2 += angle_speed
        if keys[pygame.K_UP]:
            angle2 -= angle_speed

        # Angle limits
        angle1 = max(-180, min(180, angle1))
        angle2 = max(-180, min(180, angle2))

    # Auto mode: calculate angles to reach target
    if control_mode == "auto":
        a1, a2 = inverse_kinematics(target_pos[0], target_pos[1], link1_len, link2_len)
        if a1 is not None and a2 is not None:
            angle1, angle2 = a1, a2
            target_color = TARGET_COLOR_REACHABLE
        else:
            target_color = TARGET_COLOR  # Red = unreachable

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

    # Draw target point
    if control_mode == "auto":
        pygame.draw.circle(screen, target_color, target_pos, 12, 2)
        pygame.draw.circle(screen, target_color, target_pos, 5)

    # Display current angles
    text1 = font.render(f"Shoulder: {angle1:.1f}°", True, TEXT_COLOR)
    text2 = font.render(f"Elbow: {angle2:.1f}°", True, TEXT_COLOR)
    screen.blit(text1, (20, 20))
    screen.blit(text2, (20, 50))

    # Display control mode
    mode_text = "AUTO (mouse)" if control_mode == "auto" else "MANUAL (arrows)"
    mode_color = MODE_COLOR_AUTO if control_mode == "auto" else MODE_COLOR_MANUAL
    mode_surface = font.render(f"Mode: {mode_text}", True, mode_color)
    screen.blit(mode_surface, (WIDTH - mode_surface.get_width() - 20, 20))

    # Control hint
    hint = font.render("SPACE: toggle mode | Drag target with mouse", True, (150, 150, 150))
    screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 40))

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()