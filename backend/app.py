"""Flask interface and JSON API; passwords remain transient in memory."""
import os
from pathlib import Path
from flask import Flask, jsonify, render_template, request
from services.password_analyzer import analyze_password
from services.password_generator import generate_password
from services.analytics import record, dashboard

ROOT=Path(__file__).resolve().parents[1]
app=Flask(__name__,template_folder=str(ROOT/"frontend"),static_folder=str(ROOT/"frontend"/"static"))
app.config["MAX_CONTENT_LENGTH"]=16*1024
DB_PATH=Path(os.environ.get("ANALYTICS_DB",ROOT/"data"/"analytics.sqlite3"))
ANALYTICS_ENABLED=os.environ.get("ENABLE_ANALYTICS","false").lower()=="true"

@app.get("/")
def index(): return render_template("index.html")

@app.post("/api/analyze")
def api_analyze():
    body=request.get_json(silent=True)
    if not isinstance(body,dict) or not isinstance(body.get("password"),str): return jsonify({"error":"JSON body must include a text password."}),400
    try:
        result=analyze_password(body["password"],body.get("context") if isinstance(body.get("context"),dict) else None)
        if ANALYTICS_ENABLED: record(result,DB_PATH)
        return jsonify(result)
    except ValueError as exc: return jsonify({"error":str(exc)}),400

@app.get("/api/dashboard/stats")
def api_stats(): return jsonify(dashboard(DB_PATH))

@app.get("/api/analytics/weaknesses")
def api_weaknesses(): return jsonify({"weaknesses":dashboard(DB_PATH)["weaknesses"]})

@app.post("/api/generate-password")
def api_generate():
    body=request.get_json(silent=True) or {}
    try: return jsonify({"password":generate_password(int(body.get("length",20)),**{k:bool(body.get(k,True)) for k in ("uppercase","lowercase","numbers","symbols")})})
    except (ValueError,TypeError): return jsonify({"error":"Choose length 16, 20, or 24 and at least one character group."}),400

if __name__=="__main__": app.run(host="127.0.0.1",port=5000,debug=False)
