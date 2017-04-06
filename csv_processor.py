from datetime import date

from exceptions import ValueError
import csv

teams_filename = "Teams.csv"
players_filename = "Master.csv"
franchises_filename = "TeamsFranchises.csv"
batting_filename = "Batting.csv"
pitching_filename = "Pitching.csv"
fielding_filename = "Fielding.csv"
awards_players_filename = "AwardsPlayers.csv"
managers_filename = "Managers.csv"
hof_filename = "HallOfFame.csv"
allstar_filename = "AllstarFull.csv"
appearances_filename = "Appearances.csv"
postbattingstats_filename = "BattingPost.csv"
postpitchingstats_filename = "PitchingPost.csv"
postfieldingstats_filename = "FieldingPost.csv"
salaries_filename = "Salaries.csv"


nbatting = "batting"
npitching = "pitching"
nfielding = "fielding"
nteams = "teams"
nfranchises = "franchises"
nplayers = "players"
nawards_players = "awards-players"
nmanagers = "managers"
nhof = "halloffame"
nallstar = "allstar"
nappearances = "appearances"
npostbattingstats = "batting-post"
npostpitchingstats = "pitching-post"
npostfieldingstats = "fielding-post"
nsalaries = "salaries"


class Team:
    def __init__(self,t,franchises):
        self.year = int(t[0])
        self.lgID = t[1]   
        self.teamID = t[2]
        self.franchID = t[3]
        self.divID = t[4]
        self.rank = int(t[5])
        self.games = int(t[6])
        self.games_at_home = None
        if not t[7]=='' :
            self.games_at_home = int(t[7])
        self.wins = int(t[8])
        self.losses = int(t[9])
        self.division_winner = t[10]=='Y'
        self.wildcard_winner = t[11]=='Y'
        self.league_winner = t[12]=='Y'
        self.world_series_winner = t[13]=='Y'
        self.runs = int(t[14])
        self.at_bats = int(t[15])
        self.hits = int(t[16])
        self.doubles = int(t[17])
        self.triples = int(t[18])
        self.homeruns = int(t[19])
        self.bb = None
        if not t[20]=='' :
            self.bb = int(t[20])
        self.so = None
        if not t[21]=='' :
            self.so = int(t[21])
        self.stolenBases = None
        if not t[22]=='' :
            self.stolenBases = int(t[22])
        self.caughtStealing = None
        if not t[23]=='' :
            self.caughtStealing = int(t[23])
        self.hitsByPicth = None
        if not t[24]=='' :
            self.hitsByPicth = int(t[24])
        self.sacrificeFlies = None
        if not t[25]=='' :
            self.sacrificeFlies = int(t[25])
        self.opponentRuns = int(t[26])
        self.earnedRuns = int(t[27])
        self.earnedRunsAverage = float(t[28])
        self.completeGames = int(t[29])
        self.shutouts = int(t[30])
        self.saves = int(t[31])
        self.outsPitched = int(t[32])
        self.hitsAllowed = int(t[33])
        self.homerunsAllowed = int(t[34])
        self.bbAllowed = int(t[35])
        self.soByPitchers = int(t[36])
        self.errors = int(t[37])
        self.doublePlays = None
        if not t[38]=='' :
            self.doublePlays = int(t[38])
        self.fieldingPercentage = float(t[39])
        self.name = t[40]
        self.park = t[41]
        self.attendance = None
        if not t[42]=='' :
            self.attendance = int(t[42])
        self.threeYearBattersParckFactor = int(t[43])
        self.threeYearPitchersParckFactor = int(t[44])
        self.bbrefTeamId = t[45]
        self.teamIdLahman45 = t[46]
        self.retroTeamId = t[47]
        self.franchises = franchises
        
    def getFranchise(self):
        return self.franchises[self.franchID]

class Franchise:
    
    def __init__(self,f):
        self.tID = f[0]
        self.name = f[1]
        self.active = f[2]=='Y'
        self.association = f[3]
    
class BaseStats:
    
    def __init__(self,f):
        self.playerID = f[0] if not f[0]=='' else None
        self.year = int(f[1]) if not f[1]=='' else None 
        self.stintID = f[2] if not f[2]=='' else None
        self.teamID = f[3] if not f[3]=='' else None
        self.leagueID = f[4] if not f[4]=='' else None
            
class BattingStats(BaseStats):

    def __init__(self,bs):
        BaseStats.__init__(self,bs)        
        self.games =  int(bs[5]) if not bs[5]=='' else None
        self.atBats = int(bs[6]) if not bs[6]=='' else None
        self.runs =  int(bs[7]) if not bs[7]=='' else None
        self.hits = int(bs[8]) if not bs[8]=='' else None 
        self.doubles = int(bs[9]) if not bs[9]=='' else None
        self.triples = int(bs[10]) if not bs[10]=='' else None
        self.homeruns = int(bs[11]) if not bs[11]=='' else None
        self.rbi = int(bs[12]) if not bs[12]=='' else None
        self.stolenBases = int(bs[13]) if not bs[13]=='' else None
        self.caughtStealing = int(bs[14]) if not bs[14]=='' else None
        self.bb = int(bs[15]) if not bs[15]=='' else None
        self.so = int(bs[16]) if not bs[16]=='' else None
        self.intentionalWalks = int(bs[17]) if not bs[17]=='' else None
        self.hitByPitch =  int(bs[18]) if not bs[18]=='' else None
        self.sacrificeHits = int(bs[19]) if not bs[19]=='' else None
        self.sacrificeFlies = int(bs[20]) if not bs[20]=='' else None
        self.doublePlay = int(bs[21]) if not bs[21]=='' else None
    
    def ave(self):
        return (self.hits*1000/self.atBats) if self.atBats!=0 else None
    
    def totalBases(self):
        return self.hits + self.doubles + 2*self.triples + 3*self.homeruns
        
    def slugging(self):
        return self.totalBases()*1000/self.atBats if self.atBats!=0 else None
        
class PostBattingStats(BattingStats):

    def __init__(self,s):
        pbs = [s[2],s[0],s[1]]+ [s[i] for i in range(3,22)]
        BattingStats.__init__(self,pbs)
        self.round = s[1]
         

class PitchingStats(BaseStats):
    
    def __init__(self,ps):
        BaseStats.__init__(self,ps)
        self.wins = int(ps[5]) if not ps[5]=='' else None
        self.losses = int(ps[6]) if not ps[6]=='' else None
        self.games = int(ps[7]) if not ps[7]=='' else None
        self.gamesStarted = int(ps[8]) if not ps[8]=='' else None
        self.gamesCompleted = int(ps[9]) if not ps[9]=='' else None
        self.shutouts = int(ps[10]) if not ps[10]=='' else None
        self.saves = int(ps[11]) if not ps[11]=='' else None
        self.outsPitched = int(ps[12]) if not ps[12]=='' else None
        self.hits = int(ps[13]) if not ps[13]=='' else None
        self.earnedRuns = int(ps[14]) if not ps[14]=='' else None
        self.homeruns = int(ps[15]) if not ps[15]=='' else None
        self.bb = int(ps[16]) if not ps[16]=='' else None
        self.so = int(ps[17]) if not ps[17]=='' else None
        self.opponentsAverage = int(float(ps[18])*1000) if not (ps[18]=='' or ps[18]=='-') else None
        self.earnedRunAverage = float(ps[19]) if not ps[19]=='' else None
        self.intentionalWalks = int(ps[20]) if not ps[20]=='' else None
        self.wildPitches = int(ps[21]) if not ps[21]=='' else None
        self.battersHitByPitch = int(ps[22]) if not ps[22]=='' else None
        self.balks = int(ps[23]) if not ps[23]=='' else None
        self.battersFacedByPitcher = int(ps[24]) if not ps[24]=='' else None
        self.gamesFinished = int(ps[25]) if not ps[25]=='' else None
        self.runsAllowed = int(ps[26]) if not ps[26]=='' else None
        self.sacrificeByOpposingBatters = int(ps[27]) if not ps[27]=='' else None
        self.sacrificeFliesByOpposingBatters = int(ps[28]) if not ps[28]=='' else None
        self.battersGroundedIntoDoublePlay = int(ps[29]) if not ps[29]=='' else None
        
class PostPitchingStats(PitchingStats):

    def __init__(self,s):
        pps = [s[0],s[1],s[2]]+ [s[i] for i in range(3,30)]
        PitchingStats.__init__(self,pps)
        self.round = s[2]
         

class PositionFieldingStats(BaseStats):

    def __init__(self,fs):
        BaseStats.__init__(self,fs)
        self.position = fs[5] 
        self.games = int(fs[6]) if not fs[6]=='' else None
        self.gamesStarted = int(fs[7]) if not fs[7]=='' else None
        self.innOuts = int(fs[8]) if not fs[8]=='' else None
        self.putOuts = int(fs[9]) if not fs[9]=='' else None
        self.assists = int(fs[10]) if not fs[10]=='' else None
        self.errors = int(fs[11]) if not fs[11]=='' else None
        self.doublePlays = int(fs[12]) if not fs[12]=='' else None
        self.passedBalls = int(fs[13]) if not fs[13]=='' else None
        self.wildPitches = int(fs[14]) if not fs[14]=='' else None
        self.opponentStolenBases = int(fs[15]) if not fs[15]=='' else None
        self.opponentsCaughtStealing = int(fs[16]) if not fs[16]=='' else None
        self.zoneRating = int(fs[17]) if not fs[17]=='' else None

class PostPositionFieldingStats(PositionFieldingStats):

    def __init__(self,s):
        pfs = [s[0],s[1],s[4],s[2],s[3]]+ [s[i] for i in range(5,13)] + [''] + [s[i] for i in range(14,17)] + ['']
        PositionFieldingStats.__init__(self,pfs)
        self.round = s[4]
        self.triplePlay = s[13] if not s[13]=='' else None

class FieldingStats:

    def __init__(self):
        self.positions = {}

    def addStats(self,fieldingStats):
        self.positions[fieldingStats.position] = fieldingStats
        
    def __iter__(self):
        for i in self.positions:
            yield self.positions[i]
    
    def getPositionStats(self,position):
        if position in self.positions:
            return self.positions[position]
        return None
    
    def getResumeStats(self):
        return None
    
    def getPositions(self):
        return self.positions.keys()
        
    def getMostPlayedPosition(self):
        mpos = None
        played = 0
        for p in self.positions:
            if p.games > played:
                played = p.games
                mpos = p
        return mpos

class Stats:

    def __init__(self):
        self.stats = {nbatting:None,npitching:None,nfielding:None}
    
    def getFieldingStats(self):
        return self.stats[nfielding]
        
    def setFieldingStats(self,stats):
        self.stats[nfielding]=stats
            
    def getPitchingStats(self):
        return self.stats[npitching]
        
    def setPitchingStats(self,stats):
        self.stats[npitching]=stats

    def getBattingStats(self):
        return self.stats[nbatting]
        
    def setBattingStats(self,stats):
        self.stats[nbatting]=stats
        
        
class SeasonStats:

    def __init__(self,year):
        self.year = year
        self.stats = {}
        
    def getNumberOfStats(self):
        return len(self.stats.items())
        
    def getStatsKeys(self):
        return self.stats.keys()
        
    def __iter__(self):
        for i in self.stats:
            yield self.stats[i]
            
    def __len__(self):
        return len(self.stats.items())
        
    def __getitem__(self,key):
        return self.stats[key]
        
    def hasStats(self,stintID):
        return stintID in self.stats
         
    def setStats(self,stintID,stats):
        self.stats[stintID]=stats
        
    def getStats(self,stintID):
        return self.stats[stintID]

class Manage:

    def __init__(self,m):
        self.id = m[0]
        self.year = int(m[1])
        self.teamID = m[2]
        self.leagueID = m[3]
        self.inseason = int(m[4])
        self.games = int(m[5])
        self.wins = int(m[6])
        self.losses =  int(m[7])
        self.rank = int(m[8]) if not m[8]=='' else None
        self.playerManager = m[9]=='Y' 

class Management:

    def __init__(self,management):
        self.management = management
        
    def __len__(self):
        return len(self.management.items())
        
    def __getitem__(self,key):
        return self.management[key]
        
    def __iter__(self):
        for i in self.management:
            yield self.management[i]
            
    def addManage(self,manage):
        self.management[(manage.id,manage.year,manage.teamID,manage.inseason)] = manage
        
    def getManagementByPlayer(self,playerID):
        return Management({k:v for k,v in self.management.items() if v.id == playerID})
        
    def getManagementByYear(self,year):
        return Management({k:v for k,v in self.management.items() if v.year == year})

class Player:

    def __init__(self,p):
        self.salaries = Salaries({})
        self.poststats_by_year = {}
        self.appearances = PlayersAppearances({})
        self.allStar = AllStar({})
        self.hofInfo = HoF({})
        self.awards = Awards({})
        self.management = Management({})
        self.stats_by_year = {}
        self.id = p[0]
        self.birthYear = p[1]
        self.birthMonth = p[2]
        self.birthDay = p[3] 
        self.birthCountry = p[4]
        self.birthState = p[5]
        self.birthCity = p[6]
        self.deathYear = p[7]
        self.deathMonth = p[8]
        self.deathDay = p[9]
        self.deathCountry = p[10]
        self.deathState = p[11]
        self.deathCity = p[12]
        self.nameFirst = p[13]
        self.nameLast = p[14]
        self.nameGiven = p[15]
        self.weight = p[16]
        self.height = p[17]
        self.bats = p[18]
        self.throws = p[19]
        self.debut = convert_date(p[20])
        self.finalGame = convert_date(p[21])
        self.retroID = p[22]
        self.bbrefID = p[23]
        
    def fullName(self):
        return self.nameGiven+" "+self.nameLast
        
    def commonName(self):
        return self.nameFirst+" "+self.nameLast
        
    def addStats(self,year, seasonStats):
        self.stats_by_year[year] = seasonStats
        
    def addPoststats(self,year, postSeasonStats):
        self.poststats_by_year[year] = postSeasonStats
    
    def getStatsBySeason(self,seasonYear):
            return self.stats_by_year[seasonYear]
            
    def getPoststatsBySeason(self,seasonYear):
            return self.poststats_by_year[seasonYear]

    def wasPlayer(self):
        return len(self.stats_by_year.keys())!=0
        
    def wasManager(self):
        return len(self.management)!=0
            
    def setAwards(self,awards):
        self.awards = awards
        
    def getAwards(self):
        return self.awards
        
    def getManagement(self):
        return self.management
        
    def getHoFInfo(self):
        return self.hofInfo
        
    def getAllStar(self):
        return self.allStar
        
    def getAppearances(self):
        return self.appearances
        
    def getSalaries(self):
        return self.salaries
        
    def isHallOfFamer(self):
        if len(self.hofInfo) == 0 :
            return False
        for i in self.hofInfo:
            if i.inducted:
                return True
        return False
        
    def wasAllStar(self):
        return len(self.allStar)!=0
        
    def pitched(self):
        if len(self.stats_by_year.items())==0:
            return False
        for year in self.stats_by_year:
            for s in self.stats_by_year[year]:
                if s.getPitchingStats()!= None:
                    return True
        return False
        
    def getAppearancesfromYear(self,year):
        app_list = {}
        for app in self.getAppearances():
            if app.year == year:
                app_list[(app.year,app.teamID,app.playerID)] = app
        return PlayersAppearances(app_list)
        
    def getPitchingResume(self):
        return resumePitching(self.id,self.stats_by_year)
        
    def getBattingResume(self):
        return resumeBatting(self.id,self.stats_by_year)
        
    def getAppearancesResume(self):
        return resumeAppearances(self.id,self.getAppearances())
         
    def isPitcher(self):
        app = self.getAppearancesResume()
        if app==None:
            return False
        dh = app.gamesAsDesignatedHitter if app.gamesAsDesignatedHitter!=None else 0
        return app.gamesAsPitcher > (app.gamesAsCatcher + dh + app.gamesAsSecondBaseman + app.gamesAsShortstop + app.gamesAsThirdBaseman + app.gamesAsRightfielder + app.gamesAsCenterFielder + app.gamesAsLeftfielder)
        
    def getWorldSeriesTitlesPlayed(self,teams):
        theteams = teams
        titles = []
        ps = self.poststats_by_year
        for year in ps:
            if not ('WS' in ps[year].getStatsKeys()):
                continue
            st = ps[year].getStats('WS')
            bs = st.getBattingStats()
            if bs!=None:
                team = theteams[(bs.year,bs.teamID)]
                if team.world_series_winner:
                    titles.append((year,team))
                    continue
            pis = st.getPitchingStats()
            if pis!=None:
                team = theteams[(pis.year,pis.teamID)]
                if team.world_series_winner:
                    titles.append((year,team))
                    continue
            fs = st.getFieldingStats()
            if fs!=None:
                for pos in fs:
                    team = theteams[(pos.year,pos.teamID)]
                    if team.world_series_winner:
                        titles.append((year,team))
                        break
        return titles
        
    def getDebutAge(self):
        if int(self.debut.month) >= int(self.birthMonth) and int(self.debut.day) >= int(self.birthDay):
            return int(self.debut.year) - int(self.birthYear)
        return int(self.debut.year) - int(self.birthYear) -1
    
    
        

class Teams:

    def __init__(self,teams):
        self.teams = teams
        
    def __len__(self):
        return len(self.teams.items())
        
    def __getitem__(self,key):
        return self.teams[key]
        
    def getTeamsFromFranchise(self,franchID):
        fteams = {}
        for t in [i[1] for i in self.teams.items()]:
            if t.franchID == franchID:
                fteams[(t.year,t.teamID)] = t
        return Teams(fteams)
        
    def getTeamsByYear(self,year):
        yteams = {}
        for t in [i[1] for i in self.teams.items()]:
            if t.year == year:
                yteams[(t.year,t.teamID)] = t
        return Teams(yteams)
        
    def getWorldSeriesChamps(self):
        wsteams = {}
        for t in [i[1] for i in self.teams.items()]:
            if t.world_series_winner:
                wsteams[(t.year,t.teamID)] = t
        return Teams(wsteams)        

class Award:

    def __init__(self,a):
        self.playerID = a[0]
        self.awardID = a[1]
        self.year = int(a[2])
        self.leagueID = a[3]
        self.tie = a[4]=='Y'
        self.notes = a[5]
        
class Awards:

    def __init__(self,awards):
        self.awards = awards
        
    def __len__(self):
        return len(self.awards.items())
        
    def __getitem__(self,key):
        return self.awards[key]
        
    def __iter__(self):
        for i in self.awards:
            yield self.awards[i]
            
    def addAward(self,award):
        self.awards[(award.playerID,award.awardID,award.year)]=award
        
    def getAwardsByPlayer(self,playerID):
        return Awards({k:v for k,v in self.awards.items() if v.playerID == playerID})
        
    def getAwardsByYear(self,year):
        return Awards({k:v for k,v in self.awards.items() if v.year == year})    

class Franchises:

    def __init__(self,franchises ):
        self.franchises = franchises
        
    def __len__(self):
        return len(self.franchises.items())
        
    def __getitem__(self,key):
        return self.franchises[key]
    
class Players:

    def __init__(self,players ):
        self.players = players
        
    def __len__(self):
        return len(self.players.items())
        
    def __getitem__(self,key):
        return self.players[key]
    
    def __iter__(self):
        for i in self.players:
            yield self.players[i]        
        
    def fromCountry(self,country):
        return Players(players={k:v for k,v in self.players.items() if v.birthCountry.lower()==country.lower()})
    
    def startYear(self,year):
        return Players(players={k:v for k,v in self.players.items() if v.debut.year == year})
        
    def playingInYear(self,year):
        return Players(players={k:v for k,v in self.players.items() if year in v.stats_by_year})
        
    def allStar(self,year):
        return Players(players={k:v for k,v in self.players.items() if len([a for a in v.getAllStar() if a.year==year])!=0})
        
class HoFPlayerVotation:
    
    def __init__(self,hf):
        self.playerID = hf[0]
        self.year = int(hf[1])
        self.votedBy = hf[2]
        self.ballots =  int(hf[3]) if not hf[3]=='' else None
        self.neededVotes = int(hf[4])  if not hf[4]=='' else None
        self.votes = int(hf[5]) if not hf[5]=='' else None
        self.inducted = hf[6]=='Y'
        self.category = hf[7]
        self.note = hf[8]
        
class HoF:

    def __init__(self,votations):
        self.votations = votations
        
    def __len__(self):
        return len(self.votations.items())
    
    def __iter__(self):
        for i in self.votations:
            yield self.votations[i]  
            
    def addVotation(self, votation):
        self.votations[(votation.playerID,votation.year,votation.votedBy)] = votation
        
class AllStarPlayer:

    def __init__(self,asp):
        self.playerID = asp[0]
        self.year= int(asp[1])
        self.gameNum = int(asp[2])
        self.retrosheetGameID = asp[3]
        self.teamID = asp[4]
        self.lgID = asp[5]
        self.played = int(asp[6])==1 if not asp[6]=='' else None
        self.startingPos = asp[7]

class AllStar:

    def __init__(self,playersByYear):
        self.playersByYear = playersByYear
        
    def __len__(self):
        return len(self.playersByYear.items())
    
    def __iter__(self):
        for i in self.playersByYear:
            yield self.playersByYear[i]  
            
    def addAllStarPlayer(self, asPlayer):
        self.playersByYear[(asPlayer.playerID,asPlayer.year,asPlayer.gameNum)] = asPlayer
        
class Appearances:

    def __init__(self,app):
        self.year = int(app[0]) if not app[0]=='' else None
        self.teamID = app[1]
        self.leagueID = app[2]
        self.playerID = app[3]
        self.gamesPlayed = int(app[4]) if not app[4]=='' else None
        self.gamesStarted = int(app[5]) if not app[5]=='' else None
        self.gamesBatting = int(app[6]) if not app[6]=='' else None
        self.gamesAtDefense = int(app[7]) if not app[7]=='' else None
        self.gamesAsPitcher = int(app[8]) if not app[8]=='' else None
        self.gamesAsCatcher = int(app[9]) if not app[9]=='' else None
        self.gamesAsFirstbaseman = int(app[10]) if not app[10]=='' else None
        self.gamesAsSecondBaseman = int(app[11]) if not app[11]=='' else None
        self.gamesAsThirdBaseman = int(app[12]) if not app[12]=='' else None
        self.gamesAsShortstop = int(app[13]) if not app[13]=='' else None
        self.gamesAsLeftfielder = int(app[14]) if not app[14]=='' else None
        self.gamesAsCenterFielder = int(app[15]) if not app[15]=='' else None
        self.gamesAsRightfielder = int(app[16]) if not app[16]=='' else None
        self.gamesAsOutfielder = int(app[17]) if not app[17]=='' else None
        self.gamesAsDesignatedHitter = int(app[18]) if not app[18]=='' else None
        self.gamesAsPinchHitter = int(app[19]) if not app[19]=='' else None
        self.gamesAsPinchRunner = int(app[20]) if not app[20]=='' else None
        
class PlayersAppearances:

    def __init__(self,appearances):
        self.appearances = appearances
        
    def __len__(self):
        return len(self.appearances.items())
    
    def __iter__(self):
        for i in self.appearances:
            yield self.appearances[i]  
            
    def addApperances(self, appearance):
        self.appearances[(appearance.playerID,appearance.year,appearance.teamID)] = appearance
        
class Salary:

    def __init__(self,s):
        self.year = int(s[0])
        self.teamID = s[1]
        self.leagueID = s[2]
        self.playerID = s[3]
        self.salary = int(s[4])
        
class Salaries:

    def __init__(self,salaries):
        self.salaries = salaries

    def __len__(self):
        return len(self.salaries.items())
    
    def __iter__(self):
        for i in self.salaries:
            yield self.salaries[i]  
            
    def addSalary(self, salary):
        self.salaries[(salary.playerID,salary.year,salary.teamID)] = salary

def resumeBatting(playerID, stats_by_year):
    thestats_by_year = stats_by_year
    if len(thestats_by_year.items())==0:
        return None
    bs_list = [playerID,'','','','']+[0 for i in range(0,17)]
    for year in thestats_by_year:
        for s in thestats_by_year[year]:
            lsb = s.getBattingStats()
            if lsb!= None:
                bs_list[5] += lsb.games
                bs_list[6] += lsb.atBats
                bs_list[7] += lsb.runs
                bs_list[8] += lsb.hits
                bs_list[9] += lsb.doubles
                bs_list[10] += lsb.triples
                bs_list[11] += lsb.homeruns
                bs_list[12] += lsb.rbi
                bs_list[13] += lsb.stolenBases
                if lsb.caughtStealing!=None and bs_list[14]!='': 
                    bs_list[14] += lsb.caughtStealing
                else:
                    bs_list[14] = ''
                if lsb.bb!=None and bs_list[15]!='': 
                    bs_list[15] += lsb.bb
                else:
                    bs_list[15] = ''
                if lsb.so!=None and bs_list[16]!='': 
                    bs_list[16] += lsb.so
                else:
                    bs_list[16] = ''
                if lsb.intentionalWalks!=None and bs_list[17]!='': 
                    bs_list[17] += lsb.intentionalWalks
                else:
                    bs_list[17] = ''
                if lsb.hitByPitch!=None and bs_list[18]!='': 
                    bs_list[18] += lsb.hitByPitch
                else:
                    bs_list[18] = ''
                if lsb.sacrificeHits!=None and bs_list[19]!='': 
                    bs_list[19] += lsb.sacrificeHits
                else:
                    bs_list[19] = ''
                if lsb.sacrificeFlies!=None and bs_list[20]!='': 
                    bs_list[20] += lsb.sacrificeFlies
                else:
                    bs_list[20] = ''
                if lsb.doublePlay!=None and bs_list[21]!='': 
                    bs_list[21] += lsb.doublePlay
                else:
                    bs_list[21] = ''
    return  BattingStats(bs_list)


        
def resumePitching(playerID, stats_by_year):
    thestats_by_year = stats_by_year
    if len(thestats_by_year.items())==0:
        return None
    ps_list = [playerID,'','','','']+[0 for i in range(0,25)]
    for year in thestats_by_year:
        for s in thestats_by_year[year]:
            lsp = s.getPitchingStats()
            if lsp!= None:
                ps_list[5] += lsp.wins
                ps_list[6] += lsp.losses
                ps_list[7] += lsp.games
                ps_list[8] += lsp.gamesStarted
                ps_list[9] += lsp.gamesCompleted
                ps_list[10] += lsp.shutouts
                ps_list[11] += lsp.saves
                ps_list[12] += lsp.outsPitched
                ps_list[13] += lsp.hits
                ps_list[14] += lsp.earnedRuns
                ps_list[15] += lsp.homeruns
                ps_list[16] += lsp.bb
                ps_list[17] += lsp.so
                if lsp.intentionalWalks!=None and ps_list[20]!='': 
                    ps_list[20] += lsp.intentionalWalks
                else:
                    ps_list[20] = ''
                ps_list[21] += lsp.wildPitches
                ps_list[22] += lsp.battersHitByPitch
                ps_list[23] += lsp.balks
                ps_list[24] += lsp.battersFacedByPitcher
                ps_list[25] += lsp.gamesFinished
                ps_list[26] += lsp.runsAllowed
                if lsp.sacrificeByOpposingBatters!=None and ps_list[27]!='': 
                    ps_list[27] += lsp.sacrificeByOpposingBatters
                else:
                    ps_list[27] = ''
                if lsp.sacrificeFliesByOpposingBatters!=None and ps_list[28]!='': 
                    ps_list[28] += lsp.sacrificeFliesByOpposingBatters
                else:
                    ps_list[28] = ''
                if lsp.battersGroundedIntoDoublePlay!=None and ps_list[29]!='': 
                    ps_list[29] += lsp.battersGroundedIntoDoublePlay
                else:
                    ps_list[29] = ''
    ps_list[19] = round(ps_list[14]*9/(ps_list[12]/3.0),2)
    ps_list[18] = round(float(ps_list[13])/(ps_list[24]-ps_list[22]-ps_list[16]),3)
    return  PitchingStats(ps_list)
        
def resumeAppearances(playerID,appearances):
    theappearances = appearances
    if len(theappearances)==0:
        return None
    app_list = ['','','',playerID]+[0 for i in range(0,17)]
    for app in theappearances:
        if app!= None:
            if app.gamesPlayed!=None and app_list[4]!='': 
                app_list[4] += app.gamesPlayed
            else:
                app_list[4] = ''
            if app.gamesStarted!=None and app_list[5]!='': 
                app_list[5] += app.gamesStarted
            else:
                app_list[5] = ''
            if app.gamesBatting!=None and app_list[6]!='': 
                app_list[6] += app.gamesBatting
            else:
                app_list[6] = ''
            if app.gamesAtDefense!=None and app_list[7]!='': 
                app_list[7] += app.gamesAtDefense
            else:
                app_list[7] = ''
            app_list[8] += app.gamesAsPitcher
            app_list[9] += app.gamesAsCatcher
            app_list[10] += app.gamesAsFirstbaseman
            app_list[11] += app.gamesAsSecondBaseman
            app_list[12] += app.gamesAsThirdBaseman
            app_list[13] += app.gamesAsShortstop
            app_list[14] += app.gamesAsLeftfielder
            app_list[15] += app.gamesAsCenterFielder
            app_list[16] += app.gamesAsRightfielder
            if app.gamesAsOutfielder!=None and app_list[17]!='': 
                app_list[17] += app.gamesAsOutfielder
            else:
                app_list[17] = ''
            if app.gamesAsDesignatedHitter!=None and app_list[18]!='': 
                app_list[18] += app.gamesAsDesignatedHitter
            else:
                app_list[18] = ''
            if app.gamesAsPinchHitter!=None and app_list[19]!='': 
                app_list[19] += app.gamesAsPinchHitter
            else:
                app_list[19] = ''
            if app.gamesAsPinchRunner!=None and app_list[20]!='': 
                app_list[20] += app.gamesAsPinchRunner
            else:
                app_list[20] = ''
    return  Appearances(app_list)
    
def convert_date(thedate):
    d = thedate.split("-")
    if len(d)!=3:
        return None
    return date(int(d[0]),int(d[1]),int(d[2]))
    
def get_data_lists(folder="db/"):
    lists = {}
    lists[nteams] = list(csv.reader(open(folder+teams_filename,"r"),delimiter=","))[1:]
    lists[nfranchises] = list(csv.reader(open(folder+franchises_filename,"r"),delimiter=","))[1:]
    lists[nplayers] = list(csv.reader(open(folder+players_filename,"r"),delimiter=","))[1:]
    lists[nbatting] = list(csv.reader(open(folder+batting_filename,"r"),delimiter=","))[1:]
    lists[npitching] = list(csv.reader(open(folder+pitching_filename,"r"),delimiter=","))[1:]
    lists[nfielding] = list(csv.reader(open(folder+fielding_filename,"r"),delimiter=","))[1:]
    lists[nawards_players] = list(csv.reader(open(folder+awards_players_filename,"r"),delimiter=","))[1:]
    lists[nmanagers] = list(csv.reader(open(folder+managers_filename,"r"),delimiter=","))[1:]
    lists[nhof] = list(csv.reader(open(folder+hof_filename,"r"),delimiter=","))[1:]
    lists[nallstar] = list(csv.reader(open(folder+allstar_filename,"r"),delimiter=","))[1:]
    lists[nappearances] = list(csv.reader(open(folder+appearances_filename,"r"),delimiter=","))[1:]
    lists[npostbattingstats] = list(csv.reader(open(folder+postbattingstats_filename,"r"),delimiter=","))[1:]
    lists[npostpitchingstats] = list(csv.reader(open(folder+postpitchingstats_filename,"r"),delimiter=","))[1:]
    lists[npostfieldingstats] = list(csv.reader(open(folder+postfieldingstats_filename,"r"),delimiter=","))[1:]
    lists[nsalaries] = list(csv.reader(open(folder+salaries_filename,"r"),delimiter=","))[1:]
    
    return lists

def get_salaries(data_lists=get_data_lists(folder="db/")):
    salaries = {}
    for s in data_lists[nsalaries]:
        salaries[(s[3],int(s[0]),s[1])] = Salary(s)
    return Salaries(salaries)


def get_appearances(data_lists=get_data_lists(folder="db/")):
    playersAppearances = {}
    for app in data_lists[nappearances]:
        playersAppearances[(int(app[0]),app[1],app[3])] = Appearances(app)
    return PlayersAppearances(playersAppearances)
    
def get_allstar(data_lists=get_data_lists(folder="db/")):
    allstarplayers = {}
    for asp in data_lists[nallstar]:
        allstarplayers[(asp[0],int(asp[1]),asp[2])] = AllStarPlayer(asp)
    return AllStar(allstarplayers)


def get_hof(data_lists=get_data_lists(folder="db/")):
    votations = {}
    for hf in data_lists[nhof]:
        votations[(hf[0],int(hf[1]),hf[2])] = HoFPlayerVotation(hf)
    return HoF(votations)

def get_management(data_lists=get_data_lists(folder="db/")):
    manages = {}
    for t in data_lists[nmanagers]:
        manages[(t[0],t[1],t[2],t[4])] = Manage(t)
    return Management(manages)

def get_teams(data_lists=get_data_lists(folder="db/")):
    franchises = get_franchises(data_lists)
    teams = {}
    for t in data_lists[nteams]:
        teams[(int(t[0]),t[2])] = Team(t,franchises)
    return Teams(teams)

def get_franchises(data_lists=get_data_lists(folder="db/")):
    franchises = {}
    for t in data_lists[nfranchises]:
        franchises[t[0]]=Franchise(t)
    return Franchises(franchises)
    
def get_awards(data_lists=get_data_lists(folder="db/")):
    awards = {}
    for t in data_lists[nawards_players]:
        awards[(t[0],t[1],t[2])]=Award(t)
    return Awards(awards)

def get_stats(data_lists=get_data_lists(folder="db/")):
    items = {}
    for i in data_lists[nbatting]:
        b = BattingStats(i)
        if not b.playerID in items:
            items[b.playerID]= {}
        if not b.year in items[b.playerID]:
            ss = SeasonStats(b.year)
            s = Stats()
            s.setBattingStats(b)
            ss.setStats(b.stintID,s)
            items[b.playerID][b.year] = ss
        elif not items[b.playerID][b.year].hasStats(b.stintID):
            s = Stats()
            s.setBattingStats(b)
            items[b.playerID][b.year].setStats(b.stintID,s)
        else: 
            items[b.playerID][b.year].getStats(b.stintID).setBattingStats(b)
    for i in data_lists[npitching]:
        p = PitchingStats(i)
        if not p.playerID in items:
            items[p.playerID]= {}
        if not p.year in items[p.playerID]:
            ss = SeasonStats(p.year)
            s = Stats()
            s.setPitchingStats(p)
            ss.setStats(p.stintID,s)
            items[p.playerID][p.year] = ss
        elif not items[p.playerID][p.year].hasStats(p.stintID):
            s = Stats()
            s.setPitchingStats(p)
            items[p.playerID][p.year].setStats(p.stintID,s)
        else: 
            items[p.playerID][p.year].getStats(p.stintID).setPitchingStats(p)
    for i in data_lists[nfielding]:
        f = PositionFieldingStats(i)
        if not f.playerID in items:
            items[f.playerID]= {}
        if not f.year in items[f.playerID]:
            ss = SeasonStats(p.year)
            s = Stats()
            fs = FieldingStats()
            fs.addStats(f)
            s.setFieldingStats(fs)
            ss.setStats(f.stintID,s)
            items[f.playerID][p.year] = ss
        elif not items[f.playerID][f.year].hasStats(f.stintID):
            s = Stats()
            fs = FieldingStats()
            fs.addStats(f)
            s.setFieldingStats(fs)
            ss.setStats(f.stintID,s)
            items[f.playerID][f.year].setStats(f.stintID,s)
        else: 
            fs = items[f.playerID][f.year].getStats(f.stintID).getFieldingStats()
            if fs == None:
                ft = FieldingStats()
                ft.addStats(f)
                items[f.playerID][f.year].getStats(f.stintID).setFieldingStats(ft)
            else:
                items[f.playerID][f.year].getStats(f.stintID).getFieldingStats().addStats(f)                    
    return items
    
def get_poststats(data_lists=get_data_lists(folder="db/")):
    items = {}
    for i in data_lists[npostbattingstats]:
        b = PostBattingStats(i)
        if not b.playerID in items:
            items[b.playerID]= {}
        if not b.year in items[b.playerID]:
            ss = SeasonStats(b.year)
            s = Stats()
            s.setBattingStats(b)
            ss.setStats(b.stintID,s)
            items[b.playerID][b.year] = ss
        elif not items[b.playerID][b.year].hasStats(b.stintID):
            s = Stats()
            s.setBattingStats(b)
            items[b.playerID][b.year].setStats(b.stintID,s)
        else: 
            items[b.playerID][b.year].getStats(b.stintID).setBattingStats(b)
    for i in data_lists[npostpitchingstats]:
        p = PostPitchingStats(i)
        if not p.playerID in items:
            items[p.playerID]= {}
        if not p.year in items[p.playerID]:
            ss = SeasonStats(p.year)
            s = Stats()
            s.setPitchingStats(p)
            ss.setStats(p.stintID,s)
            items[p.playerID][p.year] = ss
        elif not items[p.playerID][p.year].hasStats(p.stintID):
            s = Stats()
            s.setPitchingStats(p)
            items[p.playerID][p.year].setStats(p.stintID,s)
        else: 
            items[p.playerID][p.year].getStats(p.stintID).setPitchingStats(p)
    for i in data_lists[npostfieldingstats]:
        f = PostPositionFieldingStats(i)
        if not f.playerID in items:
            items[f.playerID]= {}
        if not f.year in items[f.playerID]:
            ss = SeasonStats(p.year)
            s = Stats()
            fs = FieldingStats()
            fs.addStats(f)
            s.setFieldingStats(fs)
            ss.setStats(f.stintID,s)
            items[f.playerID][p.year] = ss
        elif not items[f.playerID][f.year].hasStats(f.stintID):
            s = Stats()
            fs = FieldingStats()
            fs.addStats(f)
            s.setFieldingStats(fs)
            ss.setStats(f.stintID,s)
            items[f.playerID][f.year].setStats(f.stintID,s)
        else: 
            fs = items[f.playerID][f.year].getStats(f.stintID).getFieldingStats()
            if fs == None:
                ft = FieldingStats()
                ft.addStats(f)
                items[f.playerID][f.year].getStats(f.stintID).setFieldingStats(ft)
            else:
                items[f.playerID][f.year].getStats(f.stintID).getFieldingStats().addStats(f)                    
    return items
            
def get_players(data_lists=get_data_lists(folder="db/")):
    players = {}
    for p in data_lists[nplayers]:
        temp_player = Player(p)
        players[p[0]] = temp_player
    pl = Players(players)
    salaries = get_salaries(data_lists)
    for salary in salaries:
        try:
            pl[salary.playerID].getSalaries().addSalary(salary)
        except:
            print("Salary: "+salary.playerID)
    awards = get_awards(data_lists)
    for a in awards:
        pl[a.playerID].getAwards().addAward(a)
    management = get_management(data_lists)
    for m in management:
        try:
            pl[m.id].getManagement().addManage(m)
        except:
            print("Management: "+m.id)
    items = get_stats(data_lists)
    for playerID in items:
        for year in items[playerID]:
            pl[playerID].addStats(year,items[playerID][year])
    postitems = get_poststats(data_lists)
    for playerID in postitems:
        for year in postitems[playerID]:
            pl[playerID].addPoststats(year,postitems[playerID][year])
    hof = get_hof(data_lists)
    for v in hof:
        try:
            pl[v.playerID].getHoFInfo().addVotation(v)
        except:
            print("HoF: "+v.playerID)
    allstar = get_allstar(data_lists)
    for asp in allstar:
        try:
            pl[asp.playerID].getAllStar().addAllStarPlayer(asp)
        except:
            print("AllStar: "+asp.playerID)
    appearances = get_appearances(data_lists)
    for app in appearances:
        try:
            pl[app.playerID].getAppearances().addApperances(app)
        except:
            print("Appearances: "+app.playerID)
    return pl
    

def main():

    return 0

if __name__ == '__main__':
    main()

