from flask import (
    Blueprint, url_for, redirect, g, render_template, flash, request, session
)

from surf_app.auth import login_required

bp = Blueprint('beaches',__name__)

@bp.route('/beaches')
@login_required
def beaches_home():
    beach_list = get_beaches()
    return render_template('beaches/beaches_home.html',beaches=beach_list)


def get_beaches():
    """
    Returns a list of Beach ID and name, the IDs are according to MSW's web API.
    """
    beaches = [{'beach_id': 255, 'beach_name':'Linda Mar / Pacifica'},
                {'beach_id': 819, 'beach_name':'Ocean Beach'}]

    return beaches
