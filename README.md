# spaCy NER Visualizer

A simple web-based testing interface for spaCy Named Entity Recognition (NER), designed to run cleanly inside a GitHub Codespace (single-origin FastAPI setup).

## Getting Started

### 1. Install Dependencies
Install the required packages using pip:
```bash
pip install -r requirements.txt 
```

### 2. Download a spaCy Model
Download the default model before running the server:
```bash  
python -m spacy download en_core_web_sm
```
*(Optional: You can also download `en_core_web_md` or `en_core_web_lg` if you wish to compare different model sizes.)*

### 3. Run the Server
Launch the server via uvicorn: 
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Running in GitHub Codespaces

1. When you run the `uvicorn` command, GitHub Codespaces will automatically detect that port `8000` is active and forward it.
2. A popup notification will appear in the bottom-right corner of the editor. Click **Open in Browser** or go to the **Ports** tab in your terminal panel and click the local address globe icon.
3. Because the frontend and backend are served from the same FastAPI instance, relative fetch routes (`/extract-entities`) are used. This completely avoids cross-origin (CORS) issues when using Codespaces forwarded URLs.

## License

This project is licensed under the MIT License:

```text
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
