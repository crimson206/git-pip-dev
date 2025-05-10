from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()


# 모델 정의
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # 관계 설정
    packages = relationship("Package", back_populates="owner")

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"


class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, index=True)
    repository = Column(String(255), nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    # 관계 설정
    owner = relationship("User", back_populates="packages")
    categories = relationship("Category", back_populates="module")

    def __repr__(self):
        return f"<Package(name='{self.name}', repository='{self.repository}')>"


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    module_id = Column(Integer, ForeignKey("packages.id"), nullable=False)
    index_url = Column(String(255))
    assembled = Column(Boolean, default=True)

    # 관계 설정
    module = relationship("Package", back_populates="categories")
    releases = relationship("Release", back_populates="category")

    def __repr__(self):
        return f"<Category(name='{self.name}', assembled={self.assembled})>"


class Release(Base):
    __tablename__ = "releases"

    id = Column(Integer, primary_key=True)
    version = Column(String(50), nullable=False)
    commit = Column(String(40), nullable=False)  # commit hash
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # 관계 설정
    category = relationship("Category", back_populates="releases")

    def __repr__(self):
        return f"<Release(version='{self.version}', commit='{self.commit}')>"
