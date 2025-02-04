import logging
from pathlib import Path
from src.embeddings.embedding_generator import EmbeddingGenerator
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_embedding_generator():
    """Test embedding generator with sample data"""
    try:
        # Initialize generator
        generator = EmbeddingGenerator()
        
        # Test cases
        test_texts = [
            "Đây là câu test thứ nhất.",
            "Câu thứ hai dài hơn một chút để test độ dài khác nhau.",
            "Câu thứ ba có chứa số 123 và ký tự đặc biệt @#$.",
            "Câu thứ tư rất dài để test xử lý văn bản dài. " * 5
        ]
        
        logger.info("Testing single embedding generation...")
        embedding = generator.generate_embedding(test_texts[0])
        if embedding is not None:
            logger.info(f"Single embedding size: {len(embedding)}")
            logger.info(f"First 5 values: {embedding[:5]}")
        
        logger.info("\nTesting batch embedding generation...")
        embeddings = generator.generate_embeddings_batch(test_texts)
        success_count = sum(1 for e in embeddings if e is not None)
        logger.info(f"Successfully generated {success_count}/{len(test_texts)} embeddings")
        
        return success_count == len(test_texts)
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    load_dotenv()
    success = test_embedding_generator()
    logger.info(f"\nOverall test {'passed' if success else 'failed'}")