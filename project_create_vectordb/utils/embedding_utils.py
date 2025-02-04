import together
import logging
from typing import List, Dict
from pathlib import Path
import time
from ..config.settings import TOGETHER_MODEL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    def __init__(self, model_name: str = TOGETHER_MODEL):
        self.model_name = model_name
        
    def create_embedding(self, text: str) -> List[float]:
        """Tạo embedding cho một đoạn text"""
        try:
            response = together.Embeddings.create(
                input=[text],
                model=self.model_name
            )
            
            if 'data' in response and len(response['data']) > 0:
                return response['data'][0]['embedding']
            else:
                raise ValueError(f"Invalid response format: {response}")
                
        except Exception as e:
            logger.error(f"Error creating embedding: {str(e)}")
            raise
            
    def create_batch_embeddings(self, texts: List[str], batch_size: int = 10) -> List[List[float]]:
        """Tạo embeddings cho nhiều đoạn text theo batch"""
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            try:
                response = together.Embeddings.create(
                    input=batch,
                    model=self.model_name
                )
                
                if 'data' in response:
                    batch_embeddings = [item['embedding'] for item in response['data']]
                    embeddings.extend(batch_embeddings)
                    
                    logger.info(f"Processed batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")
                    time.sleep(0.5)  # Tránh rate limit
                    
            except Exception as e:
                logger.error(f"Error in batch {i//batch_size + 1}: {str(e)}")
                raise
                
        return embeddings
