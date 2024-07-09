import requests

APIkey = '7f2a4b0e9e8f0aaa556e50295f047d137f05982cf576327262b0c9efa7c4b1a2'

url = f'https://apiv2.allsportsapi.com/football/?met=Livescore&APIkey={APIkey}'

response = requests.get(url, timeout=30)

def print_event(event):
    print(f"### Event: {event['event_home_team']} vs {event['event_away_team']}")
    print(f"- **Event Key:** {event['event_key']}")
    print(f"- **Event Date:** {event['event_date']}")
    print(f"- **Event Time:** {event['event_time']}")
    print(f"- **Event Status:** {event['event_status']} (live)")
    print(f"- **Country:** {event['country_name']}")
    print(f"- **League:** {event['league_name']}")
    if 'league_logo' in event and event['league_logo']:
        print(f"  - **League Logo:** ![League Logo]({event['league_logo']})")
    if 'country_logo' in event and event['country_logo']:
        print(f"  - **Country Logo:** ![Country Logo]({event['country_logo']})")
    print(f"- **Home Team:** {event['event_home_team']}")
    print(f"  - **Home Team Key:** {event['home_team_key']}")
    print(f"  - **Home Team Logo:** ![Home Team Logo]({event['home_team_logo']})")
    print(f"- **Away Team:** {event['event_away_team']}")
    print(f"  - **Away Team Key:** {event['away_team_key']}")
    print(f"  - **Away Team Logo:** ![Away Team Logo]({event['away_team_logo']})")
    print(f"- **Event Halftime Result:** {event['event_halftime_result']}")
    print(f"- **Event Final Result:** {event['event_final_result']}")
    if 'event_ft_result' in event and event['event_ft_result']:
        print(f"- **Event FT Result:** {event['event_ft_result']}")
    if 'event_penalty_result' in event and event['event_penalty_result']:
        print(f"- **Event Penalty Result:** {event['event_penalty_result']}")
    if 'event_stadium' in event and event['event_stadium']:
        print(f"- **Event Stadium:** {event['event_stadium']}")
    if 'event_referee' in event and event['event_referee']:
        print(f"- **Event Referee:** {event['event_referee']}")
    if 'event_home_formation' in event and event['event_home_formation']:
        print(f"- **Event Home Formation:** {event['event_home_formation']}")
    if 'event_away_formation' in event and event['event_away_formation']:
        print(f"- **Event Away Formation:** {event['event_away_formation']}")
    if 'goalscorers' in event and event['goalscorers']:
        print(f"- **Goalscorers:** {event['goalscorers']}")
    if 'substitutes' in event and event['substitutes']:
        print(f"- **Substitutes:** {event['substitutes']}")
    if 'cards' in event and event['cards']:
        print(f"- **Cards:** {event['cards']}")
    if 'vars' in event and event['vars']:
        print(f"- **Vars:** ")
        print(f"  - **Home Team:** {event['vars']['home_team']}")
        print(f"  - **Away Team:** {event['vars']['away_team']}")
    if 'lineups' in event and event['lineups']:
        print(f"- **Lineups:**")
        print(f"  - **Home Team:**")
        print(f"    - **Starting Lineups:** {event['lineups']['home_team']['starting_lineups']}")
        print(f"    - **Substitutes:** {event['lineups']['home_team']['substitutes']}")
        print(f"    - **Coaches:** {event['lineups']['home_team']['coaches']}")
        print(f"    - **Missing Players:** {event['lineups']['home_team']['missing_players']}")
        print(f"  - **Away Team:**")
        print(f"    - **Starting Lineups:** {event['lineups']['away_team']['starting_lineups']}")
        print(f"    - **Substitutes:** {event['lineups']['away_team']['substitutes']}")
        print(f"    - **Coaches:** {event['lineups']['away_team']['coaches']}")
        print(f"    - **Missing Players:** {event['lineups']['away_team']['missing_players']}")
    if 'statistics' in event and event['statistics']:
        print(f"- **Statistics:** {event['statistics']}")
    print()  # Add an empty line for better readability between events
#doc
if response.status_code == 200:
    result = response.json()
    for event in result["result"]:
        print_event(event)
else:
    print(f'Error: {response.status_code}')
