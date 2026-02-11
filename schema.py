from pydantic import BaseModel
from typing import List, Union, Dict, Optional

# The request schema
class QueryRequest(BaseModel):
    query: Union[str, list[str]]
    model: str = "gpt-4o-mini"
    top_k: int = 3
    filter_filename: Optional[str] = None

# sources schema
class Source(BaseModel):
    filename: str
    content_snippet: str #a small preview of source text 

#
class  RAGResponse(BaseModel):
    answer: str
    sources: List[Source]

