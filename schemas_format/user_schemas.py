from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from .masterdata_schemas import InstitutionRequestOutSchema, SkillRequestOutSchema, WorkChildRequestOutSchema, BusinessTypeRequestOutSchema
# User


class UserRequestInSchema(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    user_image_prifile: Optional[str] = None
    user_image_cover: Optional[str] = None
    user_image_cover_position: Optional[str] = None
    user_type: Optional[int] = None
    active: Optional[int] = None

    class Config:
        orm_mode = True


class UserDetailRequestInSchema(BaseModel):
    ud_bio: Optional[str] = None
    ud_birhday: Optional[date] = None
    ud_gender: Optional[int] = 0
    ud_phone: Optional[str] = None
    ud_address: Optional[str] = None
    tambon_id: Optional[int] = None
    country_id: Optional[int] = None

    class Config:
        orm_mode = True


class UserDetailRequestOutSchema(BaseModel):
    ud_id: Optional[int] = None
    ud_bio: Optional[str] = None
    ud_birhday: Optional[date] = None
    ud_gender: Optional[int] = 0
    ud_phone: Optional[str] = None
    ud_address: Optional[str] = None
    ud_code: Optional[str] = None
    tambon_id: Optional[int] = None
    country_id: Optional[int] = None
    user_id: Optional[str] = None
    user_tambon: object
    user_country: object

    class Config:
        orm_mode = True


class UserCompanyRequestInSchema(BaseModel):
    uc_company_name: Optional[str] = None
    uc_company_website: Optional[str] = None
    uc_company_remark1: Optional[str] = None
    uc_company_remark2: Optional[str] = None
    uc_company_cover: Optional[str] = None
    bt_id: Optional[int] = None

    class Config:
        orm_mode = True


class UserCompanyRequestOutSchema(BaseModel):
    uc_company_name: Optional[str] = None
    uc_company_website: Optional[str] = None
    uc_company_remark1: Optional[str] = None
    uc_company_remark2: Optional[str] = None
    uc_company_cover: Optional[str] = None
    bt_id: Optional[int] = None
    company_business: BusinessTypeRequestOutSchema

    class Config:
        orm_mode = True


class UserRequestOutSchema(BaseModel):
    user_id: Optional[str] = None
    username: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    user_image_prifile: Optional[str] = None
    user_image_cover: Optional[str] = None
    user_image_cover_position: Optional[str] = None
    user_type: Optional[int] = None
    active: Optional[int] = None
    create_date: Optional[datetime] = None
    update_date: Optional[datetime] = None
    user_main_detail: List[UserDetailRequestOutSchema]
    user_main_company: List[UserCompanyRequestOutSchema]

    class Config:
        orm_mode = True


class UserRequestOutOptionSchema(BaseModel):
    status: str
    status_code: str
    message: str
    page: int
    per_page: int
    total_page: int
    total_data: int
    total_filter_data: int
    data: List[UserRequestOutSchema]


class UserLoginSchema(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

    class Config:
        orm_mode = True


class UserLoginOutSchema(BaseModel):
    user_id: Optional[str] = None
    username: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    user_image_prifile: Optional[str] = None
    user_image_cover: Optional[str] = None
    user_image_cover_position: Optional[str] = None
    user_type: Optional[int] = None

    class Config:
        orm_mode = True


class UserCompanyRegisterRequestInSchema(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    active: Optional[int] = None
    detail: UserDetailRequestInSchema
    company: UserCompanyRequestInSchema

    class Config:
        orm_mode = True


class UserCandidateRegisterRequestInSchema(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    active: Optional[int] = None
    detail: UserDetailRequestInSchema

    class Config:
        orm_mode = True


class UserSalaryRequestInSchema(BaseModel):
    us_salary_start: Optional[int] = None
    us_salary_end: Optional[int] = None

    class Config:
        orm_mode = True


class UserHireTypeRequestInSchema(BaseModel):
    uh_type: Optional[int] = None

    class Config:
        orm_mode = True


class UserWorkTypeRequestInSchema(BaseModel):
    wc_id: Optional[int] = None

    class Config:
        orm_mode = True


class UserWorkTypeRequestOutSchema(BaseModel):
    wc_id: Optional[int] = None
    user_work_child: WorkChildRequestOutSchema

    class Config:
        orm_mode = True


class ExperienceRequestInSchema(BaseModel):
    exp_comapany: Optional[str] = None
    exp_year_start: Optional[int] = None
    exp_year_end: Optional[int] = None
    exp_last_position: Optional[str] = None
    exp_last_salary: Optional[str] = None
    exp_responsibility: Optional[str] = None
    active: Optional[int] = None
    user_id: Optional[str] = None

    class Config:
        orm_mode = True


class ExperienceRequestOutSchema(BaseModel):
    exp_id: Optional[int] = None
    exp_comapany: Optional[str] = None
    exp_year_start: Optional[int] = None
    exp_year_end: Optional[int] = None
    exp_last_position: Optional[str] = None
    exp_last_salary: Optional[float] = None
    exp_responsibility: Optional[str] = None
    active: Optional[int] = None
    create_date: Optional[datetime] = None
    udp_date: Optional[datetime] = None
    user_id: Optional[str] = None

    class Config:
        orm_mode = True


class EducationRequestInSchema(BaseModel):
    edu_degree: Optional[int] = None
    edu_faculty: Optional[str] = None
    edu_major: Optional[str] = None
    edu_graduation_year: Optional[int] = None
    edu_gpa: Optional[float] = None
    active: Optional[int] = None
    institution_id: Optional[int] = None
    user_id: Optional[str] = None

    class Config:
        orm_mode = True


class EducationRequestOutSchema(BaseModel):
    edu_id: Optional[int] = None
    edu_degree: Optional[int] = None
    edu_faculty: Optional[str] = None
    edu_major: Optional[str] = None
    edu_graduation_year: Optional[int] = None
    edu_gpa: Optional[float] = None
    active: Optional[int] = None
    create_date: Optional[datetime] = None
    udp_date: Optional[datetime] = None
    institution_id: Optional[int] = None
    user_id: Optional[str] = None
    edu_institution: InstitutionRequestOutSchema

    class Config:
        orm_mode = True


class EducationRequestInSchema(BaseModel):
    edu_degree: Optional[int] = None
    edu_faculty: Optional[str] = None
    edu_major: Optional[str] = None
    edu_graduation_year: Optional[int] = None
    edu_gpa: Optional[float] = None
    active: Optional[int] = None
    institution_id: Optional[int] = None
    user_id: Optional[str] = None

    class Config:
        orm_mode = True


class StrengthRequestInSchema(BaseModel):
    strength_name: Optional[str] = None
    user_id: Optional[str] = None

    class Config:
        orm_mode = True


class StrengthRequestOutSchema(BaseModel):
    strength_id: Optional[int] = None
    strength_name: Optional[str] = None
    create_date: Optional[datetime] = None
    udp_date: Optional[datetime] = None
    user_id: Optional[str] = None

    class Config:
        orm_mode = True


class HobbiesRequestInSchema(BaseModel):
    hobby_name: Optional[str] = None
    user_id: Optional[str] = None

    class Config:
        orm_mode = True


class HobbiesRequestOutSchema(BaseModel):
    hobby_id: Optional[int] = None
    hobby_name: Optional[str] = None
    create_date: Optional[datetime] = None
    udp_date: Optional[datetime] = None
    user_id: Optional[str] = None

    class Config:
        orm_mode = True


class RewardsRequestInSchema(BaseModel):
    reward_name: Optional[str] = None
    reward_file_path: Optional[str] = None
    user_id: Optional[str] = None

    class Config:
        orm_mode = True


class RewardsRequestOutSchema(BaseModel):
    reward_id: Optional[int] = None
    reward_name: Optional[str] = None
    reward_file_path: Optional[str] = None
    create_date: Optional[datetime] = None
    udp_date: Optional[datetime] = None
    user_id: Optional[str] = None

    class Config:
        orm_mode = True


class LanguagRequestInSchema(BaseModel):
    language_code: Optional[str] = None
    language_overall: Optional[str] = None
    language_type: Optional[str] = None
    language_score: Optional[str] = None
    user_id: Optional[str] = None

    class Config:
        orm_mode = True


class LanguagRequestOutSchema(BaseModel):
    language_id: Optional[int] = None
    language_code: Optional[str] = None
    language_overall: Optional[str] = None
    language_type: Optional[str] = None
    language_score: Optional[str] = None
    create_date: Optional[datetime] = None
    udp_date: Optional[datetime] = None
    user_id: Optional[str] = None

    class Config:
        orm_mode = True


class SkillProfileRequestInSchema(BaseModel):
    skill_profile_detail: Optional[str] = None
    skill_id: Optional[int] = None
    user_id: Optional[str] = None

    class Config:
        orm_mode = True


class SkillProfileRequestOutSchema(BaseModel):
    skill_profile_id: Optional[int] = None
    skill_profile_detail: Optional[str] = None
    create_date: Optional[datetime] = None
    udp_date: Optional[datetime] = None
    skill_id: Optional[int] = None
    user_id: Optional[str] = None
    skill_profile_child: SkillRequestOutSchema

    class Config:
        orm_mode = True


class PortfolioRequestIntSchema(BaseModel):
    portfolio_name: Optional[str] = None
    portfolio_path: Optional[str] = None
    portfolio_type: Optional[int] = None
    active: Optional[int] = None

    class Config:
        orm_mode = True


class PortfolioRequestOutSchema(BaseModel):
    portfolio_id: Optional[int] = None
    portfolio_name: Optional[str] = None
    portfolio_path: Optional[str] = None
    portfolio_type: Optional[int] = None
    active: Optional[int] = None
    create_date: Optional[datetime] = None
    udp_date: Optional[datetime] = None
    user_id: Optional[str] = None

    class Config:
        orm_mode = True
