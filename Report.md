What and why:
    what does it do:
The website that I used AI to create has the user input the name of a film and then retrieves similar films from countries outside the U.S. from a movie database of 21000 movies. The website then uses LLM to break down the essence of the recommended films and how they are similar to the film the user input.
    Who is it for:
The website's audience is targeted towards individuals who love film and want to explore what film other countries have to offer. The website also serves as a means for people to learn about other cultures outside the U.S.
    What was hard about getting the AI behavior right:
In the initial stages of development, the movie database was much smaller than 21000 movies, which resulted in cases where the AI would hallucinate, generating films that didn't share themes. There was also an issue when upgrading to the database, where I reached the limit on OpenAI token limit, which forced me to implement a time.sleep() to circumvent the limit.

Iterations:
    V1:
Change: I initially developed the end-to-end pipeline using a custom dataset that only included 5 foreign films.
Motivating Example: When I enter a film, the system's AI would force hallucinations to make connections between films that had no relevance to each other due to the limited number of films available for comparison.
Delta: The initial V1 proved that the goal was feasible but was lacking a larger dataset of foreign films. 
Conclusion: V1 successfully proved that the LLM could interact with a dataset of movies. V1 also highlighted the issue of requiring a large dataset of films so that OpenAI wouldn't force hallucinations between films of no relevance. 
    V2:
Change: I changed the 5-movie test set to a database that included around 21000 foreign films. OpenAI had an error 429 due to reaching the token limit; to fix this, I implemented time.sleep into my code to limit the number of films being sent to the API. time.sleep allows OpenAI token counter to reset.
Motivating Example: When searching for Forrest Gump, the V2 system was able to retrieve relevant foreign films such as Snug Horn (Thailand) and Der müde Tod (Germany) and draw relevance between the films, such as sharing specific traits or narrative techniques.
Delta: The delta between V1 and V2 is V2's movie database was significantly increased by over 21000, which removed the need for forced hallucinations between films. 
Conclusion: V2 shows that film retrieval from the database is working and demonstrating that OpenAI can generate relevant connections between films. 
    V3:
Change: I made it so that instead of hallucinating when entering a movie that doesn't exist, the website now lets the user know to check their spelling or to try another film. Also, pressing 'enter' now works as a method of searching.
Motivating Example: If the user enters something like "Coffee Constellation", V2 would hallucinate connections. In V3, the LLM identifies fake films and sends a message to check spelling or to try another film.
Delta: The delta between V2 and V3 is that V2 would output anything regardless of what it was. V3 offers validation and error handling, preventing hallucinations for films that don't exist.
Conclusion: V3 now uses the LLM to minimize hallucinations by implementing a validation check to determine if the film is real or not through the OpenAI model. Pressing 'enter' now works for searching.

Code Walkthrough:
    User Action:
The user types and enters "Forrest Gump" into the search bar.

app/main.py (lines 30-32) - st.form manages the search bar. When the user types "Forrest Gump" and presses/clicks enter, the user input is then assigned to user_movie. 

app/main.py (line 40) - result = recommend(user_movie) is then executed, which passes Forrest Gump to engine.py.

app/engine.py (line 51) - The code executes query = extract(movie_title). The movie title is then sent to the OpenAI API via extract. 

app/engine.py (lines 16-25) - The AI validates the movie by setting the temperature=0.0 and a strict system prompt, ensuring the film is real.

app/engine.py (lines 54-55) - Because Forrest Gump is a real film, if "FAKE" in query.upper(): is bypassed and enters the retrieval step.

app/engine.py (Lines 57/27-31) - candidates = retrieve(query) is executed and takes the extracted themes to (lines 27-31) text-embedding-3-small where they are vectorized. index.search then compares against the movie dataset (data/films.index) to find the 5 similar films from a foreign country.

app/engine.py (lines 58/33-47) - synthesize is called and sends the 5 most similar films to OpenAI to generate a brief comparison to Forrest Gump. 

app/main.py (lines 50-58) - Since Forrest Gump is a real movie, the warning is bypassed. json.loads is then used to convert metadata into a readable format and displayed on the user's screen through st.subheader and st.caption.


AI Disclosure & Safety:
AI Tools Used:
OpenAI: Acts as the brain, generating text and finding most similar films. Also checks authenticity of movies
Gemini: Used as a prompt engineer assistant, write small portions of code, break down assignment instructions, and create fake movie names.
Kiro: Used to write the majority of the code. 

For this project, I used Gemini and Kiro. First, I would create my prompt. I would then feed my prompt into Gemini and have Gemini tailor my prompt so it was more refined. This refined prompt would then be entered into Kiro to generate code that was then implemented. 

Failures: 
Initially, when I would enter the name of a fake movie, OpenAI would hallucinate returning films and similar themes from those movies and comparing them to a movie that doesn't exist.

Initially, the AI would generate json.loads() to read the dataset. The website would then crash due to the poorly formatted dataset. To fix this, I had to use (.replace("'", '"')) to avoid crashes. 

Safety Risks:
Prompt Injection and Hallucination: Because the user's input is sent to OpenAI prompt in engine.py, a malicious user could bypass the system instructions by asking it to ignore instructions. In order to prevent this, I instructed the to only accept the names of movies and return an error message if it was not the name of a movie, mitigating the chances of prompt inject and hallucination.