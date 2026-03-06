"""
PULSE Service - Test Suite Factory Business Logic
"""
from uuid import UUID, uuid4
from typing import Optional

from graph.connection import get_neo4j_session
from ai.router import llm_call
from ai.prompts.pulse.test_generation_v1 import build_prompt as build_test_prompt


class PulseService:
    """Service for test case generation and management."""

    async def start_generation(
        self,
        requirement_ids: list,
        tenant_id: UUID,
        test_types: list
    ) -> UUID:
        """Start async test generation job."""
        task_id = uuid4()
        return task_id

    async def generate_for_requirement(
        self,
        requirement_id: UUID,
        tenant_id: UUID,
        test_types: list
    ) -> list:
        """Generate test cases for a single requirement."""
        req = await self._get_requirement_with_context(requirement_id, tenant_id)
        if not req:
            return []
        
        prompt = build_test_prompt(
            requirement_text=req['text'],
            clarity_flags=req.get('flags', []),
            regulatory_clauses=req.get('regulatory_clauses', []),
            test_types=test_types
        )
        
        response = await llm_call("test_generation", prompt)
        test_cases = self._parse_test_cases(response.content)
        
        return test_cases

    async def get_results(self, result_id: UUID, tenant_id: UUID) -> Optional[list]:
        """Get generated test cases."""
        return None

    async def review_test_case(
        self,
        test_id: UUID,
        tenant_id: UUID,
        action: str,
        edited_content: Optional[str],
        user_id: UUID
    ) -> None:
        """Process human review of test case."""
        async with get_neo4j_session() as session:
            await session.run(
                """
                MATCH (t:TestCase {id: $id, tenant_id: $tenant_id})
                SET t.approval_status = $status,
                    t.reviewed_by = $user_id,
                    t.reviewed_at = datetime()
                """,
                id=str(test_id),
                tenant_id=str(tenant_id),
                status=action,
                user_id=str(user_id)
            )

    async def export_file(
        self,
        test_ids: list,
        tenant_id: UUID,
        format: str
    ) -> str:
        """Export test cases to file."""
        return f"https://storage.qantam.ai/exports/test_cases.{format}"

    async def push_to_jira(self, test_ids: list, tenant_id: UUID) -> list:
        """Push approved test cases to Jira Zephyr."""
        return []

    async def get_coverage(self, project_id: UUID, tenant_id: UUID) -> dict:
        """Calculate test coverage for project."""
        return {
            "total_requirements": 0,
            "covered_requirements": 0,
            "coverage_percentage": 0
        }

    async def get_roi_metrics(self, project_id: UUID, tenant_id: UUID) -> dict:
        """Calculate ROI metrics."""
        return {
            "total_generated": 0,
            "approved": 0,
            "edited": 0,
            "rejected": 0,
            "approval_rate": 0,
            "hours_saved": 0
        }

    async def _get_requirement_with_context(
        self,
        req_id: UUID,
        tenant_id: UUID
    ) -> Optional[dict]:
        """Fetch requirement with CLARITY flags from QKG."""
        async with get_neo4j_session() as session:
            result = await session.run(
                """
                MATCH (r:Requirement {id: $id, tenant_id: $tenant_id})
                OPTIONAL MATCH (r)-[:HAS_FLAG]->(f:Flag)
                RETURN r, collect(f) as flags
                """,
                id=str(req_id),
                tenant_id=str(tenant_id)
            )
            record = await result.single()
            if not record:
                return None
            
            req = dict(record['r'])
            req['flags'] = [dict(f) for f in record['flags'] if f]
            return req

    def _parse_test_cases(self, content: str) -> list:
        """Parse LLM response into test cases."""
        import json
        try:
            data = json.loads(content)
            return data.get('test_cases', [])
        except json.JSONDecodeError:
            return []
