import datetime
import model_tweet as mdt

def schedule_seriea():
  
  update_dates = ['2016-10-18','2016-10-24','2016-10-28','2016-11-01','2016-11-07','2016-11-21','2016-11-29','2016-12-06','2016-12-13','2016-12-19','2016-12-23']
	
  today_date =  datetime.date.today().isoformat()
  
  if today_date in update_dates:
    mdt.post_tweet("seriea")
    

def schedule_epl():
  
  update_dates = ['2016-11-22','2016-11-28','2016-12-06','2016-12-12','2016-12-15','2016-12-20','2016-12-29','2017-01-02','2017-01-05']
	
  today_date =  datetime.date.today().isoformat()
  
  if today_date in update_dates:
    mdt.post_tweet("epl")

def schedule_laliga():
  
  update_dates = ['2016-11-29','2016-12-06','2016-12-13','2016-12-20','2017-01-09']
	
  today_date =  datetime.date.today().isoformat()
  
  if today_date in update_dates:
    mdt.post_tweet("laliga")

def schedule_bundesliga():
  
  update_dates = ['2016-12-05','2016-12-12','2016-12-19','2017-12-22','2017-01-23']
	
  today_date =  datetime.date.today().isoformat()
  
  if today_date in update_dates:
    mdt.post_tweet("bundesliga")
    
if __name__	== "__main__":
	schedule_epl()
	schedule_seriea()
	schedule_laliga()
	schedule_bundesliga()