test = [[{'game_id': -1, 'name': 'standard', 'start_time': '2023-02-18 05:25:33.486758+00:00', 'finish_time': None, 'ends': 0, 'winner': '', 'competitors': [{'player_id': 1, 'first_name': 'Sally', 'last_name': '1', 'score': '1'}, {'player_id': 2, 'first_name': 'bob', 'last_name': '2', 'score': '2'}]}],
[{'game_id': -1, 'name': 'standard', 'start_time': '2023-02-18 05:25:33.486758+00:00', 'finish_time': None, 'ends': 0, 'winner': '', 'competitors': [{'player_id': 1, 'first_name': 'Jen', 'last_name': '1', 'score': '6'}, {'player_id': 2, 'first_name': 'harry', 'last_name': '2', 'score': '3'}]}]]

config = [{'game_id': -1, 'name': 'standard', 'start_time': '2023-02-18 05:25:33.486758+00:00', 'finish_time': None, 'ends': 0, 'winner': '', 'competitors': [{'player_id': 1, 'first_name': '', 'last_name': '', 'score': ''}, {'player_id': 2, 'first_name': '', 'last_name': '', 'score': ''}]}]

for i in test:
	for o in i[0]['competitors']:
		print(o['first_name'][0])