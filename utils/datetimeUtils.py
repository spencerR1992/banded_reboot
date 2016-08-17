from datetime import datetime
import pytz


def localizeDatetime(date, time, timezone = 'America/Chicago'):
	d = datetime.strptime(date + ' ' + time, '%m/%d/%Y  %H:%M')
	return pytz.timezone(timezone).localize(d)



