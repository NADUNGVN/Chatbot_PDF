from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime

@dataclass
class TextChunk:
    content: str
    metadata: Dict
    
    def __post_init__(self):
        if not isinstance(self.metadata, dict):
            self.metadata = {}
        
        # Thêm timestamp
        self.metadata['created_at'] = datetime.now().isoformat()
        
        # Đảm bảo content là string
        if not isinstance(self.content, str):
            self.content = str(self.content)
        
        # Chuẩn hóa content
        self.content = self.content.strip()
