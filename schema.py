from pydantic import BaseModel
from typing import List

class ThemedWordList(BaseModel):
    words: List[str]
