RESULT_DICT = 1
COMPETITION_TYPE = 0
BANNED_PLAYER = 'ban'

def printCompetitor(competitor):
    '''
    Given the data of a competitor, the function prints it in a specific format.
    Arguments:
        competitor: {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country, 
                        'result': result}
    '''
    competition_name = competitor['competition name']
    competition_type = competitor['competition type']
    competitor_id = competitor['competitor id']
    competitor_country = competitor['competitor country']
    result = competitor['result']
    
    assert(isinstance(result, int)) # Updated. Safety check for the type of result

    print(f'Competitor {competitor_id} from {competitor_country} participated in {competition_name} ({competition_type}) and scored {result}')


def printCompetitionResults(competition_name, winning_gold_country, winning_silver_country, winning_bronze_country):
    '''
    Given a competition name and its champs countries, the function prints the winning countries 
        in that competition in a specific format.
    Arguments:
        competition_name: the competition name
        winning_gold_country, winning_silver_country, winning_bronze_country: the champs countries
    '''
    undef_country = 'undef_country'
    countries = [country for country in [winning_gold_country, winning_silver_country, winning_bronze_country] if country != undef_country]
    print(f'The winning competitors in {competition_name} are from: {countries}')


def key_sort_competitor(competitor):
    '''
    A helper function that creates a special key for sorting competitors.
    Arguments:
        competitor: a dictionary contains the data of a competitor in the following format: 
                    {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country, 
                        'result': result}
    '''
    competition_name = competitor['competition name']
    result = competitor['result']
    return (competition_name, result)

def readParseData(file_name):
    '''
    Given a file name, the function returns a list of competitors.
    Arguments: 
        file_name: the input file name. Assume that the input file is in the directory of this script.
    Return value:
        A list of competitors, such that every record is a dictionary, in the following format:
            {'competition name': competition_name, 'competition type': competition_type,
                'competitor id': competitor_id, 'competitor country': competitor_country, 
                'result': result}
    '''
    competitors_in_competitions = []
    competitors_list = {}
    with open(file_name, 'r') as fd:
        for line in fd:
            args = line.split()
            if args[0] == 'competitor':
                #{(int)competitor id: (str)competitor country}
                competitors_list[int(args[1])] = args[2]
            elif args[0] == 'competition':
                tmp_dict = {
                    'competition name': args[1],
                    'competitor id': int(args[2]),
                    'competition type': args[3],
                    'result': int(args[4])
                }
                competitors_in_competitions.append(tmp_dict)
    for obj in competitors_in_competitions:
        obj['competitor country'] = competitors_list[obj['competitor id']]
    return competitors_in_competitions

def calcNonKnockoutChamps(result_dict, is_timed):
    champs = []
    tmp_list = sorted(list(result_dict.items()), key=lambda x: x[1], reverse=(is_timed != True))
    id_list = [competitor_id for (competitor_id, _) in tmp_list[0:3]]
    champs.extend(id_list)
    undef_country = 'undef_country'
    while len(champs) < 3:
        champs.append(undef_country)
    return champs
       
def calcKnockoutChamps(result_dict):
    undef_country = 'undef_country'
    champs = [undef_country, undef_country, undef_country]
    for comperitor_id in result_dict:
        if result_dict[comperitor_id] == 1:
            champs[0] = comperitor_id
        elif result_dict[comperitor_id] == 2:
            champs[1] = comperitor_id
        elif result_dict[comperitor_id] == 3:
            champs[2] = comperitor_id
    return champs

def calcCompetitionsResults(competitors_in_competitions):
    '''
    Given the data of the competitors, the function returns the champs countries for each competition.
    Arguments:
        competitors_in_competitions: A list that contains the data of the competitors
                                    (see readParseData return value for more info)
    Retuen value:
        A list of competitions and their champs (list of lists). 
        Every record in the list contains the competition name and the champs, in the following format:
        [competition_name, winning_gold_country, winning_silver_country, winning_bronze_country]
    '''
    competitions_champs = []
    competitions_list = {}
    for obj in competitors_in_competitions:
        if obj['competition name'] in competitions_list:
            result_dict = competitions_list[obj['competition name']][RESULT_DICT]
            if obj['competitor id'] in result_dict:
                result_dict[obj['competitor id']] = BANNED_PLAYER
            else:
                result_dict[obj['competitor id']] = obj['result']
        else:
            competitions_list[obj['competition name']] = [obj['competition type'], {obj['competitor id']: obj['result']}]
    for competition, list in competitions_list.items():
        no_bans = {competitor: result for (competitor, result) in list[RESULT_DICT].items() if isinstance(result, int)}
        if list[COMPETITION_TYPE] == 'timed':
            champs = calcNonKnockoutChamps(no_bans, is_timed=True)
        elif list[COMPETITION_TYPE] == 'untimed':
            champs = calcNonKnockoutChamps(no_bans, is_timed=False)
        elif list[COMPETITION_TYPE] == 'knockout':
            champs = calcKnockoutChamps(no_bans)
        undef_country = 'undef_country'
        if champs[0] != undef_country:
            country_list = []
            for competitor in champs:
                if competitor == undef_country:
                    country_list.append(undef_country)
                else:
                    for entry in competitors_in_competitions:
                        if entry['competitor id'] == competitor:
                            country_list.append(entry['competitor country'])
                            break
            competitions_champs.append([competition, *country_list])
    return competitions_champs

def partA(file_name = 'input.txt', allow_prints = True):
    # read and parse the input file
    competitors_in_competitions = readParseData(file_name)
    if allow_prints:
        # competitors_in_competitions are sorted by competition_name (string) and then by result (int)
        for competitor in sorted(competitors_in_competitions, key=key_sort_competitor):
            printCompetitor(competitor)
    
    # calculate competition results
    competitions_results = calcCompetitionsResults(competitors_in_competitions)
    if allow_prints:
        for competition_result_single in sorted(competitions_results):
            printCompetitionResults(*competition_result_single)
    
    return competitions_results


#def partB(file_name = 'input.txt'):
 #   competitions_results = partA(file_name, allow_prints = False)
    # TODO Part B


if __name__ == "__main__":
    '''
    The main part of the script.
    __main__ is the name of the scope in which top-level code executes.
    
    To run only a single part, comment the line below which correspondes to the part you don't want to run.
    '''    
    file_name = 'test2.txt'

    partA(file_name)
   # partB(file_name)