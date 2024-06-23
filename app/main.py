import os
import traceback
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from urllib.parse import urlencode
import time
import json
from fastapi.staticfiles import StaticFiles

from app.read_search_file import ReadSearchFile
from app.list_files import list_log_files
from app.config import *
from app.util import *
from app.models import *

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create a metadata directory
os.makedirs(METADATA_DIR, exist_ok=True)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    custom_errors = []
    for error in errors:
        custom_errors.append({
            "field_name": error.get('loc', '')[1],
            "message": error.get('msg', '')
        })
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content = jsonable_encoder({"errors": custom_errors})
    )

def construct_url(request: Request, filename: str, n: int, keyword: str, page: int):
    """
    Construct url for pagination
    Parameter:
        - request: (Request)
        - filename: (String) File name/ File path of the log file inside the ‘/var/log/’ directory.
        - n: (Integer) The last number of lines or lines with keyword (if keyword specified) to be returned
        - keyword: (String) The keyword or phrase to search for within the log file.
        - page: (Integer) Page number for pagination
    Returns:
        - url (string)
    """
    query_params = {}
    query_params['filename'] = filename
    query_params['page'] = page
    if n is not None:
        query_params['n'] = n
    if keyword is not None:
        query_params['keyword'] = keyword
    return str(request.url.replace(query=urlencode(query_params)))

@app.get("/api/v1/logs", response_model=PaginatedResponse)
def get_data(request: Request, filename: str, n: Optional[int] = None, keyword: Optional[str] = None,
             page: Optional[int] = 1):
    """
    Endpoint to fetch log lines.
    Parameters:
        - filename: (String) File name/ File path of the log file inside the ‘/var/log/’ directory.
        - n: (Integer) The last number of lines or lines with keyword (if keyword specified) to be returned
        - keyword: (String) The keyword or phrase to search for within the log file.
        - page: (Integer) Page number for pagination
    Returns:
        - JSONResponse: log lines / errors
    """
    print('Request..........')
    print(f'filename: {filename}')
    print(f'n: {str(n)}')
    print(f"Keyword: {str(keyword)}")
    try:
        keyword = clean_request_params(keyword)
        file_path = os.path.join(LOG_ROOT_DIR, filename)
        print(f'file path: {file_path}')
        if not check_file_exists(file_path):
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=jsonable_encoder(
                                    Response(status=status.HTTP_404_NOT_FOUND,
                                             message="File not found.")))
        if page < 1:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=jsonable_encoder(
                                    Response(status=status.HTTP_404_NOT_FOUND,
                                             message="Page not found.")))
        if keyword is not None:
            metadata_filename = get_keyword_metadata_filename(filename, keyword)
        else:
            metadata_filename = get_metadata_filename(filename)
        # If visiting a page directly without visiting previous pages
        if page > 1:
            if not check_file_exists(METADATA_DIR + metadata_filename):
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                    content=jsonable_encoder(
                                        Response(status=status.HTTP_404_NOT_FOUND,
                                                 message="Page not found.")))
            with open(METADATA_DIR + metadata_filename, "r") as mf:
                try:
                    position = json.loads(mf.read())[get_page_key(page)]
                except KeyError as ke:
                    print("Exception: Page metadata not found!")
                    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                        content=jsonable_encoder(
                                            Response(status=status.HTTP_404_NOT_FOUND,
                                                     message="Page not found.")))
        start_time = time.time()
        lines, more_lines = ReadSearchFile(file_name=filename, n=n, keyword=keyword).read_search_backwards(page=page)
        print(f"Time taken: {str(time.time() - start_time)} seconds")

        next_page = construct_url(request=request, filename=filename, keyword=keyword, n=n, page=page + 1) if more_lines and len(lines) > 0 else None
        previous_page = construct_url(request=request, filename=filename, keyword=keyword, n=n, page=page - 1) if page > 1 else None
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(
                                PaginatedResponse(page=page, page_size=PAGE_SIZE, line_count=len(lines),
                                    data=lines, next_page=next_page, previous_page=previous_page)))
    except Exception as e:
        print(f"Exception: {str(e)}")
        print(str(traceback.format_exc()))
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content=jsonable_encoder(
                                Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                         message="Internal server error.")))

@app.get("/api/v1/files", response_model=PaginatedResponse)
def get_log_files():
    """
    Endpoint to get the list of log files
    Returns:
        - JSONResponse: list of log files with paths
    """
    try:
        files = list_log_files()
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(FileListResponse(file_count=len(files),
                                                                      files=files)))
    except Exception as e:
        print(f"Exception: {str(e)}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content=jsonable_encoder(
                                Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                         message="Internal server error.")))