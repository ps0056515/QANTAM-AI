"""
SIGNAL Service - Release Quality Score Business Logic
"""
from uuid import UUID
from typing import Optional
from dataclasses import dataclass

from graph.connection import get_neo4j_session
from ai.router import llm_call


@dataclass
class ReleaseData:
    total_requirements: int
    tested_requirements: int
    open_p0: int
    open_p1: int
    open_p2: int
    tests_passed: int
    tests_executed: int
    avg_rqs: float


@dataclass
class RQSResult:
    score: float
    go_nogo: str
    breakdown: dict


class SignalService:
    """Service for release quality scoring and documentation."""

    async def calculate_rqs(self, release_id: UUID, tenant_id: UUID) -> RQSResult:
        """Calculate Release Quality Score."""
        # Fetch release data from QKG
        data = await self._get_release_data(release_id, tenant_id)
        
        # Coverage score (35% weight)
        if data.total_requirements > 0:
            coverage = (data.tested_requirements / data.total_requirements) * 100
        else:
            coverage = 0
        coverage_score = min(coverage, 100) * 0.35

        # Defect score (30% weight) - penalise open high-severity
        defect_penalty = (data.open_p0 * 30 + data.open_p1 * 15 + data.open_p2 * 5)
        defect_score = max(0, 100 - defect_penalty) * 0.30

        # Test execution score (25% weight)
        if data.tests_executed > 0:
            pass_rate = (data.tests_passed / data.tests_executed) * 100
        else:
            pass_rate = 0
        test_score = pass_rate * 0.25

        # CLARITY quality score (10% weight)
        clarity_score = data.avg_rqs * 0.10

        total = coverage_score + defect_score + test_score + clarity_score
        
        if total > 80:
            go_nogo = "GO"
        elif total > 60:
            go_nogo = "CONDITIONAL"
        else:
            go_nogo = "NO-GO"

        return RQSResult(
            score=round(total, 1),
            go_nogo=go_nogo,
            breakdown={
                "coverage_score": round(coverage_score, 1),
                "defect_score": round(defect_score, 1),
                "test_score": round(test_score, 1),
                "clarity_score": round(clarity_score, 1)
            }
        )

    async def get_decision(self, release_id: UUID, tenant_id: UUID) -> Optional[dict]:
        """Get Go/No-Go decision with evidence."""
        rqs = await self.calculate_rqs(release_id, tenant_id)
        
        evidence = []
        blocking_issues = []
        required_actions = []
        
        # Analyze breakdown for evidence
        if rqs.breakdown['coverage_score'] < 30:
            blocking_issues.append("Test coverage below 85%")
            required_actions.append("Add test cases for uncovered requirements")
        
        if rqs.breakdown['defect_score'] < 25:
            blocking_issues.append("Open P0/P1 defects")
            required_actions.append("Resolve critical defects before release")
        
        if rqs.breakdown['test_score'] < 20:
            blocking_issues.append("Test pass rate below 80%")
            required_actions.append("Fix failing tests or investigate root cause")
        
        return {
            "release_id": str(release_id),
            "score": rqs.score,
            "decision": rqs.go_nogo,
            "breakdown": rqs.breakdown,
            "evidence": evidence,
            "blocking_issues": blocking_issues,
            "required_actions": required_actions
        }

    async def generate_documents(
        self,
        release_id: UUID,
        tenant_id: UUID,
        doc_types: list[str]
    ) -> list[dict]:
        """Generate release documentation suite."""
        documents = []
        
        for doc_type in doc_types:
            if doc_type == "test_summary":
                doc = await self._generate_test_summary(release_id, tenant_id)
            elif doc_type == "defect_summary":
                doc = await self._generate_defect_summary(release_id, tenant_id)
            elif doc_type == "executive_briefing":
                doc = await self._generate_executive_briefing(release_id, tenant_id)
            elif doc_type == "compliance_evidence":
                doc = await self._generate_compliance_evidence(release_id, tenant_id)
            elif doc_type == "release_certificate":
                doc = await self._generate_release_certificate(release_id, tenant_id)
            else:
                continue
            
            documents.append(doc)
        
        return documents

    async def get_history(self, release_id: UUID, tenant_id: UUID) -> dict:
        """Get historical RQS scores for comparison."""
        # TODO: Fetch from PostgreSQL audit logs
        return {"history": []}

    async def _get_release_data(self, release_id: UUID, tenant_id: UUID) -> ReleaseData:
        """Fetch release data from QKG."""
        async with get_neo4j_session() as session:
            result = await session.run(
                """
                MATCH (rel:Release {id: $release_id, tenant_id: $tenant_id})
                OPTIONAL MATCH (rel)-[:INCLUDES]->(req:Requirement)
                OPTIONAL MATCH (req)-[:REQUIRES_TESTING]->(tc:TestCase {approval_status: 'approved'})
                OPTIONAL MATCH (rel)-[:HAS_DEFECT]->(d:Defect)
                WITH rel, 
                     count(DISTINCT req) as total_reqs,
                     count(DISTINCT tc) as tested_reqs,
                     sum(CASE WHEN d.severity = 'P0' AND d.status = 'open' THEN 1 ELSE 0 END) as p0,
                     sum(CASE WHEN d.severity = 'P1' AND d.status = 'open' THEN 1 ELSE 0 END) as p1,
                     sum(CASE WHEN d.severity = 'P2' AND d.status = 'open' THEN 1 ELSE 0 END) as p2,
                     avg(req.rqs_score) as avg_rqs
                RETURN total_reqs, tested_reqs, p0, p1, p2, avg_rqs
                """,
                release_id=str(release_id),
                tenant_id=str(tenant_id)
            )
            record = await result.single()
            
            if not record:
                return ReleaseData(0, 0, 0, 0, 0, 0, 0, 0)
            
            return ReleaseData(
                total_requirements=record['total_reqs'] or 0,
                tested_requirements=record['tested_reqs'] or 0,
                open_p0=record['p0'] or 0,
                open_p1=record['p1'] or 0,
                open_p2=record['p2'] or 0,
                tests_passed=0,  # TODO: Integrate test execution results
                tests_executed=0,
                avg_rqs=record['avg_rqs'] or 100
            )

    async def _generate_test_summary(self, release_id: UUID, tenant_id: UUID) -> dict:
        """Generate test summary report."""
        # Use local LLM for report formatting
        prompt = f"Generate a test summary report for release {release_id}"
        response = await llm_call("report_formatting", prompt)
        
        return {
            "type": "test_summary",
            "title": "Test Summary Report",
            "content": response.content,
            "url": f"https://storage.qantam.ai/reports/{release_id}/test_summary.pdf"
        }

    async def _generate_defect_summary(self, release_id: UUID, tenant_id: UUID) -> dict:
        """Generate defect summary report."""
        return {
            "type": "defect_summary",
            "title": "Defect Summary Report",
            "url": f"https://storage.qantam.ai/reports/{release_id}/defect_summary.pdf"
        }

    async def _generate_executive_briefing(self, release_id: UUID, tenant_id: UUID) -> dict:
        """Generate executive briefing."""
        return {
            "type": "executive_briefing",
            "title": "Executive Briefing",
            "url": f"https://storage.qantam.ai/reports/{release_id}/executive_briefing.pdf"
        }

    async def _generate_compliance_evidence(self, release_id: UUID, tenant_id: UUID) -> dict:
        """Generate compliance evidence package."""
        return {
            "type": "compliance_evidence",
            "title": "Compliance Evidence Package",
            "url": f"https://storage.qantam.ai/reports/{release_id}/compliance_evidence.pdf"
        }

    async def _generate_release_certificate(self, release_id: UUID, tenant_id: UUID) -> dict:
        """Generate release certificate."""
        return {
            "type": "release_certificate",
            "title": "Release Certificate",
            "url": f"https://storage.qantam.ai/reports/{release_id}/release_certificate.pdf"
        }
