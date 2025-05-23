from fastapi import FastAPI, Response, status, Query
from fastapi.middleware.cors import CORSMiddleware
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

## Default route
@app.get("/")
async def root():
    return {"message": "FastAPI is running on Render!"}

# Mô hình dữ liệu
class Overall(BaseModel):
    user_count: int
    course_count: int
    teacher_count: int
    field_count: int
    school_count: int
@app.get("/api/overall", response_model=List[Overall])
async def get_overall():
    overall_df = pl.read_parquet(os.path.join(main_path, "data/overall.parquet"))
    overall = (
        overall_df.rename({"user_count":"user_count", "course_count":"course_count", "school_count":"school_count", "teacher_count":"teacher_count", "field_count":"field_count" })
            .to_dicts()
    )

    return Response(
        content=json.dumps({"data": overall}, ensure_ascii=False),
        media_type="application/json; charset=utf-8",
        status_code=status.HTTP_200_OK
    )

## Mô hình dữ liệu
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
async def get_fields():
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
async def get_teachers():
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

# API để lấy top 10 khoá học
class CourseUser(BaseModel):
    id: str
    user_count: int
@app.get("/api/student_count_on_course", response_model=List[CourseUser])
async def get_course_user():
    course_user_df = pl.read_parquet(os.path.join(main_path, "data/course_user_count.parquet"))
    course_user = (
        course_user_df.rename({"course_id": "id", "user_count": "user_count"})
            .to_dicts()
    )

    return Response(
        content=json.dumps({"data": course_user}, ensure_ascii=False),
        media_type="application/json; charset=utf-8",
        status_code=status.HTTP_200_OK
    )

# API để lấy top 10 lĩnh vực có nhiều ngừoi học nhất
class FieldUser(BaseModel):
    name: str
    user_count: int
@app.get("/api/student_count_on_field", response_model=List[FieldUser])
async def get_field_user():
    field_user_df = pl.read_parquet(os.path.join(main_path, "data/field_user_count.parquet"))
    field_user = (
        field_user_df.rename({"course_field": "name", "user_count": "user_count"})
            .to_dicts()
    )

    return Response(
        content=json.dumps({"data": field_user}, ensure_ascii=False),
        media_type="application/json; charset=utf-8",
        status_code=status.HTTP_200_OK
    )

# API để lấy user
@app.get("/api/get_student_by_name", response_model=List[Student])
async def get_user_by_name(query: str = Query(..., min_length=1)):
    user_df = pl.read_parquet(os.path.join(main_path, "data/user_df.parquet"))

    filtered = (
        user_df
            .filter(pl.col("user_name").str.to_lowercase().str.contains(query.lower()))
            .rename({"user_id": "id", "user_name": "name"})
            .to_dicts()
        )
    
    return  Response(
        content=json.dumps({"data": filtered}, ensure_ascii=False),
        media_type="application/json; charset=utf-8",
        status_code=status.HTTP_200_OK
    )