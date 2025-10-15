# pyodide-pygame-demo

https://ryanking13.github.io/pyodide-pygame-demo

## Local Development

For local testing, you can use the URL replacement tool to switch between production and localhost URLs:

### Switch to localhost for testing:
```bash
python tools/replace_urls.py localhost
python -m http.server 8000
```

Then visit: http://localhost:8000/

### Switch back to production URLs:
```bash
python tools/replace_urls.py production
```

### Check current configuration:
```bash
python tools/replace_urls.py status
```
