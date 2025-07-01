import re
from rapidfuzz import fuzz

def clean_sentences(sentences, textCase='normal'):
    cleaned = []
    for sentence in sentences:
        print(f"Cleaning sentence: {sentence}")
        words = re.sub(r'—', ' ', sentence)
        words = re.sub(r'-', ' ', words)
        words = re.sub(r'[^a-zA-Z0-9\s\']', '', words)
        words = re.sub(r'\s+', ' ', words).strip()
        if textCase == 'lower':
            words = words.lower()
        elif textCase == 'upper':
            words = words.upper()
        elif textCase == 'title':
            words = words.title()
        elif textCase == 'normal':
            pass
        cleaned.append(words)
    return cleaned


def format_words_into_lines_from_script(words, script_lines, textCase='normal'):
    if not words:
        print("Warning: No words transcribed. Cannot format lines.")
        return []
    if not script_lines:
        print("Warning: No script lines provided. Cannot format.")
        return []
    print("Formatting words into lines from script...")
    cleaned_script = clean_sentences(script_lines, textCase)
    lines = []
    word_index = 0
    for script_line in cleaned_script:
        script_words = script_line.split()
        line_start_time = None
        line_end_time = None
        for i in range(len(script_words)):
            if word_index < len(words):
                similarity = fuzz.ratio(script_words[i].lower(), words[word_index]['text'].lower())
                print(similarity, script_words[i].lower(), words[word_index]['text'].lower())
                if similarity >= 50:
                    if line_start_time is None:
                        line_start_time = words[word_index]['start']
                    line_end_time = words[word_index]['end']
                    word_index += 1
            else:
                pass
        
        if line_start_time is not None and line_end_time is not None:
            lines.append({
                'text': script_line.strip(),
                'start': line_start_time,
                'end': line_end_time
            })
    return lines