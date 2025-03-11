from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship, Session
from models.base import Base


class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    location = Column(String, nullable=False)
    action = Column(String, nullable=False)
    resolved = Column(Boolean, default=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=True)

    # Create relationship to Property model
    property = relationship("Property", back_populates="issues")

    def __repr__(self):
        return f"<Issue(id={self.id}, description='{self.description}', resolved={self.resolved})>"

    @staticmethod
    def create(db: Session, issue_data: dict):
        issue = Issue(**issue_data)
        db.add(issue)
        db.commit()
        db.refresh(issue)
        return issue

    @staticmethod
    def get(db: Session, issue_id: int):
        return db.query(Issue).filter(Issue.id == issue_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Issue).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, issue_id: int, issue_data: dict):
        issue = Issue.get(db, issue_id)
        if issue:
            for key, value in issue_data.items():
                setattr(issue, key, value)
            db.commit()
            db.refresh(issue)
        return issue

    @staticmethod
    def delete(db: Session, issue_id: int):
        issue = Issue.get(db, issue_id)
        if issue:
            db.delete(issue)
            db.commit()
            return True
        return False
