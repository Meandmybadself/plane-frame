#!/bin/bash

echo "Watching for changes in Python files..."
echo "Press Ctrl+C to stop"

run_planeframe() {
    echo "Change detected in: $1"
    python3 $HOME/Sites/planeframe/test_image_generation.py
}

fswatch -0 -e ".*" -i "\.py$" $HOME/Sites/planeframe/ | while read -d "" file; do
    run_planeframe "$file"
done 