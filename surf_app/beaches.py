from flask import (
    Blueprint, url_for, redirect, g, render_template, flash, request, session
)

from surf_app import app
import requests
from surf_app.auth import login_required

bp = Blueprint('beaches',__name__)

@bp.route('/beaches')
@login_required
def beaches_home():
    beach_info = get_beach_info()
    return render_template('beaches/beaches_home.html',beaches=beach_info)


def get_beach_info():
    """
    Returns a list of Beach ID and name, the IDs are according to MSW's web API.
    """
    beaches = [{'beach_id': 255, 'beach_name':'Linda Mar / Pacifica'},
                {'beach_id': 819, 'beach_name':'Ocean Beach'}]


    for beach in beaches:
        beach_url = app.config['MSW_API_URL'].format(key=app.config['MSW_API_KEY'],spot_id=beach['beach_id'])
        msw_response = requests.get(beach_url)

        try:
            msw_response.raise_for_status()
        except Exception as exc:
            print("There was a problem with MagicSeaWeed API:",(exc))

        beach_info = msw_response.json()

        parameters = ["localTimestamp", "swell.minBreakingHeight",
                    "swell.maxBreakingHeight","swell.probability",
                    "swell.components[primary].compassDirection",
                    "wind.speed","wind.compassDirection","condition.temperature"]

        beach["beach_info"] = beach_info[0]

    return beaches
