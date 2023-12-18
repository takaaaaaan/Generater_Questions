import cv2
import streamlit as st
import numpy as np
from PIL import Image
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
import requests
import base64
import openai


# 이미지의 명암 대조 조정하기
def adjust_contrast(img, contrast=1.5):
    img = img.astype(np.float32)
    img = img * contrast
    img = np.clip(img, 0, 255)
    return img.astype(np.uint8)


def generate_questions(text, num_questions):
    # 이제 OpenAI로 질문 생성을 시작합니다。
    openai.api_key = "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"

    for i in range(num_questions):
        messages = []

        # 텍스트의 i번째 줄을 사용자 입력으로 설정
        user_content = text.split('\n')[i]

        messages.append({"role": "user", "content": f"{user_content}"})

        prompt = f"사용자의 텍스트 '{user_content}'를 기반으로 질문을 생성하세요."
        messages.append({"role": "system", "content": prompt})

        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k", messages=messages)

        assistant_content = completion.choices[0].message["content"].strip()

        messages.append({"role": "assistant", "content": f"{assistant_content}"})

        st.title(f"⚔문제 {i+1}⚔")

        st.write(f"{assistant_content}")


class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.capture_enabled = False
        self.saved_image = None

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")

        # 플래그가 활성화되었을 때 이미지 캡처하기
        if self.capture_enabled:
            self.saved_image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            self.capture_enabled = False

        return img


st.title('😊문제를 업로드해주세요~!!😊')

# 이미지 소스 선택 옵션
option = st.selectbox('이미지 소스를 선택하세요', ('이미지 소스 선택', '이미지 업로드', '카메라로 캡처하기'))

img = None

if option == '이미지 업로드':
    uploaded_file = st.file_uploader("이미지를 선택하세요...", type="jpg")
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        img = np.array(img)

elif option == '카메라로 캡처하기':
    ctx = webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)

    if st.button('캡처하기'):
        ctx.video_transformer.capture_enabled = True
        st.write('이미지가 캡처되었습니다.')

    if ctx.video_transformer and ctx.video_transformer.saved_image is not None:
        img = ctx.video_transformer.saved_image

# 이미지가 있는 경우 OpenCV 효과 적용
if img is not None:
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contrast_img = adjust_contrast(gray_img)

    # 이미지 출력
    st.image(contrast_img, caption='처리 후 이미지', use_column_width=True)

    # 이미지 저장
    cv2.imwrite('processed_image.jpg', contrast_img)

    # 이미지 파일 읽기
    with open("processed_image.jpg", "rb") as img_file:
        my_string = base64.b64encode(img_file.read()).decode()

    # 요청 페이로드 준비
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
        url='https://vision.googleapis.com/v1/images:annotate?key=AIzaSyDAMkNqy8UIL4xN40FbTVE5zYC0ucq8Mtw',
        json=request_payload)

    # 응답에서 텍스트 추출
    text = response.json()['responses'][0]['fullTextAnnotation']['text']
    st.title("📖원본 문장📖")
    st.write(text)

    # Google Cloud Vision에서 얻은 텍스트 사용
if option == '이미지 업로드' or option == '카메라로 캡처하기':
    with st.form(key='question_creation'):
        # "문제 생성" ボタン
        submit_button = st.form_submit_button('문제 생성')
        # Usage
        if submit_button:
            # Google Cloud Vision에서 얻은 텍스트 사용
            if text is not None:
                user_content = text
            else:
                user_content = "기본 텍스트"  # 또는 원하는 내용으로 대체

            # 문제 생성을 원하는 횟수를 설정합니다。
            num_questions = len(text.split('\n')) # 텍스트의 줄 수에 따라 문제의 수를 결정

            generate_questions(user_content, num_questions)