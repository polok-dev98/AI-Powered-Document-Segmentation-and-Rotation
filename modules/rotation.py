import cv2
import numpy as np

def correct_angle_vertical(image, verbose=False):
    """Correct the orientation of an image."""
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    coords = np.column_stack(np.where(thresh > 0))
    rect = cv2.minAreaRect(coords)
    theta = rect[-1]

    if theta < -45:
        angle = -(theta + 90)
    elif theta > 45:
        angle = -(theta - 90)
    else:
        angle = -theta

    h, w = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    rotated = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_CUBIC, borderValue=(255, 255, 255))

    gray_rotated = cv2.cvtColor(rotated, cv2.COLOR_RGB2GRAY)
    _, mask = cv2.threshold(gray_rotated, 240, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    all_points = np.vstack([pt for contour in contours for pt in contour])
    hull = cv2.convexHull(all_points)
    x, y, w, h = cv2.boundingRect(hull)

    cropped = rotated[y + 3 : y + h - 3, x + 3 : x + w - 3]
    return cropped
