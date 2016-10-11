import datetime
import model_tweet as mdt

def schedule():
	
	update_dates = ['2016-10-11','2016-10-11','2016-10-11','2016-10-11','2016-10-11','2016-10-11','2016-10-11','2016-10-11','2016-10-11','2016-10-11']
	today_date =  datetime.date.today().isoformat()

	if today_date in update_dates:
		mdt.post_tweet()
	