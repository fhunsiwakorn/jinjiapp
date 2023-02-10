from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel


class InstitutionRequestInSchema(BaseModel):
    institution_name: Optional[str] = None
    active: Optional[int] = None

    class Config:
        orm_mode = True


class InstitutionRequestOutSchema(BaseModel):
    institution_id: Optional[int] = None
    institution_name: Optional[str] = None
    active: Optional[int] = None
    create_date: Optional[datetime] = None
    udp_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class InstitutionOutOptionSchema(BaseModel):
    status: str
    status_code: str
    message: str
    page: int
    per_page: int
    total_page: int
    total_data: int
    total_filter_data: int
    data: List[InstitutionRequestOutSchema]


class SkillRequestInSchema(BaseModel):
    skill_name: Optional[str] = None
    description: Optional[str] = None
    skill_group_type: Optional[str] = None
    active: Optional[int] = None

    class Config:
        orm_mode = True


class SkillRequestOutSchema(BaseModel):
    skill_id: Optional[int] = None
    skill_name: Optional[str] = None
    description: Optional[str] = None
    skill_group_type: Optional[int] = None
    active: Optional[int] = None
    create_date: Optional[datetime] = None
    udp_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class SkillFullRequestOutSchema(BaseModel):
    main_skill_id: Optional[int] = None
    main_skill_name: Optional[str] = None
    subskills: List[SkillRequestOutSchema]

    class Config:
        orm_mode = True


class WorkParentRequestInSchema(BaseModel):
    wp_name: Optional[str] = None
    active: Optional[int] = None

    class Config:
        orm_mode = True


class WorkParentRequestOutSchema(BaseModel):
    wp_id: Optional[int] = None
    wp_name: Optional[str] = None
    active: Optional[int] = None
    create_date: Optional[datetime] = None
    udp_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class WorkChildRequestInSchema(BaseModel):
    wc_name: Optional[str] = None
    active: Optional[int] = None
    wp_id: Optional[int] = None

    class Config:
        orm_mode = True


class WorkChildRequestOutSchema(BaseModel):
    wc_id: Optional[int] = None
    wc_name: Optional[str] = None
    active: Optional[int] = None
    create_date: Optional[datetime] = None
    udp_date: Optional[datetime] = None
    wp_id: Optional[int] = None

    class Config:
        orm_mode = True


class WorkFullOptionRequestOutSchema(BaseModel):
    wp_id: Optional[int] = None
    wp_name: Optional[str] = None
    active: Optional[int] = None
    create_date: Optional[datetime] = None
    udp_date: Optional[datetime] = None
    wp_wc: List[WorkChildRequestOutSchema]

    class Config:
        orm_mode = True


class BusinessTypeRequestInSchema(BaseModel):
    bt_name: Optional[str] = None
    active: Optional[int] = None

    class Config:
        orm_mode = True


class BusinessTypeRequestOutSchema(BaseModel):
    bt_id: Optional[int] = None
    bt_name: Optional[str] = None
    active: Optional[int] = None
    create_date: Optional[datetime] = None
    udp_date: Optional[datetime] = None

    class Config:
        orm_mode = True
