import cv2
import numpy as np
#for all this detecting players

jersey_rgb = (215, 14, 55) #indiana fever red jersey
free_thow_rgb = (245,35,65,255)
def convert_rgb_to_hsv(rgb_color): #making sure the colors are readable
    """
    Converts an RGB color to HSV. hsv is hue,saturation,value(brightness)
    
    Args:
        rgb_color (tuple): RGB values (R, G, B) in the range 0-255.

    Returns:
        tuple: HSV values (H, S, V) in the range 0-255.
    """
    rgb_color = np.uint8([[rgb_color]])  # Create a dummy image
    hsv_color = cv2.cvtColor(rgb_color, cv2.COLOR_RGB2HSV)
    return hsv_color[0][0]

jersey_hsv = convert_rgb_to_hsv(jersey_rgb)
#print("Jersey HSV:", jersey_hsv)

free_throw_hsv = convert_rgb_to_hsv(free_thow_rgb)
#print("Free throw/court colors:", free_throw_hsv)

def get_hsv_range(base_hsv, tolerance=(10, 50, 50)): #accounts for changes in lighting
    """
    Generates an HSV range for color detection.
    
    Args:
        base_hsv (tuple): Base HSV values (H, S, V).
        tolerance (tuple): Tolerance for each channel (H, S, V).

    Returns:
        tuple: Lower and upper bounds for HSV.
    """
    lower_bound = np.clip(np.array(base_hsv) - np.array(tolerance), 0, 255)
    upper_bound = np.clip(np.array(base_hsv) + np.array(tolerance), 0, 255)
    return lower_bound.astype(int), upper_bound.astype(int)

lower_hsv, upper_hsv = get_hsv_range(jersey_hsv)
lower_free_throw, upper_free_throw = get_hsv_range(free_throw_hsv)

#function to locate players based on jersey colors
def player_detection(frame, lower_hsv, upper_hsv, lower_free_throw, upper_free_throw):
    # Convert frame to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for the jersey color
    player_mask = cv2.inRange(hsv_frame, lower_hsv, upper_hsv)
    
    # Create a mask for the free throw line
    free_throw_mask = cv2.inRange(hsv_frame, lower_free_throw, upper_free_throw)

    # Exclude the free throw line area by masking out the regions from the player mask
    final_mask = cv2.bitwise_and(player_mask, cv2.bitwise_not(free_throw_mask))

    # Find contours in the final mask
    contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return contours



# #function to draw bows. inputs video screenshot. output is a box on the screen
def draw_boxes(frame, contours):
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Filter out small contours (optional)
            # Get the bounding box for each contour
            x, y, w, h = cv2.boundingRect(contour)
            
            # Draw a rectangle around the player
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green box with thickness 2
            
    return frame
