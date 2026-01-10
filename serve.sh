#!/bin/bash
# Simple server to run the Resume PDF Editor
# Usage: ./serve.sh [port]

PORT=${1:-8080}

echo "=========================================="
echo "  Resume PDF Editor"
echo "=========================================="
echo ""
echo "Starting server at http://localhost:$PORT"
echo "Open http://localhost:$PORT/editor.html in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Try Python 3 first, then Python 2
if command -v python3 &> /dev/null; then
    python3 -m http.server $PORT
elif command -v python &> /dev/null; then
    python -m SimpleHTTPServer $PORT
else
    echo "Error: Python is required to run the server"
    exit 1
fi
