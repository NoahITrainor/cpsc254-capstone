What the website does:
The app allows a user to enter the name of a movie and discover 5 similar movies. The app is using OpenAI to search the movie database and generate comparisions on why the selected films are similar to the user's film.

Setup Instructions:

Windows:

1. git clone https://github.com/NoahITrainor/cpsc254-capstone.git
2. cd cpsc254-capstone
3. python -m venv venv
4. Command Prompt: venv\Scripts\activate.bat
5. pip install -r requirements.txt
6. make a copy of .env.example and rename it to .env  
        copy .env.example .env
7. Enter your OpenAI Key into .env
8. streamlit run app/main.py
9. python eval/run_eval.py

Linux & Mac
1. git clone https://github.com/NoahITrainor/cpsc254-capstone.git
2. cd cpsc254-capstone
3. python3 -m venv venv
4. source venv/bin/activate
5. pip install -r requirements.txt
6. cp .env.example .env (Open the new .env file and replace 'your_api_key_here' with your OpenAI API key)
7. streamlit run app/main.py
8. python3 eval/run_eval.py