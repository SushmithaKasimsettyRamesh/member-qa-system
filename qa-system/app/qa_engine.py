# app/qa_engine.py
import os
from openai import OpenAI
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class QAEngine:
    """
    the brain of the operation
    uses OpenAI to answer questions based on member data
    """
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        # using gpt-4o-mini cause it's cheaper and fast enough for this
        self.model = "gpt-4o-mini"
        
    def answer_question(self, question: str, context: str) -> str:
        """
        ask GPT a question with context from member messages
        this is where the magic happens (or doesn't lol)
        """
        
        # craft the prompt - this took some iterations to get right
        system_prompt = """You are a helpful assistant that answers questions about member data.
You will be given member messages as context, and you need to answer questions accurately.

Rules:
- Only use information from the provided context
- If the answer isn't in the context, say "I don't have enough information to answer that"
- Be concise but complete
- Extract specific details like dates, numbers, names accurately
- Don't make assumptions or hallucinate data
"""
        
        user_prompt = f"""Context (Member Messages):
{context}

Question: {question}

Please provide a direct answer based only on the information above."""
        
        try:
            logger.info(f"sending question to OpenAI: {question}")
            
            # call the API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,  # low temp for factual answers
                max_tokens=300  # keep answers reasonable length
            )
            
            answer = response.choices[0].message.content.strip()
            logger.info(f"got answer: {answer[:100]}...")
            
            return answer
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return f"Error processing question: {str(e)}"