CREATE TABLE IF NOT EXISTS llm_models (
    organization_id UUID NOT NULL,
    model_id TEXT NOT NULL,
    name TEXT NOT NULL,
    provider TEXT NOT NULL,
    status TEXT NOT NULL
        CHECK (status IN ('available', 'disabled', 'not_configured')),
    endpoint_or_path TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (organization_id, model_id)
);

CREATE INDEX IF NOT EXISTS llm_models_organization_idx
    ON llm_models (organization_id);