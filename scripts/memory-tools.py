#!/usr/bin/env python3
"""SQLite-backed memory tools for Codex Mother System.

This script intentionally uses only Python standard library modules so the
memory backend can run in a fresh project without dependency installation.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
import uuid
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "memory" / "index.db"
DEFAULT_SCHEMA = ROOT / "memory" / "schema.sql"

MEMORY_TYPES = (
    "lesson",
    "feature",
    "decision",
    "pattern",
    "validation",
    "candidate",
    "note",
)


def connect(db_path: Path = DEFAULT_DB) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def ensure_initialized(conn: sqlite3.Connection, schema_path: Path = DEFAULT_SCHEMA) -> None:
    if not schema_path.exists():
        raise SystemExit(f"Schema file not found: {schema_path}")
    conn.executescript(schema_path.read_text(encoding="utf-8"))
    conn.commit()


def normalize_csv(values: list[str] | None) -> str | None:
    if not values:
        return None
    flattened: list[str] = []
    for value in values:
        for part in value.split(","):
            part = part.strip()
            if part:
                flattened.append(part)
    return ",".join(dict.fromkeys(flattened)) if flattened else None


def print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return {key: row[key] for key in row.keys()}


def build_safe_fts_query(query: str) -> str:
    """Build a forgiving FTS5 query from real-world bug/feature text.

    Raw FTS5 MATCH input can fail on punctuation-heavy strings such as
    "5MB -> 4.5MB" or file paths. Tokenizing and quoting each term keeps
    search useful without making users think in SQLite query syntax.
    """

    tokens = re.findall(r"[\w.\-/:\u4e00-\u9fff]+", query, flags=re.UNICODE)
    cleaned = [token.strip(".-/:_") for token in tokens]
    cleaned = [token for token in cleaned if token]
    if not cleaned:
        escaped = query.replace('"', '""').strip()
        return f'"{escaped}"' if escaped else '""'
    return " OR ".join(f'"{token.replace(chr(34), chr(34) * 2)}"' for token in cleaned)


def like_pattern(query: str) -> str:
    return f"%{query.replace('%', r'\%').replace('_', r'\_')}%"


def cmd_init(args: argparse.Namespace) -> None:
    with connect(args.db) as conn:
        ensure_initialized(conn, args.schema)
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type IN ('table', 'view') ORDER BY name"
        ).fetchall()
        conn.execute(
            "INSERT INTO maintenance_log(action, details) VALUES (?, ?)",
            ("init", f"Initialized memory database at {args.db}"),
        )
        conn.commit()
    print_json(
        {
            "ok": True,
            "db": str(args.db),
            "schema": str(args.schema),
            "tables": [row["name"] for row in tables],
        }
    )


def cmd_record_item(args: argparse.Namespace) -> None:
    metadata_json = args.metadata_json
    if args.metadata:
        metadata_json = json.dumps(args.metadata, ensure_ascii=False)

    with connect(args.db) as conn:
        ensure_initialized(conn, args.schema)
        cur = conn.execute(
            """
            INSERT INTO memory_items(
                project,
                type,
                title,
                summary,
                problem,
                solution,
                patterns,
                files,
                tags,
                validation,
                confidence,
                source_session,
                metadata_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                args.project,
                args.type,
                args.title,
                args.summary,
                args.problem,
                args.solution,
                normalize_csv(args.patterns),
                normalize_csv(args.files),
                normalize_csv(args.tags),
                args.validation,
                args.confidence,
                args.source_session,
                metadata_json,
            ),
        )
        item_id = cur.lastrowid
        if args.source_session:
            conn.execute(
                """
                INSERT OR IGNORE INTO session_memory_links(session_id, memory_item_id, relation)
                VALUES (?, ?, ?)
                """,
                (args.source_session, item_id, "created"),
            )
        conn.commit()
    print_json({"ok": True, "id": item_id, "type": args.type, "project": args.project})


def cmd_search(args: argparse.Namespace) -> None:
    with connect(args.db) as conn:
        ensure_initialized(conn, args.schema)
        fts_query = args.query if args.raw_fts else build_safe_fts_query(args.query)
        params: list[Any] = [fts_query]
        project_filter = ""
        type_filter = ""
        if args.project:
            project_filter = "AND mi.project = ?"
            params.append(args.project)
        if args.type:
            type_filter = "AND mi.type = ?"
            params.append(args.type)
        params.append(args.limit)
        try:
            rows = conn.execute(
                f"""
                SELECT
                    mi.id,
                    mi.project,
                    mi.type,
                    mi.title,
                    mi.summary,
                    mi.solution,
                    mi.patterns,
                    mi.files,
                    mi.tags,
                    mi.validation,
                    mi.confidence,
                    mi.created_at,
                    bm25(memory_fts) AS rank
                FROM memory_fts
                JOIN memory_items mi ON mi.id = memory_fts.rowid
                WHERE memory_fts MATCH ?
                {project_filter}
                {type_filter}
                ORDER BY rank
                LIMIT ?
                """,
                params,
            ).fetchall()
            mode = "fts5"
        except sqlite3.OperationalError as exc:
            if args.raw_fts:
                raise
            like_params: list[Any] = []
            project_where = ""
            type_where = ""
            pattern = like_pattern(args.query)
            like_params.extend([pattern] * 8)
            if args.project:
                project_where = "AND project = ?"
                like_params.append(args.project)
            if args.type:
                type_where = "AND type = ?"
                like_params.append(args.type)
            like_params.append(args.limit)
            rows = conn.execute(
                f"""
                SELECT id, project, type, title, summary, solution, patterns, files,
                       tags, validation, confidence, created_at, NULL AS rank
                FROM memory_items
                WHERE (
                    title LIKE ? ESCAPE '\\' OR
                    summary LIKE ? ESCAPE '\\' OR
                    problem LIKE ? ESCAPE '\\' OR
                    solution LIKE ? ESCAPE '\\' OR
                    patterns LIKE ? ESCAPE '\\' OR
                    files LIKE ? ESCAPE '\\' OR
                    tags LIKE ? ESCAPE '\\' OR
                    validation LIKE ? ESCAPE '\\'
                )
                {project_where}
                {type_where}
                ORDER BY created_at DESC, id DESC
                LIMIT ?
                """,
                like_params,
            ).fetchall()
            mode = f"like-fallback: {exc}"
    print_json(
        {
            "ok": True,
            "query": args.query,
            "fts_query": fts_query,
            "mode": mode,
            "results": [row_to_dict(row) for row in rows],
        }
    )


def cmd_recent(args: argparse.Namespace) -> None:
    params: list[Any] = []
    project_filter = ""
    type_filter = ""
    if args.project:
        project_filter = "WHERE project = ?"
        params.append(args.project)
    if args.type:
        if project_filter:
            type_filter = "AND type = ?"
        else:
            type_filter = "WHERE type = ?"
        params.append(args.type)
    params.append(args.limit)

    with connect(args.db) as conn:
        ensure_initialized(conn, args.schema)
        rows = conn.execute(
            f"""
            SELECT id, project, type, title, summary, tags, confidence, created_at
            FROM memory_items
            {project_filter}
            {type_filter}
            ORDER BY created_at DESC, id DESC
            LIMIT ?
            """,
            params,
        ).fetchall()
    print_json({"ok": True, "results": [row_to_dict(row) for row in rows]})


def cmd_record_session(args: argparse.Namespace) -> None:
    session_id = args.id or str(uuid.uuid4())
    with connect(args.db) as conn:
        ensure_initialized(conn, args.schema)
        conn.execute(
            """
            INSERT INTO sessions(
                id,
                project,
                task_summary,
                key_decisions,
                validation_summary,
                memory_updated,
                status,
                started_at,
                metadata_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                project = excluded.project,
                task_summary = excluded.task_summary,
                key_decisions = excluded.key_decisions,
                validation_summary = excluded.validation_summary,
                memory_updated = excluded.memory_updated,
                status = excluded.status,
                ended_at = datetime('now'),
                metadata_json = excluded.metadata_json
            """,
            (
                session_id,
                args.project,
                args.task_summary,
                args.key_decisions,
                args.validation_summary,
                1 if args.memory_updated else 0,
                args.status,
                args.started_at,
                args.metadata_json,
            ),
        )
        conn.commit()
    print_json({"ok": True, "session_id": session_id, "project": args.project})


def cmd_candidate_upsert(args: argparse.Namespace) -> None:
    with connect(args.db) as conn:
        ensure_initialized(conn, args.schema)
        existing = conn.execute(
            "SELECT id, count FROM skill_candidates WHERE name = ? AND project = ?",
            (args.name, args.project),
        ).fetchone()
        if existing:
            candidate_id = existing["id"]
            new_count = existing["count"] + args.increment
            conn.execute(
                """
                UPDATE skill_candidates
                SET
                    trigger = COALESCE(?, trigger),
                    evidence = COALESCE(?, evidence),
                    validation = COALESCE(?, validation),
                    scope = COALESCE(?, scope),
                    boundary = COALESCE(?, boundary),
                    suggested_skill = COALESCE(?, suggested_skill),
                    tags = COALESCE(?, tags),
                    status = COALESCE(?, status),
                    confidence = ?,
                    count = ?,
                    updated_at = datetime('now')
                WHERE id = ?
                """,
                (
                    args.trigger,
                    args.evidence,
                    args.validation,
                    args.scope,
                    args.boundary,
                    args.suggested_skill,
                    normalize_csv(args.tags),
                    args.status,
                    args.confidence,
                    new_count,
                    candidate_id,
                ),
            )
        else:
            cur = conn.execute(
                """
                INSERT INTO skill_candidates(
                    name,
                    project,
                    trigger,
                    evidence,
                    validation,
                    scope,
                    boundary,
                    suggested_skill,
                    tags,
                    status,
                    count,
                    confidence
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    args.name,
                    args.project,
                    args.trigger,
                    args.evidence,
                    args.validation,
                    args.scope,
                    args.boundary,
                    args.suggested_skill,
                    normalize_csv(args.tags),
                    args.status,
                    args.increment,
                    args.confidence,
                ),
            )
            candidate_id = cur.lastrowid
        if args.evidence:
            conn.execute(
                """
                INSERT INTO skill_candidate_evidence(
                    candidate_id,
                    project,
                    memory_item_id,
                    evidence,
                    validation
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (candidate_id, args.project, args.memory_item_id, args.evidence, args.validation),
            )
        conn.commit()
    print_json({"ok": True, "candidate_id": candidate_id, "name": args.name, "project": args.project})


def cmd_candidates(args: argparse.Namespace) -> None:
    params: list[Any] = []
    where: list[str] = []
    if args.project:
        where.append("project = ?")
        params.append(args.project)
    if args.status:
        where.append("status = ?")
        params.append(args.status)
    where_sql = f"WHERE {' AND '.join(where)}" if where else ""
    params.append(args.limit)
    with connect(args.db) as conn:
        ensure_initialized(conn, args.schema)
        rows = conn.execute(
            f"""
            SELECT id, name, project, trigger, evidence, validation, scope, boundary,
                   suggested_skill, tags, status, count, confidence, updated_at
            FROM skill_candidates
            {where_sql}
            ORDER BY count DESC, updated_at DESC
            LIMIT ?
            """,
            params,
        ).fetchall()
    print_json({"ok": True, "results": [row_to_dict(row) for row in rows]})


def cmd_record_skill_usage(args: argparse.Namespace) -> None:
    with connect(args.db) as conn:
        ensure_initialized(conn, args.schema)
        cur = conn.execute(
            """
            INSERT INTO skill_usage(skill_name, project, task_summary, success, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (args.skill_name, args.project, args.task_summary, 1 if args.success else 0, args.notes),
        )
        conn.commit()
    print_json({"ok": True, "id": cur.lastrowid, "skill_name": args.skill_name})


def cmd_stats(args: argparse.Namespace) -> None:
    with connect(args.db) as conn:
        ensure_initialized(conn, args.schema)
        memory_by_type = conn.execute(
            "SELECT type, COUNT(*) AS count FROM memory_items GROUP BY type ORDER BY type"
        ).fetchall()
        candidates_by_status = conn.execute(
            "SELECT status, COUNT(*) AS count FROM skill_candidates GROUP BY status ORDER BY status"
        ).fetchall()
        skill_usage = conn.execute(
            """
            SELECT skill_name,
                   COUNT(*) AS uses,
                   ROUND(AVG(success) * 100, 2) AS success_rate
            FROM skill_usage
            GROUP BY skill_name
            ORDER BY uses DESC, skill_name
            LIMIT ?
            """,
            (args.limit,),
        ).fetchall()
        sessions = conn.execute("SELECT COUNT(*) AS count FROM sessions").fetchone()["count"]
    print_json(
        {
            "ok": True,
            "memory_by_type": [row_to_dict(row) for row in memory_by_type],
            "candidates_by_status": [row_to_dict(row) for row in candidates_by_status],
            "skill_usage": [row_to_dict(row) for row in skill_usage],
            "sessions": sessions,
        }
    )


def cmd_maintenance(args: argparse.Namespace) -> None:
    with connect(args.db) as conn:
        ensure_initialized(conn, args.schema)
        conn.execute("INSERT INTO memory_fts(memory_fts) VALUES ('optimize')")
        conn.execute("ANALYZE")
        conn.execute(
            "INSERT INTO maintenance_log(action, details) VALUES (?, ?)",
            ("maintenance", f"vacuum={args.vacuum}"),
        )
        conn.commit()
        if args.vacuum:
            conn.execute("VACUUM")
    print_json({"ok": True, "vacuum": args.vacuum})


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="Path to SQLite index.db")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA, help="Path to schema.sql")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Codex Mother System memory tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize memory database")
    add_common_args(init_parser)
    init_parser.set_defaults(func=cmd_init)

    record_parser = subparsers.add_parser("record-item", help="Record a memory item")
    add_common_args(record_parser)
    record_parser.add_argument("--project", required=True)
    record_parser.add_argument("--type", choices=MEMORY_TYPES, required=True)
    record_parser.add_argument("--title", required=True)
    record_parser.add_argument("--summary", required=True)
    record_parser.add_argument("--problem")
    record_parser.add_argument("--solution")
    record_parser.add_argument("--patterns", nargs="*")
    record_parser.add_argument("--files", nargs="*")
    record_parser.add_argument("--tags", nargs="*")
    record_parser.add_argument("--validation")
    record_parser.add_argument("--confidence", type=float, default=0.8)
    record_parser.add_argument("--source-session")
    record_parser.add_argument("--metadata-json")
    record_parser.add_argument("--metadata", action="append", help="key=value metadata entries")
    record_parser.set_defaults(func=cmd_record_item)

    search_parser = subparsers.add_parser("search", help="Search memory items using FTS5")
    add_common_args(search_parser)
    search_parser.add_argument("query")
    search_parser.add_argument("--project")
    search_parser.add_argument("--type", choices=MEMORY_TYPES)
    search_parser.add_argument("--limit", type=int, default=10)
    search_parser.add_argument("--raw-fts", action="store_true", help="Use query as raw FTS5 MATCH syntax")
    search_parser.set_defaults(func=cmd_search)

    recent_parser = subparsers.add_parser("recent", help="List recent memory items")
    add_common_args(recent_parser)
    recent_parser.add_argument("--project")
    recent_parser.add_argument("--type", choices=MEMORY_TYPES)
    recent_parser.add_argument("--limit", type=int, default=10)
    recent_parser.set_defaults(func=cmd_recent)

    session_parser = subparsers.add_parser("record-session", help="Record a session summary")
    add_common_args(session_parser)
    session_parser.add_argument("--id")
    session_parser.add_argument("--project", required=True)
    session_parser.add_argument("--task-summary", required=True)
    session_parser.add_argument("--key-decisions")
    session_parser.add_argument("--validation-summary")
    session_parser.add_argument("--memory-updated", action="store_true")
    session_parser.add_argument("--status", choices=("completed", "partial", "blocked", "failed"), default="completed")
    session_parser.add_argument("--started-at")
    session_parser.add_argument("--metadata-json")
    session_parser.set_defaults(func=cmd_record_session)

    candidate_parser = subparsers.add_parser("candidate-upsert", help="Create or update a skill candidate")
    add_common_args(candidate_parser)
    candidate_parser.add_argument("--name", required=True)
    candidate_parser.add_argument("--project", default="*")
    candidate_parser.add_argument("--trigger", required=True)
    candidate_parser.add_argument("--evidence", required=True)
    candidate_parser.add_argument("--validation")
    candidate_parser.add_argument("--scope")
    candidate_parser.add_argument("--boundary")
    candidate_parser.add_argument("--suggested-skill")
    candidate_parser.add_argument("--tags", nargs="*")
    candidate_parser.add_argument("--status", choices=("candidate", "reviewing", "approved", "rejected", "promoted"), default="candidate")
    candidate_parser.add_argument("--increment", type=int, default=1)
    candidate_parser.add_argument("--confidence", type=float, default=0.7)
    candidate_parser.add_argument("--memory-item-id", type=int)
    candidate_parser.set_defaults(func=cmd_candidate_upsert)

    candidates_parser = subparsers.add_parser("candidates", help="List skill candidates")
    add_common_args(candidates_parser)
    candidates_parser.add_argument("--project")
    candidates_parser.add_argument("--status", choices=("candidate", "reviewing", "approved", "rejected", "promoted"))
    candidates_parser.add_argument("--limit", type=int, default=20)
    candidates_parser.set_defaults(func=cmd_candidates)

    usage_parser = subparsers.add_parser("record-skill-usage", help="Record skill usage result")
    add_common_args(usage_parser)
    usage_parser.add_argument("--skill-name", required=True)
    usage_parser.add_argument("--project", default="*")
    usage_parser.add_argument("--task-summary")
    usage_parser.add_argument("--success", action="store_true")
    usage_parser.add_argument("--notes")
    usage_parser.set_defaults(func=cmd_record_skill_usage)

    stats_parser = subparsers.add_parser("stats", help="Show memory backend stats")
    add_common_args(stats_parser)
    stats_parser.add_argument("--limit", type=int, default=20)
    stats_parser.set_defaults(func=cmd_stats)

    maintenance_parser = subparsers.add_parser("maintenance", help="Optimize/analyze memory database")
    add_common_args(maintenance_parser)
    maintenance_parser.add_argument("--vacuum", action="store_true")
    maintenance_parser.set_defaults(func=cmd_maintenance)

    return parser


def parse_metadata(values: list[str] | None) -> dict[str, str] | None:
    if not values:
        return None
    data: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise SystemExit(f"Invalid metadata entry, expected key=value: {value}")
        key, val = value.split("=", 1)
        data[key.strip()] = val.strip()
    return data


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if hasattr(args, "metadata"):
        args.metadata = parse_metadata(args.metadata)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
