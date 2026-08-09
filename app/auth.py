from functools import wraps

from flask import (
    session,
    redirect,
    url_for,
    flash
)


# =========================================================
# ADMIN AUTHORIZATION DECORATOR
# =========================================================
def admin_required(func):

    @wraps(func)
    def decorated(
        *args,
        **kwargs
    ):

        admin_id = session.get(
            "admin_id"
        )

        role = session.get(
            "role"
        )

        # -----------------------------------------------------
        # INVALID OR MISSING SESSION
        # -----------------------------------------------------
        if (
            not admin_id
            or role != "admin"
        ):

            # Remove any stale session data.
            session.clear()

            flash(
                "Please login as administrator.",
                "warning"
            )

            return redirect(
                url_for(
                    "admin.login"
                )
            )

        # -----------------------------------------------------
        # VALID ADMIN SESSION
        # -----------------------------------------------------
        return func(
            *args,
            **kwargs
        )

    return decorated