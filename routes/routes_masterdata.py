from typing import Optional

import requests
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import and_, asc, desc, or_
from sqlalchemy.orm import Session
from typing import List
from authen import auth_request
from database import get_db
from function import ceil, ternaryZero, todaytime
from models import BusinessType, Country, Institution, Skill, TambonThai, WorkChild, WorkParent
from schemas_format.general_schemas import FilterRequestSchema, ResponseData, ResponseProcess
from schemas_format.masterdata_schemas import BusinessTypeRequestInSchema, BusinessTypeRequestOutSchema, InstitutionRequestInSchema, InstitutionOutOptionSchema, SkillRequestInSchema, SkillFullRequestOutSchema, SkillRequestOutSchema, WorkChildRequestInSchema, WorkChildRequestOutSchema, WorkParentRequestInSchema, WorkFullOptionRequestOutSchema
from data_common import main_skill
router_masterdata = APIRouter()


class locationFilter(BaseModel):
    district_name: Optional[str] = None
    amphur_name: Optional[str] = None
    province_name: Optional[str] = None


@router_masterdata.get("/install_default_data")
def install_default_data(db: Session = Depends(get_db)):
    total_country = db.query(Country).count()
    status_country = False
    total_tambon_thai = db.query(TambonThai).count()
    status_location_thai = False
    if total_country <= 0:
        api_url_country = "https://masterdata.thaionzon.com/country"
        response_country = requests.get(api_url_country)
        list_country = response_country.json()
        obj = []
        for row_country in list_country:
            # print(row_country["country_name_th"])
            _country = Country(
                country_name_th=str(
                    row_country["country_name_th"]).strip(),
                country_name_eng=str(
                    row_country["country_name_eng"]).strip(),
                country_official_name_th=str(
                    row_country["country_official_name_th"]).strip(),
                country_official_name_eng=str(
                    row_country["country_official_name_eng"]).strip(),
                capital_name_th=str(
                    row_country["capital_name_th"]).strip(),
                capital_name_eng=str(
                    row_country["capital_name_eng"]).strip(),
                zone=str(row_country["zone"]).strip(),
            )
            obj.append(_country)
        db.add_all(obj)
        db.commit()
        status_country = True
    if total_tambon_thai <= 0:
        api_url_location_thai = "https://hrc.iddrives.co.th/opendata/all_tambon.json"
        response_location_thai = requests.get(api_url_location_thai)
        list_location_thai = response_location_thai.json()
        obj = []
        for row_location_thai in list_location_thai:
            _location_thai = TambonThai(
                tambon_thai=row_location_thai["tambon_thai"],
                tambon_eng=row_location_thai["tambon_eng"],
                tambon_thai_short=row_location_thai["tambon_thai_short"],
                tambon_eng_short=row_location_thai["tambon_eng_short"],
                district_id=row_location_thai["district_id"],
                district_thai=row_location_thai["district_thai"],
                district_eng=row_location_thai["district_eng"],
                district_thai_short=row_location_thai["district_thai_short"],
                district_eng_short=row_location_thai["district_eng_short"],
                province_id=row_location_thai["province_id"],
                province_thai=row_location_thai["province_thai"],
                province_eng=row_location_thai["province_eng"],
                postcode=row_location_thai["postcode"],
            )
            obj.append(_location_thai)
        db.add_all(obj)
        db.commit()
        status_location_thai = True

    return {"country": status_country, "location_thai": status_location_thai}


@router_masterdata.post("/tambon")
def general_tambon(request: FilterRequestSchema, db: Session = Depends(get_db)):
    skip = ternaryZero(((request.page - 1) * request.per_page))
    limit = request.per_page
    search_value = str(request.search_value)
    # ค้นหาปกติ
    searchFilter = or_(TambonThai.tambon_thai.contains(search_value),
                       TambonThai.tambon_eng.contains(search_value),
                       TambonThai.tambon_thai_short.contains(search_value),
                       TambonThai.tambon_eng_short.contains(search_value),
                       TambonThai.district_thai.contains(search_value),
                       TambonThai.district_eng.contains(search_value),
                       TambonThai.district_thai_short.contains(search_value),
                       TambonThai.district_eng_short.contains(search_value),
                       TambonThai.province_thai.contains(search_value),
                       TambonThai.province_eng.contains(search_value),
                       TambonThai.postcode == search_value,
                       )
    if search_value:
        _tambon = db.query(TambonThai).filter(
            searchFilter).offset(skip).limit(limit).all()
    else:
        _tambon = db.query(TambonThai).offset(skip).limit(limit).all()
    total_data = db.query(TambonThai).count()
    total_filter_data = len(_tambon)
    total_page = ceil(total_data / request.per_page)
    return ResponseData(status="success", status_code="200", message="Success fetch all data", page=request.page, per_page=limit, total_page=total_page, total_data=total_data, total_filter_data=total_filter_data, data=_tambon)


@router_masterdata.post("/country")
def general_country(request: FilterRequestSchema, db: Session = Depends(get_db)):
    skip = ternaryZero(((request.page - 1) * request.per_page))
    limit = request.per_page
    search_value = request.search_value
    # ค้นหาปกติ
    searchFilter = or_(Country.country_name_th.contains(search_value),
                       Country.country_name_eng.contains(search_value),
                       Country.country_official_name_th.contains(search_value),
                       Country.capital_name_th.contains(search_value),
                       Country.capital_name_eng.contains(search_value))
    if search_value:
        _country = db.query(Country).filter(
            searchFilter).offset(skip).limit(limit).all()
    else:
        _country = db.query(Country).offset(skip).limit(limit).all()
    total_data = db.query(Country).count()
    total_filter_data = len(_country)
    total_page = ceil(total_data / request.per_page)
    return ResponseData(status="success", status_code="200", message="Success fetch all data", page=request.page, per_page=limit, total_page=total_page, total_data=total_data, total_filter_data=total_filter_data, data=_country)


@router_masterdata.post("/institution/create")
def create_institution(request: InstitutionRequestInSchema, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _institution = Institution(
        institution_name=request.institution_name,
        active=request.active,
        create_date=todaytime(),
        udp_date=todaytime(),
    )
    db.add(_institution)
    db.commit()
    db.refresh(_institution)
    return {"institution_id": _institution.institution_id, "institution_name": _institution.institution_name}


@router_masterdata.put("/institution/{institution_id}")
def update_institution(institution_id: int, request: InstitutionRequestInSchema,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _institution = db.query(Institution).filter(
        Institution.institution_id == institution_id).one_or_none()
    if not _institution:
        raise HTTPException(status_code=404, detail="Data not found")
    _institution.institution_name = request.institution_name
    _institution.active = request.active
    _institution.udp_date = todaytime()
    db.commit()
    return ResponseProcess(status="Ok", status_code="200", message="Success update data")


@router_masterdata.delete("/institution/{institution_id}")
def delete_institution(institution_id: int,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _institution = db.query(Institution).filter(
        Institution.institution_id == institution_id).one_or_none()
    if not _institution:
        raise HTTPException(status_code=404, detail="Data not found")
    _institution.cancelled = 0
    db.commit()
    return ResponseProcess(status="Ok", status_code="200", message="Success delete data")


@router_masterdata.post("/institution/get/all")
def general_institution(request: FilterRequestSchema, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    skip = ternaryZero(((request.page - 1) * request.per_page))
    limit = request.per_page
    search_value = request.search_value
    if search_value:
        _institution = db.query(Institution).order_by(asc(Institution.institution_name)).filter(Institution.institution_name.contains(
            search_value), Institution.cancelled == 1).offset(skip).limit(limit).all()
    else:
        _institution = db.query(Institution).filter(
            Institution.cancelled == 1).order_by(asc(Institution.institution_name)).offset(skip).limit(limit).all()
    total_data = db.query(Institution).count()
    total_filter_data = len(_institution)
    total_page = ceil(total_data / request.per_page)
    return InstitutionOutOptionSchema(status="success", status_code="200", message="Success fetch all data", page=request.page, per_page=limit, total_page=total_page, total_data=total_data, total_filter_data=total_filter_data, data=_institution)


@router_masterdata.post("/skill/create")
def create_skill(request: SkillRequestInSchema, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _skill = Skill(
        skill_name=request.skill_name,
        description=request.description,
        skill_group_type=request.skill_group_type,
        active=request.active,
        create_date=todaytime(),
        udp_date=todaytime(),
    )
    db.add(_skill)
    db.commit()
    return ResponseProcess(status="Ok", status_code="200", message="Success created data")


@router_masterdata.put("/skill/{skill_id}")
def update_skill(skill_id: int, request: SkillRequestInSchema,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _skill = db.query(Skill).filter(
        Skill.skill_id == skill_id).one_or_none()
    if not _skill:
        raise HTTPException(status_code=404, detail="Data not found")
    _skill.skill_name = request.skill_name
    _skill.description = request.description
    _skill.skill_group_type = request.skill_group_type
    _skill.active = request.active
    _skill.udp_date = todaytime()
    db.commit()
    return ResponseProcess(status="Ok", status_code="200", message="Success update data")


@router_masterdata.get("/skill/get/all", response_model=List[SkillFullRequestOutSchema])
def get_skill(db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    obj = []
    for rs in main_skill:
        main_skill_id = rs['main_skill_id']
        _skill = db.query(Skill).order_by(asc(Skill.skill_name)).filter(
            Skill.skill_group_type == main_skill_id, Skill.cancelled == 1).all()
        response = {'main_skill_id': main_skill_id,
                    'main_skill_name': rs['main_skill_name'], 'subskills': _skill}
        obj.append(response)
    return obj
@router_masterdata.get("/skill", response_model=List[SkillRequestOutSchema])
def get_skill_option(typeskill: int, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    if typeskill > 0:
        query = Skill.skill_group_type == typeskill
    else:
        query = Skill.skill_group_type > 0
    _skill = db.query(Skill).order_by(desc(Skill.create_date), asc(Skill.skill_group_type)).filter(
        Skill.cancelled == 1, query).all()
    return _skill

@router_masterdata.get("/skill", response_model=List[SkillRequestOutSchema])
def get_skill_option(typeskill: int, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    if typeskill > 0:
        query = Skill.skill_group_type == typeskill
    else:
        query = Skill.skill_group_type > 0
    _skill = db.query(Skill).order_by(desc(Skill.create_date), asc(Skill.skill_group_type)).filter(
        Skill.cancelled == 1, query).all()
    return _skill


@router_masterdata.get("/skill/get/{skill_id}", response_model=SkillRequestOutSchema)
def get_skill_by_id(skill_id: int, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _skill = db.query(Skill).order_by(asc(Skill.skill_name)).filter(
        Skill.skill_id == skill_id, Skill.cancelled == 1).one_or_none()
    if not _skill:
        raise HTTPException(status_code=404, detail="Data not found")
    return _skill


@router_masterdata.delete("/skill/{skill_id}")
def delete_skill(skill_id: int, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _skill = db.query(Skill).filter(
        Skill.skill_id == skill_id).one_or_none()
    if not _skill:
        raise HTTPException(status_code=404, detail="Data not found")
    _skill.cancelled = 0
    db.commit()
    return ResponseProcess(status="Ok", status_code="200", message="Success delete data")


@router_masterdata.post("/work_parent/create")
def create_work_parent(request: WorkParentRequestInSchema, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _work_parent = WorkParent(
        wp_name=request.wp_name,
        active=request.active,
        create_date=todaytime(),
        udp_date=todaytime(),
    )
    db.add(_work_parent)
    db.commit()
    return ResponseProcess(status="Ok", status_code="200", message="Success created data")


@router_masterdata.put("/work_parent/{wp_id}")
def update_work_parent(wp_id: int, request: WorkParentRequestInSchema,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _work_parent = db.query(WorkParent).filter(
        WorkParent.wp_id == wp_id).one_or_none()
    if not _work_parent:
        raise HTTPException(status_code=404, detail="Data not found")
    _work_parent.wp_name = request.wp_name
    _work_parent.active = request.active
    _work_parent.udp_date = todaytime()
    db.commit()
    return ResponseProcess(status="Ok", status_code="200", message="Success update data")


@router_masterdata.delete("/work_parent/{wp_id}")
def delete_work_parent(wp_id: int, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _work_parent = db.query(WorkParent).filter(
        WorkParent.wp_id == wp_id).one_or_none()
    if not _work_parent:
        raise HTTPException(status_code=404, detail="Data not found")
    _work_parent.cancelled = 0
    db.commit()
    return ResponseProcess(status="Ok", status_code="200", message="Success delete data")


@router_masterdata.get("/work_parent", response_model=List[WorkFullOptionRequestOutSchema])
def get_work_parent(db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _work_parent = db.query(WorkParent).order_by(desc(WorkParent.create_date)).filter(
        WorkParent.cancelled == 1).all()
    return _work_parent


@router_masterdata.post("/work_child/create")
def create_work_child(request: WorkChildRequestInSchema, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _work_child = WorkChild(
        wc_name=request.wc_name,
        active=request.active,
        create_date=todaytime(),
        udp_date=todaytime(),
        wp_id=request.wp_id
    )
    db.add(_work_child)
    db.commit()
    return ResponseProcess(status="Ok", status_code="200", message="Success created data")


@router_masterdata.put("/work_child/{wc_id}")
def update_work_child(wc_id: int, request: WorkChildRequestInSchema,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _work_child = db.query(WorkChild).filter(
        WorkChild.wc_id == wc_id).one_or_none()
    if not _work_child:
        raise HTTPException(status_code=404, detail="Data not found")
    _work_child.wc_name = request.wc_name
    _work_child.active = request.active
    _work_child.udp_date = todaytime()
    _work_child.wp_id = request.wp_id
    db.commit()
    return ResponseProcess(status="Ok", status_code="200", message="Success update data")


@router_masterdata.delete("/work_child/{wc_id}")
def delete_work_child(wc_id: int, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _work_child = db.query(WorkChild).filter(
        WorkChild.wc_id == wc_id).one_or_none()
    if not _work_child:
        raise HTTPException(status_code=404, detail="Data not found")
    _work_child.cancelled = 0
    db.commit()
    return ResponseProcess(status="Ok", status_code="200", message="Success delete data")


@router_masterdata.get("/work_child", response_model=List[WorkChildRequestOutSchema])
def get_work_child(db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _work_child = db.query(WorkChild).order_by(desc(WorkChild.create_date)).filter(
        WorkChild.cancelled == 1).all()
    return _work_child


@router_masterdata.get("/work_child", response_model=List[WorkChildRequestOutSchema])
def get_work_child_option_group(db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _work_child = db.query(WorkChild).order_by(desc(WorkChild.create_date)).filter(
        WorkChild.cancelled == 1).all()
    return _work_child


@router_masterdata.post("/business_type/create")
def create_business_type(request: BusinessTypeRequestInSchema, db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _business_type = BusinessType(
        bt_name=request.bt_name,
        active=request.active,
        create_date=todaytime(),
        udp_date=todaytime()
    )
    db.add(_business_type)
    db.commit()
    return ResponseProcess(status="Ok", status_code="200", message="Success created data")


@router_masterdata.put("/business_type/{bt_id}")
def update_business_type(bt_id: int, request: BusinessTypeRequestInSchema,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _business_type = db.query(BusinessType).filter(
        BusinessType.bt_id == bt_id).one_or_none()
    if not _business_type:
        raise HTTPException(status_code=404, detail="Data not found")
    _business_type.bt_name = request.bt_name
    _business_type.active = request.active
    _business_type.udp_date = todaytime()
    db.commit()
    return ResponseProcess(status="Ok", status_code="200", message="Success update data")


@router_masterdata.delete("/business_type/{bt_id}")
def delete_business_type(bt_id: int,  db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _business_type = db.query(BusinessType).filter(
        BusinessType.bt_id == bt_id).one_or_none()
    if not _business_type:
        raise HTTPException(status_code=404, detail="Data not found")
    _business_type.cancelled = 0
    db.commit()
    return ResponseProcess(status="Ok", status_code="200", message="Success delete data")


@router_masterdata.get("/business_type", response_model=List[BusinessTypeRequestOutSchema])
def get_business_type(db: Session = Depends(get_db), authenticated: bool = Depends(auth_request)):
    _business_type = db.query(BusinessType).order_by(desc(BusinessType.create_date)).filter(
        BusinessType.cancelled == 1).all()
    return _business_type
