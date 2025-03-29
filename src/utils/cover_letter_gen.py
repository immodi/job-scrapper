from groq import Groq
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
except Exception as e:
    print(e)


def get_cover_letter(job_description: str) -> str:

    try:
        if not job_description or len(job_description) == 0:
            return ""

        prompt = f"Write a cover letter for this job, here is the whole job description {job_description}."

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        return ""
