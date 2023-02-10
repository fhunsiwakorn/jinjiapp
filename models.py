from sqlalchemy import (Column, Date, DateTime, Float, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship

from database import Base
from function import generateId, generateShortId


class Country(Base):
    __tablename__ = 'app_country'
    country_id = Column(Integer, primary_key=True)
    country_name_th = Column(String(128), nullable=True)
    country_name_eng = Column(String(128), nullable=True)
    country_official_name_th = Column(String(128), nullable=True)
    country_official_name_eng = Column(String(128), nullable=True)
    capital_name_th = Column(String(128), nullable=True)
    capital_name_eng = Column(String(128), nullable=True)
    zone = Column(String(64), nullable=True)
    country_user = relationship(
        "UserDetail", back_populates="user_country")


class TambonThai(Base):
    __tablename__ = 'app_tambon_thai'
    tambon_id = Column(Integer, primary_key=True)
    tambon_thai = Column(String(128), nullable=True)
    tambon_eng = Column(String(128), nullable=True)
    tambon_thai_short = Column(String(128), nullable=True)
    tambon_eng_short = Column(String(128), nullable=True)
    district_id = Column(String(128), nullable=True)
    district_thai = Column(String(128), nullable=True)
    district_eng = Column(String(128), nullable=True)
    district_thai_short = Column(String(128), nullable=True)
    district_eng_short = Column(String(128), nullable=True)
    province_id = Column(String(128), nullable=True)
    province_thai = Column(String(128), nullable=True)
    province_eng = Column(String(128), nullable=True)
    postcode = Column(String(128), nullable=True)

    tambon_user = relationship(
        "UserDetail", back_populates="user_tambon")


# skill_group_type 1 = Computer Skills , 2 = Competency Skills , 3 = Car


class Skill(Base):
    __tablename__ = 'app_masterdata_skill'
    skill_id = Column(Integer, primary_key=True)
    skill_name = Column(String(128), nullable=True)
    description = Column(String(512), nullable=True)
    skill_group_type = Column(Integer, default=1)
    active = Column(Integer, default=1)
    create_date = Column(DateTime)
    udp_date = Column(DateTime)
    cancelled = Column(Integer, default=1)
    skill_profile_parent = relationship(
        "UserSkill", back_populates="skill_profile_child")


class WorkParent(Base):
    __tablename__ = 'app_masterdata_work_parent'
    wp_id = Column(Integer, primary_key=True)
    wp_name = Column(String(24), nullable=True)
    active = Column(Integer, default=1)
    create_date = Column(DateTime)
    udp_date = Column(DateTime)
    cancelled = Column(Integer, default=1)
    wp_wc = relationship(
        "WorkChild", back_populates="wc_wp")


class WorkChild(Base):
    __tablename__ = 'app_masterdata_work_child'
    wc_id = Column(Integer, primary_key=True)
    wc_name = Column(String(24), nullable=True)
    active = Column(Integer, default=1)
    create_date = Column(DateTime)
    udp_date = Column(DateTime)
    cancelled = Column(Integer, default=1)
    wp_id = Column(Integer, ForeignKey(
        "app_masterdata_work_parent.wp_id", ondelete="CASCADE"))
    wc_wp = relationship(
        "WorkParent", back_populates="wp_wc")
    work_child_user = relationship(
        "UserWorkType", back_populates="user_work_child")


class BusinessType(Base):
    __tablename__ = 'app_masterdata_business_type'
    bt_id = Column(Integer, primary_key=True)
    bt_name = Column(String(24), nullable=True)
    active = Column(Integer, default=1)
    create_date = Column(DateTime)
    udp_date = Column(DateTime)
    cancelled = Column(Integer, default=1)
    business_company = relationship(
        "UserCompany", back_populates="company_business")


class Institution(Base):
    __tablename__ = 'app_masterdata_institution'
    institution_id = Column(Integer, primary_key=True)
    institution_name = Column(String(128), nullable=True)
    active = Column(Integer, default=1)
    create_date = Column(DateTime)
    udp_date = Column(DateTime)
    cancelled = Column(Integer, default=1)
    institution_edu = relationship(
        "UserEducation", back_populates="edu_institution")


# user_type 1 Super Admin , 2 = HR, 3 = Candidate

# ฐานข้อมูลหลัก User
class User(Base):
    __tablename__ = 'app_user'
    user_id = Column(String(128), primary_key=True,
                     unique=True, default=generateId)
    username = Column(String(64), unique=True, index=True)
    password = Column(String(128), nullable=True)
    firstname = Column(String(128), nullable=True)
    lastname = Column(String(128), nullable=True)
    email = Column(String(48), nullable=True)
    user_image_prifile = Column(String(128), nullable=True)
    user_image_cover = Column(String(128), nullable=True)
    user_image_cover_position = Column(String(48), nullable=True)
    user_type = Column(Integer, default=0)
    active = Column(Integer, default=1)
    cancelled = Column(Integer, default=1)
    create_date = Column(DateTime)
    update_date = Column(DateTime)
    user_main_detail = relationship(
        "UserDetail", back_populates="detail_user_main")
    user_main_company = relationship(
        "UserCompany", back_populates="company_user_main")

# ud_gender 1 = Male , 2 = Female

# ฐานข้อมูลรายละเอียด User


class UserDetail(Base):
    __tablename__ = 'app_user_detail'
    ud_id = Column(Integer, primary_key=True)
    ud_bio = Column(String(128), nullable=True)
    ud_birhday = Column(Date)
    ud_gender = Column(Integer, default=0)
    ud_phone = Column(String(48), nullable=True)
    ud_address = Column(String(128), nullable=True)
    ud_code = Column(String(11), nullable=True)
    tambon_id = Column(Integer, ForeignKey(
        "app_tambon_thai.tambon_id", ondelete="CASCADE"))
    country_id = Column(Integer, ForeignKey(
        "app_country.country_id", ondelete="CASCADE"))
    user_id = Column(String(128), ForeignKey(
        "app_user.user_id", ondelete="CASCADE"))
    detail_user_main = relationship("User", back_populates="user_main_detail")

    user_tambon = relationship(
        "TambonThai", back_populates="tambon_user")
    user_country = relationship(
        "Country", back_populates="country_user")

# ฐานข้อมูลรายละเอียด User : ข้อมูลบริษัทใช้สำหรับ HR / Company


class UserCompany(Base):
    __tablename__ = 'app_user_company'
    uc_id = Column(Integer, primary_key=True)
    uc_company_name = Column(String(128), nullable=True)
    uc_company_website = Column(String(128), nullable=True)
    uc_company_remark1 = Column(String(512), nullable=True)
    uc_company_remark2 = Column(String(512), nullable=True)
    uc_company_cover = Column(String(128), nullable=True)
    bt_id = Column(Integer, ForeignKey(
        "app_masterdata_business_type.bt_id", ondelete="CASCADE"))
    user_id = Column(String(128), ForeignKey(
        "app_user.user_id", ondelete="CASCADE"))
    company_user_main = relationship(
        "User", back_populates="user_main_company")
    company_business = relationship(
        "BusinessType", back_populates="business_company")

# ฐานข้อมูลรายละเอียด User : ข้อมูลเงินเดือนใช้สำหรับ Candidate


class UserSalary(Base):
    __tablename__ = 'app_user_salary'
    us_id = Column(Integer, primary_key=True)
    us_salary_start = Column(Integer, default=0)
    us_salary_end = Column(Integer, default=0)
    user_id = Column(String(128), ForeignKey(
        "app_user.user_id", ondelete="CASCADE"))

# ฐานข้อมูลรายละเอียด User : ข้อมูลจุดแข็งใช้สำหรับ Candidate


class UserStrength(Base):
    __tablename__ = 'app_user_strength'
    strength_id = Column(Integer, primary_key=True)
    strength_name = Column(String(128), nullable=True)
    create_date = Column(DateTime)
    udp_date = Column(DateTime)
    user_id = Column(String(128), ForeignKey(
        "app_user.user_id", ondelete="CASCADE"))

# ฐานข้อมูลรายละเอียด User : ข้อมูลงานอดิเรกใช้สำหรับ Candidate


class UserHobbies(Base):
    __tablename__ = 'app_user_hobby'
    hobby_id = Column(Integer, primary_key=True)
    hobby_name = Column(String(128), nullable=True)
    create_date = Column(DateTime)
    udp_date = Column(DateTime)
    user_id = Column(String(128), ForeignKey(
        "app_user.user_id", ondelete="CASCADE"))

# ฐานข้อมูลรายละเอียด User : ข้อมูลรีวอร์ดใช้สำหรับ Candidate


class UserRewards(Base):
    __tablename__ = 'app_user_reward'
    reward_id = Column(Integer, primary_key=True)
    reward_name = Column(String(128), nullable=True)
    reward_file_path = Column(String(128), nullable=True)
    create_date = Column(DateTime)
    udp_date = Column(DateTime)
    user_id = Column(String(128), ForeignKey(
        "app_user.user_id", ondelete="CASCADE"))

# ฐานข้อมูลรายละเอียด User : ข้อมูลประเภทการว่าจ้างสำหรับ Candidate
# uh_type 1 = Full time  พนักประจำ,2 = Part time  พนักงานชั่วคราว ,3 = Freelance  ฟรีแลนซ์ , 4 =ฝึกงาน


class UserHireType(Base):
    __tablename__ = 'app_user_hiretype'
    uh_id = Column(Integer, primary_key=True)
    uh_type = Column(Integer, default=0)
    user_id = Column(String(128), ForeignKey(
        "app_user.user_id", ondelete="CASCADE"))

# ฐานข้อมูลรายละเอียด User : ข้อมูลประเภทงานสำหรับ Candidate


class UserWorkType(Base):
    __tablename__ = 'app_user_worktype'
    uw_id = Column(Integer, primary_key=True)
    wc_id = Column(Integer, ForeignKey(
        "app_masterdata_work_child.wc_id", ondelete="CASCADE"))
    user_id = Column(String(128), ForeignKey(
        "app_user.user_id", ondelete="CASCADE"))

    user_work_child = relationship(
        "WorkChild", back_populates="work_child_user")

# ฐานข้อมูลรายละเอียด User : ข้อมูลประสบการร์การทำงานใช้สำหรับ Candidate


class UserExperience(Base):
    __tablename__ = 'app_user_experience'
    exp_id = Column(Integer, primary_key=True)
    exp_comapany = Column(String(128), nullable=True)
    exp_year_start = Column(Integer, default=0)
    exp_year_end = Column(Integer, default=0)
    exp_last_position = Column(String(128), nullable=True)
    exp_last_salary = Column(Float, default=0)
    exp_responsibility = Column(String(256), nullable=True)
    active = Column(Integer, default=1)
    create_date = Column(DateTime)
    udp_date = Column(DateTime)
    user_id = Column(String(128), ForeignKey(
        "app_user.user_id", ondelete="CASCADE"))

# ฐานข้อมูลรายละเอียด User : ข้อมูลประวัติการศึกษาใช้สำหรับ Candidate


class UserEducation(Base):
    __tablename__ = 'app_user_education'
    edu_id = Column(Integer, primary_key=True)
    edu_degree = Column(Integer, default=0)
    edu_faculty = Column(String(256), nullable=True)
    edu_major = Column(String(256), nullable=True)
    edu_graduation_year = Column(Integer, default=0)
    edu_gpa = Column(Float, default=0)
    active = Column(Integer, default=1)
    create_date = Column(DateTime)
    udp_date = Column(DateTime)
    institution_id = Column(Integer, ForeignKey(
        "app_masterdata_institution.institution_id", ondelete="CASCADE"))
    user_id = Column(String(128), ForeignKey(
        "app_user.user_id", ondelete="CASCADE"))

    edu_institution = relationship(
        "Institution", back_populates="institution_edu")

# ฐานข้อมูลรายละเอียด User : ข้อมูลความสามารถด้านภาษาใช้สำหรับ Candidate


class UserLanguage(Base):
    __tablename__ = 'app_user_language'
    language_id = Column(Integer, primary_key=True)
    language_code = Column(String(24), nullable=True)
    language_overall = Column(String(24), nullable=True)
    language_type = Column(String(24), nullable=True)
    language_score = Column(String(24), nullable=True)
    create_date = Column(DateTime)
    udp_date = Column(DateTime)
    user_id = Column(String(128), ForeignKey(
        "app_user.user_id", ondelete="CASCADE"))

# ฐานข้อมูลรายละเอียด User : ข้อมูลด้านทักษะใช้สำหรับ Candidate


class UserSkill(Base):
    __tablename__ = 'app_user_skill'
    skill_profile_id = Column(Integer, primary_key=True)
    skill_profile_detail = Column(String(256), nullable=True)
    create_date = Column(DateTime)
    udp_date = Column(DateTime)
    skill_id = Column(Integer, ForeignKey(
        "app_masterdata_skill.skill_id", ondelete="CASCADE"))
    user_id = Column(String(128), ForeignKey(
        "app_user.user_id", ondelete="CASCADE"))

    skill_profile_child = relationship(
        "Skill", back_populates="skill_profile_parent")

# portfolio_type 1 = PDF , 2 = Youtube Link


class UserPortfolio(Base):
    __tablename__ = 'app_user_portfolio'
    portfolio_id = Column(Integer, primary_key=True)
    portfolio_name = Column(String(128), nullable=True)
    portfolio_path = Column(String(128), nullable=True)
    portfolio_type = Column(Integer, default=0)
    active = Column(Integer, default=1)
    create_date = Column(DateTime)
    udp_date = Column(DateTime)
    user_id = Column(String(128), ForeignKey(
        "app_user.user_id", ondelete="CASCADE"))
