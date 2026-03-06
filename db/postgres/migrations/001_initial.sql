-- QANTAM PostgreSQL Schema - Initial Migration

CREATE TABLE IF NOT EXISTS tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    plan VARCHAR(50) DEFAULT 'design_partner',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_tenant ON users(tenant_id);

CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    jira_config JSONB,
    ado_config JSONB,
    github_config JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_projects_tenant ON projects(tenant_id);

CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100),
    entity_type VARCHAR(100),
    entity_id UUID,
    ai_output JSONB,
    confidence_score DECIMAL(5,2),
    human_action VARCHAR(50),
    edited_content JSONB,
    prompt_version VARCHAR(50),
    model_used VARCHAR(100),
    latency_ms INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_audit_tenant ON audit_logs(tenant_id);

CREATE TABLE IF NOT EXISTS roi_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    hours_saved DECIMAL(10,2),
    cases_generated INTEGER,
    cases_approved INTEGER,
    issues_flagged INTEGER,
    issues_confirmed INTEGER,
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    task_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    progress INTEGER DEFAULT 0,
    payload JSONB,
    result_id UUID,
    error TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_tasks_tenant ON tasks(tenant_id);
CREATE INDEX idx_tasks_status ON tasks(status);
