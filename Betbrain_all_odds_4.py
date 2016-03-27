import time, os, datetime, re, sys, traceback, datetime, operator, copy
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AbstractScraper:
    website = ''
    pass


class BetbrainScraper(AbstractScraper):
    website = 'https://www.betbrain.com/next-matches/football/'
    scraper_name = 'Betbrain'
    #constants
    BETS_1 = [
    {'xpath': '//ol[@class="FilterChoices"]//label[@title="1X2"]//input', 'set': True},
    {'xpath': '//ol[@class="FilterChoices"]//label[@title="Both Team To Score"]//input', 'set': True},
    {'xpath': '//ol[@class="FilterChoices"]//label[@title="Clean Sheet"]//input', 'set': True},
    {'xpath': '//ol[@class="FilterChoices"]//label[@title="Corners Over Under"]//input', 'set': True},
    {'xpath': '//ol[@class="FilterChoices"]//label[@title="Double chance"]//input', 'set': True},
    {'xpath': '//ol[@class="FilterChoices"]//label[@title="Draw No Bet"]//input', 'set': True},
    {'xpath': '//ol[@class="FilterChoices"]//label[@title="First Team to score"]//input', 'set': True},
    {'xpath': '//ol[@class="FilterChoices"]//label[@title="Goal In Both Halves"]//input', 'set': True},
    {'xpath': '//ol[@class="FilterChoices"]//label[@title="Penalty Awarded"]//input', 'set': True},
    {'xpath': '//ol[@class="FilterChoices"]//label[@title="To Score In Both Halves"]//input', 'set': True},
    {'xpath': '//ol[@class="FilterChoices"]//label[@title="To Win Both Halves"]//input', 'set': True},
    {'xpath': '//ol[@class="FilterChoices"]//label[@title="To Win To Nil"]//input', 'set': True},
    ]
    BETS_2 = [
    {'xpath': '//ol[@class="FilterChoices"]//label[@title="Over Under"]//input', 'set': True},
    ]
    options = [
    {'xpath': '//a[@title="Filter the next matches with advanced tools"]', 'set': True}, 
    {'xpath': '//input[@name="selectedDisciplines"]', 'set': False},
    {'xpath': '//li[@id="l-fType"]//input[@id="fType-Mass"]', 'set': False},
    {'xpath': '//label[@class="fLiveLabel"]/input[@name="showAllEvents"]', 'set': True},
    {'xpath': '//input[@name="selectedLive"]', 'set': False},
    {'xpath': '//li[@id="l-fSport"]//label[@title="Football"]//input', 'set': True},
    {'xpath': '//input[@id="fBookies-Mass"]', 'set': False},
    {'xpath': '//li[@id="l-fBookies"]//label[@title="1xBet"]//input', 'set': True},
    {'xpath': '//li[@id="l-fBookies"]//label[@title="bet365"]//input', 'set': True},
    {'xpath': '//li[@id="l-fBookies"]//label[@title="Betcityru"]//input', 'set': True},
    {'xpath': '//li[@id="l-fBookies"]//label[@title="Betfair.com Sportsbook"]//input', 'set': True},
    {'xpath': '//li[@id="l-fBookies"]//label[@title="Favbet"]//input', 'set': True},
    {'xpath': '//li[@id="l-fBookies"]//label[@title="meridianbet"]//input', 'set': True},
    {'xpath': '//li[@id="l-fBookies"]//label[@title="Mybet"]//input', 'set': True},
    {'xpath': '//li[@id="l-fBookies"]//label[@title="Marathon"]//input', 'set': True},
    {'xpath': '//li[@id="l-fBookies"]//label[@title="Pinnacle Sports"]//input', 'set': True},
    {'xpath': '//li[@id="l-fBookies"]//label[@title="PlanetWin365"]//input', 'set': True},
    {'xpath': '//li[@id="l-fBookies"]//label[@title="William Hill"]//input', 'set': True},
    ]
    def __init__(cls):
        pass
    @classmethod
    def scrape(cls, num, n):
        try:
            BETS=[]
            opts = copy.deepcopy(cls.options)
            if num==1:
                BETS=cls.BETS_1
            if num==2:
                BETS=cls.BETS_2
            for i in range(len(BETS)):
                opts.insert(6+i, BETS[i])
            return cls._scrape(opts, num)
        except:
            print 'Failed scraping from', cls.website
            traceback.print_exc(file=sys.stdout)
            return []
    @classmethod
    def _scrape(cls, opts, num):
        print "here we go!"
        chromedriver = "/home/alice/chromedriver"
#        chromedriver = "C:/Users/Marko/Documents/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        driver = webdriver.Chrome(chromedriver)
        actions = ActionChains(driver)
        driver.maximize_window()
        wait=WebDriverWait(driver, 20)
        games=[]
        URLS = []
        game_ids=[]
        driver.get('https://www.betbrain.com/next-matches/football/')
        script = "arguments[0].value = arguments[1];"
        d = driver.find_element_by_id("username")
        driver.execute_script(script, d, 'bts') 
        d = driver.find_element_by_id("password")
        driver.execute_script(script, d, '123456') 
        driver.find_element_by_xpath('//button[@name="LoginButton"]').click()
        print "filters"
        driver.get('https://www.betbrain.com/next-matches/football/')
        cls.set_filters(wait, driver, opts)
        script = "arguments[0].value = arguments[1];"
        d = driver.find_element_by_id("fDate-Start")
        today=datetime.datetime.now().strftime("%d-%m-%y")
        driver.execute_script(script, d, today) 
        d.submit() 
        d = driver.find_element_by_id("fDate-End")
        end_date = datetime.datetime.now() + datetime.timedelta(days=7)
        end_date = end_date.strftime("%d-%m-%y")
        driver.execute_script(script, d, end_date) 
        d.submit() 
        driver.find_element_by_xpath('//form[@class="ControlFilters"]//button[@id="fSubmit"]').click()
        if num!=2:
            driver.execute_script("window.scrollTo(0, 300);")
            xp='//div[@class="MatchListStatus"]//div[@class="ExpandParams"]//a'
            element = wait.until(EC.presence_of_element_located((By.XPATH, xp))).click()
            time.sleep(6)
        print "scrolling"
        cls.scroll_down(driver)
        print "list of matches"
        list_of_matches = BeautifulSoup(driver.page_source, "html.parser") #html5lib
        list_of_matches = list_of_matches.find('ol', {'class': 'TheList Collapsable NextMatchesList NextMatchesFilterList'})
        list_of_matches = list_of_matches.findAll('li', {'itemscope': 'itemscope'})
        #driver.quit()
        a=[list_of_matches.count(t) for t in list_of_matches]
        print len(list_of_matches), max(a)
        for i in range(max(a)):
            for inx, game in enumerate(list_of_matches):
                if list_of_matches.count(game)>1:
                    del(list_of_matches[inx])
        print len(list_of_matches)
        print "processing"
        for match in list_of_matches:
            summary = match.find('div', {'class': 'MatchDetails'})
            if not summary.find('span', {'class': 'Setting DateTime'}):
                continue
            #main info
            game={}
            game['match'] = summary.find('span', {'class': 'MDxEventName'}).getText().replace('-','vs')
            [game['date'], game['time']]=cls.clean_date(summary)
            game['league']=cls.clean_league(summary)
            game['scraper_name']=cls.scraper_name
            #bets
            print game['match']
            bet_name = summary.find('span', {'class': 'ShowingBetType'}).getText()
            if bet_name == "Over Under, 2.5":
                bets = match.find('ol', {'class': "OddsList ThreeWay"})
                odds = [float(i.getText()) for i in bets.findAll('span', {'class': 'Odds'})]
                operators = [i.getText() for i in bets.findAll('span', {'class': 'BM OTBookie'})]
                game['0-2 goals']={'Odd': [odds[1]], 'Operator': [operators[1]]}
                game['3+ goals']={'Odd': [odds[0]], 'Operator': [operators[0]]}
            if bet_name == "1X2":
                bets = match.find('ol', {'class': "OddsList ThreeWay"})
                odds = [float(i.getText()) for i in bets.findAll('span', {'class': 'Odds'})]
                operators = [i.getText() for i in bets.findAll('span', {'class': 'BM OTBookie'})]
                game['1']={'Odd': [odds[0]], 'Operator': [operators[0]]}
                game['X']={'Odd': [odds[1]], 'Operator': [operators[1]]}
                game['2']={'Odd': [odds[2]], 'Operator': [operators[2]]}
            types=match.findAll('li', {'class': "SLItem"})
            for bet in types:
                try:
                    bet_name = bet.find('span', {'class': 'SLTitleText'}).getText()
                    if bet_name == '1X2':
                        try:
                            abc=game['1']
                            continue
                        except:
                            cls.get_odds(bet,game,['1','X','2'])
                            continue
                    if bet_name == '1X2, 1st half':
                        cls.get_odds(bet,game,['PP 1', 'PP X','PP 2'])
                        continue
                    if bet_name == '1X2, 2nd half':
                        cls.get_odds(bet,game,['DP 1', 'DP X','DP 2'])
                        continue
                    if bet_name == 'Both Team To Score':
                        cls.get_odds(bet,game,['GG','NG'])
                        continue
                    if bet_name == 'Both Team To Score, 1st half':
                        cls.get_odds(bet,game,['PP GG','PP NG'])
                        continue
                    if bet_name == 'Both Team To Score, 2nd half':
                        cls.get_odds(bet,game,['DP GG','DP NG'])
                        continue
                    if bet_name == 'Clean Sheet':
                        cls.get_odds(bet,game,['Team 2 0 goals', 'Team 1 0 goals'])
                        continue
                    if bet_name in ['Corners Over Under, %d.5'%d for d in range(0,11)]:
                        try:
                            abc=game['Korneri Vise(over)']
                            continue
                        except:
                            cls.get_odds(bet,game,['Korneri Vise(over)','Korneri Manje(under)'])
                            continue
                    if bet_name == 'Double chance':
                        cls.get_odds(bet,game,['1X', 'X2', '12'])
                        continue
                    if bet_name == 'Double chance, 1st half':
                        cls.get_odds(bet,game,['PP 1X', 'PP X2', 'PP 12'])
                        continue
                    if bet_name == 'Double chance, 2nd half':
                        cls.get_odds(bet,game,['DP 1X', 'DP X2', 'DP 12'])
                        continue
                    if bet_name == 'Draw No Bet':
                        cls.get_odds(bet,game,['DNB 1', 'DNB 2'])
                        continue
                    if bet_name == 'Draw No Bet, 1st half':
                        cls.get_odds(bet,game,['PP DNB 1', 'PP DNB 2'])
                        continue
                    if bet_name == 'Draw No Bet, 2nd half':
                        cls.get_odds(bet,game,['DP DNB 1', 'DP DNB 2'])
                        continue
                    if bet_name == 'First Team to score':
                        cls.get_odds(bet,game,['Team 1 Prvi Daje Gol', 'Tr 0-0', 'Team 2 Prvi Daje Gol'])
                        continue
                    if bet_name == 'First Team to score, 1st half':
                        cls.get_odds(bet,game,['Team 1 PP Prvi Daje Gol', 'PP Tr 0-0', 'Team 2 PP Prvi Daje Gol'])
                        continue
                    if bet_name == 'First Team to score, 2nd half':
                        cls.get_odds(bet,game,['Team 1 DP Prvi Daje Gol', 'DP Tr 0-0', 'Team 2 DP Prvi Daje Gol'])
                        continue
                    if bet_name == 'Goal In Both Halves':
                        cls.get_odds(bet,game,['1+PP&1+DP', 'NE 1+PP&1+DP'])
                        continue
                    if bet_name == 'Over Under, 1.5':
                        cls.get_odds(bet,game,['2+ goals','0-1 goals'])
                        continue
                    if bet_name == 'Over Under, 2.5':
                        cls.get_odds(bet,game,['3+ goals','0-2 goals'])
                        continue
                    if bet_name == 'Over Under, 3.5':
                        cls.get_odds(bet,game,['4+ goals','0-3 goals'])
                        continue
                    if bet_name == 'Over Under, 4.5':
                        cls.get_odds(bet,game,['5+ goals','0-4 goals'])
                        continue
                    if bet_name == 'Over Under, 5.5':
                        cls.get_odds(bet,game,['6+ goals','0-5 goals'])
                        continue
                    if bet_name == 'Over Under, 1st half, 1.5':
                        cls.get_odds(bet,game,['PP 2+ goals','PP 0-1 goals'])
                        continue
                    if bet_name == 'Over Under, 1st half, 2.5':
                        cls.get_odds(bet,game,['PP 3+ goals','PP 0-2 goals'])
                        continue
                    if bet_name == 'Over Under, 1st half, 3.5':
                        cls.get_odds(bet,game,['PP 4+ goals','PP 0-3 goals'])
                        continue
                    if bet_name == 'Over Under, 1st half, 4.5':
                        cls.get_odds(bet,game,['PP 5+ goals','PP 0-4 goals'])
                        continue
                    if bet_name == 'Over Under, 1st half, 5.5':
                        cls.get_odds(bet,game,['PP 6+ goals','PP 0-5 goals'])
                        continue
                    if bet_name == 'Over Under, 2nd half, 1.5':
                        cls.get_odds(bet,game,['DP 2+ goals','DP 0-1 goals'])
                        continue
                    if bet_name == 'Over Under, 2nd half, 2.5':
                        cls.get_odds(bet,game,['DP 3+ goals','DP 0-2 goals'])
                        continue
                    if bet_name == 'Over Under, 2nd half, 3.5':
                        cls.get_odds(bet,game,['DP 4+ goals','DP 0-3 goals'])
                        continue
                    if bet_name == 'Over Under, 2nd half, 4.5':
                        cls.get_odds(bet,game,['DP 5+ goals','DP 0-4 goals'])
                        continue
                    if bet_name == 'Over Under, 2nd half, 5.5':
                        cls.get_odds(bet,game,['DP 6+ goals','DP 0-5 goals'])
                        continue
                    if bet_name == 'Penalty Awarded':
                        cls.get_odds(bet,game,['Penal','NE Penal'])
                        continue
                    if bet_name == 'Team Clean Sheet, 0':
                        cls.get_odds(bet,game,['Team 1 0 goals','Team 1 1+ goals'])
                        print "ok", game['Team 1 0 goals'],game['Team 1 1+ goals']
                        continue
                    if bet_name == 'Team To Score, 0':
                        cls.get_odds(bet,game,['Team 1 0 goals','Team 1 1+ goals'])
                        print "ok", game['Team 1 0 goals'],game['Team 1 1+ goals']
                        continue
                    if bet_name == 'Team To Score, 1st half, 0':
                        cls.get_odds(bet,game,['DOM PP 1+ goals','DOM PP 0 goals'])
                        continue
                    if bet_name == 'Team To Score, 2nd half, 0':
                        cls.get_odds(bet,game,['DOM DP 1+ goals','DOM DP 0 goals'])
                        continue
                    if bet_name == 'To Score In Both Halves':
                        cls.get_odds(bet,game,['DOM 1+&1+','GOST 1+&1+'])
                        continue
                    if bet_name == 'To Win Both Halves':
                        cls.get_odds(bet,game,['Dupla pobeda 1','Dupla pobeda 2'])
                        continue
                    if bet_name == 'To Win To Nil':
                        cls.get_odds(bet,game,['Sigurna pobeda 1','Sigurna pobeda 2'])
                        continue
                except:
                    continue
            games+=[game]
        list_of_matches[:] = []
        a=[games.count(t) for t in games]
        print len(games), max(a)
        for i in range(max(a)):
            for inx, game in enumerate(games):
                if games.count(game)>1:
                    del(games[inx])
        print len(games)
        import gc
        gc.collect()
        return games
    @classmethod
    def get_odds(cls,bet,game,cols):
        try:
            odds = [float(i.getText()) for i in bet.findAll('span', {'class': 'Odds'})]
            for i in range(len(cols)):
                game[cols[i]]=odds[i]
            print odds
        except:
            print bet.find('span', {'class': 'SLTitleText'}).getText()
            pass
    #browser
    @classmethod
    def set_filters(cls,wait,driver,options):
        actions = ActionChains(driver)
        for opt in options:
            try:
                element = driver.find_element_by_xpath(opt['xpath'])
            except:
                actions.send_keys(Keys.ARROW_DOWN)
            if (element.is_selected() != opt['set']):
                try:
                    element.click()
                    time.sleep(.5)
                    if ('label' in opt['xpath']) and (element.is_selected() != opt['set']):
                        while (element.is_selected() != opt['set']):
                            element.send_keys(Keys.ARROW_DOWN)
                            element.click()
                except:
                    driver.execute_script("window.scrollBy(0, -300);")
                    element = wait.until(EC.presence_of_element_located((By.XPATH, opt['xpath'])))
                    time.sleep(1)
                    element.click()
            if 'fType-Mass' in opt['xpath']:
                element.click()
                element.click()
                time.sleep(5)
                element.click()
                element.click()
    @classmethod
    def scroll_down(cls,driver):
        xp = '//a[@title="See all the live and upcoming matches"]'
        wait=WebDriverWait(driver, 20)
        try:
            while (True):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                element = wait.until(EC.presence_of_element_located((By.XPATH, xp)))
                element.click()
                time.sleep(1.5)
        except selenium.common.exceptions.ElementNotVisibleException:
            pass	
#data processing
    @classmethod
    def clean_date(cls,summary):
        date_str = summary.find('span', {'class': 'Setting DateTime'}).getText()
        full_date=datetime.datetime.strptime(date_str, "%d/%m/%y %H:%M")
        full_date+=datetime.timedelta(hours=1)
        date_s = '%d.%d' % (full_date.day, full_date.month)
        time_s = '%d:%d' % (full_date.hour, full_date.minute)
        if (full_date.minute<10):
            time_s = '%d:0%d' % (full_date.hour, full_date.minute)
        else:
            time_s = '%d:%d' % (full_date.hour, full_date.minute)
        if (full_date.hour<10):
            time_s='0'+time_s
        return [date_s, time_s]
    @classmethod
    def clean_league(cls,summary):
        country = summary.find('span', {'class': 'Flag'}).getText()
        league = summary.find('span', {'class': 'Tour'}).getText()
        if country != 'World':
            league=country+' - '+league
        return league


s1=BetbrainScraper().scrape(1,1)
s2=BetbrainScraper().scrape(2,2)
