from pydantic import BaseModel, ConfigDict


class Tag(BaseModel):

    id: int
    tag_name: str
    tag_color: str

    model_config = ConfigDict(from_attributes=True)


class CreateTag(BaseModel):

    tag_name: str
    tag_color: str