from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
import pyarrow.parquet as pq
import polars as pl
from typing import Dict, List, Any
from pydantic import BaseModel
import json
import os


main_path = os.getcwd()

app = FastAPI(title="Education Analytics API")

# CORS để frontend truy cập API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Thay bằng domain frontend thật khi deploy
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mô hình dữ liệu
class Teacher(BaseModel):
    id: str

class Student(BaseModel):
    id: str
    name: str

class Course(BaseModel):
    id: str
    name: str

class Field(BaseModel):
    name: str



    
# API để lấy danh sách học sinh
@app.get("/api/students", response_model=List[Student])
async def get_students():
    user_df = pl.read_parquet(os.path.join(main_path, "data/user_df.parquet"))
    students = (
        user_df.rename({"user_id": "id", "user_name": "name"})
          .to_dicts()
    )
    
    return  Response(
        content=json.dumps({"data": students}, ensure_ascii=False),
        media_type="application/json; charset=utf-8",
        status_code=status.HTTP_200_OK
    )

# API để lấy danh sách môn học
@app.get("/api/courses", response_model=List[Course])
async def get_courses():
    course_df = pl.read_parquet(os.path.join(main_path, "data/course_df.parquet"))
    courses = (
        course_df.rename({"course_id": "id", "course_name": "name"})
            .to_dicts()
    )

    return Response(
        content=json.dumps({"data": courses}, ensure_ascii=False),
        media_type="application/json; charset=utf-8",
        status_code=status.HTTP_200_OK
    )

# API để lấy danh sách field
@app.get("/api/fields", response_model=List[Field])
async def get_courses():
    fields_df = pl.read_parquet(os.path.join(main_path, "data/field_df.parquet"))
    fields = (
        fields_df.rename({"field_name": "name"})
            .to_dicts()
    )

    return Response(
        content=json.dumps({"data": fields}, ensure_ascii=False),
        media_type="application/json; charset=utf-8",
        status_code=status.HTTP_200_OK
    )

# API để lấy danh sách giáo viên
@app.get("/api/teachers", response_model=List[Teacher])
async def get_courses():
    teacher_df = pl.read_parquet(os.path.join(main_path, "data/teacher_df.parquet"))
    teacher = (
        teacher_df.rename({"teacher_id": "id"})
            .to_dicts()
    )

    return Response(
        content=json.dumps({"data": teacher}, ensure_ascii=False),
        media_type="application/json; charset=utf-8",
        status_code=status.HTTP_200_OK
    )
