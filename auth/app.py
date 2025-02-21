import json
import random
from flask import Flask, flash, jsonify, request, render_template, redirect, session, url_for
from flask_cors import CORS
from flask_login import logout_user,login_user,LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
# app.secret_key = 'my_key' 

CORS(app)  # Enable cross-origin requests
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  #Cookie Same site attribute
app.config['SESSION_COOKIE_SECURE'] = True
app.secret_key = 'This_is_very_secret'
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        

@login_manager.user_loader
def load_user(user_id ):
    return User(user_id)

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

@app.route('/chat')
def chatbox():
    return render_template('chat.html')

@app.route('/result')
def show_result():
    query = request.args.get('query') 
    response = get_advice()  # Call the API endpoint
    return render_template('result.html', query=query, response=response)




    # Load the JSON data from the file
# with open('auth/schemes.json', 'r') as file:
#     schemes_data = json.load(file)
#     print("Loaded schemes data:", schemes_data) 

def load_schemes():
    with open("auth/schemes.json", "r") as file:
        schemes_data = json.load(file)
    print("Loaded schemes data:", schemes_data)  # Moved print statement inside function
    return schemes_data

@app.route("/api/schemes", methods=["GET", "POST"])
def api_schemes():
    schemes = load_schemes()
    query = request.form.get("query", "").lower()

    # Filter schemes based on search query
    if query:
        schemes = [scheme for scheme in schemes if query in scheme["name"].lower() or query in scheme["description"].lower()]

    return render_template("schemes.html", schemes=schemes, query=query)

def get_logged_in_user():
    user_login = False
    user_info = session.get('user_name')
    if(user_info is not None):
        user_logged_in = user_info
    else:
        user_logged_in = None
    if(user_logged_in is not None):
        user_login = True

    return user_login


@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    user_login = get_logged_in_user()
    return render_template('home.html' , user_login=user_login)



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




# def scrape_schemes():
#     url = "https://www.myscheme.gov.in/search/state/Gujarat"
#     response = requests.get(url)

#     if response.status_code != 200:
#         print("Failed to fetch the website.")
#         return

#     soup = BeautifulSoup(response.text, 'html.parser')

#     schemes = []
#     # Locate broader elements
#     for item in soup.find_all('div'):  # Replace 'div' with a more specific tag if possible
#         name = item.find('h3')  # Look for headings inside the div
#         category = item.find('p', text=lambda x: 'Category:' in x if x else False)
#         eligibility = item.find('p', text=lambda x: 'Eligibility:' in x if x else False)

#         if name:  # Ensure no null values
#             schemes.append({
#                 "name": name.text.strip(),
#                 "category": category.text.strip() if category else "N/A",
#                 "eligibility": eligibility.text.strip() if eligibility else "N/A"
#             })

#     # Save the data to a JSON file
#     with open('schemes.json', 'w') as file:
#         json.dump(schemes, file, indent=4)

# if __name__ == "__main__":
#     scrape_schemes()
#     print("Data saved to schemes.json!")


# import requests
# from bs4 import BeautifulSoup

# # Step 1: Fetch the website content
# url = "https://www.myscheme.gov.in/search/state/Gujarat"
# response = requests.get(url)

# if response.status_code != 200:
#     print("Failed to fetch the website.")
# else:
#     # Step 2: Parse the HTML
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Step 3: Debug the HTML content
#     print(soup.prettify())  # This prints the entire HTML content in a readable format

NEWS_API_KEY = '2515d7423baa4da4bd9f7956508cf0e5'  # Replace with your NewsAPI key # Replace with your NewsAPI key
NEWS_API_URL = 'https://newsapi.org/v2/everything'

@app.route('/news/women', methods=['GET'])
def get_indian_news():
    try:
        params = {
            'q': 'women',
            'language': 'en',
            'sortBy': 'publishedAt',
            'apiKey': NEWS_API_KEY,
            'domains': 'ndtv.com,indiatoday.in,hindustantimes.com,indianexpress.com'  # Specific Indian news sources
        }
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()
        news_data = response.json()
        return jsonify(news_data['articles'])
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500




legal_advice = {
    "domestic_violence": {
        "rights": [
            "Right to live in a safe environment free from violence.",
            "Right to protection under the Domestic Violence Act, 2005.",
            "Right to seek police assistance and legal remedies.",
        ],
        "advice": [
            "Keep a record of incidents of violence.",
            "Seek immediate medical attention if injured.",
            "Contact a women's helpline or a lawyer specializing in domestic violence.",
            "Consider filing a police complaint.",
        ]
    },
    "sexual_harassment": {
        "rights": [
            "Right to a workplace free from sexual harassment.",
            "Right to file a complaint under the Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013.",
            "Right to seek legal remedies.",
        ],
        "advice": [
            "Report the incident to your HR department or a designated internal complaints committee.",
            "Gather evidence such as emails, messages, or witness testimonies.",
            "Consult with a lawyer specializing in sexual harassment.",
        ]
    },
    "property_rights": {
        "rights": [
            "Right to inherit property equally with male heirs.",
            "Right to own and manage property independently.",
        ],
        "advice": [
            "Consult with a legal professional to understand your property rights.",
            "Ensure your name is included in property documents.",
            "Be aware of your rights under the Hindu Succession Act and other relevant laws.",
        ]
    },
    "divorce": {
        "rights": [
            "Right to file for divorce under various grounds.",
            "Right to alimony and child custody.",
        ],
        "advice": [
            "Consult with a family lawyer to understand your options.",
            "Gather necessary documentation such as marriage certificate and financial records.",
            "Explore mediation and counseling options before proceeding with legal action.",
        ]
    }
}

@app.route('/chat', methods=['POST'])
def get_advice():
    """
    Endpoint to get legal advice based on the user's query.

    Args:
        query: The user's query describing their legal issue.

    Returns:
        JSON response containing relevant rights and advice.
    """
    data = request.get_json()
    query = data.get('query')

    # Simple keyword matching (replace with more sophisticated NLP techniques)
    best_match = None
    for issue, info in legal_advice.items():
        if issue in query.lower():
            best_match = issue
            break

    if best_match:
        return jsonify({
            "issue": best_match,
            "rights": legal_advice[best_match]["rights"],
            "advice": legal_advice[best_match]["advice"]
        })
    else:
        return jsonify({
            "message": "Sorry, I couldn't find relevant information for your query."
        }), 404



@app.route('/api/data', methods=['POST'])
def receive_data():
    if request.headers['Content-Type'] == 'application/json':
        try:
            data = request.get_json()
            # Process the JSON data here
            result = process_data(data)  # Example: process_data function
            return jsonify({'message': 'Data received successfully', 'result': result}), 200
        except Exception as e:
            return jsonify({'error': f'Error processing JSON data: {e}'}), 400
    else:
        return jsonify({'error': 'Unsupported Media Type'}), 415

def process_data(data):
    # Example: Process the received JSON data
    # Here you would perform the desired operations 
    # on the 'data' dictionary
    
    # For example, sum the values of a list:
    if 'numbers' in data:
        return sum(data['numbers']) 
    
    # Return a default value or handle other cases as needed
    return "No specific processing defined"

if __name__ == '__main__':
    app.run(debug=True)

