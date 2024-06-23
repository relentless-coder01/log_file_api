import pytest
from fastapi.testclient import TestClient
from urllib.parse import urlencode

from app.main import app

API_URL = "/api/v1/logs"
client = TestClient(app)

# Test files
FILE1 = "small/file1.log"
FILE3 = "small/file3.log"
LARGE_REVIEWS_FILE = "large/amz_reviews/reviews_log.txt"

def test_file_not_found():
    query_params = {
        "filename": "file_not_exists.log"
    }
    response = client.get(f"{API_URL}?{urlencode(query_params)}")
    assert response.status_code == 404

def test_filename_missing():
    query_params = {
    }
    response = client.get(f"{API_URL}?{urlencode(query_params)}")
    assert response.status_code == 400
    resp_data = response.json()
    assert resp_data["errors"][0]["message"] == "Field required"

def test_invalid_n():
    query_params = {
        "filename": FILE3,
        "n": "abj"
    }
    response = client.get(f"{API_URL}?{urlencode(query_params)}")
    assert response.status_code == 400
    resp_data = response.json()
    assert resp_data["errors"][0]["message"] == "Input should be a valid integer, unable to parse string as an integer"

def test_invalid_n_empty():
    query_params = {
        "filename": FILE3,
        "n": ""
    }
    response = client.get(f"{API_URL}?{urlencode(query_params)}")
    assert response.status_code == 400
    resp_data = response.json()
    assert resp_data["errors"][0]["message"] == "Input should be a valid integer, unable to parse string as an integer"

def test_read_small_file_whole():
    query_params = {
        "filename": FILE3
    }
    response = client.get(f"{API_URL}?{urlencode(query_params)}")
    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data["page"] == 1
    assert len(resp_data["data"]) == 24

def test_read_small_file_n_lines():
    query_params = {
        "filename": FILE3,
        "n": 10
    }
    response = client.get(f"{API_URL}?{urlencode(query_params)}")
    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data["page"] == 1
    assert len(resp_data["data"]) == 10

def test_read_small_file_n_lines_with_pagination():
    query_params = {
        "filename": FILE1,
        "n": 120
    }
    response = client.get(f"{API_URL}?{urlencode(query_params)}")
    resp_data = response.json()
    assert response.status_code == 200
    assert resp_data["page"] == 1
    assert len(resp_data["data"]) == 50
    assert resp_data["next_page"] is not None

    response2 = client.get(resp_data["next_page"])
    assert response2.status_code == 200
    resp_data2 = response2.json()
    assert resp_data2["page"] == 2
    assert len(resp_data2["data"]) == 50
    assert resp_data2["next_page"] is not None

    response3 = client.get(resp_data2["next_page"])
    assert response3.status_code == 200
    resp_data3 = response3.json()
    assert resp_data3["page"] == 3
    assert len(resp_data3["data"]) == 20

def test_read_small_file_search():
    query_params = {
        "filename": FILE3,
        "keyword": "yumm"
    }
    response = client.get(f"{API_URL}?{urlencode(query_params)}")
    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data["page"] == 1
    assert len(resp_data["data"]) == 3

def test_read_small_file_search_whole_word():
    query_params = {
        "filename": FILE3,
        "keyword": "I"
    }
    response = client.get(f"{API_URL}?{urlencode(query_params)}")
    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data["page"] == 1
    assert len(resp_data["data"]) == 11

def test_read_small_file_search_phrase():
    query_params = {
        "filename": FILE3,
        "keyword": "It is"
    }
    response = client.get(f"{API_URL}?{urlencode(query_params)}")
    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data["page"] == 1
    assert len(resp_data["data"]) == 1

def test_read_small_file_search_n_lines():
    query_params = {
        "filename": FILE3,
        "keyword": "to",
        "n": 3
    }
    response = client.get(f"{API_URL}?{urlencode(query_params)}")
    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data["page"] == 1
    assert len(resp_data["data"]) == 3

def test_read_small_file_search_spl_chars():
    query_params = {
        "filename": FILE3,
        "keyword": "i'll",
    }
    response = client.get(f"{API_URL}?{urlencode(query_params)}")
    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data["page"] == 1
    assert len(resp_data["data"]) == 5

def test_read_small_file_search_empty():
    query_params = {
        "filename": FILE3,
        "keyword": "",
    }
    response = client.get(f"{API_URL}?{urlencode(query_params)}")
    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data["page"] == 1
    assert len(resp_data["data"]) == 24

# Large file > 1GB
def test_read_large_file_whole():
    query_params = {
        "filename": LARGE_REVIEWS_FILE
    }
    response = client.get(f"{API_URL}?{urlencode(query_params)}")
    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data["page"] == 1
    assert len(resp_data["data"]) == 50

def test_read_large_file_n_lines():
    query_params = {
        "filename": LARGE_REVIEWS_FILE,
        "n": 25
    }
    response = client.get(f"{API_URL}?{urlencode(query_params)}")
    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data["page"] == 1
    assert len(resp_data["data"]) == 25

def test_read_large_file_n_lines_with_pagination():
    query_params = {
        "filename": LARGE_REVIEWS_FILE,
        "n": 135
    }
    response = client.get(f"{API_URL}?{urlencode(query_params)}")
    resp_data = response.json()
    assert response.status_code == 200
    assert resp_data["page"] == 1
    assert len(resp_data["data"]) == 50
    assert resp_data["next_page"] is not None

    response2 = client.get(resp_data["next_page"])
    assert response2.status_code == 200
    resp_data2 = response2.json()
    assert resp_data2["page"] == 2
    assert len(resp_data2["data"]) == 50
    assert resp_data2["next_page"] is not None

    response3 = client.get(resp_data2["next_page"])
    assert response3.status_code == 200
    resp_data3 = response3.json()
    assert resp_data3["page"] == 3
    assert len(resp_data3["data"]) == 35

def test_read_large_file_search():
    query_params = {
        "filename": LARGE_REVIEWS_FILE,
        "keyword": "good"
    }
    response = client.get(f"{API_URL}?{urlencode(query_params)}")
    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data["page"] == 1
    assert len(resp_data["data"]) == 50

def test_read_large_file_search_keyword_in_first_line():
    query_params = {
        "filename": LARGE_REVIEWS_FILE,
        "keyword": "good"
    }
    response = client.get(f"{API_URL}?{urlencode(query_params)}")
    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data["page"] == 1
    assert len(resp_data["data"]) == 50