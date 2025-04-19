# one-shots

### hex-to-oklch.html

This standalone HTML file implements a web-based tool that converts hexadecimal color codes into their corresponding OKLCH color format. It provides a user-friendly interface where users can:

- Enter a JSON object mapping color names to hex values.
- Convert the hex values to OKLCH using inline JavaScript functions.
- Preview the colors via dynamic swatches.
- Generate and copy the resulting CSS variables formatted with OKLCH values.


### css-perspective.html

This standalone file provides an interactive demo showcasing 3D card rotation effects based on cursor movement. It includes:

- Two card elements (one with standard sensitivity, one with enhanced sensitivity) that rotate in 3D as the user hovers over them.
- CSS styles defining the card appearance, transitions, box shadows, and the overall layout.
- JavaScript logic that calculates the cursor position relative to each card to dynamically adjust rotation and shadow effects.
- Slider controls that let users adjust parameters such as the perspective depth and rotation sensitivity for each card in real time.


### unpack.py

This Python script organizes files within a given directory based on their file extension and name pattern. Its main features include:

- Scanning the root directory (recursively) for files with a specified extension (or regex pattern).
- Retaining files whose names match a user-provided regular expression.
- Moving files that do not match the pattern to a designated "_other" subdirectory (with support for dry-run mode to preview changes).
- Handling case-insensitive file extensions while avoiding name conflicts during file moves.

### unjson.py

This Python utility extracts a JSON snippet embedded within a Markdown file, parses its "text" array into structured sections, and reformats the content back into Markdown with chapter headings. It supports options for pretty-printing, output redirection, and in-place file overwrites.
