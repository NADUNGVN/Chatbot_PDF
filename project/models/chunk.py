from dataclasses import dataclass
from typing import Dict
from datetime import datetime

@dataclass
class TextChunk:
    file_name: str
    ma_thu_tuc: str
    ten_thu_tuc: str
    section: str
    content: str
    chunk_id: str
    position: int
    timestamp: datetime = datetime.now()
    
    @property
    def length(self) -> int:
        return len(self.content)
    
    def to_dict(self) -> Dict:
        return {
            "chunk_id": self.chunk_id,
            "file_name": self.file_name,
            "ma_thu_tuc": self.ma_thu_tuc,
            "ten_thu_tuc": self.ten_thu_tuc,
            "section": self.section,
            "content": self.content,
            "position": self.position,
            "timestamp": self.timestamp.isoformat(),
            "length": self.length
        }
