from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey, Boolean, Integer
from sqlalchemy.orm import declarative_base
import datetime
import uuid

Base = declarative_base()

def gen_id():
    return str(uuid.uuid4())

class Job(Base):
    __tablename__ = "jobs"
    id = Column(String, primary_key=True, default=gen_id)
    query = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class LogEvent(Base):
    __tablename__ = "logs"
    id = Column(String, primary_key=True, default=gen_id)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    job_id = Column(String, index=True)
    agent_id = Column(String)
    event_type = Column(String)
    input_hash = Column(String, nullable=True)
    output_hash = Column(String, nullable=True)
    latency_ms = Column(Float, nullable=True)
    token_count = Column(Integer, nullable=True)
    policy_violations = Column(String, nullable=True)
    details = Column(JSON, nullable=True)

class ToolCall(Base):
    __tablename__ = "tool_calls"
    id = Column(String, primary_key=True, default=gen_id)
    job_id = Column(String, index=True)
    agent_id = Column(String)
    tool_name = Column(String)
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    latency_ms = Column(Float, nullable=True)
    status = Column(String)
    retries = Column(Integer, default=0)

class EvaluationRun(Base):
    __tablename__ = "evaluations"
    id = Column(String, primary_key=True, default=gen_id)
    test_case_id = Column(String)
    run_id = Column(String)
    scores = Column(JSON)
    justification = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class PromptRewrite(Base):
    __tablename__ = "prompt_rewrites"
    id = Column(String, primary_key=True, default=gen_id)
    agent_id = Column(String)
    dimension = Column(String)
    content = Column(String)
    proposed_rewrite = Column(String)
    justification = Column(String)
    status = Column(String, default="pending") # pending, approved, rejected
