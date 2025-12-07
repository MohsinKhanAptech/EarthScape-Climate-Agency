from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_mail import Message

from app import mail

feedback = Blueprint("feedback", __name__)


@feedback.route("/contact", methods=["GET", "POST"])
def contact():
    """
    Feedback & Support Page.
    Allows users to report issues or ask for help.
    """
    if request.method == "POST":
        subject = request.form.get("subject")
        message_body = request.form.get("message")
        user_email = request.form.get("email")

        sender_info = f"From: {user_email}"
        if current_user.is_authenticated:
            sender_info += f" (User: {current_user.username})"

        try:
            msg = Message(
                subject=f"[EarthScape Support] {subject}",
                recipients=["muhammadmohsinkhan.aptech@gmail.com"],
                body=f"{message_body}\n\n--\n{sender_info}",
                sender=user_email,
            )

            # Send Email (This requires MAIL_SERVER setup in .env)
            mail.send(msg)
            flash(
                "Thank you! Your feedback has been sent to our support team.", "success"
            )
            return redirect(url_for("views.index"))

        except Exception as e:
            flash(f"Error sending email: {e}", "danger")

    return render_template("feedback.html")
