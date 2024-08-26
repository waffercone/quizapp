from flask import Flask ,jsonify,render_template,request
from flask_cors import CORS
from main import get_ticket_response_pydantic

query = """
Provide me 5 Questions on Python based on beginner Level Understanding
"""

# --------------------------------------------------------------
# Providing a JSON Schema
# --------------------------------------------------------------




app = Flask( __name__) 
CORS(app)
#@app.get("/")
#def index_get():
 #   return render_template("base.html")

@app.post("/predict")
def predict():
    data = request.get_json()
    language = data.get('Language')
    level = data.get('Level')
    print(language)
    print(level)
    
    # Use the language and level parameters as needed in your function
    
    message = get_ticket_response_pydantic(language=language , level=level)
    
    return message



if   __name__ == "__main__" : 
  
    app.run(debug=True)
  
