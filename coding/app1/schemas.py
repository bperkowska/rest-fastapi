"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, Field, ConfigDict


class TaskBase(BaseModel):
    """Base Task schema with shared fields."""
    name: str = Field(min_length=3, max_length=100, description="Nazwa zadania")


class TaskCreate(TaskBase):
    """Schema for creating a task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    name: str = Field(min_length=1, max_length=100, description="Nazwa zadania")


class TaskResponse(TaskBase):
    """Schema for task response."""
    id: int

    model_config = ConfigDict(from_attributes=True)