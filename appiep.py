import os
from flask import Flask, render_template, request
from groq import Groq

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key='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')

# Function to get food recommendations from Groq based on mood
def get_food_recommendations(mood):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f'''Recommend food based on the following mood: 
                {mood} 
                give only response and in json and nothing elses
                the format must be strict to 
                food_recommendations : [...items]
                ''',
            }
        ],
        model="llama3-8b-8192",  # Replace with the correct model if necessary
    )
    
    # Extract food recommendations from the API response
    food_recommendations = chat_completion.choices[0].message.content

    # Convert the food recommendations to a list (if the response is in string format)
    # Assuming the response is a JSON-like string, you may need to parse it
    print(food_recommendations)
    try:
        food_json = eval(food_recommendations)  # Not the safest, but for example purposes
        return food_json.get('food_recommendations', [])
    except Exception as e:
        return ["Error parsing food recommendations"]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the mood from the form
        mood = request.form['mood']
        
        # Get food recommendations for the given mood
        food_recommendations = get_food_recommendations(mood)
        print(food_recommendations)
        
        # Render the template with the food recommendations
        return render_template('index.html', food_recommendations=food_recommendations)
    
    return render_template('index.html', food_recommendations=None)

if __name__ == '__main__':
    app.run(debug=True)
