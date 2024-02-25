import datetime
from typing import Optional, TypeVar, Generic

from pydantic import BaseModel, ConfigDict, Field

ID_BOOK = TypeVar('ID_BOOK')
ID_STUDENT = TypeVar('ID_STUDENT')


class ErrorMessageDetails(BaseModel, Generic[ID_BOOK, ID_STUDENT]):
    student_id: ID_STUDENT
    book_id: ID_BOOK


ErrorDataT = TypeVar('ErrorDataT', bound=ErrorMessageDetails)


class ErrorMessageSchema(BaseModel, Generic[ErrorDataT]):
    message: str
    details: Optional[ErrorDataT] = None


class BookSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(gt=0)
    name: str = Field(serialization_alias='title')
    count: int = Field(gt=0)
    release_date: datetime.datetime
    author_id: int = Field(gt=0)


class TitleSchema(BaseModel):
    title: str = Field(min_length=1)


class CollectionBooksSchema(BaseModel):
    books: list[BookSchema]


class StudentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(gt=0)
    name: str = Field(min_length=1)
    surname: str = Field(min_length=1)
    phone: str = Field(min_length=2)
    email: str = Field(pattern=r'\b\w+@\w+\.\w+\b')
    average_score: float
    scholarship: bool


class CollectionStudentsSchema(BaseModel):
    students: list[StudentSchema]


class ReceivingBooksSchema(BaseModel):
    id: int
    book_id: int = Field(gt=0)
    student_id: int = Field(gt=0)
    date_of_issue: datetime.datetime
    date_of_return: Optional[datetime.datetime]


class ReceivingBooksInputValidate(BaseModel):
    book_id: int = Field(gt=0)
    student_id: int = Field(gt=0)
