import cv2
import numpy as np

# Load the JPEG image using OpenCV
image_path = 'reference_data/banksy_barcode_robot.jpg'
original_image = cv2.imread(image_path)

# Check if the image was loaded successfully
if original_image is None:
    print("Error: Could not read the image.")
    exit()

def make():
    for i in range(10):
        # Add jitter or noise to the image
        # You can adjust the scale to control the amount of noise
        scale = 20
        noise = np.random.normal(0, scale, original_image.shape).astype(np.uint8)
        noisy_image = cv2.add(original_image, noise)
        # Display the original and noisy images
        # cv2.imshow("Original Image", original_image)
        # cv2.imshow("Noisy Image", noisy_image)
        # Wait for a key press and then close the windows
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # Write
        cv2.imwrite(f'sample_submission/banksy_barcode_robot_{i+1}.jpg', noisy_image)


make()