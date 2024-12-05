from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration
DATABASE_URI = "sqlite:///data/chat_data.db"
Base = declarative_base()
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the KnowledgeBase table
class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True)
    content = Column(Text)

# Initialize the database
def init_db():
    Base.metadata.create_all(bind=engine)

# Add sample data
def add_sample_data():
    session = SessionLocal()
    examples = [
        KnowledgeBase(topic="President of the United States", content="Joe Biden is the 46th president of the United States."),
        KnowledgeBase(topic="Capital of the United States", content="The capital of the United States is Washington, D.C."),
    ]
    session.add_all(examples)
    session.commit()
    session.close()