"""
CLARITY Service - Requirement Intelligence Business Logic
"""
from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime

from graph.connection import get_neo4j_session
from ai.router import llm_call
from ai.prompts.clarity.ambiguity_v1 import build_prompt as build_ambiguity_prompt


class ClarityService:
    """Service for requirement analysis and intelligence."""

    async def start_analysis(
        self,
        project_id: UUID,
        tenant_id: UUID,
        source: str,
        content: Optional[str] = None,
        source_id: Optional[str] = None
    ) -> UUID:
        """Start async requirement analysis job."""
        task_id = uuid4()
        
        # TODO: Push to Redis task queue
        # For now, return task_id for polling
        
        return task_id

    async def ingest_document(
        self,
        project_id: UUID,
        tenant_id: UUID,
        filename: str,
        content: bytes
    ) -> UUID:
        """Ingest and parse uploaded document."""
        task_id = uuid4()
        
        # Parse document based on type
        if filename.endswith('.docx'):
            text = self._parse_docx(content)
        elif filename.endswith('.pdf'):
            text = self._parse_pdf(content)
        else:
            text = content.decode('utf-8')
        
        # Chunk into requirements
        requirements = self._chunk_requirements(text)
        
        # Create QKG nodes
        for req in requirements:
            await self._create_requirement_node(
                tenant_id=tenant_id,
                project_id=project_id,
                text=req,
                source="upload",
                source_id=filename
            )
        
        return task_id

    async def sync_jira(
        self,
        project_id: UUID,
        tenant_id: UUID,
        jira_project_key: str
    ) -> UUID:
        """Sync requirements from Jira project."""
        task_id = uuid4()
        # TODO: Implement Jira OAuth and sync
        return task_id

    async def analyse_requirement(
        self,
        requirement_id: UUID,
        tenant_id: UUID
    ) -> dict:
        """Run AI analysis on a single requirement."""
        # Fetch requirement from QKG
        req = await self._get_requirement(requirement_id, tenant_id)
        if not req:
            return None
        
        # Run ambiguity detection
        prompt = build_ambiguity_prompt(req['text'])
        response = await llm_call("ambiguity_detection", prompt)
        
        # Parse and store flags
        # TODO: Parse JSON response and create Flag nodes
        
        return {
            "requirement_id": requirement_id,
            "flags": [],
            "rqs_score": 100
        }

    async def get_results(self, result_id: UUID, tenant_id: UUID) -> Optional[dict]:
        """Get analysis results."""
        # TODO: Fetch from QKG
        return None

    async def update_flag_status(
        self,
        flag_id: UUID,
        tenant_id: UUID,
        status: str
    ) -> None:
        """Update flag status (approve/dismiss)."""
        async with get_neo4j_session() as session:
            await session.run(
                """
                MATCH (f:Flag {id: $flag_id, tenant_id: $tenant_id})
                SET f.status = $status, f.updated_at = datetime()
                """,
                flag_id=str(flag_id),
                tenant_id=str(tenant_id),
                status=status
            )

    async def generate_health_report(
        self,
        project_id: UUID,
        tenant_id: UUID
    ) -> str:
        """Generate Requirement Health Report PDF."""
        # TODO: Generate PDF and upload to MinIO
        return "https://storage.qantam.ai/reports/placeholder.pdf"

    async def _create_requirement_node(
        self,
        tenant_id: UUID,
        project_id: UUID,
        text: str,
        source: str,
        source_id: str
    ) -> UUID:
        """Create requirement node in QKG."""
        req_id = uuid4()
        traceability_seed = uuid4()
        
        async with get_neo4j_session() as session:
            await session.run(
                """
                CREATE (r:Requirement {
                    id: $id,
                    tenant_id: $tenant_id,
                    project_id: $project_id,
                    traceability_seed: $seed,
                    text: $text,
                    source_system: $source,
                    source_id: $source_id,
                    rqs_score: 100,
                    status: 'ingested',
                    created_at: datetime()
                })
                """,
                id=str(req_id),
                tenant_id=str(tenant_id),
                project_id=str(project_id),
                seed=str(traceability_seed),
                text=text,
                source=source,
                source_id=source_id
            )
        
        return req_id

    async def _get_requirement(self, req_id: UUID, tenant_id: UUID) -> Optional[dict]:
        """Fetch requirement from QKG."""
        async with get_neo4j_session() as session:
            result = await session.run(
                """
                MATCH (r:Requirement {id: $id, tenant_id: $tenant_id})
                RETURN r
                """,
                id=str(req_id),
                tenant_id=str(tenant_id)
            )
            record = await result.single()
            return dict(record['r']) if record else None

    def _parse_docx(self, content: bytes) -> str:
        """Parse Word document."""
        from io import BytesIO
        from docx import Document
        doc = Document(BytesIO(content))
        return '\n'.join([p.text for p in doc.paragraphs])

    def _parse_pdf(self, content: bytes) -> str:
        """Parse PDF document."""
        from io import BytesIO
        from pypdf import PdfReader
        reader = PdfReader(BytesIO(content))
        return '\n'.join([page.extract_text() for page in reader.pages])

    def _chunk_requirements(self, text: str) -> list[str]:
        """Split document into individual requirements."""
        # Simple chunking by paragraph for now
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        return [p for p in paragraphs if len(p) > 20]
