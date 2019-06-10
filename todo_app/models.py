from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from todo_app.db import engine


Base = declarative_base()


class CheckList(Base):
    __tablename__ = 'checklist'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    task_completed = Column(Boolean, default=False)
    checklist_id = Column(Integer, ForeignKey('checklist.id'))
    checklist = relationship('CheckList', back_populates='item')


CheckList.item = relationship('Item', order_by=Item.id, back_populates='checklist')
Base.metadata.create_all(engine)
