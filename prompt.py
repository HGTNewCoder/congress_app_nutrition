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
template_nutrition_food_exercise =""" 
You are a medical nutrition expert. ONLY return clean, semantic HTML — no explanations, no meta comments, no extra paragraphs. Do NOT include <html> or <body> tags — only the HTML fragment. If there are multiple diseases, combine them into one answer, but DO NOT write or mention their names anywhere in the response. Format the output exactly as follows: 
<h3>Food</h3> 
<ul> 
<li>Specific food name 1</li> 
<li>Specific food name 2</li> 
<li>Specific food name 3</li> 
<li>Specific food name 4</li> 
<li>Specific food name 5</li> 
</ul> 
<h3>Exercise</h3> 
<ul> 
<li>Specific exercise name 1</li> 
<li>Specific exercise name 2</li> 
<li>Specific exercise name 3</li> 
<li>Specific exercise name 4</li> 
<li>Specific exercise name 5</li> 
</ul> 
Here is the patient information you must base your recommendations on: {information} 
""" 

prompt_nutrition_food_exercise = PromptTemplate( 
    input_variables=["information"], 
    template=template_nutrition_food_exercise, 
) 

nutrition_food_exercise_chain = LLMChain(llm=my_llm_model, prompt=prompt_nutrition_food_exercise) 

template_routine = """ 
You are a medical nutrition expert. Create a daily routine table in HTML based on {list_of_food_and_exercise} from 5-6 am to 10-11 pm. Please do not give me any important notes or recommendations, just ONLY the HTML table. **IMPORTANT: Do NOT include markdown delimiters like
html or
. Your response must start *directly* with the <table> tag and end *directly* with the </table> tag.** Format the table exactly like this: 
<table> 
<thead> 
<tr> 
<th>Time</th> 
<th>Activity</th> 
</tr> 
</thead> 
<tbody> 
<tr> 
<td>5:00 AM - 6:00 AM</td> 
<td>...Activity...</td> 
</tr> 
<tr> 
<td>6:00 AM - 7:00 AM</td> 
<td>...Activity...</td> 
</tr> 
</tbody> 
</table> 
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
