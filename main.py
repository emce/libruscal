import json

import caldav
from librus_apix.client import new_client, Client, Token

from applecalendar import AppleCalendar
from current_week import CurrentWeek

from flask import Flask, jsonify
from flask_restx import Api, Resource

from schedule import Schedule

app = Flask(__name__)
with open('config.json', 'r') as f:
    app.config.update(json.load(f))

api = Api(app, version=app.config['VERSION'], title='Librus & iCloud Sync API',
          description='API for syncing Librus timetable with iCloud Calendar')

ns = api.namespace('sync', description='Sync operations')


@ns.route('/sync')
class LibrusICloudSync(Resource):
    @api.doc(params={'librus_username': 'Librus username',
                     'librus_password': 'Librus password',
                     'icloud_name': 'iCloud calendar name',
                     'icloud_username': 'iCloud username',
                     'icloud_password': 'iCloud password'})
    def post(self):
        params = api.payload
        calendar = AppleCalendar(
            get_dav_client(params['icloud_username'], params['icloud_password']),
            params['icloud_name']
        )
        schedule = Schedule(get_librus_client(params['librus_username'], params['librus_password']))
        result = calendar.process_schedule(schedule.get_current_week())
        return jsonify(result)


nt = api.namespace('read', description='Read operations')


@nt.route('/schedule')
class ReadSchedule(Resource):
    @api.doc(params={'librus_username': 'Librus username',
                     'librus_password': 'Librus password'})
    def post(self):
        params = api.payload
        current_week = CurrentWeek()
        schedule = Schedule(get_librus_client(params['librus_username'], params['librus_password']))
        return jsonify({
            'start': current_week.monday,
            'end': current_week.friday,
            'events': schedule.get_current_week()
        })


@nt.route('/calendar')
class ReadCalendar(Resource):
    @api.doc(params={'icloud_name': 'iCloud calendar name',
                     'icloud_username': 'iCloud username',
                     'icloud_password': 'iCloud password'})
    def post(self):
        params = api.payload
        current_week = CurrentWeek()
        calendar = AppleCalendar(get_dav_client(params['icloud_username'], params['icloud_password']), params['icloud_name'])
        return jsonify({
            'start': current_week.monday,
            'end': current_week.friday,
            'events': calendar.get_current_week()
        })


@nt.route('/clear')
class ClearCalendar(Resource):
    @api.doc(params={'icloud_name': 'iCloud calendar name',
                     'icloud_username': 'iCloud username',
                     'icloud_password': 'iCloud password'})
    def post(self):
        params = api.payload
        calendar = AppleCalendar(get_dav_client(params['icloud_username'], params['icloud_password']), params['icloud_name'])
        return jsonify(calendar.clear_current_week())


def get_librus_client(login, password):
    client: Client = new_client()
    _token: Token = client.get_token(login, password)
    key = client.token.API_Key
    token = Token(API_Key=key)
    return new_client(token=token)


def get_dav_client(login, password):
    url = "https://caldav.icloud.com"
    client = caldav.DAVClient(url=url, username=login, password=password)
    return client.principal()


if __name__ == '__main__':
    app.run(debug=True, host=app.config['HOST'], port=app.config['PORT'])
