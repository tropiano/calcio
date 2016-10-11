import datetime
import model_tweet as mdt

def schedule():
	
	update_dates = ['2016-10-18','2016-10-24','2016-10-28','2016-11-01','2016-11-07','2016-11-21','2016-11-29','2016-12-06','2016-12-13','2016-12-19','2016-12-23']
	today_date =  datetime.date.today().isoformat()

	if today_date in update_dates:
		mdt.post_tweet()
	