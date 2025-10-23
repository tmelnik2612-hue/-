from flask import Flask, render_template, abort
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound
import os
from datetime import datetime, timedelta
import random

app = Flask(__name__)

MOCK_REPOS = [
    {
        'name': 'awesome-project',
        'owner': 'developer',
        'description': 'An awesome open-source project for developers',
        'language': 'Python',
        'stars': 1234,
        'forks': 456,
        'updated': datetime.now() - timedelta(days=2),
        'is_public': True
    },
    {
        'name': 'web-framework',
        'owner': 'developer',
        'description': 'Modern web framework with clean architecture',
        'language': 'JavaScript',
        'stars': 892,
        'forks': 123,
        'updated': datetime.now() - timedelta(days=5),
        'is_public': True
    },
    {
        'name': 'machine-learning',
        'owner': 'datascience',
        'description': 'Collection of ML algorithms and models',
        'language': 'Python',
        'stars': 3456,
        'forks': 789,
        'updated': datetime.now() - timedelta(days=1),
        'is_public': True
    },
    {
        'name': 'react-components',
        'owner': 'frontend',
        'description': 'Reusable React components library',
        'language': 'TypeScript',
        'stars': 2134,
        'forks': 567,
        'updated': datetime.now() - timedelta(days=7),
        'is_public': True
    },
    {
        'name': 'api-server',
        'owner': 'backend',
        'description': 'RESTful API server with authentication',
        'language': 'Go',
        'stars': 456,
        'forks': 89,
        'updated': datetime.now() - timedelta(days=3),
        'is_public': True
    }
]

MOCK_FILES = {
    'awesome-project': {
        'README.md': {
            'type': 'file',
            'content': '''# Awesome Project

This is an amazing open-source project!

## Features

- Easy to use
- Well documented
- Active community
- Regular updates

## Installation

```bash
pip install awesome-project
```

## Usage

```python
import awesome

awesome.run()
```
''',
            'language': 'markdown',
            'size': 1234
        },
        'main.py': {
            'type': 'file',
            'content': '''def hello_world():
    print("Hello, GitHub Clone!")

def main():
    hello_world()
    return 0

if __name__ == "__main__":
    main()
''',
            'language': 'python',
            'size': 156
        },
        'config.json': {
            'type': 'file',
            'content': '''{
  "name": "awesome-project",
  "version": "1.0.0",
  "author": "developer",
  "license": "MIT"
}
''',
            'language': 'json',
            'size': 98
        }
    }
}

USERS = {
    'developer': {
        'name': 'Developer',
        'bio': 'Full-stack developer and open-source enthusiast',
        'location': 'Ukraine',
        'repos': 12,
        'followers': 234,
        'following': 89
    },
    'datascience': {
        'name': 'Data Scientist',
        'bio': 'Machine learning researcher',
        'location': 'Kyiv',
        'repos': 8,
        'followers': 567,
        'following': 123
    }
}

@app.route('/')
def index():
    return render_template('index.html', repos=MOCK_REPOS)

@app.route('/<owner>/<repo>')
def repository(owner, repo):
    repo_data = next((r for r in MOCK_REPOS if r['name'] == repo and r['owner'] == owner), None)
    if not repo_data:
        abort(404)
    
    files = MOCK_FILES.get(repo, {
        'README.md': {
            'type': 'file',
            'content': f'# {repo}\n\nThis is {owner}/{repo} repository.',
            'language': 'markdown',
            'size': 100
        }
    })
    
    return render_template('repository.html', repo=repo_data, files=files, owner=owner)

@app.route('/<owner>/<repo>/blob/<path:filepath>')
def file_view(owner, repo, filepath):
    repo_data = next((r for r in MOCK_REPOS if r['name'] == repo and r['owner'] == owner), None)
    if not repo_data:
        abort(404)
    
    files = MOCK_FILES.get(repo, {})
    file_data = files.get(filepath)
    
    if not file_data or file_data['type'] != 'file':
        abort(404)
    
    content = file_data['content']
    language = file_data.get('language', 'text')
    
    try:
        if language == 'text':
            lexer = guess_lexer(content)
        else:
            lexer = get_lexer_by_name(language)
        formatter = HtmlFormatter(style='github-dark', linenos=True, cssclass='highlight')
        highlighted_code = highlight(content, lexer, formatter)
        css = formatter.get_style_defs('.highlight')
    except ClassNotFound:
        highlighted_code = f'<pre>{content}</pre>'
        css = ''
    
    return render_template('file.html', 
                         repo=repo_data, 
                         owner=owner,
                         filepath=filepath,
                         code=highlighted_code,
                         css=css,
                         lines=len(content.split('\n')),
                         size=file_data['size'])

@app.route('/<username>')
def profile(username):
    user = USERS.get(username)
    if not user:
        abort(404)
    
    user_repos = [r for r in MOCK_REPOS if r['owner'] == username]
    
    return render_template('profile.html', user=user, username=username, repos=user_repos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
