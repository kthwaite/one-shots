# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "typer",
#     "rich",
# ]
# ///

"""
Extract JSON mistakenly written into a Markdown file and format it back to markdown.

This tool extracts JSON content from a Markdown file, processes the 'text' array,
and converts it back to properly formatted Markdown with chapter headings.
"""

import json
import re
from pathlib import Path
from typing import Any

import typer
from rich.console import Console

app = typer.Typer(help="Extract JSON from Markdown and format as Markdown")
console = Console()


def extract_json_from_markdown(content: str) -> dict[str, Any] | None:
    """
    Extract JSON content from a Markdown file using regex.

    Args:
        content: String content of the Markdown file

    Returns:
        Parsed JSON object or None if no JSON is found
    """
    # Look for JSON-like content (anything between curly braces)
    json_match = re.search(r"\{.*\}", content, re.DOTALL)

    if not json_match:
        return None

    json_str = json_match.group(0)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        console.print("[bold red]Error:[/] Failed to parse JSON content from the file")
        return None


def convert_to_markdown(json_data: dict[str, Any]) -> str:
    """
    Convert JSON data to Markdown format.

    Args:
        json_data: Parsed JSON data

    Returns:
        Formatted Markdown string
    """
    if "text" not in json_data:
        console.print("[bold yellow]Warning:[/] No 'text' key found in JSON")
        return ""

    markdown_content = []

    for i, section in enumerate(json_data["text"], 1):
        if not isinstance(section, dict) or "text" not in section:
            console.print(
                f"[bold yellow]Warning:[/] Section {i} is missing 'text' key, skipping"
            )
            continue

        paragraphs = section["text"]
        if not isinstance(paragraphs, list):
            console.print(
                f"[bold yellow]Warning:[/] 'text' in section {i} is not an array, skipping"
            )
            continue

        # Add chapter heading
        markdown_content.append(f"# Chapter {i}")
        markdown_content.append("")  # Empty line after heading

        # Add paragraphs with double newlines between them
        markdown_content.append("\n\n".join(paragraphs))

    return "\n\n".join(markdown_content)


@app.command()
def extract(
    input_file: Path = typer.Argument(
        ...,
        help="Input Markdown file containing JSON",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    output_file: Path = typer.Option(
        None, "--output", "-o", help="Output Markdown file (default: stdout)"
    ),
    overwrite: bool = typer.Option(
        False,
        "--overwrite",
        "-w",
        help="Overwrite the input file with the extracted Markdown",
    ),
    pretty: bool = typer.Option(
        False,
        "--pretty",
        "-p",
        help="Pretty print the JSON before processing (for debugging)",
    ),
) -> None:
    """
    Extract JSON from a Markdown file and format it back as proper Markdown.
    """
    try:
        content = input_file.read_text(encoding="utf-8")
    except Exception as e:
        console.print(f"[bold red]Error:[/] Failed to read file: {e}")
        raise typer.Exit(1)

    # Extract JSON content
    json_data = extract_json_from_markdown(content)
    if not json_data:
        console.print("[bold red]Error:[/] No valid JSON found in the input file")
        raise typer.Exit(1)

    # Debug: Print the extracted JSON
    if pretty:
        console.print("[bold blue]Extracted JSON:[/]")
        console.print_json(json.dumps(json_data))

    # Convert to Markdown
    markdown_content = convert_to_markdown(json_data)

    # Output the result
    if overwrite:
        if output_file:
            console.print(
                "[bold yellow]Warning:[/] Both --output and --overwrite specified; using --overwrite"
            )
        try:
            input_file.write_text(markdown_content, encoding="utf-8")
            console.print(
                f"[bold green]Success:[/] Markdown written back to {input_file}"
            )
        except Exception as e:
            console.print(f"[bold red]Error:[/] Failed to overwrite input file: {e}")
            raise typer.Exit(1)
    elif output_file:
        try:
            output_file.write_text(markdown_content, encoding="utf-8")
            console.print(f"[bold green]Success:[/] Markdown written to {output_file}")
        except Exception as e:
            console.print(f"[bold red]Error:[/] Failed to write output file: {e}")
            raise typer.Exit(1)
    else:
        # Print to stdout
        print(markdown_content)


if __name__ == "__main__":
    app()
