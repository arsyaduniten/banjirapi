from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from scraper.info.models import Info
from lxml import html
import requests

info = Blueprint('info', __name__)


@info.route('/')
@info.route('/home')
def home():
    return "Welcome to the Banjir API Home. Made by Azad Arsyad"


class InfoView(MethodView):

    def get(self, page=1, state=None):
        state = state.upper()
        pageurl = 'http://publicinfobanjir.water.gov.my/View/OnlineFloodInfo/PublicWaterLevel.aspx?scode='+state
        page = requests.get(pageurl)
        tree = html.fromstring(page.content)
        stations = tree.xpath('//span[starts-with(@id, "ContentPlaceHolder1_grdStation_lbl_StationName_")]/text()')
        district = tree.xpath('//a[starts-with(@id, "ContentPlaceHolder1_grdStation_lbl_District_")]/text()')
        river_basin = tree.xpath('//span[starts-with(@id, "ContentPlaceHolder1_grdStation_lbl_basin_")]/text()')
        latest_update = tree.xpath('//span[starts-with(@id, "ContentPlaceHolder1_grdStation_lbl_LastUpdate_")]/text()')
        water_level = tree.xpath('//span[starts-with(@id, "ContentPlaceHolder1_grdStation_DailyRainFall_1_")]/text()')

        info = [{'station': stations, 'district': district, 'river_basin': river_basin, 'latest_update': latest_update, 'water_level': water_level} for stations, district, river_basin, latest_update, water_level in zip(stations, district, river_basin, latest_update, water_level)]
        if bool(request.args):
            querystring = request.args.to_dict(flat=True)
            print("qs>>>", querystring)
            print("type>>>", type(querystring))
            results = []
            for sets in info:
                for query, value in querystring.items():
                    if sets[query] == value:
                        results.append(sets.copy())
            return jsonify(results)
        else:
            return jsonify(info)


info_view = InfoView.as_view('info_view')
from scraper import app
app.add_url_rule(
    '/<string:state>', view_func=info_view, methods=['GET']
)
