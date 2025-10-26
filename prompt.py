from langchain.prompts import PromptTemplate 
from langchain.chains import LLMChain, SimpleSequentialChain 
from langchain_google_vertexai import VertexAI 
from flask import request 
import os 
from dotenv import load_dotenv 

load_dotenv()

# Initialize LLM model 
my_llm_model = VertexAI( 
    model=os.getenv("MODEL"), 
    project=os.getenv("PROJECT"), 
    location=os.getenv("LOCATION") 
) 

# Template for nutrition and exrcise 
# template_nutrition_food_exercise =""" 
# You are a medical nutrition expert. ONLY return clean, semantic HTML — no explanations, no meta comments, no extra paragraphs. Do NOT include <html> or <body> tags — only the HTML fragment. If there are multiple diseases, combine them into one answer, but DO NOT write or mention their names anywhere in the response. Format the output exactly as follows: 
# <h3>Food</h3> 
# <ul> 
# <li>Specific food name 1</li> 
# <li>Specific food name 2</li> 
# <li>Specific food name 3</li> 
# <li>Specific food name 4</li> 
# <li>Specific food name 5</li>    
# </ul> 
# <h3>Exercise</h3> 
# <ul> 
# <li>Specific exercise name 1</li> 
# <li>Specific exercise name 2</li> 
# <li>Specific exercise name 3</li> 
# <li>Specific exercise name 4</li> 
# <li>Specific exercise name 5</li> 
# </ul> 
# Here is the patient information you must base your recommendations on: {information} 
# """ 

# template_nutrition_food_exercise = """
# You are a certified medical nutrition expert. 
# Create a concise, well-structured HTML fragment (not a full page) with Food and Exercise recommendations based on: {information}.

# Guidelines:
# - Output must start with <section> and end with </section>.
# - No <html>, <head>, <body>, styles, or comments.
# - Use minimal, semantic HTML with clear class names.
# - Include two parts: 🥗 Food and 💪 Exercise.
# - Give specific, practical items (e.g., “Grilled salmon”, “Brisk walking 30 min”), not general categories.
# - Use natural ordering: light morning items first, heavier or restorative ones later.

# Format:
# <section class="recommendation-section">
#   <div class="recommendation-card">
#     <h3 class="category-title">🥗 Food</h3>
#     <ul class="recommendation-list">
#       <li>Food 1</li>
#       <li>Food 2</li>
#       <li>Food 3</li>
#       <li>Food 4</li>
#       <li>Food 5</li>
#     </ul>
#   </div>
#   <div class="recommendation-card">
#     <h3 class="category-title">💪 Exercise</h3>
#     <ul class="recommendation-list">
#       <li>Exercise 1</li>
#       <li>Exercise 2</li>
#       <li>Exercise 3</li>
#       <li>Exercise 4</li>
#       <li>Exercise 5</li>
#     </ul>
#   </div>
# </section>

# Now fill the same structure with realistic, specific recommendations derived from {information}.
# """

template_nutrition_food_exercise = """
You are a certified medical nutrition expert. 
Generate a concise HTML fragment (not a full page) with Food and Exercise recommendations based on: {information}.

Rules:
- Output must start with <section> and end with </section>.
- Use <span class="material-symbols-outlined">...</span> for each icon instead of <img>.
- Icons you can use:
  - restaurant, nutrition, local_drink, favorite, self_improvement, fitness_center, bedtime
- Do NOT include <html>, <head>, <body>, styles, or comments.

Example:
<section class="recommendation-section">
  <div class="recommendation-card">
    <h3 class="category-title">🥗 Food</h3>
    <ul class="recommendation-list">
      <li><span class="material-symbols-outlined">restaurant</span> Grilled salmon with vegetables</li>
      <li><span class="material-symbols-outlined">local_drink</span> Stay hydrated throughout the day</li>
    </ul>
  </div>
  <div class="recommendation-card">
    <h3 class="category-title">💪 Exercise</h3>
    <ul class="recommendation-list">
      <li><span class="material-symbols-outlined">favorite</span> Brisk walking 30 min</li>
      <li><span class="material-symbols-outlined">self_improvement</span> Morning yoga or stretching</li>
      <li><span class="material-symbols-outlined">bedtime</span> Adequate rest and recovery</li>
    </ul>
  </div>
</section>
"""


prompt_nutrition_food_exercise = PromptTemplate( 
    input_variables=["information"], 
    template=template_nutrition_food_exercise, 
) 

nutrition_food_exercise_chain = LLMChain(llm=my_llm_model, prompt=prompt_nutrition_food_exercise) 

# template_routine = """
# You are a medical nutrition and fitness expert. 
# Generate a visually aesthetic HTML fragment (not a full HTML page) that shows a daily routine table from 5–6 AM to 10–11 PM 
# based on {list_of_food_and_exercise}.

# **Rules:**
# 1. Output must start directly with <table> and end directly with </table>. No <html>, <head>, <body>, or <style> tags.
# 2. The table must contain two columns: "Time" and "Activity".
# 3. Use clean semantic HTML — no inline CSS, no comments, no extra text.
# 4. Keep the structure simple and responsive-ready (use <thead> and <tbody>).
# 5. Do not include notes, recommendations, or explanations.

# Format the HTML fragment exactly like this:

# <table class="routine-table">
#   <caption>🌞 Daily Routine</caption>
#   <thead>
#     <tr>
#       <th>Time</th>
#       <th>Activity</th>
#     </tr>
#   </thead>
#   <tbody>
#     <tr>
#       <td>5:00 AM - 6:00 AM</td>
#       <td>Morning jog and stretching</td>
#     </tr>
#     <tr>
#       <td>6:00 AM - 7:00 AM</td>
#       <td>Breakfast: oatmeal and fruits</td>
#     </tr>
#   </tbody>
# </table>

# Now generate your own table following this exact format using {list_of_food_and_exercise}.
# """

template_routine = """
You are a medical nutrition and fitness expert. 
Generate a clean HTML fragment (not a full page) showing a daily routine table from 5–6 AM to 10–11 PM based on: {list_of_food_and_exercise}.

Rules:
- Start directly with <table>, end directly with </table>.
- Two columns: "Time" and "Activity".
- Include <caption> at top.
- Use semantic HTML with these classes:
  - <table class="routine-table">
  - <thead>, <tbody>, and optional <tr class="highlight-row"> for key activities.
- No inline CSS, comments, or extra paragraphs.
- Keep consistent casing (e.g., capitalize activity titles).

Format:
<table class="routine-table">
  <caption>🌞 Daily Routine</caption>
  <thead>
    <tr><th>Time</th><th>Activity</th></tr>
  </thead>
  <tbody>
    <tr><td>5:00 AM - 6:00 AM</td><td>Morning jog and stretching</td></tr>
    <tr class="highlight-row"><td>12:00 PM - 1:00 PM</td><td>Lunch and rest</td></tr>
  </tbody>
</table>

Now generate your table using the same format based on {list_of_food_and_exercise}.
"""



prompt_routine = PromptTemplate( 
    input_variables=["list_of_food_and_exercise"], 
    template=template_routine, 
) 

routine_chain = LLMChain(llm=my_llm_model, prompt=prompt_routine) 

# Combine both chains 
chain = SimpleSequentialChain(chains=[nutrition_food_exercise_chain, routine_chain]) 

# Template of the important thing 
template_nutrition_important =""" 
You are a medical nutrition expert. The characteristic of person : {information} List exactly **10** essential things to notice for the disease(s). In each list item, highlight the single most important key phrase using <strong> tags. ONLY return a clean HTML unordered list (<ul>). Do not include <html> or <body> tags. No explanations, just the list. **IMPORTANT: Do NOT include markdown delimiters like
or
. Your response must start *directly* with the <ul> tag and end *directly* with the </ul> tag.** Format exactly as follows: 
<ul> 
<li>This is the <strong>first key point</strong>.</li> 
<li>This is the <strong>second key point</strong>.</li> 
<li>What things you must <strong>always carry with you</strong>.</li> 
<li>What you should do to <strong>protect yourself</strong>.</li> 
<li>Any other key ways to <strong>support that person</strong>.</li> 
<li>This is the <strong>sixth key point</strong>.</li> 
<li>This is the <strong>seventh key point</strong>.</li> 
<li>This is the <strong>eighth key point</strong>.</li> 
<li>This is the <strong>ninth key point</strong>.</li> 
<li>This is the <strong>tenth key point</strong>.</li> 
</ul> 
""" 

prompt_nuitrion_important= PromptTemplate( 
    input_variables=["information"], 
    template=template_nutrition_important, 
) 

important_chain= LLMChain(llm=my_llm_model, prompt=prompt_nuitrion_important) 

def generate_routine(): 
    """ 
    Input: diseases: list of disease names (strings) weight: user's weight in kg (float) Output: str: LLM-generated routine text 
    """ 
    # Build input string 
    name = request.form.get("name") 
    age = request.form.get("age") 
    weight = float(request.form.get("weight")) 
    height = request.form.get('height') 
    sex = request.form.get('sex') 
    race = request.form.get('race') 
    selected_diseases = request.form.getlist("disease") 
    question_str = f"Diseases: {', '.join(selected_diseases)}; Weight: {weight}kg ; Age:{age} ; Height: {height}cm ; Sex: {sex} ; Race: {race}" 
    answer = chain.run(question_str) 
    return answer 

def generate_food_exercise(): 
    # build input string 
    name = request.form.get("name") 
    age = request.form.get("age") 
    weight = float(request.form.get("weight")) 
    height = request.form.get('height') 
    sex = request.form.get('sex') 
    race = request.form.get('race') 
    selected_diseases = request.form.getlist("disease") 
    question_str = f"Diseases: {', '.join(selected_diseases)}; Weight: {weight}kg ; Age:{age} ; Height: {height}cm ; Sex: {sex} ; Race: {race}" 
    answer = nutrition_food_exercise_chain.run(question_str) 
    return answer 

def generate_important(): 
    # build input string 
    name = request.form.get("name") 
    age = request.form.get("age") 
    weight = float(request.form.get("weight")) 
    height = request.form.get('height') 
    sex = request.form.get('sex') 
    race = request.form.get('race') 
    selected_diseases = request.form.getlist("disease") 
    question_str = f"Diseases: {', '.join(selected_diseases)}; Weight: {weight}kg ; Age:{age} ; Height: {height}cm ; Sex: {sex} ; Race: {race}" 
    answer = important_chain.run(question_str) 
    return answer 
