
import re
import shutil
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECTS_DIR = BACKEND_DIR / "generated_projects"


def create_project_files(project_data: dict) -> dict:
    """Safely create generated project files."""

    if not isinstance(project_data, dict):
        raise ValueError("Invalid project data.")

    project_name = project_data.get("project_name", "my-project")
    files = project_data.get("files", [])

    project_name = re.sub(
        r"[^a-zA-Z0-9_-]",
        "-",
        str(project_name).strip().lower()
    ).strip("-")

    if not project_name:
        raise ValueError("Invalid project name.")

    if not isinstance(files, list) or not files:
        raise ValueError("No project files provided.")

    if len(files) > 50:
        raise ValueError("Too many project files.")

    # Validate all files before creating anything.
    validated_files = []
    seen_paths = set()
    total_size = 0

    for index, file_info in enumerate(files):

        if not isinstance(file_info, dict):
            raise ValueError(
                f"File number {index + 1} is not a valid JSON object."
            )

        relative_path = file_info.get("path")
        content = file_info.get("content")

        if not isinstance(relative_path, str) or not relative_path.strip():
            raise ValueError(
                f"File number {index + 1} has an invalid path."
            )

        if not isinstance(content, str):
            raise ValueError(
                f"File number {index + 1} has invalid content."
            )

        relative_path = relative_path.replace("\\", "/").strip()
        file_path = Path(relative_path)

        if (
            file_path.is_absolute()
            or ".." in file_path.parts
            or ":" in relative_path
            or relative_path.startswith("/")
            or not file_path.parts
        ):
            raise ValueError("Unsafe file path detected.")

        normalized_path = file_path.as_posix().lower()

        if normalized_path in seen_paths:
            raise ValueError("Duplicate file path detected.")

        seen_paths.add(normalized_path)

        content_size = len(content.encode("utf-8"))
        total_size += content_size

        if content_size > 500_000:
            raise ValueError("Individual file is too large.")

        if total_size > 5_000_000:
            raise ValueError("Generated project is too large.")

        validated_files.append((file_path, content))

    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

    project_path = PROJECTS_DIR / project_name

    if project_path.exists():
        raise FileExistsError(
            f"Project already exists: {project_name}"
        )

    project_path.mkdir(parents=True)

    try:
        for file_path, content in validated_files:

            target_path = (project_path / file_path).resolve()

            if not target_path.is_relative_to(project_path.resolve()):
                raise ValueError("File path is outside project directory.")

            target_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            target_path.write_text(
                content,
                encoding="utf-8"
            )

        return {
            "success": True,
            "project_name": project_name,
            "project_path": str(project_path),
            "files_created": len(validated_files)
        }

    except Exception:
        shutil.rmtree(project_path, ignore_errors=True)
        raise
