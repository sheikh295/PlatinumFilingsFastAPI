from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BigInteger
from db import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(BigInteger, index=True, primary_key=True)
    fei_no = Column(BigInteger, index=True)
    address = Column(String, index=True)
    registered_agent = Column(Boolean, index=True)
    agent_name = Column(String, index=True)
    agent_address = Column(String, index=True)
    authorized_manager = Column(String, index=True)
    authorized_manager_two = Column(String, index=True)
    authorized_manager_three = Column(String, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone_no = Column(BigInteger, index=True)
    certificate = Column(Boolean, index=True)
    signing_officer_name = Column(String, index=True)
    signing_officer_signature = Column(String, index=True)
    signing_officer_title = Column(String, index=True)
    business_entity = Column(String, index=True)