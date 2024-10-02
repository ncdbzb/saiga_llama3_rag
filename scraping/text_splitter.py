def split_text(text: str, chunk_size: int, separators=None) -> list[str]:
    if separators is None:
        separators = ["\n", " "]

    def split_with_separators(text, separators):
        if not separators:
            return [text]
        separator = separators[0]
        return [chunk for part in text.split(separator) for chunk in split_with_separators(part, separators[1:])]

    chunks = split_with_separators(text, separators)
    final_chunks = []
    for chunk in chunks:
        if len(chunk) > chunk_size:
            final_chunks.extend([chunk[i:i + chunk_size] for i in range(0, len(chunk), chunk_size)])
        else:
            final_chunks.append(chunk)
    return final_chunks