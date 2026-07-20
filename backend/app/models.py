import uuid

from sqlalchemy import Column, String, Boolean, DateTime, Date, Enum as SqlEnum, func, text

from enum import Enum

from app.database import Base

class Priority(str, Enum):
    LOW='low'
    MEDIUM='medium'
    HIGH='high'

class Todo(Base):
    __tablename__="todos"

    id = Column(
        String(36),
        primary_key=True,
        default=uuid.uuid4,
    )

    title = Column(
        String(255),
        nullable=False,
    )

    completed = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text('0'),
        index=True,
    )

    priority = Column(
        SqlEnum(
            Priority,
            name='priority',
            values_callable=lambda priority_enum: [
                item.value for item in priority_enum
            ]
        ),
        nullable=False,
        default=Priority.MEDIUM,
        server_default=text('medium'),
        index=True,
    )

    due_date = Column(
        Date,
        nullable=True,
        index=True,
    )

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    def __repr__(self):
        return f"<Todo(id={self.id}, title='{self.title}', completed={self.completed})>"