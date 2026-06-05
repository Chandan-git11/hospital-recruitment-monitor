import sys
from pathlib import Path

from flask import Blueprint, jsonify, request

# Project Root
ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

from scraper.core.config import DATABASE_PATH
from scraper.services.database import JobDatabase

# Blueprint
api_bp = Blueprint("api", __name__)


# =========================
# Home Route
# =========================

@api_bp.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Healthcare Career Monitor API",
        "status": "running",
        "endpoints": [
            "/api/jobs",
            "/api/jobs/count",
            "/api/jobs/new",
            "/api/jobs/hospital/<name>",
            "/api/search?q=nurse",
            "/api/stats",
            "/api/analytics/hospitals",
            "/api/analytics/departments"
        ]
    })


# =========================
# Get Jobs
# =========================

@api_bp.route("/jobs", methods=["GET"])
def get_jobs():

    db = JobDatabase(DATABASE_PATH)

    hospital = request.args.get("hospital")

    if hospital:
        jobs = db.fetch_by_hospital(hospital)
    else:
        jobs = db.fetch_all()

    # Optional Pagination
    page = request.args.get("page")
    limit = request.args.get("limit")

    if page and limit:
        page = int(page)
        limit = int(limit)

        start = (page - 1) * limit
        end = start + limit

        return jsonify(jobs[start:end])

    return jsonify(jobs)


# =========================
# Count Jobs
# =========================

@api_bp.route("/jobs/count", methods=["GET"])
def get_job_count():

    db = JobDatabase(DATABASE_PATH)

    return jsonify({
        "count": db.count_jobs()
    })


# =========================
# New Jobs
# =========================

@api_bp.route("/jobs/new", methods=["GET"])
def get_new_jobs():

    db = JobDatabase(DATABASE_PATH)

    return jsonify(
        db.fetch_new_jobs()
    )


# =========================
# Jobs By Hospital
# =========================

@api_bp.route("/jobs/hospital/<name>", methods=["GET"])
def get_jobs_by_hospital(name):

    db = JobDatabase(DATABASE_PATH)

    return jsonify(
        db.fetch_by_hospital(name)
    )


# =========================
# Search Jobs
# =========================

@api_bp.route("/search", methods=["GET"])
def search_jobs():

    keyword = request.args.get("q", "").lower()

    db = JobDatabase(DATABASE_PATH)

    jobs = db.fetch_all()

    results = []

    for job in jobs:

        title = job.get("title", "").lower()
        department = job.get("department", "").lower()
        location = job.get("location", "").lower()
        hospital = job.get("hospital", "").lower()

        if (
            keyword in title
            or keyword in department
            or keyword in location
            or keyword in hospital
        ):
            results.append(job)

    return jsonify(results)


# =========================
# Dashboard Stats
# =========================

@api_bp.route("/stats", methods=["GET"])
def get_stats():

    db = JobDatabase(DATABASE_PATH)

    jobs = db.fetch_all()

    hospitals = {
        job.get("hospital", "")
        for job in jobs
    }

    return jsonify({
        "total_jobs": db.count_jobs(),
        "new_jobs": len(db.fetch_new_jobs()),
        "jobs_added_today": db.jobs_added_today(),
        "total_hospitals": len(hospitals)
    })


# =========================
# Analytics - Hospital Wise
# =========================

@api_bp.route("/analytics/hospitals", methods=["GET"])
def analytics_hospitals():

    db = JobDatabase(DATABASE_PATH)

    return jsonify(
        db.jobs_by_hospital()
    )


# =========================
# Analytics - Department Wise
# =========================

@api_bp.route("/analytics/departments", methods=["GET"])
def analytics_departments():

    db = JobDatabase(DATABASE_PATH)

    return jsonify(
        db.jobs_by_department()
    )
# Analytics - Location Wise

@api_bp.route("/analytics/locations", methods=["GET"])
def analytics_locations():

    db = JobDatabase(DATABASE_PATH)

    jobs = db.fetch_all()

    locations = {}

    for job in jobs:

        location = (
            job.get("location")
            or "Unknown"
        )

        locations[location] = (
            locations.get(location, 0) + 1
        )

    return jsonify(locations)