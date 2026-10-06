"""Opt-in SQLite analytics storing metadata only. No password fields exist."""
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

def connect(path):
    db=sqlite3.connect(path); db.row_factory=sqlite3.Row
    db.executescript("CREATE TABLE IF NOT EXISTS analyses(analysis_id INTEGER PRIMARY KEY, score INTEGER NOT NULL, classification TEXT NOT NULL, password_length INTEGER NOT NULL, unique_character_ratio REAL NOT NULL, weakness_count INTEGER NOT NULL, created_at TEXT NOT NULL); CREATE TABLE IF NOT EXISTS findings(finding_id INTEGER PRIMARY KEY, analysis_id INTEGER NOT NULL, finding_type TEXT NOT NULL, severity TEXT NOT NULL, description TEXT NOT NULL, FOREIGN KEY(analysis_id) REFERENCES analyses(analysis_id));")
    return db

def record(result, path):
    db=connect(path); m=result["metrics"]
    cur=db.execute("INSERT INTO analyses(score,classification,password_length,unique_character_ratio,weakness_count,created_at) VALUES(?,?,?,?,?,?)",(result["score"],result["classification"],m["length"],m["unique_character_ratio"],sum(f["code"]!="entropy_caveat" for f in result["findings"]),datetime.now(timezone.utc).isoformat()))
    for f in result["findings"]:
        db.execute("INSERT INTO findings(analysis_id,finding_type,severity,description) VALUES(?,?,?,?)",(cur.lastrowid,f["code"],f["severity"],f["description"]))
    db.commit(); db.close()

def dashboard(path):
    db=connect(path)
    rows=db.execute("SELECT classification,COUNT(*) count FROM analyses GROUP BY classification").fetchall()
    avg=db.execute("SELECT COALESCE(AVG(score),0) avg,COUNT(*) total FROM analyses").fetchone()
    weaknesses=db.execute("SELECT finding_type,COUNT(*) count FROM findings GROUP BY finding_type ORDER BY count DESC LIMIT 10").fetchall()
    lengths=db.execute("SELECT CASE WHEN password_length<8 THEN '<8' WHEN password_length<12 THEN '8–11' WHEN password_length<16 THEN '12–15' ELSE '16+' END band,COUNT(*) count FROM analyses GROUP BY band").fetchall()
    scores=db.execute("SELECT CASE WHEN score<21 THEN '0–20' WHEN score<41 THEN '21–40' WHEN score<61 THEN '41–60' WHEN score<81 THEN '61–80' ELSE '81–100' END band,COUNT(*) count FROM analyses GROUP BY band").fetchall()
    db.close()
    return {"total":avg["total"],"average_score":round(avg["avg"],1),"classification_counts":{x["classification"]:x["count"] for x in rows},"weaknesses":[dict(x) for x in weaknesses],"length_distribution":[dict(x) for x in lengths],"score_distribution":[dict(x) for x in scores]}
