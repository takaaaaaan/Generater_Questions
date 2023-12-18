import streamlit as st

def render():
    st.title("Code<Generator.py>")
    line_number = st.selectbox("Display line number",["표시","가리기"])
    line_number = True if line_number == "표시" else False
    code = '''
import cv2
import streamlit as st
import numpy as np
from PIL import Image
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
import requests
import base64
import openai
from googletrans import Translator
import pymysql.cursors
import time
# from logging import getLogger,StreamHandler

# lagger = getLogger(__name__)
# handler = StreamHandler()



tr = Translator()

openai.api_key = "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"

assistant_content = None
answer = None
row_id = None


# Language code mapping
language_code_mapping = {
    "한국어": "ko",
    "English": "en",
    "日本語": "ja",
    "中文": "zh-CN",  # Simplified Chinese
    "မြန်မာဘာသာ": "my"  # Burmese (Myanmar)
}


def render():  
    # 이미지의 명암 대조 조정하기
    def adjust_contrast(img, contrast=1.5):
        img = img.astype(np.float32)
        img = img * contrast
        img = np.clip(img, 0, 255)
        return img.astype(np.uint8)
    
    def generate_questions(text, num_questions, question_type, difficulty, topic, language):
        # 질문 생성 시작
        messages = []
        global assistant_content
        
        # 使用者からの情報設定
        language_code = language_code_mapping.get(language)
        if not language_code:
            st.write(f"오류: 잘못된 언어를 선택했습니다. 다음 중에서 선택하십시오: {list(language_code_mapping.keys())}")
            return
        
        # 사용자로부터의 정보 설정
        user_message = {
            "role": "user",
            "content": tr.translate(text=f"""
            Hello ChatGPT, I would like to create exam questions from a specific text. Please help me create questions based on the information below.
            - Language: {language}
            - Text to use: {text}
            - Question format I want to create: {question_type}
            - Number of questions: {num_questions}
            - Difficulty: {difficulty}
            - Topic of the question: {topic}
            I would appreciate it if you could create the best questions based on the above information. Thank you.
            """, dest=language_code).text
        }

        messages.append(user_message)

        # OpenAI Chat model 호출
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",  # 최신 모델명으로 바꿔주세요
            messages=messages,
        )

        assistant_content = response.choices[0].message["content"].strip()


        st.write(f"📝\n{assistant_content}")

        connection = pymysql.connect(host='localhost',
                                    user='root',
                                    password='',
                                    db='Quiz',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # Create a new record with the assistant_content
                sql = "INSERT INTO `moning` (`Quiz_qust`) VALUES (%s)"
                cursor.execute(sql, (assistant_content,))

                # Get the ID of the new row
                global row_id  # Make it global so it can be used in other functions
                row_id = cursor.lastrowid

            connection.commit()
        finally:
            connection.close()
                
    
    def generate_answer(text, question, answer_type, language):
        
        global answer
        # 使用者からの情報設定
        language_code = language_code_mapping.get(language)
        if not language_code:
            st.write(f"오류: 잘못된 언어를 선택했습니다. 다음 중에서 선택하십시오: {list(language_code_mapping.keys())}")
            return

        user_message = {
            "role": "user",
            "content": tr.translate(text=f"""
            Hello ChatGPT, please tell me the answer to the question I just created.
            - Language: {language}
            - Question text: {question}
            - Reference text: {text}
            - Answer format: {answer_type}
            Based on the above information, I would appreciate it if you could create the optimal answer. Thank you.
            """, dest=language_code).text
        }

        # OpenAI Chat model 호출
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",  # 최신 모델명으로 바꿔주세요
            messages=[user_message],
        )

        answer = response.choices[0].message["content"].strip()
        st.write(f" 💡: {answer}")

        # Connect to the database and update the record
        connection = pymysql.connect(host='localhost',
                                    user='root',
                                    password='',
                                    db='Quiz',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # Update the record with the answer
                sql = "UPDATE `moning` SET `Quiz_ans` = %s WHERE `id` = %s"
                cursor.execute(sql, (answer, row_id))

            connection.commit()
        finally:
            connection.close()

        return answer


    st.title("😊문제를 업로드해주세요~!!😊")
    with st.form(key='settings',):
        st.header('📑문제 형식을 설정')
        num_questions = st.slider('문제 수를 선택해주세요', min_value=1, max_value=10, value=5, step=1)
        question_type = st.selectbox('문제 형식을 선택하세요', options=["선택지 문제", "빈칸 채우기 문제", "간단 서술형 문제"], index=0)
        language = st.selectbox('문제 언어를 선택해주세요',options=["한국어","English","日本語","中文","မြန်မာဘာသာ"])
        col1, col2, col3 = st.columns(3)
        difficulty = col1.radio('난이도를 선택하세요', ["쉬움", "보통", "어려움", "매우 어려움"])
        topic = col2.radio('문제 주제', ["전체적인 주제", "특정 부분에 초점을 맞춤"])
        answer_type = col3.radio('답변 유형', ["다지선다", "참거짓", "간단 서술형", "서술형", "수치형"])

        submit_button = st.form_submit_button('저장')

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

    # 이미지 소스 선택 옵션
    option = st.selectbox('이미지 소스를 선택하세요', ('이미지 소스 선택', '📥이미지 업로드', '📸카메라로 캡처하기'))

    img = None
    count = 0
    if option == '📥이미지 업로드':
        uploaded_file = st.file_uploader("이미지를 선택하세요...", type="jpg")
        if uploaded_file is not None:
            img = Image.open(uploaded_file)
            img = np.array(img)

    elif option == '📸카메라로 캡처하기':
        ctx = webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)

        if st.button('캡처하기'):
            st.caption('2번 눌러주세요')
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
        cv2.imwrite('./inputs/processed_image.jpg', contrast_img)

        # 이미지 파일 읽기
        with open("./inputs/processed_image.jpg", "rb") as img_file:
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


        # レスポンスからテキスト抽出
        text = response.json()['responses'][0]['fullTextAnnotation']['text']
        st.title("📖원본 문장📖")
        st.text(text)
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='root',
                                    password='',
                                    db='Quiz',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Update the same row with the extracted text
                sql = "UPDATE `moning` SET `Quiz_text` = %s WHERE `id` = %s"
                cursor.execute(sql, (text, row_id))  # `text` is your new data

            connection.commit()
        finally:
            connection.close()
        
        # Get language code from mapping
        language_code = language_code_mapping.get(language)
        translated_text = tr.translate(text=text, dest=language_code).text
        st.title("📖번역 문장📖")
        st.text(translated_text)
        
        # Connect to the database and update the record
        connection = pymysql.connect(host='localhost',
                                    user='root',
                                    password='',
                                    db='Quiz',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # Update the record with the translated_text
                sql = "UPDATE `moning` SET `Quiz_trans` = %s WHERE `id` = %s"
                cursor.execute(sql, (translated_text, row_id))

            connection.commit()
        finally:
            connection.close()
                
                
    # Google Cloud Vision에서 얻은 텍스트 사용
    if option == '📥이미지 업로드' or option == '📸카메라로 캡처하기':
        with st.form(key='question_creation'):
            # "문제 생성" 버튼
            submit_button = st.form_submit_button('✅문제 생성')
            # Usage
            if submit_button:
                generate_questions(text, num_questions, question_type, difficulty, topic,language)
                time.sleep(1)  # Wait for 1 second
                generate_answer(text, num_questions, answer_type,language)
        '''
    st.code(code,language = 'python',line_numbers=line_number)