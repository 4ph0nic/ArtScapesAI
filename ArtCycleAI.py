#############################################
#                                           #
#          ArtCycleAI by 4ph0nic            #
#                                           #
#############################################
import requests
import pygame
from io import BytesIO
import datetime
import time
import random
import os
import openai

# Set up screen
pygame.init()
screen_width, screen_height = 800, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("AI Images")

# Set up OpenAI API key and endpoint URL
openai.api_key = os.getenv("API-KEY-HERE")  # Retrieve API key from environment variable
image_generation_url = "https://api.openai.com/v1/images/generations"

# Generate AI images using OpenAI API
def generate_image(style="random"):
    # Show loading screen
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)
    text = font.render("Generating image...", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    # Set up request payload as a JSON object
    art_styles = {
        "realism_landscapes": "a realism oil painting of a landscape",
        "impressionism_landscapes": "an impressionist painting of a landscape"
    }

    payload = {
        "model": "image-alpha-001",
        "prompt": art_styles.get(style, "a random image"),
        "num_images": 1,
        "size": "512x512",  # Update this line to a supported size
        "response_format": "url"
    }

    # Set up HTTP headers for request
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + "" # place your api key here
    }

    retries = 3
    while retries > 0:
        # Send HTTP POST request to OpenAI API endpoint
        response = requests.post(image_generation_url, headers=headers, json=payload)

        # Check response status code
        if response.status_code == 200:
            # Get URL for generated image from response JSON object
            response_json = response.json()
            image_url = response_json["data"][0]["url"]

            # Download image data and display on screen
            image_data = requests.get(image_url).content
            original_image = pygame.image.load(BytesIO(image_data))
            scaled_image = pygame.transform.scale(original_image, (screen_width, screen_height))  # Scale the image
            screen.blit(scaled_image, (0, 0))
            pygame.display.flip()

            # Save image to disk
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            image_path = os.path.join("images", f"ai_image_{timestamp}.png")
            pygame.image.save(scaled_image, image_path)  # Save the scaled_image
            return  # Exit the function after successfully generating the image
        else:
            print(f"Error: Response status code: {response.status_code}")
            print(f"Error details: {response.text}")
            retries -= 1

    print("Error: Failed to generate AI image")

# Create images directory if it doesn't exist
if not os.path.exists("images"):
    os.makedirs("images")

# Set up initial image
generate_image(style="realism_landscapes")

# Main event loop
art_style_cycle = ["realism_landscapes", "impressionism_landscapes"]
current_style_index = 0
next_image_time = datetime.datetime.now() + datetime.timedelta(minutes=30)  # Change this to 30 minutes
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if datetime.datetime.now() >= next_image_time:
        generate_image(style=art_style_cycle[current_style_index])
        current_style_index = (current_style_index + 1) % len(art_style_cycle)
        next_image_time = datetime.datetime.now() + datetime.timedelta(minutes=30)
    
    time.sleep(1)

# Clean up and exit
pygame.quit()
