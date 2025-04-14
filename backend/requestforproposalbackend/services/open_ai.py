import openai
import numpy as np
from django.conf import settings
from project.models import FunctionalAreaEmbedding
import requests
from bs4 import BeautifulSoup

openai.api_key = settings.OPENAI_API_KEY

class ChatService:
    @staticmethod
    def process_prompt(prompt: str):
        if "store functional areas to database" in prompt.lower():
            return ChatService._handle_storage(prompt)
        elif "use functional areas" in prompt.lower():
            return ChatService._handle_rfp_generation(prompt)
        return ChatService._generate_chat_response(prompt)

    @staticmethod
    def _generate_chat_response(prompt: str):
        completion = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return {"answer": completion.choices[0].message.content.strip(), "rfp_sections": {}}

    @staticmethod
    def _handle_storage(prompt: str):
        document_text = prompt.split("CONTENT:")[1].strip()
        
        embedding_response = openai.embeddings.create(
            model="text-embedding-3-small",
            input=document_text
        )
        
        FunctionalAreaEmbedding.objects.create(
            area_name=ChatService._extract_area_name(document_text),
            text=document_text,
            embedding=embedding_response.data[0].embedding
        )
        
        return {"answer": "Functional areas stored successfully", "rfp_sections": {}}

    @staticmethod
    def _handle_rfp_generation(prompt: str):
        user_question = prompt.split("use functional areas")[1].strip()
        
        query_embedding = openai.embeddings.create(
            model="text-embedding-3-small",
            input=user_question
        ).data[0].embedding
        
        relevant_areas = ChatService._find_similar_areas(query_embedding)
        
        rfp_prompt = f"""
        **Task 1:** Answer the user question using functional area knowledge:
        {user_question}

        **Task 2:** Generate RFP-ready technical sections using:
        {[f"name: {area.area_name}, description: {area.text}" for area in relevant_areas]}

        **Format:**
        ANSWER: [Your answer]
        RFP_SECTIONS:
        - [Section 1 Title]: [Content]
        - [Section 2 Title]: [Content]
        """
        
        completion = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": settings.RFP_SYSTEM_PROMPT},
                {"role": "user", "content": rfp_prompt}
            ]
        )
        print(completion.choices[0].message.content)
        
        return ChatService._parse_rfp_response(completion.choices[0].message.content)

    @staticmethod
    def _find_similar_areas(query_embedding, threshold=0.75):
        areas = FunctionalAreaEmbedding.objects.all()
        similar = []
        
        for area in areas:
            similarity = np.dot(query_embedding, area.embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(area.embedding)
            )
            if similarity > threshold:
                area.similarity = similarity
                similar.append(area)
        
        return sorted(similar, key=lambda x: x.similarity, reverse=True)[:3]

    @staticmethod
    def _parse_rfp_response(response_text):
        import re
        answer_match = re.search(r"ANSWER:(.*?)(?=RFP_SECTIONS:)", response_text, re.DOTALL)
        rfp_sections_match = re.findall(r"- \[(.*?)\]: (.*)", response_text)
        functional_areas = {match[0]: match[1] for match in rfp_sections_match}
        return {
            "answer": answer_match.group(1).strip() if answer_match else "",
            "rfp_sections": functional_areas
        }
    
    @staticmethod
    def get_information_from_website(url: str):
        import requests
        from bs4 import BeautifulSoup

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        truncated_text = ' '.join(text.split()[:300])  # Truncate to approximately 200 words

        prompt = f"Extract the following information and create a meaningful paragraph with a maximum of 200 words: {truncated_text}"
        completion = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Extract information from the given text and create a meaningful paragraph with a maximum of 200 words."},
                {"role": "user", "content": prompt}
            ]
        )
        return {"answer": completion.choices[0].message.content.strip(), "rfp_sections": {}}

    @staticmethod
    def refactor_information(information: str):
        refactor_prompt = f"Refactor the following information: {information}"
        completion = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Refactor the given information for clarity and conciseness."},
                {"role": "user", "content": refactor_prompt}
            ]
        )
        return {"answer": completion.choices[0].message.content.strip(), "rfp_sections": {}}