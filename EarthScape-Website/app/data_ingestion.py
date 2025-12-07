import os

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

ingestion = Blueprint("ingestion", __name__)


@ingestion.route("/ingest", methods=["GET", "POST"])
@login_required
def trigger_ingestion():
    """
    Allows admins to upload new datasets or trigger HDFS ingestion.
    """
    if request.method == "POST":
        # Simulate triggering a Hadoop Job
        flash("Ingestion Job Submitted to Hadoop Cluster (Job ID: #9923)", "info")
        return redirect(url_for("ingestion.trigger_ingestion"))

    return render_template("ingest.html")
