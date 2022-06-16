from sqlalchemy import Column, Integer, String

from database import Base


class Images(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    file = Column(String)
    file_name = Column(String)

    def __init__(self, file, file_name):
        self.file = file
        self.file_name = file_name

    def __repr__(self):
        return "<Image('%s')>" % (self.file_name)
