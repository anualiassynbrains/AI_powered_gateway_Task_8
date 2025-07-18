import json
import sys
from groq import AsyncGroq
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

client = AsyncGroq(api_key=os.getenv('GROQ_API'))
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
async def estimate_cost_request(text):
        prompt = (
        "Evaluate the complexity of the following text. Return a single integer in JSON format as: {\"cost\": <int from 1 to 10>}.\n"
        "Consider length, vocabulary, and topic complexity.You should not include any other texts just return only the value\n\n"
        f"{text}"
        )
        response = await client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        content = response.choices[0].message.content
        print("Raw Model Output:", content)

        try:
            data = json.loads(content)
            return int(data.get("cost"))
        except Exception as e:
            raise ValueError(f"Failed to parse model output: {content}") from e
        
text_input = '''Indian history documents encompass a wide range of sources, including archives, manuscripts, inscriptions, and literary works, offering insights into various periods and aspects of the subcontinent's past. The National Archives of India, located in New Delhi, serves as a primary repository for records of the Government of India, including those from the East India Company and subsequent colonial administrations. These records cover diverse fields like revenue, political affairs, military matters, and commercial transactions, providing valuable information for researchers and historians. Key Sources of Indian History Documents: National Archives of India: This is the central repository for government records, including those related to the East India Company and the British Raj. Abhilekh Patal: An online portal of the National Archives of India, providing access to digitized collections and reference media. British Pathé Newsreels: Digitized newsreels offer visual documentation of historical events and daily life in India during the colonial period.'''


if __name__ == "__main__":
    summary = asyncio.run(estimate_cost_request(text_input))
    print(summary)