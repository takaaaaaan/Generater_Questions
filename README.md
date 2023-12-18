
# Generater_Questions

This `Generater_Questions` is designed to facilitate the creation, processing, and management of exam questions. The application consists of three main components, each rendered as a separate page within the Streamlit interface.

## Features

- **Page 1: Question Creation**
  - Users can select the number of questions, question type, language, difficulty level, and topic.
  - It supports capturing images via upload or camera, processes them using OpenCV for text extraction, and generates questions using OpenAI's ChatGPT model.

- **Page 2: Demo Page**
  - This page serves as a demonstration area for various functionalities.

- **Page 3: Code Page**
  - Displays code snippets with options to show or hide line numbers.
  - Includes Python code for database operations and Streamlit widgets.

## Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/takaaaaaan/Generater_Questions
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit App**
   ```bash
   streamlit run Generator.py
   ```

## Usage

Navigate through the sidebar to access different pages:

- **📝문제 만들기**: For generating exam questions.
- **📄📱🎨Demo Page**: To explore the demo features.
- **Code Page**: To view and interact with the code.

## Technologies Used

- Streamlit
- OpenCV for image processing
- OpenAI GPT-3 for generating questions and answers
- Google Translate for language translation
- MySQL for database operations
- Google Cloud Vision API for text detection

## Contributing

Contributions to enhance the application are welcome. Please follow the standard procedures for contributing to a GitHub repository.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

MIT
