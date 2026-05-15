import streamlit as st
import sys
import os
import json

# --- DEBUGGING START ---
# This forces the app to look in the current folder for engine.py
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# This forces the app to look in the root folder for the data/ folder
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)
# --- DEBUGGING END ---

try:
    from engine import recommend
except Exception as e:
    st.error(f"Error loading the AI engine: {e}")
    st.stop()

st.set_page_config(page_title="Cross-Cultural Recs", page_icon="🎬")

st.title("🎬 Cross-Cultural Movie Recommender")
st.caption("Find foreign films with the same 'soul' as your favorites.")

# --- THE "PRESS ENTER" FIX ---
with st.form(key='search_form'):
    user_movie = st.text_input("Enter a movie you love:")
    submit_button = st.form_submit_button(label='Search')

# Run this block only if the button is clicked OR Enter is pressed
# Run this block only if the button is clicked OR Enter is pressed
if submit_button and user_movie:
    with st.spinner("Analyzing themes and searching 21,000+ films..."):
        try:
            # This calls your backend logic to get the matches
            results = recommend(user_movie) 
            
            # --- THE "MOVIE NOT FOUND" FIX ---
            # If 'results' comes back empty (e.g., None or []), trigger the warning
            if not results: 
                st.warning(f"Hmm, we couldn't find '{user_movie}'. Please check your spelling or try another film!")
            
            # If results DO exist, show them normally
            else:
                st.markdown("### Recommended Films:")
                
                for r in results:
                    st.subheader(r['title'])
                    
                    try:
                        country_dict = json.loads(r['country'].replace("'", '"')) 
                        clean_country = ", ".join(country_dict.values())
                    except:
                        clean_country = r['country']
                        
                    st.caption(f"📍 Region: {clean_country}")
                    st.write(r["explanation"])
                    st.divider()
                    
        except Exception as e:
            st.error(f"AI Search Error: {e}")