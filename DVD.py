import os
import random
import tkinter as tk
from tkinter import filedialog

import pygame
import win32con
import win32gui

# Initialize pygame
pygame.init()

# Get screen dimensions
screen_info = pygame.display.Info()
window_width = screen_info.current_w
window_height = screen_info.current_h

# Set up the display
window = pygame.display.set_mode((window_width, window_height), pygame.NOFRAME)
pygame.display.set_caption("DVD")

# Set window style to layered (allows transparency)
hwnd: int = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

# Set the window background color to transparent
win32gui.SetLayeredWindowAttributes(hwnd, 0, 0, win32con.LWA_COLORKEY)


# Load the image with a transparent background

def load_image_path():
    if os.path.exists("image_path.txt"):
        with open("image_path.txt", "r") as file:
            return file.readline().strip()
    return None
def choose_image():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select an Image File", filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
    return file_path

def save_image_path(image_file_path):
    with open("image_path.txt", "w") as file:
        file.write(image_file_path)


saved_image_path = load_image_path()
if saved_image_path:
    image_file_path = saved_image_path
else:
    image_file_path = choose_image()
    if image_file_path:
        save_image_path(image_file_path)

        print("No image selected. Exiting...")
        pygame.quit()
        exit()

# Load the image with a transparent background
image = pygame.image.load(image_file_path)
image_rect = image.get_rect()

# Load the image with a transparent background
image_file_path = choose_image()
if image_file_path:
    image = pygame.image.load(image_file_path)
else:
    print("No image selected. Exiting...")
    pygame.quit()
    exit()


def r_image(image, width, height):
    return pygame.transform.scale(image, (width, height))


def update_position(x, y, velocity_x, velocity_y):
    x += velocity_x
    y += velocity_y
    return x, y


def check_collisions(x, y, image_rect, velocity_x, velocity_y, window_width, window_height):
    if x < 0 or x + image_rect.width > window_width:
        velocity_x *= -1
    if y < 0 or y + image_rect.height > window_height:
        velocity_y *= -1
    return velocity_x, velocity_y


# Resize the image
image_width = 200  # Adjust the desired width
image_height = 350  # Adjust the desired height
image = r_image(image, image_width, image_height)
image_rect = image.get_rect()


# Initial position and velocity
x = random.randint(0, window_width - image_rect.width)
y = random.randint(0, window_height - image_rect.height)
initial_speed = 0.5
velocity_x = initial_speed
velocity_y = initial_speed

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    x, y = update_position(x, y, velocity_x, velocity_y)
    velocity_x, velocity_y = check_collisions(x, y, image_rect, velocity_x, velocity_y, window_width, window_height)

    # Fill the window with a transparent color
    window.fill((0, 0, 0))  # Transparent background

    # Draw the image at the new position
    window.blit(image, (x, y))

    # Update the display
    pygame.display.update()


# Quit pygame
pygame.quit()
