from pydantic import BaseModel, Field

class CheckSpoilerRequest(BaseModel):
    # extra field forbid
    model_config = {"extra": "forbid"}

    video_id: str = Field(
        pattern=r"^[a-zA-Z0-9_-]{11}$",
        description="Video ID, it must be 11 characters long",
    )
    title: str = Field(
        min_length=1,
        description="Video title, it must not be empty",
    )
