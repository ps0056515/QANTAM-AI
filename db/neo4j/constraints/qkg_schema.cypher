// QANTAM Quality Knowledge Graph (QKG) Schema
// Neo4j constraints and indexes for multi-tenant intelligence graph

// ============================================
// CONSTRAINTS - Ensure data integrity
// ============================================

// Requirement uniqueness per tenant
CREATE CONSTRAINT requirement_unique IF NOT EXISTS
FOR (r:Requirement) REQUIRE (r.tenant_id, r.id) IS UNIQUE;

// TestCase uniqueness per tenant
CREATE CONSTRAINT testcase_unique IF NOT EXISTS
FOR (t:TestCase) REQUIRE (t.tenant_id, t.id) IS UNIQUE;

// Defect uniqueness per tenant
CREATE CONSTRAINT defect_unique IF NOT EXISTS
FOR (d:Defect) REQUIRE (d.tenant_id, d.id) IS UNIQUE;

// CodeModule uniqueness per tenant
CREATE CONSTRAINT codemodule_unique IF NOT EXISTS
FOR (m:CodeModule) REQUIRE (m.tenant_id, m.name) IS UNIQUE;

// RegulatoryClause uniqueness
CREATE CONSTRAINT regulation_unique IF NOT EXISTS
FOR (rc:RegulatoryClause) REQUIRE (rc.framework, rc.clause_id) IS UNIQUE;

// ============================================
// INDEXES - Query performance
// ============================================

// Tenant isolation - CRITICAL for security
CREATE INDEX requirement_tenant IF NOT EXISTS
FOR (r:Requirement) ON (r.tenant_id);

CREATE INDEX testcase_tenant IF NOT EXISTS
FOR (t:TestCase) ON (t.tenant_id);

CREATE INDEX defect_tenant IF NOT EXISTS
FOR (d:Defect) ON (d.tenant_id);

// Traceability seed - links requirements to test cases
CREATE INDEX requirement_seed IF NOT EXISTS
FOR (r:Requirement) ON (r.traceability_seed);

CREATE INDEX testcase_seed IF NOT EXISTS
FOR (t:TestCase) ON (t.traceability_seed);

// Project scoping
CREATE INDEX requirement_project IF NOT EXISTS
FOR (r:Requirement) ON (r.project_id);

// Status filtering
CREATE INDEX testcase_status IF NOT EXISTS
FOR (t:TestCase) ON (t.approval_status);

CREATE INDEX defect_severity IF NOT EXISTS
FOR (d:Defect) ON (d.severity);

// ============================================
// SAMPLE NODE STRUCTURES (for reference)
// ============================================

// (:Requirement {
//   id: UUID,
//   tenant_id: UUID,
//   project_id: UUID,
//   traceability_seed: UUID,
//   source_system: "jira" | "ado" | "confluence" | "upload",
//   source_id: String,
//   text: String,
//   rqs_score: Float,
//   status: "ingested" | "analysed" | "approved",
//   created_at: DateTime
// })

// (:TestCase {
//   id: UUID,
//   tenant_id: UUID,
//   traceability_seed: UUID,
//   title: String,
//   steps: [String],
//   expected_result: String,
//   type: "positive" | "negative" | "edge" | "compliance",
//   confidence_score: Float,
//   approval_status: "pending" | "approved" | "edited" | "rejected",
//   prompt_version: String,
//   created_at: DateTime
// })

// (:Defect {
//   id: UUID,
//   tenant_id: UUID,
//   source_id: String,
//   severity: "P0" | "P1" | "P2" | "P3",
//   category: "ui" | "logic" | "data" | "performance" | "security",
//   root_cause_module: String,
//   resolution_time: Integer,
//   created_at: DateTime
// })

// ============================================
// KEY RELATIONSHIPS
// ============================================

// (:Requirement)-[:REQUIRES_TESTING]->(:TestCase)
// (:Requirement)-[:HAS_FLAG]->(:Flag)
// (:TestCase)-[:COVERS]->(:CodeModule)
// (:CodeModule)-[:HAS_DEFECT]->(:Defect)
// (:Requirement)-[:MAPS_TO_REGULATION]->(:RegulatoryClause)
// (:Defect)-[:ESCAPED_AS]->(:ProductionIncident)
// (:ProductionIncident)-[:TRACED_TO_GAP_IN]->(:TestCase)
