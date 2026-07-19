from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum, DateTime, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
import enum
from database import Base

class IndicatorTypeEnum(str, enum.Enum):
    IP = "IP"
    DOMAIN = "DOMAIN"
    URL = "URL"
    HASH = "HASH"


class ThreatIntelCache(Base):
    __tablename__ = "threat_intel_cache"

    indicator = Column(String(2048), primary_key=True, index=True)
    indicator_type = Column(SQLAlchemyEnum(IndicatorTypeEnum), nullable=False)
    is_malicious = Column(Boolean, nullable=False, default=False)
    overall_score = Column(Integer, nullable=False, default=0)
    raw_data = Column(JSONB, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
