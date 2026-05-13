PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS schema_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

INSERT INTO schema_meta(key, value)
VALUES ('schema_version', '2')
ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = datetime('now');

CREATE TABLE IF NOT EXISTS memory_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN (
        'lesson',
        'feature',
        'decision',
        'pattern',
        'validation',
        'candidate',
        'note'
    )),
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    problem TEXT,
    solution TEXT,
    patterns TEXT,
    files TEXT,
    tags TEXT,
    validation TEXT,
    confidence REAL NOT NULL DEFAULT 0.8 CHECK (confidence >= 0 AND confidence <= 1),
    source_session TEXT,
    import_key TEXT,
    metadata_json TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_memory_items_project ON memory_items(project);
CREATE INDEX IF NOT EXISTS idx_memory_items_type ON memory_items(type);
CREATE INDEX IF NOT EXISTS idx_memory_items_created_at ON memory_items(created_at);
CREATE INDEX IF NOT EXISTS idx_memory_items_tags ON memory_items(tags);
CREATE UNIQUE INDEX IF NOT EXISTS idx_memory_items_import_key
ON memory_items(import_key)
WHERE import_key IS NOT NULL;

CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
    title,
    summary,
    problem,
    solution,
    patterns,
    files,
    tags,
    validation,
    project,
    content='memory_items',
    content_rowid='id'
);

CREATE TRIGGER IF NOT EXISTS memory_items_ai AFTER INSERT ON memory_items
BEGIN
    INSERT INTO memory_fts(
        rowid,
        title,
        summary,
        problem,
        solution,
        patterns,
        files,
        tags,
        validation,
        project
    )
    VALUES (
        new.id,
        new.title,
        new.summary,
        new.problem,
        new.solution,
        new.patterns,
        new.files,
        new.tags,
        new.validation,
        new.project
    );
END;

CREATE TRIGGER IF NOT EXISTS memory_items_ad AFTER DELETE ON memory_items
BEGIN
    INSERT INTO memory_fts(
        memory_fts,
        rowid,
        title,
        summary,
        problem,
        solution,
        patterns,
        files,
        tags,
        validation,
        project
    )
    VALUES (
        'delete',
        old.id,
        old.title,
        old.summary,
        old.problem,
        old.solution,
        old.patterns,
        old.files,
        old.tags,
        old.validation,
        old.project
    );
END;

CREATE TRIGGER IF NOT EXISTS memory_items_au AFTER UPDATE ON memory_items
BEGIN
    INSERT INTO memory_fts(
        memory_fts,
        rowid,
        title,
        summary,
        problem,
        solution,
        patterns,
        files,
        tags,
        validation,
        project
    )
    VALUES (
        'delete',
        old.id,
        old.title,
        old.summary,
        old.problem,
        old.solution,
        old.patterns,
        old.files,
        old.tags,
        old.validation,
        old.project
    );

    INSERT INTO memory_fts(
        rowid,
        title,
        summary,
        problem,
        solution,
        patterns,
        files,
        tags,
        validation,
        project
    )
    VALUES (
        new.id,
        new.title,
        new.summary,
        new.problem,
        new.solution,
        new.patterns,
        new.files,
        new.tags,
        new.validation,
        new.project
    );
END;

CREATE TABLE IF NOT EXISTS skill_candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    project TEXT NOT NULL DEFAULT '*',
    trigger TEXT NOT NULL,
    evidence TEXT NOT NULL,
    validation TEXT,
    scope TEXT,
    boundary TEXT,
    suggested_skill TEXT,
    tags TEXT,
    status TEXT NOT NULL DEFAULT 'candidate' CHECK (status IN (
        'candidate',
        'reviewing',
        'approved',
        'rejected',
        'promoted'
    )),
    count INTEGER NOT NULL DEFAULT 1,
    confidence REAL NOT NULL DEFAULT 0.7 CHECK (confidence >= 0 AND confidence <= 1),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(name, project)
);

CREATE INDEX IF NOT EXISTS idx_skill_candidates_project ON skill_candidates(project);
CREATE INDEX IF NOT EXISTS idx_skill_candidates_status ON skill_candidates(status);
CREATE INDEX IF NOT EXISTS idx_skill_candidates_updated_at ON skill_candidates(updated_at);

CREATE TABLE IF NOT EXISTS skill_candidate_evidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER NOT NULL,
    project TEXT NOT NULL,
    memory_item_id INTEGER,
    evidence TEXT NOT NULL,
    validation TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY(candidate_id) REFERENCES skill_candidates(id) ON DELETE CASCADE,
    FOREIGN KEY(memory_item_id) REFERENCES memory_items(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    project TEXT NOT NULL,
    task_summary TEXT NOT NULL,
    key_decisions TEXT,
    validation_summary TEXT,
    memory_updated INTEGER NOT NULL DEFAULT 0 CHECK (memory_updated IN (0, 1)),
    status TEXT NOT NULL DEFAULT 'completed' CHECK (status IN (
        'completed',
        'partial',
        'blocked',
        'failed'
    )),
    started_at TEXT,
    ended_at TEXT NOT NULL DEFAULT (datetime('now')),
    metadata_json TEXT
);

CREATE INDEX IF NOT EXISTS idx_sessions_project ON sessions(project);
CREATE INDEX IF NOT EXISTS idx_sessions_ended_at ON sessions(ended_at);

CREATE TABLE IF NOT EXISTS session_memory_links (
    session_id TEXT NOT NULL,
    memory_item_id INTEGER NOT NULL,
    relation TEXT NOT NULL DEFAULT 'created',
    PRIMARY KEY(session_id, memory_item_id, relation),
    FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE,
    FOREIGN KEY(memory_item_id) REFERENCES memory_items(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS skill_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_name TEXT NOT NULL,
    project TEXT NOT NULL DEFAULT '*',
    task_summary TEXT,
    success INTEGER NOT NULL CHECK (success IN (0, 1)),
    notes TEXT,
    used_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_skill_usage_skill ON skill_usage(skill_name);
CREATE INDEX IF NOT EXISTS idx_skill_usage_project ON skill_usage(project);
CREATE INDEX IF NOT EXISTS idx_skill_usage_used_at ON skill_usage(used_at);

CREATE TABLE IF NOT EXISTS maintenance_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    details TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
