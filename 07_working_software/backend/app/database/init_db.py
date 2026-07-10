"""Creates all tables and inserts seed/demo data. Run with: python -m app.database.init_db"""

import json
import uuid
from datetime import datetime, timedelta

from app.api.security import hash_password
from app.database.models import (
    Base,
    ChatMessage,
    Conflict,
    ConversationHistory,
    Customer,
    Document,
    Recommendation,
)
from app.database.session import SessionLocal, engine


def _uuid() -> str:
    return str(uuid.uuid4())


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        if db.query(Customer).count() > 0:
            print("Database already seeded, skipping.")
            return

        analyst = Customer(
            customer_id=_uuid(), email="analyst@acme.com", name="Priya Sharma",
            organization="Acme Corp", role="user", hashed_password=hash_password("Password123"),
        )
        knowledge_manager = Customer(
            customer_id=_uuid(), email="kmanager@acme.com", name="Raj Mehta",
            organization="Acme Corp", role="user", hashed_password=hash_password("Password123"),
        )
        admin = Customer(
            customer_id=_uuid(), email="admin@acme.com", name="System Admin",
            organization="Acme Corp", role="admin", hashed_password=hash_password("Password123"),
        )
        db.add_all([analyst, knowledge_manager, admin])
        db.flush()

        documents = [
            Document(
                document_id=_uuid(), customer_id=analyst.customer_id,
                file_name="remote_work_policy_2024.pdf", file_path="/data/documents/seed_1.pdf",
                file_size=204800, file_type="pdf", status="indexed", total_chunks=12,
                indexed_date=datetime.utcnow(), doc_metadata=json.dumps({"title": "Remote Work Policy 2024"}),
            ),
            Document(
                document_id=_uuid(), customer_id=analyst.customer_id,
                file_name="remote_work_policy_2025.pdf", file_path="/data/documents/seed_2.pdf",
                file_size=215040, file_type="pdf", status="indexed", total_chunks=13,
                indexed_date=datetime.utcnow(), doc_metadata=json.dumps({"title": "Remote Work Policy 2025"}),
            ),
            Document(
                document_id=_uuid(), customer_id=analyst.customer_id,
                file_name="q2_vendor_risk_report.xlsx", file_path="/data/documents/seed_3.xlsx",
                file_size=512000, file_type="xlsx", status="indexed", total_chunks=28,
                indexed_date=datetime.utcnow(), doc_metadata=json.dumps({"title": "Q2 Vendor Risk Report"}),
            ),
            Document(
                document_id=_uuid(), customer_id=knowledge_manager.customer_id,
                file_name="board_meeting_notes.eml", file_path="/data/documents/seed_4.eml",
                file_size=40960, file_type="eml", status="indexed", total_chunks=4,
                indexed_date=datetime.utcnow(), doc_metadata=json.dumps({"title": "Board Meeting Notes"}),
            ),
            Document(
                document_id=_uuid(), customer_id=knowledge_manager.customer_id,
                file_name="vendor_onboarding_deck.pptx", file_path="/data/documents/seed_5.pptx",
                file_size=3145728, file_type="pptx", status="processing", total_chunks=0,
                doc_metadata=json.dumps({"title": "Vendor Onboarding Deck"}),
            ),
        ]
        db.add_all(documents)
        db.flush()

        conversation = ConversationHistory(
            conversation_id=_uuid(), customer_id=analyst.customer_id, title="Q2 Vendor Risk Review"
        )
        db.add(conversation)
        db.flush()

        db.add_all(
            [
                ChatMessage(
                    message_id=_uuid(), conversation_id=conversation.conversation_id, sender_type="user",
                    message_text="What's our vendor risk exposure this quarter?",
                ),
                ChatMessage(
                    message_id=_uuid(), conversation_id=conversation.conversation_id, sender_type="assistant",
                    message_text="2 vendors are flagged as high-risk in the Q2 report due to contract "
                                 "renewal gaps and compliance lapses.",
                    sources=json.dumps(
                        [{"document_id": documents[2].document_id, "document_name": documents[2].file_name,
                          "snippet": "Vendor X: compliance lapse noted...", "relevance_score": 0.91}]
                    ),
                    confidence_score=0.87,
                ),
            ]
        )

        db.add(
            Conflict(
                conflict_id=_uuid(), conversation_id=conversation.conversation_id,
                customer_id=analyst.customer_id,
                conflict_description="Remote work days differ: 2024 policy allows 2 days/week, "
                                      "2025 policy allows 3 days/week.",
                source_documents=json.dumps([documents[0].document_id, documents[1].document_id]),
                severity="medium", resolved=False,
            )
        )

        db.add(
            Recommendation(
                recommendation_id=_uuid(), conversation_id=conversation.conversation_id,
                customer_id=analyst.customer_id,
                recommendation_text="Schedule a review with Procurement — 2 vendors flagged as high-risk in Q2 report.",
                confidence_score=0.87,
                supporting_documents=json.dumps([documents[2].document_id]),
                status="pending",
            )
        )

        db.commit()
        print("Seed data inserted: 3 customers, 5 documents, 1 conversation, 1 conflict, 1 recommendation.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
