from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from scraper.info.models import Info
from lxml import html
import requests

info = Blueprint('info', __name__)

@info.route('/')
@info.route('/home')
def home():
    return "Welcome to the Banjir API Home."


class InfoView(MethodView):

    def get(self, page=1, state=None):
        if not state:
            infos = Info.query.paginate(page, 10).items
            res = {}
            for info in infos:
                res[info.id] = {
                    'station_name': info.name,
                    'district': info.district,
                    'river_basin': info.river_basin,
                    'last_update': info.last_update,
                    'water_level': info.water_level,
                }
        else:
            pageurl = 'http://publicinfobanjir.water.gov.my/View/OnlineFloodInfo/PublicWaterLevel.aspx?scode='+state
            page = requests.get(pageurl)
            tree = html.fromstring(page.content)
            stations = tree.xpath('//span[starts-with(@id, "ContentPlaceHolder1_grdStation_lbl_StationName_")]/text()')
            district = tree.xpath('//a[starts-with(@id, "ContentPlaceHolder1_grdStation_lbl_District_")]/text()')
            river_basin = tree.xpath('//span[starts-with(@id, "ContentPlaceHolder1_grdStation_lbl_basin_")]/text()')
            latest_update = tree.xpath('//span[starts-with(@id, "ContentPlaceHolder1_grdStation_lbl_LastUpdate_")]/text()')
            water_level = tree.xpath('//span[starts-with(@id, "ContentPlaceHolder1_grdStation_DailyRainFall_1_")]/text()')

            info = [{'station': stations, 'district': district, 'river_basin': river_basin, 'latest_update': latest_update, 'water_level': water_level} for stations, district, river_basin, latest_update, water_level in zip(stations, district, river_basin, latest_update, water_level)]
        return jsonify(info)


info_view = InfoView.as_view('info_view')
from scraper import app
app.add_url_rule(
    '/info/<string:state>', view_func=info_view, methods=['GET']
)