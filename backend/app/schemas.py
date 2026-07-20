from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator, ConfigDict

from app.models import Priority


class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    priority: Priority = Priority.MEDIUM
    due_date: date | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        title = value.strip()

        if not title:
            raise ValueError("任务标题不能为空")

        return title

class TodoUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    completed: bool | None = None
    priority: Priority | None = None
    due_date: date | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        if value is None:
            return None

        title = value.strip()

        if not title:
            raise ValueError("任务标题不能为空")

        return title

class TodoRead(BaseModel):
    id: str
    title: str
    completed: bool
    priority: Priority
    due_date: date | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)