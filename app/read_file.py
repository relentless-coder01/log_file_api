import os
import json
from config import *
from util import *

class ReadFile:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_path = os.path.join(LOG_ROOT_DIR, file_name)
        self.metadata_file = get_metadata_filename(file_name)

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

    def read_file_backwards(self, n, page):
        try:
            total_lines_read = (page - 1) * PAGE_SIZE
            # If n is not mentioned, we read the entire file
            if n is None:
                n = float('inf')

            print(f"Reading for Page: {str(page)}")
            if PAGE_SIZE == 0:
                return [], False
            with open(self.file_path, 'rb') as fp:
                metadata = self.get_metadata(page)
                bytes_left = metadata.get(get_page_key(page), 0)
                print(f"Bytes left to read: {str(bytes_left)}")
                # Seek to the bytes left ending relatively for each page
                fp.seek(bytes_left, 0)
                print(f"Initial file pointer at: {str(fp.tell())}")
                lines = []
                residue = ''
                # O(bytes read for the page)
                while bytes_left > 0 and len(lines) < PAGE_SIZE and total_lines_read < n:
                    lines_to_append = []
                    # Determine chunks to read and seek pointer
                    chunks_to_read = min(CHUNK_SIZE, bytes_left)
                    fp.seek(-chunks_to_read, 1)
                    chunk = fp.read(chunks_to_read).decode('utf-8')
                    # Adjust bytes left
                    bytes_left = bytes_left - len(chunk)
                    # After reading reset fp
                    fp.seek(-len(chunk), 1)
                    # Split the lines
                    chunk_lines = chunk.splitlines(keepends=True)
                    # Assume first part of the chunk as residue, we dont know until we read above it
                    if bytes_left > 0:
                        residue = chunk_lines.pop(0)
                    if len(residue) >= LINE_SIZE:
                        # Break the residue into lines based on our predefined upper limit for Line size
                        residue_lines = [residue[0:i] if i-LINE_SIZE < 0 else residue[i-LINE_SIZE:i] for i in range(len(residue), 0, -LINE_SIZE)][::-1]
                        if len(residue_lines) > 1:
                            residue = residue_lines.pop(0)
                        chunk_lines = residue_lines + chunk_lines
                    # We know for sure the remaining part of the chunk are complete lines
                    no_lines_to_append = min(n - total_lines_read, PAGE_SIZE - len(lines))
                    # Add these lines in reverse
                    chunk_lines = chunk_lines[::-1]
                    lines_to_append.extend(chunk_lines[:no_lines_to_append])
                    lines.extend([line.rstrip() for line in lines_to_append])
                    # Push the remaining as residue
                    residue = residue + "".join(chunk_lines[no_lines_to_append:])
                    # We are not gonna include residue, lets leave it for the next read
                    bytes_left = bytes_left + len(residue)
                    fp.seek(len(residue), 1)
                    # Clear residue after marking the pointer
                    residue = ''
                    total_lines_read += len(lines_to_append)
                if total_lines_read < n and bytes_left > 0:
                    more_lines = True
                    # Store bytes left at the end of this page so next page can use it
                    metadata[get_page_key(page + 1)] = bytes_left
                    self.store_metadata(metadata)
                else:
                    more_lines = False
                return lines, more_lines
        except FileNotFoundError as e:
            return [], False
