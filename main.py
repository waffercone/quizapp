

from openai import OpenAI
from pydantic import BaseModel, Field

from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
MODEL = "gpt-4o-2024-08-06"


system_prompt = """
You are an AI Quiz Bot. You will be provided with a question,
and 4 options, including the answer for the questions.
And you will generate question based on difficulty level 1 to 20
"""




# --------------------------------------------------------------
# Using Pydantic
# --------------------------------------------------------------


class TicketResolution(BaseModel):
    class QuizQuestion(BaseModel):
        question: str = Field(description="question on the required topic.")
        options: list[str] = Field(description="4 options for the question")
        answer : str  = Field(description="Answer of the question")
        explanations: list[str] = Field(description="Reasons why each incorrect option is wrong")

    questions: list[QuizQuestion]
    
    confidence: float = Field(description="Confidence in the resolution (0-1)")


def get_ticket_response_pydantic(language: str , level : str):
    query = f"""
Provide me 5 Questions on {language} based on  Level {level} Understanding
"""

    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        response_format=TicketResolution,
    )

    response_pydantic =  completion.choices[0].message.parsed
    response = response_pydantic.model_dump()
    return((response))


if __name__ == "__main__":
    print(get_ticket_response_pydantic(language='java'))
