#!/usr/bin/env python3
"""Database seeding script for Agent Router API."""

import asyncio
import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models import Agent, Feature, Role, Route, Condition
from app.config import settings


async def seed_database():
    """Seed the database with sample data."""
    print("🌱 Starting database seeding...")
    
    async for session in get_db():
        try:
            # Check if data already exists
            existing_agents = await session.execute(select(Agent))
            if existing_agents.scalars().first():
                print("⚠️  Database already contains data. Skipping seeding.")
                return
            
            print("📝 Creating sample agents...")
            agents = [
                Agent(
                    id=uuid.uuid4(),
                    name="Claude Agent",
                    description="Anthropic's Claude AI assistant for complex reasoning tasks",
                    source_type="MCP",
                    endpoint="https://api.anthropic.com/v1/messages",
                    api_key="claude_api_key_123",
                    status="active",
                    health="healthy",
                    config_data={"model": "claude-3-sonnet", "max_tokens": 4000}
                ),
                Agent(
                    id=uuid.uuid4(),
                    name="GPT-4 Agent",
                    description="OpenAI's GPT-4 for general AI tasks and conversations",
                    source_type="MCP",
                    endpoint="https://api.openai.com/v1/chat/completions",
                    api_key="gpt_api_key_456",
                    status="active",
                    health="healthy",
                    config_data={"model": "gpt-4", "temperature": 0.7}
                ),
                Agent(
                    id=uuid.uuid4(),
                    name="Code Assistant",
                    description="Specialized agent for code generation and review",
                    source_type="A2A",
                    endpoint="https://code-assistant.example.com/api",
                    api_key="code_api_key_789",
                    status="active",
                    health="healthy",
                    config_data={"languages": ["python", "javascript", "typescript"]}
                ),
                Agent(
                    id=uuid.uuid4(),
                    name="Data Analyst",
                    description="Agent specialized in data analysis and visualization",
                    source_type="WORKFLOW",
                    endpoint="https://data-analyst.example.com/api",
                    api_key="data_api_key_101",
                    status="active",
                    health="healthy",
                    config_data={"tools": ["pandas", "matplotlib", "seaborn"]}
                ),
                Agent(
                    id=uuid.uuid4(),
                    name="Document Processor",
                    description="Agent for processing and analyzing documents",
                    source_type="MCP",
                    endpoint="https://doc-processor.example.com/api",
                    api_key="doc_api_key_202",
                    status="inactive",
                    health="unhealthy",
                    config_data={"supported_formats": ["pdf", "docx", "txt"]}
                )
            ]
            
            print("📝 Creating sample features...")
            features = [
                Feature(
                    id=uuid.uuid4(),
                    name="User Authentication",
                    description="Handle user login, registration, and session management",
                    store_type="HTTP_JSON",
                    url="https://auth-service.example.com/features",
                    token="auth_token_123",
                    status="active",
                    config_data={"endpoints": ["/login", "/register", "/logout"]}
                ),
                Feature(
                    id=uuid.uuid4(),
                    name="File Upload",
                    description="Upload and manage files with various formats",
                    store_type="S3",
                    url="s3://file-storage-bucket/features",
                    token="s3_token_456",
                    status="active",
                    config_data={"max_size": "10MB", "allowed_types": ["jpg", "png", "pdf"]}
                ),
                Feature(
                    id=uuid.uuid4(),
                    name="Email Notifications",
                    description="Send email notifications to users",
                    store_type="HTTP_JSON",
                    url="https://email-service.example.com/features",
                    token="email_token_789",
                    status="active",
                    config_data={"templates": ["welcome", "reset_password", "notification"]}
                ),
                Feature(
                    id=uuid.uuid4(),
                    name="Data Export",
                    description="Export data in various formats (CSV, JSON, Excel)",
                    store_type="GIT",
                    url="https://github.com/example/data-export-features",
                    token="git_token_101",
                    status="active",
                    config_data={"formats": ["csv", "json", "xlsx"], "batch_size": 1000}
                ),
                Feature(
                    id=uuid.uuid4(),
                    name="Real-time Chat",
                    description="Real-time messaging and chat functionality",
                    store_type="HTTP_JSON",
                    url="https://chat-service.example.com/features",
                    token="chat_token_202",
                    status="inactive",
                    config_data={"websocket": True, "rooms": True}
                ),
                Feature(
                    id=uuid.uuid4(),
                    name="Payment Processing",
                    description="Process payments with multiple payment gateways",
                    store_type="HTTP_JSON",
                    url="https://payment-service.example.com/features",
                    token="payment_token_303",
                    status="active",
                    config_data={"gateways": ["stripe", "paypal", "square"]}
                )
            ]
            
            print("📝 Creating sample roles...")
            roles = [
                Role(
                    id=uuid.uuid4(),
                    name="Program Author",
                    description="Can create and manage programs and content",
                    permissions=["create_program", "edit_program", "delete_program"],
                    is_custom=True,
                    source="CUSTOM"
                ),
                Role(
                    id=uuid.uuid4(),
                    name="Learner",
                    description="Can access and participate in learning programs",
                    permissions=["view_program", "submit_assignment", "view_progress"],
                    is_custom=True,
                    source="CUSTOM"
                ),
                Role(
                    id=uuid.uuid4(),
                    name="Reviewer",
                    description="Can review and approve content and submissions",
                    permissions=["review_content", "approve_submission", "provide_feedback"],
                    is_custom=True,
                    source="CUSTOM"
                ),
                Role(
                    id=uuid.uuid4(),
                    name="Admin",
                    description="Full administrative access to the system",
                    permissions=["*"],
                    is_custom=True,
                    source="CUSTOM"
                ),
                Role(
                    id=uuid.uuid4(),
                    name="Manager",
                    description="Can manage teams and oversee operations",
                    permissions=["manage_team", "view_reports", "assign_tasks"],
                    is_custom=True,
                    source="CUSTOM"
                ),
                Role(
                    id=uuid.uuid4(),
                    name="Guest",
                    description="Limited access for guest users",
                    permissions=["view_public_content"],
                    is_custom=True,
                    source="CUSTOM"
                ),
                Role(
                    id=uuid.uuid4(),
                    name="EC2FullAccess",
                    description="Full access to EC2 instances",
                    permissions=["ec2:*"],
                    is_custom=False,
                    source="AWS"
                ),
                Role(
                    id=uuid.uuid4(),
                    name="S3ReadOnlyAccess",
                    description="Read-only access to S3 buckets",
                    permissions=["s3:GetObject", "s3:ListBucket"],
                    is_custom=False,
                    source="AWS"
                )
            ]
            
            # Add all entities to session
            session.add_all(agents)
            session.add_all(features)
            session.add_all(roles)
            
            # Commit to get IDs
            await session.commit()
            
            print("📝 Creating sample routes...")
            # Create some sample routes
            routes = [
                Route(
                    id=uuid.uuid4(),
                    feature_id=features[0].id,  # User Authentication
                    agent_id=agents[0].id,      # Claude Agent
                    rules={"allowAll": True, "allowed": [], "disallowed": []},
                    conditional=False,
                    status="active"
                ),
                Route(
                    id=uuid.uuid4(),
                    feature_id=features[1].id,  # File Upload
                    agent_id=agents[2].id,      # Code Assistant
                    rules={"allowAll": False, "allowed": ["Admin", "Manager"], "disallowed": ["Guest"]},
                    conditional=False,
                    status="active"
                ),
                Route(
                    id=uuid.uuid4(),
                    feature_id=features[2].id,  # Email Notifications
                    agent_id=agents[1].id,      # GPT-4 Agent
                    rules={"allowAll": True, "allowed": [], "disallowed": []},
                    conditional=False,
                    status="active"
                ),
                Route(
                    id=uuid.uuid4(),
                    feature_id=features[3].id,  # Data Export
                    agent_id=agents[3].id,      # Data Analyst
                    rules={"allowAll": False, "allowed": ["Admin", "Manager", "Reviewer"], "disallowed": ["Guest"]},
                    conditional=True,
                    status="active"
                )
            ]
            
            session.add_all(routes)
            await session.commit()
            
            print("📝 Creating sample conditions...")
            conditions = [
                Condition(
                    id=uuid.uuid4(),
                    name="Business Hours",
                    description="Only allow access during business hours (9 AM - 5 PM)",
                    condition_type="time_based",
                    condition_data={
                        "start_time": "09:00",
                        "end_time": "17:00",
                        "timezone": "UTC",
                        "days_of_week": ["monday", "tuesday", "wednesday", "thursday", "friday"]
                    }
                ),
                Condition(
                    id=uuid.uuid4(),
                    name="High Priority Users",
                    description="Allow access for high priority users regardless of time",
                    condition_type="role_based",
                    condition_data={
                        "allowed_roles": ["Admin", "Manager"],
                        "override_time_restrictions": True
                    }
                )
            ]
            
            session.add_all(conditions)
            await session.commit()
            
            print("✅ Database seeding completed successfully!")
            print(f"📊 Created {len(agents)} agents, {len(features)} features, {len(roles)} roles, {len(routes)} routes, and {len(conditions)} conditions")
            
        except Exception as e:
            print(f"❌ Error seeding database: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


if __name__ == "__main__":
    asyncio.run(seed_database())
