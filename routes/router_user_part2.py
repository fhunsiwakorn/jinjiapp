from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from passlib.hash import sha256_crypt
from sqlalchemy import desc, asc, or_
from sqlalchemy.orm import Session, joinedload

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

@router_user_part2.get("/salary/{user_id}", response_model=UserSalaryRequestInSchema)
def get_user_salary(user_id: str,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _user = db.query(UserSalary).filter(
        UserSalary.user_id == user_id).one()
    return _user