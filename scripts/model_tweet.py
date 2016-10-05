import pandas as pd 
from sklearn.externals import joblib
import numpy as np
import csv
import tweepy
import json
import matplotlib.pyplot as plt

def get_teams(df):
    
    teams = []
    
    for i,cal in enumerate(df.iterrows()):
        teams.append(cal[1]["HomeTeam"])
        teams.append(cal[1]["AwayTeam"])

        if i == 9: 
            return teams

			
def build_features(df, teams):

    team_features = []
    
    for team in teams:
        #print team_a
        team_home = df[df['HomeTeam']==team]
        team_away = df[df['AwayTeam']==team]
        
        #shots made
        team_s    = team_away["AS"].sum()  + team_home["HS"].sum()
        #shots on-target made
        team_st   = team_away["AST"].sum() + team_home["HST"].sum()
        #shots conceded
        team_sc    = team_away["HS"].sum()  + team_home["AS"].sum()
        #shots on-target conceded
        team_stc   = team_away["HST"].sum() + team_home["AST"].sum()
        #corners awarded
        team_c    = team_away["AC"].sum()  + team_home["HC"].sum()
        #corners conceded
        team_cc    = team_away["HC"].sum()  + team_home["AC"].sum()

        team_features.append([team_s,team_sc,team_st,team_stc,team_c,team_cc])

    return team_features

	
def build_target(df, teams):

    team_target = []
    
    for team in teams:
        #print team_a
        t      = df[(df['HomeTeam']==team) | (df['AwayTeam']==team)]
        team_home = df[df['HomeTeam']==team]
        team_away = df[df['AwayTeam']==team]

        team_h_win = len(team_home[team_home['FTHG']>team_home['FTAG']])
        team_a_win = len(team_away[team_away['FTAG']>team_away['FTHG']])
        team_draw = len(t[t['FTAG']==t['FTHG']])

        team_points = 3*team_a_win + 3*team_h_win + team_draw
        team_target.append(team_points)

    return team_target

def autolabel(rects, team_real, team_pred, ax):
    # attach some text labels
    for t,p,rect in zip(team_real,team_pred,rects):
        width = rect.get_width()
        ax.text(1.02*width, rect.get_y() + rect.get_height()/0.9, 
                '%.1f' % float(t-p),
                ha='left', va='top', size=14)


def main():
				
	df_week = pd.read_csv("http://www.football-data.co.uk/mmz4281/1617/I1.csv")
	teams_1617 = get_teams(df_week)
	targ_1617 = build_target(df_week, teams_1617)
	feat_1617 = build_features(df_week, teams_1617)
	model_1 = joblib.load('../data/linreg_model.pkl')
	pred_1617 = model_1.predict(feat_1617)

	ranking  = []
	realrank = []

	for t,p,tg in zip(teams_1617,pred_1617,targ_1617):
		ranking.append((t, p, tg))
		
	for t,p in zip(teams_1617,targ_1617):
		realrank.append((t, p))

		
	ranking.sort(key=lambda x: x[2],reverse=True)
	teams_pred_real = []

	for t,p,tg in ranking:
		#print t,'{:.1f}'.format(p),'{:.0f}'.format(tg), '{:.1f}'.format(tg-p)
		teams_pred_real.append((t,'{:.1f}'.format(p),'{:.1f}'.format(tg)))

	team_names = [x[0] for x in teams_pred_real]
	team_pred =  [float(x[1]) for x in teams_pred_real]
	team_real =  [float(x[2]) for x in teams_pred_real]

	team_names.reverse()
	team_pred.reverse()
	team_real.reverse()

	width = 0.35       # the width of the bars
	space = 0.07       # the space bw the bars

	n = 20
	ind = np.arange(n)

	fig, ax = plt.subplots(figsize=(12, 12))

	rects1 = ax.barh(ind, team_pred, width, color='r')
	rects2 = ax.barh(ind + width + space, team_real, width, color='#27AE60')

	# add some text for labels, title and axes ticks
	ax.set_xlabel('Points')
	ax.set_title('Serie A predicted vs real points')
	ax.set_yticks(ind + width)
	ax.set_yticklabels(team_names,size=14,family='sans-serif')

	ax.legend((rects1[0], rects2[0]), ('Predicted', 'Real'), loc=4)

	#autolabel(rects1)
	autolabel(rects2,team_real,team_pred,ax)
	plt.savefig("serieA.png")

	with open('../data/credentials.json', 'r') as fp:
		api_cred = json.load(fp)
		
	CONSUMER_KEY = api_cred["CONSUMER_KEY"]
	CONSUMER_SECRET = api_cred["CONSUMER_SECRET"]
	OAUTH_TOKEN = api_cred["OAUTH_TOKEN"]
	OAUTH_TOKEN_SECRET = api_cred["OAUTH_SECRET"]
	
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

	api = tweepy.API(auth)

	api.update_with_media(filename="serieA.png",status="After 7 matches predicted vs actual points for #serieA.")

if __name__	== "__main__":
	main()