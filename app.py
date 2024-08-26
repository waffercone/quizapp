from flask import Flask, request, jsonify
import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Set up the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_question(topic):
    prompt = f"Generate a unique multiple-choice question on {topic} with 4 answer choices. Provide the correct answer and explanations for why the other choices are incorrect."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert quiz question creator."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.7,
    )

    message = response.choices[0].message['content'].strip()

    # Parse the response to extract question, choices, and correct answer
    lines = message.split("\n")
    question = lines[0].strip()
    choices = [line.strip() for line in lines[1:5]]
    correct_answer = lines[5].strip().split(":")[1].strip()
    explanations = {
        choice.split(":")[0].strip(): choice.split(":")[1].strip()
        for choice in lines[6:]
    }

    return {
        "question": question,
        "choices": choices,
        "correct_answer": correct_answer,
        "explanations": explanations,
    }

@app.route('/generate-questions', methods=['POST'])
def generate_quiz():
    data = request.json
    topic = data.get('topic')

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    questions = []
    for _ in range(data.get('num_questions', 5)):  # Default to 5 questions if not provided
        question_data = generate_question(topic)
        questions.append(question_data)

    return jsonify({"questions": questions})

if __name__ == '__main__':
    app.run(debug=True)
