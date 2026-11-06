
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.project_builder.project_builder_service import generate_project
from app.project_builder.file_manager import create_project_files
from app.project_builder.zip_service import create_project_zip


router = APIRouter(
    prefix="/api/project-builder",
    tags=["Project Builder"]
)


class ProjectRequest(BaseModel):
    project_idea: str = Field(
        ...,
        min_length=10,
        max_length=2000
    )


@router.post("/generate")
def generate_project_api(request: ProjectRequest):

    try:
        # Step 1: Generate project using AI
        project_data = generate_project(request.project_idea)

        # Step 2: Create project files
        file_result = create_project_files(project_data)

        # Step 3: Create ZIP file
        zip_result = create_project_zip(
            file_result["project_name"]
        )

        # Step 4: Prepare generated code for frontend
        generated_files = [
            {
                "path": file_info["path"],
                "content": file_info["content"]
            }
            for file_info in project_data["files"]
        ]

        return {
            "success": True,
            "message": "Project generated successfully.",
            "project_name": file_result["project_name"],
            "description": project_data.get("description", ""),
            "files_created": file_result["files_created"],
            "files": generated_files,
            "download_url": (
                f"/api/project-builder/download/"
                f"{file_result['project_name']}"
            )
        }

    except FileExistsError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Project generation failed. Please try again."
        )


@router.get("/download/{project_name}")
def download_project(project_name: str):

    try:
        zip_result = create_project_zip(project_name)
        zip_path = zip_result["zip_path"]

        return FileResponse(
            path=zip_path,
            media_type="application/zip",
            filename=f"{project_name}.zip"
        )

    except (ValueError, FileNotFoundError):
        raise HTTPException(
            status_code=404,
            detail="Project ZIP file not found."
        )
