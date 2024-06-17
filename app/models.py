from pydantic import BaseModel
from typing import List, Optional

class PaginatedResponse(BaseModel):
    page: int
    page_size: int
    line_count: int
    data: List[str]
    next_page: Optional[str]
    previous_page: Optional[str]

class Response(BaseModel):
    status: int
    message: str