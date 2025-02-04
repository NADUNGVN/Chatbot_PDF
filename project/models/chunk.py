from dataclasses import dataclass
from typing import Dict

@dataclass
class TextChunk:
    file_name: str
    ma_thu_tuc: str
    ten_thu_tuc: str
    section: str
    content: str
    
    def to_dict(self) -> Dict:
        return {
            "file_name": self.file_name,
            "ma_thu_tuc": self.ma_thu_tuc,
            "ten_thu_tuc": self.ten_thu_tuc,
            "section": self.section,
            "content": self.content
        }
