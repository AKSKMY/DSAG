from flask import Flask, request, render_template_string
import pandas as pd

app = Flask(__name__)

# Load the dataset
file_path = r"Dataset\item_list_with_coordinates.csv"
data = pd.read_csv(file_path)

# KMP Algorithm
def kmp_search(pattern, text):
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps
    
    lps = compute_lps(pattern)
    i = j = 0
    matches = []
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            matches.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return matches

# HTML Template
template = """
<!doctype html>
<html>
<head>
    <title>Pattern Search</title>
</head>
<body>
    <h1>Search Pattern in Dataset</h1>
    <form method="post">
        Pattern: <input type="text" name="pattern">
        <input type="submit" value="Search">
    </form>
    {% if matches %}
    <h2>Matches Found:</h2>
    <table border="1">
        <tr>
            <th>Row Index</th>
            <th>Content</th>
        </tr>
        {% for match in matches %}
        <tr>
            <td>{{ match[0] }}</td>
            <td>{{ match[1] }}</td>
        </tr>
        {% endfor %}
    </table>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    matches = []
    if request.method == 'POST':
        pattern = request.form['pattern']
        text = data.to_string(index=False)
        indices = kmp_search(pattern, text)
        
        # Find corresponding rows
        for idx in indices:
            row_start = text.rfind('\n', 0, idx) + 1
            row_end = text.find('\n', idx)
            if row_end == -1:
                row_end = len(text)
            row_content = text[row_start:row_end]
            row_index = len(text[:row_start].split('\n')) - 2  # Adjust for zero-based index
            matches.append((row_index, row_content))
    
    return render_template_string(template, matches=matches)

if __name__ == '__main__':
    app.run(debug=True)

# Test Case
def test_kmp_search():
    pattern = "apple"
    text = data.to_string(index=False)
    matches = kmp_search(pattern, text)
    print(f"Matches for pattern '{pattern}': {matches}")

# Call the test function
test_kmp_search()