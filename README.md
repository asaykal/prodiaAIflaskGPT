# prodiaAIflaskGPT
This is a Flask application that uses the OpenAI GPT-3.5 Turbo model to generate image prompts based on user input. The generated prompts are then sent to the Prodia API to create high-resolution and detailed images. The application provides a user interface where users can enter a keyword and receive prompt suggestions to enhance their image generation requests.

![screencapture-127-0-0-1-5000-2023-05-26-17_09_38](https://github.com/asaykal/prodiaAIflaskGPT/assets/46647858/8c8393ac-ede8-41e2-a0e9-c3b0cc84af24)

##Prerequisites
Before running this application, make sure you have the following:
-Python 3.x installed on your system.
-Prodia API key: You need to obtain an API key from Prodia to access their image generation service. This key should be set as an environment variable X_PRODIA_KEY.
-OpenAI API key: You need an OpenAI API key to make requests to the GPT-3.5 Turbo model. Set this key as an environment variable --OPENAI_API_KEY.

##Installation
1. Clone this repository: git clone https://github.com/asaykal/prodiaAIflaskGPT
2. Change into the project directory: cd prodiaAIflaskGPT
3. Install the required Python packages using pip: pip install -r requirements.txt

##Usage
1. Set the environment variables:

X_PRODIA_KEY: Set this variable to your Prodia API key.
OPENAI_API_KEY: Set this variable to your OpenAI API key.

2. Start the Flask application: python app.py

3. Access the application in your web browser at http://localhost:5000 or http://127.0.0.1:5000/

##Features
The application provides the following features:

-Prompt Suggestions: Users can enter a keyword, and the application will generate prompt suggestions using the OpenAI GPT-3.5 Turbo model. These suggestions help users write more specific and effective prompts for generating images.

-Image Generation: Users can enter a prompt, select a model, aspect ratio, and choose whether to upscale the image. The application then sends the prompt to the Prodia API to generate images based on the user's request. It creates multiple job requests to improve the chances of successful image generation.

-Image Display: The generated images are displayed on the web interface for the user to view and download.
