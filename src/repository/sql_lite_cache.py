import sqlite3


class SQLiteCache:
    """Cache layer to store and query Maven artifact data locally in SQLite."""

    def __init__(self, db_path: str = "maven_cache.db"):
        self.db_path = db_path
        self._init_db()

    # ----------------------------
    # Database initialization
    # ----------------------------

    def _init_db(self):
        """Create the database and tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS artifacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id TEXT NOT NULL,
                    artifact_id TEXT NOT NULL,
                    last_checked DATETIME,
                    last_version TEXT,
                    last_updated_at DATETIME,
                    UNIQUE(group_id, artifact_id)
                );
            """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS versions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    artifact_id INTEGER NOT NULL,
                    version TEXT NOT NULL,
                    published_at DATETIME,
                    inserted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (artifact_id) REFERENCES artifacts(id),
                    UNIQUE(artifact_id, version)
                );
            """
            )

            conn.commit()
        print("✅ SQLite cache initialized or verified.")


# ----------------------------
# Example usage
# ----------------------------
if __name__ == "__main__":
    db = SQLiteCache()
