import os.path

def check_file_exists(file_path):
    try:
        return os.path.isfile(file_path)
    except:
        return False

def get_metadata_filename(file_name):
    return f"meta-{str(file_name.replace('/', '-').split('.')[0])}.json"

def get_keyword_metadata_filename(file_name, keyword):
    return f"meta-{str(file_name.replace('/', '-').split('.')[0])}-{str(keyword)}.json"

def get_page_key(page):
    return f"page{str(page)}"

def clean_request_params(param):
    if param is None:
        return None
    if param.strip() in ['null', '']:
        return None
    return param
