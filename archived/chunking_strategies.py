class RecursiveChunker:
    def __init__(self, chunk_size=100, chunk_overlap=20):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = ["\n\n", "\n", ". ", " ", ""]

    def split_text(self, text):
        """Recursively split text until below chunk size"""
        final_chunks = []

        def recursive_split(current_text, separator_index):
            if len(current_text) < self.chunk_size:
                return [current_text]
            
            # Find best sepaprator to use
            if separator_index >= len(self.separators):
                return [current_text[:self.chunk_size]]
            

            separator = self.separators[separator_index]
            splits = current_text.split(separator) if separator else list(current_text)

            chunks = []
            current_chunk = ""

            for part in splits:
                #Add the separators back (except for last resort empty str)
                part_with_sep = part + separator if separator else part
                
                if len(current_chunk) + len(part_with_sep) <= self.chunk_size:
                    current_chunk+= part_with_sep

                else:
                    if current_chunk:
                         chunks.append(current_chunk.strip())

                    # if single part is stil too big
                    if len(part_with_sep) > self.chunk_size:
                        chunks.extend(recursive_split(part_with_sep, separator_index + 1))    
                    else:
                        current_chunk = part_with_sep
            if current_chunk:
                chunks.append(current_chunk.strip())

            return chunks
        return recursive_split(text, 0)

# --- TEST IT ---
text = "The Intern CEO is a book about leadership.\n\nIt focuses on young professionals. It covers coding, AI, and growth mindset."
chunker = RecursiveChunker(chunk_size=50)
chunks = chunker.split_text(text)

for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: '{chunk}' (Len: {len(chunk)})")
