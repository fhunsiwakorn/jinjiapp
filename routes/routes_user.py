from fastapi import APIRouter, Depends, HTTPException
from passlib.hash import sha256_crypt
from sqlalchemy import desc, asc, or_
from sqlalchemy.orm import Session, joinedload

from authen import auth_request
from database import get_db
from function import ceil, ternaryZero, todaytime
from models import User, UserDetail, UserEducation, UserExperience, UserHobbies, UserLanguage, UserRewards, UserStrength, UserSkill
from schemas_format.general_schemas import FilterRequestSchema, ResponseProcess
from schemas_format.user_schemas import EducationRequestInSchema, EducationRequestOutSchema, ExperienceRequestInSchema, StrengthRequestInSchema, StrengthRequestOutSchema, ExperienceRequestOutSchema, LanguagRequestInSchema, LanguagRequestOutSchema, HobbiesRequestInSchema, HobbiesRequestOutSchema, RewardsRequestInSchema, RewardsRequestOutSchema, UserRequestInSchema, UserRequestOutSchema, UserRequestOutOptionSchema, UserLoginSchema, UserLoginOutSchema, UserDetailRequestInSchema
from schemas_format.user_schemas import SkillProfileRequestInSchema, SkillProfileRequestOutSchema
router_user = APIRouter()

# Main Method


@ router_user.post("/create")
def create_user(request: UserRequestInSchema, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _user = db.query(User).filter(
        User.username == request.username).one_or_none()
    if _user:
        raise HTTPException(status_code=404, detail="Username Error")
    password = request.password
    password_hash = sha256_crypt.encrypt(str(password))
    _user = User(
        username=request.username,
        password=password_hash,
        firstname=request.firstname,
        lastname=request.lastname,
        email=request.email,
        user_image_prifile=request.user_image_prifile,
        user_image_cover=request.user_image_cover,
        user_image_cover_position=request.user_image_cover_position,
        user_type=request.user_type,
        active=request.active,
        create_date=todaytime(),
        update_date=todaytime()
    )
    db.add(_user)
    db.commit()
    # db.refresh(_user)
    return ResponseProcess(status="Ok", status_code="200", message="Success created data")


@router_user.put("/{user_id}")
def update_user(user_id: str, request: UserRequestInSchema,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _user = db.query(User).filter(
        User.user_id == user_id).one_or_none()
    if not _user:
        raise HTTPException(status_code=404, detail="Data not found")
    password = request.password

    if(password == "" or password == None):
        password_hash = _user.password
    else:
        password_hash = sha256_crypt.encrypt(str(password))

    _user.username = request.username
    _user.password = password_hash
    _user.firstname = request.firstname
    _user.lastname = request.lastname
    _user.email = request.email
    _user.user_image_prifile = request.user_image_prifile
    _user.user_image_cover = request.user_image_cover
    _user.user_image_cover_position = request.user_image_cover_position
    _user.user_type = request.user_type
    _user.active = request.active
    _user.update_date = todaytime()

    db.commit()
    db.refresh(_user)
    return ResponseProcess(status="Ok", status_code="200", message="Success update data")


@router_user.post("/all")
def get_user(request: FilterRequestSchema, typeuser: str = "all", db: Session = Depends(get_db),  authenticated: bool = Depends(auth_request)):

    skip = ternaryZero(((request.page - 1) * request.per_page))
    limit = request.per_page
    search_value = request.search_value
    # Filter user type : all , 1,2,3

    if typeuser == "all":
        queryfilter = User.user_type > 0
    else:
        queryfilter = User.user_type == int(typeuser)
    if search_value:
        result = db.query(User).order_by(desc(User.create_date)).filter(or_(User.firstname.contains(
            search_value), User.lastname.contains(search_value), User.username.contains(search_value)), User.cancelled == 1, queryfilter).offset(skip).limit(limit).all()
    else:
        result = db.query(User).order_by(desc(User.create_date)).filter(User.cancelled == 1,
                                                                        queryfilter).offset(skip).limit(limit).all()

    total_data = db.query(User).filter(
        User.cancelled == 1, queryfilter).count()
    total_filter_data = len(result)
    total_page = ceil(total_data / request.per_page)
    return UserRequestOutOptionSchema(status="success", status_code="200", message="Success fetch all data", page=request.page, per_page=limit, total_page=total_page, total_data=total_data, total_filter_data=total_filter_data, data=result)


@router_user.get("/{user_id}", response_model=UserRequestOutSchema)
def get_by_user_id(user_id: str,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _user = db.query(User).filter(
        User.user_id == user_id, User.cancelled == 1, User.active == 1).first()
    if not _user:
        raise HTTPException(status_code=404, detail="Data not found")

    return _user


@router_user.put("/detail/{user_id}")
def update_user_detail(user_id: str, request: UserDetailRequestInSchema,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _user = db.query(UserDetail).filter(
        UserDetail.user_id == user_id).one_or_none()
    if not _user:
        _useradd = UserDetail(
            ud_bio=request.ud_bio,
            ud_birhday=request.ud_birhday,
            ud_phone=request.ud_phone,
            ud_gender=request.ud_gender,
            ud_address=request.ud_address,
            tambon_id=request.tambon_id,
            country_id=request.country_id,
            user_id=user_id
        )
        db.add(_useradd)
        db.commit()
    else:
        _user.ud_bio = request.ud_bio
        _user.ud_birhday = request.ud_birhday
        _user.ud_phone = request.ud_phone
        _user.ud_gender = request.ud_gender
        _user.ud_address = request.ud_address
        _user.tambon_id = request.tambon_id
        _user.country_id = request.country_id
        db.commit()
    return ResponseProcess(status="Ok", status_code="200", message="Success update data")


@router_user.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _user = db.query(User).filter(User.user_id == user_id).one_or_none()
    if not _user:
        raise HTTPException(status_code=404, detail="Data not found")
    # db.delete(_user)
    _user.cancelled = 0
    db.commit()
    return ResponseProcess(status="Ok", status_code="200", message="Success delete data")


@router_user.post("/login", response_model=UserLoginOutSchema)
def login(request: UserLoginSchema, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _user = db.query(User).filter(
        User.username == request.username, User.cancelled == 1).first()
    if not _user:
        raise HTTPException(status_code=404, detail="Data not found")
    password = request.password

    # password = sha256_crypt.encrypt("password")
    chk_result = sha256_crypt.verify(str(password),  _user.password)

    if chk_result == True:
        return _user
    else:
        raise HTTPException(status_code=404, detail="Data not found")

# Detail Method


@router_user.post("/experience/create")
def create_experience(request: ExperienceRequestInSchema, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    user_id = request.user_id
    _checktotal = db.query(UserExperience).filter(
        UserExperience.user_id == user_id).count()
    if _checktotal >= 3:
        raise HTTPException(status_code=404, detail="Data not found")

    _user = UserExperience(
        exp_comapany=request.exp_comapany,
        exp_year_start=request.exp_year_start,
        exp_year_end=request.exp_year_end,
        exp_last_position=request.exp_last_position,
        exp_last_salary=request.exp_last_salary,
        exp_responsibility=request.exp_responsibility,
        active=request.active,
        create_date=todaytime(),
        udp_date=todaytime(),
        user_id=user_id
    )
    db.add(_user)
    db.commit()
    return ResponseProcess(status="Ok", status_code="200", message="Success created data")


@router_user.get("/experience/{user_id}", response_model=list[ExperienceRequestOutSchema])
def get_experience(user_id: str,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _user = db.query(UserExperience).order_by(desc(UserExperience.exp_year_end)).filter(
        UserExperience.user_id == user_id).all()
    return _user


# @router_user.put("/experience/{exp_id}")
# def update_experience(exp_id: int, request: ExperienceRequestInSchema,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     _user = db.query(UserExperience).filter(
#         UserExperience.exp_id == exp_id).one_or_none()
#     if not _user:
#         raise HTTPException(status_code=404, detail="Data not found")
#     _user.exp_comapany = request.exp_comapany
#     _user.exp_year_start = request.exp_year_start
#     _user.exp_year_end = request.exp_year_end
#     _user.exp_last_position = request.exp_last_position
#     _user.exp_last_salary = request.exp_last_salary
#     _user.exp_responsibility = request.exp_responsibility
#     _user.active = request.active
#     _user.udp_date = todaytime()
#     _user.user_id = request.user_id
#     db.commit()
#     return ResponseProcess(status="Ok", status_code="200", message="Success update data")


# @router_user.delete("/experience/{exp_id}")
# def delete_experience(exp_id: int,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     _user = db.query(UserExperience).filter(
#         UserExperience.exp_id == exp_id).one_or_none()
#     if not _user:
#         raise HTTPException(status_code=404, detail="Data not found")
#     db.delete(_user)
#     db.commit()
#     return ResponseProcess(status="Ok", status_code="200", message="Success delete data")


# @router_user.post("/education/create")
# def create_education(request: EducationRequestInSchema, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     user_id = request.user_id
#     _checktotal = db.query(UserEducation).filter(
#         UserEducation.user_id == user_id).count()
#     if _checktotal >= 3:
#         raise HTTPException(status_code=404, detail="Data not found")
#     _user = UserEducation(
#         edu_degree=request.edu_degree,
#         edu_faculty=request.edu_faculty,
#         edu_major=request.edu_major,
#         edu_graduation_year=request.edu_graduation_year,
#         edu_gpa=request.edu_gpa,
#         active=request.active,
#         create_date=todaytime(),
#         udp_date=todaytime(),
#         institution_id=request.institution_id,
#         user_id=user_id
#     )
#     db.add(_user)
#     db.commit()
#     return ResponseProcess(status="Ok", status_code="200", message="Success created data")


# @router_user.get("/education/{user_id}", response_model=list[EducationRequestOutSchema])
# def get_education(user_id: str,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     _user = db.query(UserEducation).order_by(desc(UserEducation.edu_graduation_year)).filter(
#         UserEducation.user_id == user_id).all()
#     return _user


# @router_user.put("/education/{edu_id}")
# def update_education(edu_id: int, request: EducationRequestInSchema,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     _user = db.query(UserEducation).filter(
#         UserEducation.edu_id == edu_id).one_or_none()
#     if not _user:
#         raise HTTPException(status_code=404, detail="Data not found")
#     _user.edu_degree = request.edu_degree
#     _user.edu_faculty = request.edu_faculty
#     _user.edu_major = request.edu_major
#     _user.edu_graduation_year = request.edu_graduation_year
#     _user.edu_gpa = request.edu_gpa
#     _user.active = request.active
#     _user.udp_date = todaytime()
#     _user.institution_id = request.institution_id
#     _user.user_id = request.user_id
#     db.commit()
#     return ResponseProcess(status="Ok", status_code="200", message="Success update data")


# @router_user.delete("/education/{edu_id}")
# def delete_education(edu_id: int,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     _user = db.query(UserEducation).filter(
#         UserEducation.edu_id == edu_id).one_or_none()
#     if not _user:
#         raise HTTPException(status_code=404, detail="Data not found")
#     db.delete(_user)
#     db.commit()
#     return ResponseProcess(status="Ok", status_code="200", message="Success delete data")


# @router_user.post("/strength/create")
# def create_strength(request: StrengthRequestInSchema, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     _user = UserStrength(
#         strength_name=request.strength_name,
#         create_date=todaytime(),
#         udp_date=todaytime(),
#         user_id=request.user_id
#     )
#     db.add(_user)
#     db.commit()
#     return ResponseProcess(status="Ok", status_code="200", message="Success created data")


# @router_user.put("/strength/{strength_id}")
# def update_strength(strength_id: int, request: StrengthRequestInSchema,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     _user = db.query(UserStrength).filter(
#         UserStrength.strength_id == strength_id).one_or_none()
#     if not _user:
#         raise HTTPException(status_code=404, detail="Data not found")
#     _user.strength_name = request.strength_name
#     _user.user_id = request.user_id
#     db.commit()
#     return ResponseProcess(status="Ok", status_code="200", message="Success update data")


# @router_user.get("/strength/{user_id}", response_model=list[StrengthRequestOutSchema])
# def get_strength(user_id: str,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     _user = db.query(UserStrength).order_by(asc(UserStrength.strength_id)).filter(
#         UserStrength.user_id == user_id).all()
#     return _user


# @router_user.delete("/strength/{strength_id}")
# def delete_strength(strength_id: int,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     _user = db.query(UserStrength).filter(
#         UserStrength.strength_id == strength_id).one_or_none()
#     if not _user:
#         raise HTTPException(status_code=404, detail="Data not found")
#     db.delete(_user)
#     db.commit()
#     return ResponseProcess(status="Ok", status_code="200", message="Success delete data")


# @router_user.post("/hobbies/create")
# def create_hobbies(request: HobbiesRequestInSchema, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     _user = UserHobbies(
#         hobby_name=request.hobby_name,
#         create_date=todaytime(),
#         udp_date=todaytime(),
#         user_id=request.user_id
#     )
#     db.add(_user)
#     db.commit()
#     return ResponseProcess(status="Ok", status_code="200", message="Success created data")


# @router_user.put("/hobbies/{hobby_id}")
# def update_hobbies(hobby_id: int, request: HobbiesRequestInSchema,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     _user = db.query(UserHobbies).filter(
#         UserHobbies.hobby_id == hobby_id).one_or_none()
#     if not _user:
#         raise HTTPException(status_code=404, detail="Data not found")
#     _user.hobby_name = request.hobby_name
#     _user.user_id = request.user_id
#     db.commit()
#     return ResponseProcess(status="Ok", status_code="200", message="Success update data")


# @router_user.get("/hobbies/{user_id}", response_model=list[HobbiesRequestOutSchema])
# def get_hobbies(user_id: str,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     _user = db.query(UserHobbies).order_by(asc(UserHobbies.hobby_id)).filter(
#         UserHobbies.user_id == user_id).all()
#     return _user


# @router_user.delete("/hobbies/{hobby_id}")
# def delete_hobbies(hobby_id: int,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     _user = db.query(UserHobbies).filter(
#         UserHobbies.hobby_id == hobby_id).one_or_none()
#     if not _user:
#         raise HTTPException(status_code=404, detail="Data not found")
#     db.delete(_user)
#     db.commit()
#     return ResponseProcess(status="Ok", status_code="200", message="Success delete data")


# @router_user.post("/rewards/create")
# def create_reward(request: RewardsRequestInSchema, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     _user = UserRewards(
#         reward_name=request.reward_name,
#         reward_file_path=request.reward_file_path,
#         create_date=todaytime(),
#         udp_date=todaytime(),
#         user_id=request.user_id
#     )
#     db.add(_user)
#     db.commit()
#     return ResponseProcess(status="Ok", status_code="200", message="Success created data")


# @router_user.put("/rewards/{reward_id}")
# def update_reward(reward_id: int, request: RewardsRequestInSchema,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     _user = db.query(UserRewards).filter(
#         UserRewards.reward_id == reward_id).one_or_none()
#     if not _user:
#         raise HTTPException(status_code=404, detail="Data not found")
#     _user.reward_name = request.reward_name
#     _user.reward_file_path = request.reward_file_path
#     _user.user_id = request.user_id
#     db.commit()
#     return ResponseProcess(status="Ok", status_code="200", message="Success update data")


# @router_user.get("/rewards/{user_id}", response_model=list[RewardsRequestOutSchema])
# def get_reward(user_id: str,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     _user = db.query(UserRewards).order_by(asc(UserRewards.reward_id)).filter(
#         UserRewards.user_id == user_id).all()
#     return _user


# @router_user.delete("/rewards/{reward_id}")
# def delete_reward(reward_id: int,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     _user = db.query(UserRewards).filter(
#         UserRewards.reward_id == reward_id).one_or_none()
#     if not _user:
#         raise HTTPException(status_code=404, detail="Data not found")
#     db.delete(_user)
#     db.commit()
#     return ResponseProcess(status="Ok", status_code="200", message="Success delete data")


# @router_user.post("/language/create")
# def create_language(request: LanguagRequestInSchema, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     user_id = request.user_id
#     _checktotal = db.query(UserLanguage).filter(
#         UserLanguage.user_id == user_id).count()
#     if _checktotal >= 3:
#         raise HTTPException(status_code=404, detail="Data not found")
#     _user = UserLanguage(
#         language_code=request.language_code,
#         language_overall=request.language_overall,
#         language_type=request.language_type,
#         language_score=request.language_score,
#         create_date=todaytime(),
#         udp_date=todaytime(),
#         user_id=user_id
#     )
#     db.add(_user)
#     db.commit()
#     return ResponseProcess(status="Ok", status_code="200", message="Success created data")


# @router_user.put("/language/{language_id}")
# def update_language(language_id: int, request: LanguagRequestInSchema,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     _user = db.query(UserLanguage).filter(
#         UserLanguage.language_id == language_id).one_or_none()
#     if not _user:
#         raise HTTPException(status_code=404, detail="Data not found")
#     _user.language_code = request.language_code
#     _user.language_overall = request.language_overall
#     _user.language_type = request.language_type
#     _user.language_score = request.language_score
#     _user.user_id = request.user_id
#     db.commit()
#     return ResponseProcess(status="Ok", status_code="200", message="Success update data")


# @router_user.get("/language/{user_id}", response_model=list[LanguagRequestOutSchema])
# def get_language(user_id: str,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     _user = db.query(UserLanguage).order_by(asc(UserLanguage.language_id)).filter(
#         UserLanguage.user_id == user_id).all()
#     return _user


# @router_user.delete("/language/{language_id}")
# def delete_language(language_id: int,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     _user = db.query(UserLanguage).filter(
#         UserLanguage.language_id == language_id).one_or_none()
#     if not _user:
#         raise HTTPException(status_code=404, detail="Data not found")
#     db.delete(_user)
#     db.commit()
#     return ResponseProcess(status="Ok", status_code="200", message="Success delete data")


# @router_user.post("/skill_profile/create")
# def create_skill_profile(request: SkillProfileRequestInSchema, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     user_id = request.user_id
#     _checktotal = db.query(UserSkill).filter(
#         UserSkill.user_id == user_id).count()
#     if _checktotal >= 3:
#         raise HTTPException(status_code=404, detail="Data not found")
#     _user = UserSkill(
#         skill_profile_detail=request.skill_profile_detail,
#         create_date=todaytime(),
#         udp_date=todaytime(),
#         skill_id=request.skill_id,
#         user_id=user_id
#     )
#     db.add(_user)
#     db.commit()
#     return ResponseProcess(status="Ok", status_code="200", message="Success created data")


# @router_user.get("/skill_profile/{user_id}", response_model=list[SkillProfileRequestOutSchema])
# def get_skill_profile(user_id: str,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     _user = db.query(UserSkill).options(joinedload(UserSkill.skill_profile_child)).order_by(asc(UserSkill.skill_profile_id)).filter(
#         UserSkill.user_id == user_id).all()
#     return _user


# @router_user.delete("/skill_profile/{skill_profile_id}")
# def delete_language(skill_profile_id: int,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
#     _user = db.query(UserSkill).filter(
#         UserSkill.skill_profile_id == skill_profile_id).one_or_none()
#     if not _user:
#         raise HTTPException(status_code=404, detail="Data not found")
#     db.delete(_user)
#     db.commit()
#     return ResponseProcess(status="Ok", status_code="200", message="Success delete data")
