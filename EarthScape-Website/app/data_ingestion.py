import os

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required  # <--- Added current_user

ingestion = Blueprint("ingestion", __name__)


@ingestion.route("/ingest", methods=["GET", "POST"])
@login_required
def trigger_ingestion():
    """
    Allows admins to upload new datasets or trigger HDFS ingestion.
    """
    # --- SECURITY CHECK ---
    # Redirect Analysts back to the dashboard if they try to access this page
    if current_user.role != "admin":
        flash("Access Denied: Only Administrators can ingest data.", "danger")
        return redirect(url_for("views.dashboard"))

    if request.method == "POST":
        # Simulate triggering a Hadoop Job
        flash("Ingestion Job Submitted to Hadoop Cluster (Job ID: #9923)", "info")
        return redirect(url_for("ingestion.trigger_ingestion"))

    return render_template("ingest.html")
