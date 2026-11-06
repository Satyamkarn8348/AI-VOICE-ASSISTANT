
import subprocess
from pathlib import Path
from html.parser import HTMLParser


class HTMLFileParser(HTMLParser):
    """Extract CSS and JavaScript file references from HTML."""

    def __init__(self):
        super().__init__()
        self.referenced_files = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)

        if tag == "script" and attributes.get("src"):
            self.referenced_files.append(attributes["src"])

        if tag == "link" and attributes.get("href"):
            href = attributes["href"]

            if href.endswith(".css"):
                self.referenced_files.append(href)


def validate_project(project_path: Path) -> dict:
    """Perform safe static validation of generated project files."""

    errors = []
    warnings = []

    if not project_path.exists() or not project_path.is_dir():
        raise ValueError("Project directory does not exist.")

    # Check HTML file references.
    for html_file in project_path.rglob("*.html"):

        parser = HTMLFileParser()

        try:
            parser.feed(
                html_file.read_text(encoding="utf-8")
            )
        except Exception as error:
            errors.append(
                f"HTML parsing failed: {html_file.name}: {error}"
            )
            continue

        for reference in parser.referenced_files:

            if "://" in reference or reference.startswith("//"):
                continue

            if reference.startswith(("data:", "#")):
                continue

            referenced_path = (
                html_file.parent / reference.split("?")[0].split("#")[0]
            ).resolve()

            if not referenced_path.is_relative_to(project_path.resolve()):
                errors.append(
                    f"Unsafe file reference in {html_file.name}"
                )
                continue

            if not referenced_path.is_file():
                errors.append(
                    f"Missing file referenced in {html_file.name}: {reference}"
                )

    # Check JavaScript syntax without executing the code.
    for js_file in project_path.rglob("*.js"):

        try:
            result = subprocess.run(
                ["node", "--check", str(js_file)],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=str(project_path)
            )

            if result.returncode != 0:
                errors.append(
                    f"JavaScript syntax error in {js_file.name}: "
                    f"{result.stderr.strip()}"
                )

        except FileNotFoundError:
            warnings.append(
                "Node.js is not available. JavaScript syntax was not checked."
            )
            break

        except subprocess.TimeoutExpired:
            errors.append(
                f"JavaScript validation timed out: {js_file.name}"
            )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }
