## Description

**Verbify AI** is an innovative AI-powered speech therapy platform designed to address the challenges faced by children with speech disorders, such as those diagnosed with autism spectrum disorder (ASD) or dyspraxia. These children often struggle with articulation and pronunciation, making effective communication a significant challenge. Traditional speech therapy methods can be inaccessible, not tailored to individual needs, time-consuming, and financially burdensome. Consequently, many children who could benefit from such support are unable to access it, underscoring the need for a more innovative and accessible solution.

Verbify AI leverages advanced AI capabilities to offer personalized and accessible speech therapy solutions. By integrating Gemini's cutting-edge AI technology, Verbify AI provides tailored interventions to meet the unique needs of each child. The platform features a sound-to-sound AI model, utilizing Gemini Pro, specifically designed for speech therapy. This model transcribes sound into text via an API, allowing for precise personalization.

The AI is trained on diverse datasets, enabling it to tailor interventions based on the child's current speech level. It provides encouragement during failures and celebrates achievements, fostering an empathetic and supportive therapy experience. Verbify AI empowers children with speech disorders to enhance their communication skills, build confidence, and gain independence in their interactions.

## Features

1. **AI Speech Therapist**: Provides personalized speech therapy sessions using advanced AI technology.
2. **Sound-to-Sound Model**: Utilizes Gemini Pro to transcribe sound into text for accurate personalization.
3. **Empathetic Training Approach**: Offers encouragement and applause to support children's progress and achievements.
4. **Tailored Interventions**: Adapts therapy based on the child's current speech level.
5. **Accessible and Convenient**: Overcomes the limitations of traditional speech therapy by offering a flexible and affordable solution.

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/koleshjr/verbifyai.git
   ```
2. Add a `.env` file with the following content:
   ```plaintext
   MODEL_NAME = " "  # transcription model
   HUGGINGFACE_READ_TOKEN = " "
   ELLEVEN_LABS_API = " "
   GOOGLE_API_KEY = " "
   ```
3. Install dependencies:
   ```bash
   make build
   ```
4. Start the server:
   ```bash
   make run
   ```


## Usage (Windows)

1. Clone the repository:
   ```bash
   git clone https://github.com/koleshjr/verbifyai.git
   ```

2. Navigate to the project directory:
   ```bash
   cd verbifyai
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Add a `.env` file with the following content:
   ```plaintext
   MODEL_NAME = " "  # transcription model
   HUGGINGFACE_READ_TOKEN = " "
   ELLEVEN_LABS_API = " "
   GOOGLE_API_KEY = " "
   ```

6. Start the server:
   ```bash
   python app.py
   ```

