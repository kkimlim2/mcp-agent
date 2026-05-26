CREATE TABLE IF NOT EXISTS prompts (
    id         TEXT PRIMARY KEY,
    agent_id   TEXT NOT NULL,
    version    TEXT NOT NULL,
    content    TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (agent_id, version)
);

CREATE TABLE IF NOT EXISTS evaluations (
    id            TEXT PRIMARY KEY,
    agent_id      TEXT NOT NULL,
    prompt_id     TEXT NOT NULL REFERENCES prompts(id),
    query         TEXT,
    response      TEXT,
    scores        JSON,
    overall_score REAL,
    passed        INTEGER,
    metadata      JSON,
    tags          JSON,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_agent_id
    ON evaluations(agent_id);
CREATE INDEX IF NOT EXISTS idx_prompt_id
    ON evaluations(prompt_id);
CREATE INDEX IF NOT EXISTS idx_created_at
    ON evaluations(created_at);