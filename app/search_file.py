import os
import json
import re
from config import *
from util import *

class SearchFile:
    def __init__(self, file_name, keyword):
        self.file_name = file_name
        self.file_path = os.path.join(LOG_ROOT_DIR, file_name)
        self.keyword = self.clean_keyword(keyword)
        self.pattern = self.get_regex_pattern()
        self.metadata_file = get_keyword_metadata_filename(file_name, keyword)

    def clean_keyword(self, keyword):
        return keyword.strip()

    def get_regex_pattern(self):
        return rf'(?i)(?<!\w){re.escape(self.keyword)}(?!\w)'

    def get_metadata(self, page):
        if page == 1:
            metadata = {get_page_key(page): os.path.getsize(self.file_path)}
        else:
            with open(METADATA_DIR + self.metadata_file, "r") as mf:
                metadata = json.loads(mf.read())
        return metadata

    def store_metadata(self, metadata):
        with open(METADATA_DIR + self.metadata_file, "w") as mf:
            mf.write(json.dumps(metadata))

    def search_keyword(self, n, page):
        try:
            total_lines_read = (page - 1) * PAGE_SIZE
            print(f"Reading for Page: {str(page)}")
            # If n is not mentioned, we search for all occurrences
            if n is None:
                n = float('inf')
            if PAGE_SIZE == 0 or self.keyword == '':
                return [], False

            with open(self.file_path, 'rb') as fp:
                metadata = self.get_metadata(page)
                bytes_left = metadata.get(get_page_key(page), 0)
                print(f"Bytes left to read: {str(bytes_left)}")
                # Seek to the bytes left end relatively for each page
                fp.seek(bytes_left, 0)
                print(f"Initial file pointer at: {str(fp.tell())}")
                lines = []
                residue = ''
                while bytes_left > 0 and len(lines) < PAGE_SIZE and total_lines_read < n:
                    lines_to_append = []
                    # Determine chunks to read and seek pointer
                    chunks_to_read = min(CHUNK_SIZE, bytes_left)
                    fp.seek(-chunks_to_read, 1)
                    chunk = fp.read(chunks_to_read).decode('utf-8')
                    # Adjust bytes left
                    bytes_left = bytes_left - len(chunk)
                    # After reading reset file pointer
                    fp.seek(-len(chunk), 1)
                    # Split the lines
                    chunk_lines = chunk.splitlines(keepends=True)
                    # Assume first part of the chunk as residue, we don't know until we read above it
                    if bytes_left > 0:
                        residue = chunk_lines.pop(0)
                    if len(residue) >= LINE_SIZE:
                        # Break the residue into lines based on our predefined upper limit for Line size
                        residue_lines = [residue[0:i] if i - LINE_SIZE < 0 else residue[i - LINE_SIZE:i] for i in range(len(residue), 0, -LINE_SIZE)][::-1]
                        if len(residue_lines) > 1:
                            residue = residue_lines.pop(0)
                        chunk_lines = residue_lines + chunk_lines
                    # We know for sure the remaining part of the chunk are complete lines
                    no_lines_to_append = min(n - total_lines_read, PAGE_SIZE - len(lines))
                    # Add these lines in reverse
                    chunk_lines = chunk_lines[::-1]
                    # Let us search and select lines that contains the keyword
                    for k in range(len(chunk_lines)):
                        if len(lines_to_append) == no_lines_to_append:
                            break
                        if re.search(self.pattern, chunk_lines[k]):
                            lines_to_append.append(chunk_lines[k])
                    lines.extend([line.rstrip() for line in lines_to_append])
                    # Push the remaining as residue
                    if k != len(chunk_lines)-1:
                        residue = residue + "".join(chunk_lines[k:])
                    # We are not gonna include residue, lets leave it for the next read
                    bytes_left = bytes_left + len(residue)
                    fp.seek(len(residue), 1)
                    # Clear residue after marking the pointer
                    residue = ''
                    total_lines_read += len(lines_to_append)
                if total_lines_read < n and bytes_left > 0:
                    more_lines = True
                    # Store bytes left to read at the end of this page so next page can use it
                    metadata[get_page_key(page + 1)] = bytes_left
                    self.store_metadata(metadata)
                else:
                    more_lines = False
                print(f"# Lines for Page {str(page)}: {str(len(lines))}")
                return lines, more_lines
        except FileNotFoundError as e:
            print("Exception: File not found!")
            return [], False