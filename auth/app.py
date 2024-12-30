import json
import random
from flask import Flask, flash, jsonify, request, render_template, redirect, session, url_for
from flask_login import logout_user
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)
app.secret_key = 'my_key' 

@app.route('/')
def index():
    return 'hi'

@app.route('/home')
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/schemes")
def schemes():
    return render_template("schemes.html")

@app.route("/mental-health")
def mental_health():
    return render_template("mental_health.html")

@app.route('/financial-literacy')
def financial_literacy():
    return render_template('financial_literacy.html')

@app.route('/login')
def login():
    return render_template('login.html')


# def get_logged_in_user():
#     user_login = False
#     user_info = session.get('user_name')
#     if(user_info is not None):
#         user_logged_in = user_info
#     else:
#         user_logged_in = None
#     if(user_logged_in is not None):
#         user_login = True

#     return user_login




# @app.route('/logout')
# def logout():
#     logout_user()
#     session.clear()
#     user_login = get_logged_in_user()
#     return render_template('loginPage.html' , user_login=user_login)

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('login'))
# @app.route('/Homepage')
# def Homepage():
#     return render_template('home.html')

# @app.route('/aboutPage')
# def aboutPage():
#     return render_template('about.html')

def post_api_function(url, data):
    response = ''
    try:
        response = requests.post(url, json=data)
        print(response)
    except Exception as e:
        print('An exception', e,'Occured')
    return response

def get_api_function(url):
    response = ''
    try:
        response = requests.get(url)
        print(response)
    except Exception as e:
        print('An exception', e,'Occured')
    return response

def get_service_url():
    return 'http://localhost:20000'

@app.route('/user_signup', methods=['POST'])
def user_signup():
    url = get_service_url() + '/user_signup'
    request_data = request.json   
    print(f"Received data: {request_data}")
    response = post_api_function(url, request_data)
    return json.dumps(response.json())

@app.route('/attempt_to_login', methods=['POST'])
def attempt_to_login():
    url = get_service_url() + '/attempt_to_login_for_user'
    request_data = request.json
    print(request_data)
    response = post_api_function(url, request_data)
    # result = response.json()
    # if(result['status'] == 'Login Failed'):
    #     session['user_name'] = None
    # else:
    #     session['user_name'] = request_data['user_name']
    #     session['user_type'] = request_data['user_login_type']
    #     user = User(request_data['user_name'])
    #     login_user(user)
    return response.json()


# @app.route('/get-quote')
# def get_quote():
#     try:
#         response = requests.get("https://api.quotable.io/random")  
#         data = response.json()  # Convert response to JSON format
#         return jsonify({"quote": data['content'], "author": data['author']})
#     except Exception as e:
#         print(f"Error fetching quote: {e}")
#         return jsonify({"quote": "An error occurred while fetching the quote.", "author": "Unknown"})

# List of quotes
quotes = [
    {"quote": "The most courageous act is still to think for yourself. Aloud.", "author": "Coco Chanel"},
    {"quote": "I am not free while any woman is unfree, even when her shackles are very different from my own.", "author": "Audre Lorde"},
    {"quote": "You don't make progress by standing on the sidelines, whimpering and complaining. You make progress by implementing ideas.", "author": "Sheryl Sandberg"},
    {"quote": "Well-behaved women seldom make history.", "author": "Laurel Thatcher Ulrich"},
    {"quote": "A woman is like a tea bag – you never know how strong she is until you put her in hot water.", "author": "Eleanor Roosevelt"},
    {"quote": "There is no limit to what we, as women, can accomplish.", "author": "Michelle Obama"},
    {"quote": "I am not afraid. I was born to do this.", "author": "Joan of Arc"},
    {"quote": "The question isn’t who is going to let me; it’s who is going to stop me.", "author": "Ayn Rand"},
    {"quote": "You don’t make progress by standing on the sidelines, whimpering and complaining. You make progress by implementing ideas.", "author": "Sheryl Sandberg"},
    {"quote": "Feminism is for everybody.", "author": "bell hooks"},
    {"quote": "I am my best work – I am my best work today – and I’m the one who’s going to make it happen.", "author": "Oprah Winfrey"},
    {"quote": "I raise up my voice – not so I can shout, but so that those without a voice can be heard.", "author": "Malala Yousafzai"},
    {"quote": "A girl should be two things: who and what she wants.", "author": "Coco Chanel"},
    {"quote": "The most effective way to do it, is to do it.", "author": "Amelia Earhart"},
    {"quote": "No one can make you feel inferior without your consent.", "author": "Eleanor Roosevelt"},
]


@app.route('/get-quote')
def get_quote():
    try:
        random_quote = random.choice(quotes)  # Get a random quote
        return jsonify({"quote": random_quote['quote'], "author": random_quote['author']})
    except Exception as e:
        print(f"Error fetching quote: {e}")
        return jsonify({"quote": "An error occurred while fetching the quote.", "author": "Unknown"})



# Example route to fetch articles
@app.route('/articles', methods=['GET'])
def fetch_articles():
    query = request.args.get('query', 'mental health women India')  # Default search query
    api_url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": "2515d7423baa4da4bd9f7956508cf0e5",  # Replace with your API key
        "language": "en",
        "sortBy": "publishedAt"
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        articles = [
            {
                "title": article["title"],
                "description": article["description"],
                "url": article["url"],
                "publishedAt": article["publishedAt"],
                "source": article["source"]["name"]
            }
            for article in data.get("articles", [])
        ]
        return jsonify({"articles": articles})
    else:
        return jsonify({"error": "Failed to fetch articles"}), 500




def scrape_schemes():
    url = "https://www.myscheme.gov.in/search/state/Gujarat"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch the website.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    schemes = []
    # Locate broader elements
    for item in soup.find_all('div'):  # Replace 'div' with a more specific tag if possible
        name = item.find('h3')  # Look for headings inside the div
        category = item.find('p', text=lambda x: 'Category:' in x if x else False)
        eligibility = item.find('p', text=lambda x: 'Eligibility:' in x if x else False)

        if name:  # Ensure no null values
            schemes.append({
                "name": name.text.strip(),
                "category": category.text.strip() if category else "N/A",
                "eligibility": eligibility.text.strip() if eligibility else "N/A"
            })

    # Save the data to a JSON file
    with open('schemes.json', 'w') as file:
        json.dump(schemes, file, indent=4)

if __name__ == "__main__":
    scrape_schemes()
    print("Data saved to schemes.json!")


import requests
from bs4 import BeautifulSoup

# Step 1: Fetch the website content
url = "https://www.myscheme.gov.in/search/state/Gujarat"
response = requests.get(url)

if response.status_code != 200:
    print("Failed to fetch the website.")
else:
    # Step 2: Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Step 3: Debug the HTML content
    print(soup.prettify())  # This prints the entire HTML content in a readable format



if __name__ == '__main__':
    app.run(debug=True)

