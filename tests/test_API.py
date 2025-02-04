# test_together_api.py

import os
from dotenv import load_dotenv
import logging
import time
import together

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def test_api_key():
    """Test API key có hợp lệ không"""
    try:
        # Load API key từ .env
        load_dotenv()
        api_key = os.getenv("TOGETHER_API_KEY_1")
        
        if not api_key:
            logger.error("TOGETHER_API_KEY_1 not found in .env file")
            return False
            
        logger.info(f"Found API key: {api_key[:5]}...{api_key[-4:]}")
        
        # Set API key
        together.api_key = api_key
        
        return True
        
    except Exception as e:
        logger.error(f"Error loading API key: {str(e)}")
        return False

def test_embedding():
    """Test tạo embedding"""
    try:
        # Test text
        test_text = "Đây là câu văn để test embedding model."
        
        logger.info("Testing embedding generation...")
        logger.info(f"Test text: {test_text}")
        start_time = time.time()
        
        # Gọi API với model mới
        response = together.Embeddings.create(
            input=[test_text],
            model="togethercomputer/m2-bert-80M-32k-retrieval"
        )
        
        duration = time.time() - start_time
        
        # Kiểm tra và hiển thị chi tiết response
        logger.info(f"Raw response: {response}")
        
        if 'data' in response and len(response['data']) > 0:
            embedding = response['data'][0]['embedding']
            embedding_size = len(embedding)
            logger.info(f"Successfully generated embedding of size {embedding_size}")
            logger.info(f"First 5 values of embedding: {embedding[:5]}")
            logger.info(f"Time taken: {duration:.2f} seconds")
            return True
        else:
            logger.error("Invalid response format")
            logger.error(f"Response: {response}")
            return False
            
    except Exception as e:
        logger.error(f"Error testing embedding: {str(e)}")
        logger.error(f"Exception type: {type(e)}")
        logger.error(f"Exception details: {str(e)}")
        return False

def run_all_tests():
    """Chạy tất cả các test"""
    logger.info("Starting Together AI API tests...")
    
    # Test 1: API Key
    logger.info("\n1. Testing API key...")
    if not test_api_key():
        logger.error("API key test failed. Stopping further tests.")
        return
    logger.info("API key test passed!")
    
    # Test 2: Embedding
    logger.info("\n2. Testing embedding generation...")
    embedding_success = test_embedding()
    logger.info("Embedding test: " + ("Passed!" if embedding_success else "Failed!"))
    
    # Summary
    logger.info("\nTest Summary:")
    logger.info(f"API Key: Pass")
    logger.info(f"Embedding: {'Pass' if embedding_success else 'Fail'}")

if __name__ == "__main__":
    run_all_tests()