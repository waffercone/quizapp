from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()
MODEL = "gpt-4-0613-starcode"

system_prompt = """
You are an AI Quiz Bot. You will be provided with a question,
4 options including the correct answer, and reasons why the other options are incorrect.
Generate questions based on difficulty level 1 to 20.
"""

class QuizQuestion(BaseModel):
    question: str = Field(description="Question on the required topic.")
    options: list[str] = Field(description="4 options for the question")
    answer: str = Field(description="Correct answer to the question")
    explanations: list[str] = Field(description="Reasons why each incorrect option is wrong")

class QuizSet(BaseModel):
    questions: list[QuizQuestion]
    confidence: float = Field(description="Confidence in the resolution (0-1)")

def get_quiz_questions(language: str, level: str):
    query = f"""
Provide me 5 Questions on {language} based on Level {level} Understanding.
For each question, include 4 options, the correct answer, and reasons why each incorrect option is wrong.
"""
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        response_model=QuizSet
    )
    
    response = completion.choices[0].message.model_dump()
    return response

if __name__ == "__main__":
    quiz_data = get_quiz_questions(language='java', level='intermediate')
    for question in quiz_data['questions']:
        print(f"Question: {question['question']}")
        print("Options:")
        for i, option in enumerate(question['options']):
            print(f"  {i+1}. {option}")
        print(f"Correct Answer: {question['answer']}")
        print("Explanations for incorrect options:")
        for explanation in question['explanations']:
            print(f"  - {explanation}")
        print("\n")
