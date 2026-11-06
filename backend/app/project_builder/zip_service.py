
import zipfile
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECTS_DIR = BACKEND_DIR / "generated_projects"


def create_project_zip(project_name: str) -> dict:
    """Create a ZIP file for an existing generated project."""

    if not project_name or Path(project_name).name != project_name:
        raise ValueError("Invalid project name.")

    project_path = (PROJECTS_DIR / project_name).resolve()

    if not project_path.is_relative_to(PROJECTS_DIR.resolve()):
        raise ValueError("Invalid project directory.")

    if not project_path.exists() or not project_path.is_dir():
        raise FileNotFoundError("Project does not exist.")

    zip_path = PROJECTS_DIR / f"{project_name}.zip"

    files = [
        path for path in project_path.rglob("*")
        if path.is_file()
    ]

    if not files:
        raise ValueError("Project contains no files.")

    with zipfile.ZipFile(
        zip_path,
        "w",
        compression=zipfile.ZIP_DEFLATED
    ) as zip_file:

        for file_path in files:
            relative_path = file_path.relative_to(project_path)
            zip_file.write(file_path, relative_path)

    return {
        "success": True,
        "project_name": project_name,
        "zip_path": str(zip_path),
        "zip_size_bytes": zip_path.stat().st_size
    }
