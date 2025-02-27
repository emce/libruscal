import json
from applecalendar import AppleCalendar, CurrentWeek

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
        calendar = AppleCalendar(params['icloud_username'], params['icloud_password'], params['icloud_name'])
        schedule = Schedule(params['librus_username'], params['librus_password'])

        return jsonify({'success': True})


nt = api.namespace('read', description='Read operations')

@nt.route('/schedule')
class ReadSchedule(Resource):
    @api.doc(params={'librus_username': 'Librus username',
                     'librus_password': 'Librus password'})
    def post(self):
        params = api.payload
        current_week = CurrentWeek()
        schedule = Schedule(params['librus_username'], params['librus_password'])
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
        calendar = AppleCalendar(params['icloud_username'], params['icloud_password'], params['icloud_name'])
        return jsonify({
            'start': current_week.monday,
            'end': current_week.friday,
            'events': calendar.get_current_week()
        })


if __name__ == '__main__':
    app.run(debug=True, host=app.config['HOST'], port=app.config['PORT'])