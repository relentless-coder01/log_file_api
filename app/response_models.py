from fastapi.responses import JSONResponse  # New import
from pydantic import BaseModel
from typing import Any

# class ResponseStructure(BaseModel):
#     details: Any
#     status_code: int
#
# # Custom response class
# class CustomResponse(JSONResponse):
#     def __init__(self, content: Any, status_code: int = 200, *args, **kwargs) -> None:
#         content = ResponseStructure(details=content, status_code=status_code).model_dump()
#         super().__init__(content, status_code, *args, **kwargs)

class Response(BaseModel):
    status: int
    message: str