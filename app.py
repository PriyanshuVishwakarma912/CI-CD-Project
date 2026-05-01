import json
import os
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)
NOTES_FILE = 'notes.json'

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_notes(notes):
    with open(NOTES_FILE, 'w') as f:
        json.dump(notes, f)


HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Keep Clone</title>

<script src="https://cdn.tailwindcss.com"></script>
<script src="https://unpkg.com/lucide@latest"></script>

<style>
body {
    background: #202124;
    color: #e8eaed;
    font-family: 'Roboto', sans-serif;
}

.note {
    transition: all 0.2s ease;
}
.note:hover {
    transform: scale(1.03);
}

textarea, input {
    outline: none;
}

.fade-in {
    animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
</head>

<body class="p-4">

<!-- Navbar -->
<div class="flex items-center mb-8 border-b border-gray-700 pb-3">
    <i data-lucide="menu" class="mr-4"></i>
    <h1 class="text-xl font-semibold">Keep</h1>
</div>

<!-- Create Note -->
<div class="max-w-xl mx-auto mb-10">

<form action="/add" method="POST"
class="bg-[#303134] rounded-lg p-4 shadow-md cursor-text transition-all"
onclick="expandNote(this)">

<input type="text" name="title" placeholder="Title"
class="hidden w-full bg-transparent text-lg font-bold mb-2">

<textarea name="content" placeholder="Take a note..."
rows="1"
class="w-full bg-transparent resize-none"
oninput="autoGrow(this)"></textarea>

<div class="hidden justify-between mt-2 items-center">

<input type="color" name="color" value="#303134"
class="w-8 h-8 rounded cursor-pointer">

<button class="px-4 py-1 hover:bg-gray-700 rounded">
Add
</button>

</div>

</form>
</div>

<!-- Notes Grid -->
<div class="columns-1 sm:columns-2 md:columns-3 lg:columns-4 gap-4 max-w-7xl mx-auto">

{% for note in notes %}
<div class="note break-inside-avoid p-4 mb-4 rounded-lg shadow fade-in"
style="background: {{ note.color }}">

<h2 class="font-bold mb-2">{{ note.title }}</h2>
<p class="text-gray-200 whitespace-pre-wrap">{{ note.content }}</p>

<div class="flex justify-between mt-3 opacity-0 hover:opacity-100 transition">

<a href="/pin/{{ loop.index0 }}">
<i data-lucide="pin"></i>
</a>

<a href="/delete/{{ loop.index0 }}">
<i data-lucide="trash-2"></i>
</a>

</div>

</div>
{% endfor %}

</div>

<script>
lucide.createIcons()

function expandNote(el){
    el.querySelector("input").classList.remove("hidden")
    el.querySelector("div").classList.remove("hidden")
}

function autoGrow(el){
    el.style.height = "auto"
    el.style.height = (el.scrollHeight) + "px"
}
</script>

</body>
</html>
'''

@app.route('/')
def index():
    notes = load_notes()

    # pinned notes first
    notes = sorted(notes, key=lambda x: x.get('pinned', False), reverse=True)

    return render_template_string(HTML_TEMPLATE, notes=notes)


@app.route('/add', methods=['POST'])
def add():
    notes = load_notes()

    title = request.form.get('title')
    content = request.form.get('content')
    color = request.form.get('color') or '#303134'

    if title or content:
        notes.insert(0, {
            'title': title,
            'content': content,
            'color': color,
            'pinned': False
        })
        save_notes(notes)

    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    notes = load_notes()
    if 0 <= id < len(notes):
        notes.pop(id)
        save_notes(notes)
    return redirect(url_for('index'))


@app.route('/pin/<int:id>')
def pin(id):
    notes = load_notes()
    if 0 <= id < len(notes):
        notes[id]['pinned'] = not notes[id].get('pinned', False)
        save_notes(notes)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
