from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_cover_letter(job_description: str) -> str:

    if not job_description or len(job_description) == 0:
        return ""

    prompt = f"Write a cover letter for this job, here is the whole job description {job_description}."
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    return response.text
