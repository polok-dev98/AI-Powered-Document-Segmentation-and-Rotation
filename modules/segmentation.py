import cv2
import numpy as np
from ultralytics import YOLO
from pathlib import Path

model = YOLO(r'model.pt')

def roiSegmentation_with_class(image_path):
    # Perform prediction
    res = model.predict(source=image_path)
    processed_img = None
    cropped_img_with_background = None
    mask_coords = None  # Initialize mask_coords to avoid UnboundLocalError

    if not res:
        print(f"No predictions found for {image_path}.")
        return mask_coords, processed_img, cropped_img_with_background

    for r in res:
        if len(r) == 0:
            print(f"No detections found for image {r.path}.")
            continue

        img = r.orig_img  # Original image
        img_name = Path(r.path).stem

        try:
            max_conf_pred_img = sorted(r, key=lambda x: float(x.boxes.conf.max()), reverse=True)[0]
        except IndexError:
            print(f"No predictions with valid confidence scores found for {img_name}.")
            continue

        if max_conf_pred_img.masks is not None and max_conf_pred_img.masks.xy is not None:
            # Extract contour points from xy
            contour = max_conf_pred_img.masks.xy[0].astype(np.int32).reshape(-1, 1, 2)
            
            # Draw bounding box and calculate the points
            x_coords = contour[:, 0, 0]
            y_coords = contour[:, 0, 1]
            min_x, max_x = np.min(x_coords), np.max(x_coords)
            min_y, max_y = np.min(y_coords), np.max(y_coords)

            points = {
                "top_left": (min_x, min_y),
                "bottom_left": (min_x, max_y),
                "bottom_right": (max_x, max_y),
                "top_right": (max_x, min_y),
            }

            # Calculate intermediate midpoints
            mid_points = {
                "mid_left": ((min_x + min_x) // 2, (min_y + max_y) // 2),
                "mid_right": ((max_x + max_x) // 2, (min_y + max_y) // 2),
                "mid_top": ((min_x + max_x) // 2, (min_y + min_y) // 2),
                "mid_bottom": ((min_x + max_x) // 2, (max_y + max_y) // 2),
            }

            # Combine all points
            base_points = {**points, **mid_points}
            base_order = [
                "top_left", "mid_left", "bottom_left", "mid_bottom",
                "bottom_right", "mid_right", "top_right", "mid_top"
            ]

            all_points_sequence = [base_points[key] for key in base_order]


            img_height, img_width = img.shape[:2]
            thickness = max(2, img_width // 200)
            radius = max(5, img_width // 100)

            # Calculate nearest mask coordinates
            mask_coords = []
            for pt in all_points_sequence:
                distances = np.sqrt((contour[:, 0, 0] - pt[0]) ** 2 + (contour[:, 0, 1] - pt[1]) ** 2)
                nearest_idx = np.argmin(distances)
                mask_coords.append(tuple(contour[nearest_idx][0]))

            # Convert numpy.int32 to native Python int
            mask_coords = [(int(x), int(y)) for x, y in mask_coords]

            # Create the masked image with a white background
            mask = np.zeros_like(img)
            cv2.fillPoly(mask, [contour], (255, 255, 255))  # White mask
            white_background = np.ones_like(img) * 255
            masked_img = cv2.bitwise_and(img, mask)
            masked_img = cv2.addWeighted(masked_img, 1, white_background, 1, 0)

            # Crop the region of interest and apply the mask
            cropped_img = img[min_y:max_y, min_x:max_x]
            cropped_mask = mask[min_y:max_y, min_x:max_x]
            cropped_img_with_background = np.where(cropped_mask > 0, cropped_img, 255)

            # Draw circles and lines for visualization
            for coord in mask_coords:
                cv2.circle(img, coord, radius=radius, color=(0, 0, 255), thickness=thickness)  # Solid red circles
            for i in range(len(mask_coords)):
                cv2.line(img, mask_coords[i], mask_coords[(i + 1) % len(mask_coords)], (0, 255, 0), thickness)

            processed_img = img
            break  # Process only the first detection
        else:
            print(f"No contour masks found for {img_name}")

    return mask_coords, processed_img, cropped_img_with_background
