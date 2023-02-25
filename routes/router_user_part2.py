from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from passlib.hash import sha256_crypt
from sqlalchemy import desc, asc, or_
from sqlalchemy.orm import Session, joinedload
from typing import List

from authen import auth_request
from database import get_db
from function import ceil, ternaryZero, todaytime, treeDigit, fourDigit
from models import User, UserDetail, UserCompany, UserEducation, UserExperience, UserSalary, UserHobbies, UserRewards, UserHireType, UserWorkType, UserPortfolio
from schemas_format.general_schemas import FilterRequestSchema, ResponseProcess
from schemas_format.user_schemas import UserHireTypeRequestInSchema, UserCompanyRegisterRequestInSchema, UserCandidateRegisterRequestInSchema, UserRequestOutOptionSchema, UserSalaryRequestInSchema, UserWorkTypeRequestInSchema, UserWorkTypeRequestOutSchema, PortfolioRequestIntSchema, PortfolioRequestOutSchema
router_user_part2 = APIRouter()
now = datetime.now()  # current date and time
year = now.strftime("%Y")
month = now.strftime("%m")
# Main Method


@router_user_part2.get("/rating/{user_id}")
def result_rating(user_id: str,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _profile1 = db.query(UserDetail).filter(
        UserDetail.user_id == user_id).count()
    _profile2 = db.query(UserCompany).filter(
        UserCompany.user_id == user_id).count()
    _profile3 = db.query(UserSalary).filter(
        UserSalary.user_id == user_id).count()
    _profile4 = db.query(UserHobbies).filter(
        UserHobbies.user_id == user_id).count()
    _profile5 = db.query(UserRewards).filter(
        UserRewards.user_id == user_id).count()

    _educations = db.query(UserEducation).filter(
        UserEducation.user_id == user_id).count()
    _experiences = db.query(UserExperience).filter(
        UserExperience.user_id == user_id).count()

    # วีดีโอแนะนำตนเอง
    _portfolio = db.query(UserPortfolio).filter(
        UserPortfolio.user_id == user_id, UserPortfolio.portfolio_type == 2).count()

    if _profile1 and _profile2 and _profile3 and _profile4 and _profile5 > 0:
        _rating_profile = 1
    else:
        _rating_profile = 0

    if _educations and _experiences > 0:
        _rating_edu_exp = 1
    else:
        _rating_edu_exp = 0
    if _portfolio > 0:
        _rating_port = 1
    else:
        _rating_port = 0
    result = _rating_profile + _rating_edu_exp + _rating_port
    return {'result': result}


@router_user_part2.post("/register/company/create")
def register_company(request: UserCompanyRegisterRequestInSchema, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    main = request
    detail = request.detail
    company = request.company
    _user = db.query(User).filter(
        or_(User.username == main.username, User.email == main.email)).one_or_none()
    if _user:
        raise HTTPException(status_code=404, detail="Username or E-mail Error")
    password = main.password
    password_hash = sha256_crypt.encrypt(str(password))

    _main = User(
        username=main.username,
        password=password_hash,
        firstname=main.firstname,
        lastname=main.lastname,
        email=main.email,
        user_type=2,
        active=main.active,
        create_date=todaytime(),
        update_date=todaytime(),
    )
    db.add(_main)
    db.commit()
    db.refresh(_main)
    user_id = _main.user_id
    # Detail
    total_user_company = db.query(User).filter(
        User.cancelled == 1, User.user_type == 2).count()
    total_set = total_user_company + 1
    ud_code = "CO" + str(now.strftime("%y")) + \
        str(now.strftime("%m")) + str(now.strftime("%d")) + \
        str(treeDigit(total_set))
    _detail = UserDetail(
        ud_bio=detail.ud_bio,
        ud_birhday=detail.ud_birhday,
        ud_gender=detail.ud_gender,
        ud_phone=detail.ud_phone,
        ud_address=detail.ud_address,
        ud_code=ud_code,
        tambon_id=detail.tambon_id,
        country_id=detail.country_id,
        user_id=user_id
    )
    db.add(_detail)
    db.commit()
    # Company
    _company = UserCompany(
        uc_company_name=company.uc_company_name,
        uc_company_website=company.uc_company_website,
        uc_company_remark1=company.uc_company_remark1,
        uc_company_remark2=company.uc_company_remark2,
        uc_company_cover=company.uc_company_cover,
        bt_id=company.bt_id,
        user_id=user_id
    )
    db.add(_company)
    db.commit()
    return ResponseProcess(status="Ok", status_code="200", message="Success created data")


@router_user_part2.put("/company/{user_id}")
def update_company(user_id: str, request: UserCompanyRegisterRequestInSchema, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    main = request
    detail = request.detail
    company = request.company
    _check_user = db.query(User).filter(
        or_(User.username == main.username, User.email == main.email), User.user_id != user_id).one_or_none()
    if _check_user:
        raise HTTPException(status_code=404, detail="Username or E-mail Error")
    _user = db.query(User).filter(User.user_id == user_id).one_or_none()
    if not _user:
        raise HTTPException(status_code=404, detail="Data not found")
    password = main.password
    if(password == "" or password == None):
        password_hash = _user.password
    else:
        password_hash = sha256_crypt.encrypt(str(password))
    _user.username = main.username
    _user.password = password_hash
    _user.firstname = main.firstname
    _user.lastname = main.lastname
    _user.email = main.email
    _user.active = main.active
    _user.update_date = todaytime()

    # Detail
    _user_detail = db.query(UserDetail).filter(
        UserDetail.user_id == user_id).one_or_none()
    _user_detail.ud_bio = detail.ud_bio
    _user_detail.ud_birhday = detail.ud_birhday
    _user_detail.ud_phone = detail.ud_phone
    _user_detail.ud_gender = detail.ud_gender
    _user_detail.ud_address = detail.ud_address
    _user_detail.tambon_id = detail.tambon_id
    _user_detail.country_id = detail.country_id
    db.commit()
    # Company
    _user_company = db.query(UserCompany).filter(
        UserCompany.user_id == user_id).one_or_none()
    _user_company.uc_company_name = company.uc_company_name
    _user_company.uc_company_website = company.uc_company_website
    _user_company.uc_company_remark1 = company.uc_company_remark1
    _user_company.uc_company_remark2 = company.uc_company_remark2
    _user_company.uc_company_cover = company.uc_company_cover
    _user_company.bt_id = company.bt_id
    db.commit()
    return ResponseProcess(status="Ok", status_code="200", message="Success created data")


@router_user_part2.post("/register/candidate/create")
def register_candidate(request: UserCandidateRegisterRequestInSchema, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    main = request
    detail = request.detail
    _user = db.query(User).filter(
        or_(User.username == main.username, User.email == main.email)).one_or_none()
    if _user:
        raise HTTPException(status_code=404, detail="Username or E-mail Error")
    password = main.password
    password_hash = sha256_crypt.encrypt(str(password))
    _main = User(
        username=main.username,
        password=password_hash,
        firstname=main.firstname,
        lastname=main.lastname,
        email=main.email,
        user_type=3,
        active=main.active,
        create_date=todaytime(),
        update_date=todaytime(),
    )
    db.add(_main)
    db.commit()
    db.refresh(_main)
    user_id = _main.user_id
    # Detail
    total_user_company = db.query(User).filter(
        User.cancelled == 1, User.user_type == 3).count()
    total_set = total_user_company + 1
    ud_code = "C" + str(now.strftime("%y")) + \
        str(now.strftime("%m")) + str(now.strftime("%d")) + \
        str(fourDigit(total_set))
    _detail = UserDetail(
        ud_bio=detail.ud_bio,
        ud_birhday=detail.ud_birhday,
        ud_gender=detail.ud_gender,
        ud_phone=detail.ud_phone,
        ud_address=detail.ud_address,
        ud_code=ud_code,
        tambon_id=detail.tambon_id,
        country_id=detail.country_id,
        user_id=user_id
    )
    db.add(_detail)
    db.commit()

    return ResponseProcess(status="Ok", status_code="200", message="Success created data")


@router_user_part2.post("/get/{typeuser}")
def get_user(request: FilterRequestSchema, typeuser: int, db: Session = Depends(get_db),  authenticated: bool = Depends(auth_request)):

    skip = ternaryZero(((request.page - 1) * request.per_page))
    limit = request.per_page
    search_value = request.search_value

    if search_value:
        result = db.query(User).order_by(desc(User.create_date)).filter(or_(User.firstname.contains(
            search_value), User.lastname.contains(search_value), User.username.contains(search_value)), User.user_type == typeuser, User.cancelled == 1, User.active == 1).offset(skip).limit(limit).all()
    else:
        result = db.query(User).order_by(desc(User.create_date)).filter(
            User.user_type == typeuser, User.cancelled == 1, User.active == 1).offset(skip).limit(limit).all()

    total_data = db.query(User).filter(
        User.user_type == typeuser, User.cancelled == 1, User.active == 1).count()
    total_filter_data = len(result)
    total_page = ceil(total_data / request.per_page)
    return UserRequestOutOptionSchema(status="success", status_code="200", message="Success fetch all data", page=request.page, per_page=limit, total_page=total_page, total_data=total_data, total_filter_data=total_filter_data, data=result)


@router_user_part2.post("/salary/{user_id}")
def update_user_salary(user_id: str, request: UserSalaryRequestInSchema,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _user = db.query(UserSalary).filter(
        UserSalary.user_id == user_id).one_or_none()
    if not _user:
        _useradd = UserSalary(
            us_salary_start=request.us_salary_start,
            us_salary_end=request.us_salary_end,
            user_id=user_id
        )
        db.add(_useradd)
        db.commit()
    else:
        _user.us_salary_start = request.us_salary_start
        _user.us_salary_end = request.us_salary_end
        db.commit()
    return ResponseProcess(status="Ok", status_code="200", message="Success update data")


@router_user_part2.get("/salary/{user_id}", response_model=UserSalaryRequestInSchema)
def get_user_salary(user_id: str,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _user = db.query(UserSalary).filter(
        UserSalary.user_id == user_id).one()
    return _user


@router_user_part2.post("/hiretype/{user_id}")
def create_hiretype(user_id: str, request: List[UserHireTypeRequestInSchema], db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _check_user = db.query(User).filter(
        User.user_id == user_id).one_or_none()
    if not _check_user:
        raise HTTPException(status_code=404, detail="Data not found")
    # ลบข้อมูลเก่าทิ้ง
    db.query(UserHireType).filter(
        UserHireType.user_id == user_id).delete()
    obj = []
    for row in request:
        _user = UserHireType(
            uh_type=row.uh_type,
            user_id=user_id
        )
        obj.append(_user)
    db.add_all(obj)
    db.commit()
    return ResponseProcess(status="Ok", status_code="200", message="Success created data")


@router_user_part2.get("/hiretype/{user_id}", response_model=List[UserHireTypeRequestInSchema])
def get_hiretype(user_id: str,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _user = db.query(UserHireType).filter(
        UserHireType.user_id == user_id).all()
    return _user


@router_user_part2.post("/worktype/{user_id}")
def create_worktype(user_id: str, request: List[UserWorkTypeRequestInSchema], db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _check_user = db.query(User).filter(
        User.user_id == user_id).one_or_none()
    if not _check_user:
        raise HTTPException(status_code=404, detail="Data not found")
    # ลบข้อมูลเก่าทิ้ง
    db.query(UserWorkType).filter(
        UserWorkType.user_id == user_id).delete()
    obj = []
    for row in request:
        _user = UserWorkType(
            wc_id=row.wc_id,
            user_id=user_id
        )
        obj.append(_user)
    db.add_all(obj)
    db.commit()
    return ResponseProcess(status="Ok", status_code="200", message="Success created data")


@router_user_part2.get("/worktype/{user_id}", response_model=List[UserWorkTypeRequestOutSchema])
def get_worktype(user_id: str,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _user = db.query(UserWorkType).filter(
        UserWorkType.user_id == user_id).all()
    return _user


@router_user_part2.post("/portfolio/{user_id}")
def portfolio_create(user_id: str, request: PortfolioRequestIntSchema, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    portfolio_type = request.portfolio_type
    _user = db.query(UserPortfolio).filter(
        UserPortfolio.user_id == user_id, UserPortfolio.portfolio_type == portfolio_type).one_or_none()
    if not _user:
        _useradd = UserPortfolio(
            portfolio_name=request.portfolio_name,
            portfolio_path=request.portfolio_path,
            portfolio_type=portfolio_type,
            active=request.active,
            create_date=todaytime(),
            udp_date=todaytime(),
            user_id=user_id
        )
        db.add(_useradd)
        db.commit()
    else:
        _user.portfolio_name = request.portfolio_name
        _user.portfolio_path = request.portfolio_path
        _user.active = request.active
        _user.udp_date = todaytime()
        db.commit()

    return ResponseProcess(status="Ok", status_code="200", message="Success created data")


@router_user_part2.get("/portfolio/{user_id}", response_model=PortfolioRequestOutSchema)
def get_portfolio(user_id: str, portfolio_type: int,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _user = db.query(UserPortfolio).filter(
        UserPortfolio.user_id == user_id, UserPortfolio.portfolio_type == portfolio_type).first()
    if not _user:
        raise HTTPException(status_code=404, detail="Data not found")
    return _user

@router_user_part2.delete("/portfolio/{user_id}", response_model=PortfolioRequestOutSchema)
def delete_portfolio(user_id: str, portfolio_type: int,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _user = db.query(UserPortfolio).filter(
        UserPortfolio.user_id == user_id, UserPortfolio.portfolio_type == portfolio_type).first()
    if not _user:
        raise HTTPException(status_code=404, detail="Data not found")
    db.delete(_user)
    db.commit()
    return _user

