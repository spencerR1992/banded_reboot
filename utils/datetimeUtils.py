from datetime import datetime
import pytz


def localizeDatetime(date, time, timezone = 'America/Chicago'):
	try:
		d = datetime.strptime(date + ' ' + time, '%m/%d/%Y  %H:%M')
		return pytz.timezone(timezone).localize(d)
	except Exception, e:
		raise Exception('datetime did not conform to expected behavior')



