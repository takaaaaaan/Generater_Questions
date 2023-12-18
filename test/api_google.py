# https://console.cloud.google.com/marketplace/product/google/vision.googleapis.com?project=gpthonyaku
# 여기에서 API받을 수 있어요

import cv2
import numpy as np
import requests
import base64
from PIL import Image

# 画像のコントラストを調整する関数
def adjust_contrast(img, contrast=1.5):
    img = img.astype(np.float32)
    img = img * contrast
    img = np.clip(img, 0, 255)
    return img.astype(np.uint8)

def process_image(file_path):
    # 画像を読み込む
    img = cv2.imread(file_path)

    # OpenCVのエフェクトを適用する
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contrast_img = adjust_contrast(gray_img)

    # 画像を保存する
    processed_image_path = 'processed_image.jpg'
    cv2.imwrite(processed_image_path, contrast_img)

    return processed_image_path

def detect_text(image_path, api_key):
    # Read image file
    with open(image_path, "rb") as img_file:
        my_string = base64.b64encode(img_file.read()).decode()

    # Prepare the request payload
    request_payload = {
        "requests": [
            {
                "image": {
                    "content": my_string
                },
                "features": [
                    {
                        "type": "TEXT_DETECTION"
                    }
                ]
            }
        ]
    }

    response = requests.post(
        url=f'https://vision.googleapis.com/v1/images:annotate?key={api_key}',
        json=request_payload)

    # Extract text from the response
    text = response.json()['responses'][0]['fullTextAnnotation']['text']

    return text

def main():
    image_path = 'your_image.jpg'  # Update this with the path of your image
    api_key = 'YOUR_API_KEY'  # Update this with your API key
    processed_image_path = process_image(image_path)
    text = detect_text(processed_image_path, api_key)
    print(text)

if __name__ == "__main__":
    main()
