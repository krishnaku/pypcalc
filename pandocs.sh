#!/bin/bash

# Configuration
SOURCE_DIR="pcalc/docs"               # Directory containing markdown files
OUTPUT_DIR="docs/pandoc"        # Directory to place rendered HTML
MATH_ENGINE="--mathjax"         # Use MathJax for LaTeX math support

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Process all .md files in the source directory
for file in "$SOURCE_DIR"/*.md; do
  if [ -f "$file" ]; then
    filename=$(basename "$file" .md)
    pandoc --number-sections --toc --wrap=auto "$file" -s -o "$OUTPUT_DIR/${filename}.html" --template="${SOURCE_DIR}/pandoc_template.html" $MATH_ENGINE
    echo "✓ Converted $file → $OUTPUT_DIR/${filename}.html"
  fi
done

echo "✅ All Markdown files in '$SOURCE_DIR' converted to HTML in '$OUTPUT_DIR'."
