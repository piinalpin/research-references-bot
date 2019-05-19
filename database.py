from sqlalchemy import create_engine, Table, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Query(Base):

    __tablename__ = "query"
    id = Column(Integer, primary_key=True, nullable=False)
    query_name = Column(String(255), nullable=False)

    def __init__(self, query):
        self.query_name = query

    def save(self):
        session.add(self)
        session.commit()

    @staticmethod
    def get_by_query(query):
        data = session.query(Query).filter(Query.query_name.like("%{}%".format(query))).first()
        if data is not None:
            result = {
                "id": data.id,
                "query": data.query_name,
                "details": Details.get_by_query_id(data.id)
            }
        else:
            result = None
        return result


class Details(Base):

    __tablename__ = "details"

    id = Column(Integer, primary_key=True, nullable=False)
    author = Column(String(255), nullable=False)
    title = Column(String(1028), nullable=False)
    url = Column(String(1028), nullable=False)
    year = Column(String(1028), nullable=False)
    score = Column(Float, nullable=False)
    query_id = Column(Integer, nullable=False)

    def __init__(self, author, title, url, year, score, query_id):
        self.author = author
        self.title = title
        self.url = url
        self.year = year
        self.score = score
        self.query_id = query_id

    def save(self):
        session.add(self)
        session.commit()

    @staticmethod
    def get_by_query_id(query_id):
        data = session.query(Details).filter_by(query_id=query_id).order_by(Details.score.desc()).limit(5).all()
        result = list()
        for x in data:
            obj = {
                "id": x.id,
                "author": x.author,
                "title": x.title,
                "url": x.url,
                "year": x.year,
                "score": x.score,
                "query_id": x.query_id
            }
            result.append(obj)
        return result
