import json

print(json.dumps({'cardsInHand': [{'name': 'Ice Asteroid', 'calculatedCost': 23, 'warnings': ['maxoceans']}], 'ceoCardsInHand': [], 'dealtCorporationCards': [{'name': 'Helion', 'calculatedCost': 0}, {'name': 'Thorgate', 'calculatedCost': 0, 'discount': [{'tag': 'power', 'amount': 3}]}], 'dealtPreludeCards': [], 'dealtCeoCards': [], 'dealtProjectCards': [{'name': 'Asteroid Mining', 'calculatedCost': 30}, {'name': 'Sponsors', 'calculatedCost': 6}, {'name': 'Space Elevator', 'calculatedCost': 27}, {'name': 'Arctic Algae', 'calculatedCost': 12}, {'name': 'Ironworks', 'calculatedCost': 11}, {'name': 'Steelworks', 'calculatedCost': 15}, {'name': 'Extreme-Cold Fungus', 'calculatedCost': 13}, {'name': 'Bribed Committee', 'calculatedCost': 7}, {'name': 'Hackers', 'calculatedCost': 3}, {'name': 'Lightning Harvest', 'calculatedCost': 8}], 'draftedCards': [], 'game': {'awards': [{'playerName': '', 'playerColor': '', 'name': 'Landlord', 'scores': []}, {'playerName': 'ki', 'playerColor': 'red', 'name': 'Scientist', 'scores': [{'playerColor': 'yellow', 'playerScore': 2}, {'playerColor': 'red', 'playerScore': 1}, {'playerColor': 'green', 'playerScore': 0}]}, {'playerName': 'Yellow', 'playerColor': 'yellow', 'name': 'Banker', 'scores': [{'playerColor': 'yellow', 'playerScore': 7}, {'playerColor': 'red', 'playerScore': -1}, {'playerColor': 'green', 'playerScore': 1}]}, {'playerName': '', 'playerColor': '', 'name': 'Thermalist', 'scores': []}, {'playerName': 'Green', 'playerColor': 'green', 'name': 'Miner', 'scores': [{'playerColor': 'yellow', 'playerScore': 18}, {'playerColor': 'red', 'playerScore': 4}, {'playerColor': 'green', 'playerScore': 27}]}], 'colonies': [], 'deckSize': 164, 'discardedColonies': [], 'expectedPurgeTimeMs': 1738007411761, 'gameAge': 416, 'gameOptions': {'altVenusBoard': False, 'aresExtension': False, 'boardName': 'tharsis', 'bannedCards': [], 'includedCards': [], 'ceoExtension': False, 'coloniesExtension': False, 'communityCardsOption': False, 'corporateEra': True, 'draftVariant': True, 'escapeVelocityMode': False, 'escapeVelocityBonusSeconds': 2, 'fastModeOption': False, 'includeFanMA': False, 'includeVenusMA': True, 'initialDraftVariant': False, 'moonExpansion': False, 'pathfindersExpansion': False, 'preludeDraftVariant': True, 'preludeExtension': False, 'prelude2Expansion': False, 'promoCardsOption': False, 'politicalAgendasExtension': 'Standard', 'removeNegativeGlobalEvents': False, 'showOtherPlayersVP': False, 'showTimers': True, 'shuffleMapOption': False, 'solarPhaseOption': False, 'soloTR': False, 'randomMA': 'No randomization', 'requiresMoonTrackCompletion': False, 'requiresVenusTrackCompletion': False, 'turmoilExtension': False, 'twoCorpsVariant': False, 'venusNextExtension': False, 'undoOption': False, 'underworldExpansion': False}, 'generation': 17, 'globalsPerGeneration': [], 'isSoloModeWin': False, 'lastSoloGeneration': 14, 'milestones': [{'playerName': 'ki', 'playerColor': 'red', 'name': 'Terraformer', 'scores': []}, {'playerName': 'Yellow', 'playerColor': 'yellow', 'name': 'Mayor', 'scores': []}, {'playerName': 'Yellow', 'playerColor': 'yellow', 'name': 'Gardener', 'scores': []}, {'playerName': '', 'playerColor': '', 'name': 'Builder', 'scores': []}, {'playerName': '', 'playerColor': '', 'name': 'Planner', 'scores': []}], 'oceans': 9, 'oxygenLevel': 7, 'passedPlayers': ['red', 'green'], 'phase': 'action', 'spaces': [{'x': -1, 'y': -1, 'id': '01', 'spaceType': 'colony', 'bonus': []}, {'x': -1, 'y': -1, 'id': '02', 'spaceType': 'colony', 'bonus': []}, {'x': 4, 'y': 0, 'id': '03', 'spaceType': 'land', 'bonus': [1, 1]}, {'x': 5, 'y': 0, 'id': '04', 'spaceType': 'ocean', 'bonus': [1, 1], 'tileType': 1}, {'x': 6, 'y': 0, 'id': '05', 'spaceType': 'land', 'bonus': [], 'tileType': 2, 'color': 'red'}, {'x': 7, 'y': 0, 'id': '06', 'spaceType': 'ocean', 'bonus': [3]}, {'x': 8, 'y': 0, 'id': '07', 'spaceType': 'ocean', 'bonus': [], 'tileType': 1}, {'x': 3, 'y': 1, 'id': '08', 'spaceType': 'land', 'bonus': []}, {'x': 4, 'y': 1, 'id': '09', 'spaceType': 'land', 'bonus': [1]}, {'x': 5, 'y': 1, 'id': '10', 'spaceType': 'land', 'bonus': [], 'tileType': 0, 'color': 'yellow'}, {'x': 6, 'y': 1, 'id': '11', 'spaceType': 'land', 'bonus': [], 'tileType': 0, 'color': 'red'}, {'x': 7, 'y': 1, 'id': '12', 'spaceType': 'land', 'bonus': []}, {'x': 8, 'y': 1, 'id': '13', 'spaceType': 'ocean', 'bonus': [3, 3]}, {'x': 2, 'y': 2, 'id': '14', 'spaceType': 'land', 'bonus': [3]}, {'x': 3, 'y': 2, 'id': '15', 'spaceType': 'land', 'bonus': []}, {'x': 4, 'y': 2, 'id': '16', 'spaceType': 'land', 'bonus': [], 'tileType': 2, 'color': 'yellow'}, {'x': 5, 'y': 2, 'id': '17', 'spaceType': 'land', 'bonus': [], 'tileType': 0, 'color': 'red'}, {'x': 6, 'y': 2, 'id': '18', 'spaceType': 'land', 'bonus': [], 'tileType': 2, 'color': 'yellow'}, {'x': 7, 'y': 2, 'id': '19', 'spaceType': 'land', 'bonus': []}, {'x': 8, 'y': 2, 'id': '20', 'spaceType': 'land', 'bonus': [1]}, {'x': 1, 'y': 3, 'id': '21', 'spaceType': 'land', 'bonus': [2, 0]}, {'x': 2, 'y': 3, 'id': '22', 'spaceType': 'land', 'bonus': [2]}, {'x': 3, 'y': 3, 'id': '23', 'spaceType': 'land', 'bonus': [2]}, {'x': 4, 'y': 3, 'id': '24', 'spaceType': 'land', 'bonus': [2], 'tileType': 0, 'color': 'yellow'}, {'x': 5, 'y': 3, 'id': '25', 'spaceType': 'land', 'bonus': [2, 2], 'color': 'green'}, {'x': 6, 'y': 3, 'id': '26', 'spaceType': 'land', 'bonus': [2]}, {'x': 7, 'y': 3, 'id': '27', 'spaceType': 'land', 'bonus': [2]}, {'x': 8, 'y': 3, 'id': '28', 'spaceType': 'ocean', 'bonus': [2, 2], 'tileType': 1}, {'x': 0, 'y': 4, 'id': '29', 'spaceType': 'land', 'bonus': [2, 2]}, {'x': 1, 'y': 4, 'id': '30', 'spaceType': 'land', 'bonus': [2, 2]}, {'x': 2, 'y': 4, 'id': '31', 'spaceType': 'land', 'bonus': [2, 2]}, {'x': 3, 'y': 4, 'id': '32', 'spaceType': 'ocean', 'bonus': [2, 2], 'tileType': 1}, {'x': 4, 'y': 4, 'id': '33', 'spaceType': 'ocean', 'bonus': [2, 2], 'tileType': 1}, {'x': 5, 'y': 4, 'id': '34', 'spaceType': 'ocean', 'bonus': [2, 2], 'tileType': 1}, {'x': 6, 'y': 4, 'id': '35', 'spaceType': 'land', 'bonus': [2, 2]}, {'x': 7, 'y': 4, 'id': '36', 'spaceType': 'land', 'bonus': [2, 2], 'tileType': 2, 'color': 'yellow'}, {'x': 8, 'y': 4, 'id': '37', 'spaceType': 'land', 'bonus': [2, 2], 'tileType': 0, 'color': 'yellow'}, {'x': 1, 'y': 5, 'id': '38', 'spaceType': 'land', 'bonus': [2], 'tileType': 2, 'color': 'red'}, {'x': 2, 'y': 5, 'id': '39', 'spaceType': 'land', 'bonus': [2, 2]}, {'x': 3, 'y': 5, 'id': '40', 'spaceType': 'land', 'bonus': [2]}, {'x': 4, 'y': 5, 'id': '41', 'spaceType': 'land', 'bonus': [2]}, {'x': 5, 'y': 5, 'id': '42', 'spaceType': 'land', 'bonus': [2]}, {'x': 6, 'y': 5, 'id': '43', 'spaceType': 'ocean', 'bonus': [2], 'tileType': 1}, {'x': 7, 'y': 5, 'id': '44', 'spaceType': 'ocean', 'bonus': [2], 'tileType': 1}, {'x': 8, 'y': 5, 'id': '45', 'spaceType': 'ocean', 'bonus': [2]}, {'x': 2, 'y': 6, 'id': '46', 'spaceType': 'land', 'bonus': []}, {'x': 3, 'y': 6, 'id': '47', 'spaceType': 'land', 'bonus': []}, {'x': 4, 'y': 6, 'id': '48', 'spaceType': 'land', 'bonus': []}, {'x': 5, 'y': 6, 'id': '49', 'spaceType': 'land', 'bonus': []}, {'x': 6, 'y': 6, 'id': '50', 'spaceType': 'land', 'bonus': []}, {'x': 7, 'y': 6, 'id': '51', 'spaceType': 'land', 'bonus': [2], 'tileType': 2, 'color': 'green'}, {'x': 8, 'y': 6, 'id': '52', 'spaceType': 'land', 'bonus': []}, {'x': 3, 'y': 7, 'id': '53', 'spaceType': 'land', 'bonus': [1, 1]}, {'x': 4, 'y': 7, 'id': '54', 'spaceType': 'land', 'bonus': []}, {'x': 5, 'y': 7, 'id': '55', 'spaceType': 'land', 'bonus': [3]}, {'x': 6, 'y': 7, 'id': '56', 'spaceType': 'land', 'bonus': [3]}, {'x': 7, 'y': 7, 'id': '57', 'spaceType': 'land', 'bonus': []}, {'x': 8, 'y': 7, 'id': '58', 'spaceType': 'land', 'bonus': [0]}, {'x': 4, 'y': 8, 'id': '59', 'spaceType': 'land', 'bonus': [1], 'tileType': 2, 'color': 'green'}, {'x': 5, 'y': 8, 'id': '60', 'spaceType': 'land', 'bonus': [1, 1]}, {'x': 6, 'y': 8, 'id': '61', 'spaceType': 'land', 'bonus': []}, {'x': 7, 'y': 8, 'id': '62', 'spaceType': 'land', 'bonus': []}, {'x': 8, 'y': 8, 'id': '63', 'spaceType': 'ocean', 'bonus': [0, 0], 'tileType': 1}, {'x': -1, 'y': -1, 'id': '69', 'spaceType': 'colony', 'bonus': []}], 'spectatorId': 'sf87c9af9959a', 'temperature': 8, 'isTerraformed': False, 'undoCount': 0, 'venusScaleLevel': 0, 'step': 253}, 'id': 'p5144fa80f4ec', 'runId': 'r6d46a1351d2a', 'pickedCorporationCard': [{'name': 'Helion', 'calculatedCost': 0}], 'preludeCardsInHand': [], 'thisPlayer': {'actionsTakenThisRound': 4, 'actionsTakenThisGame': 63, 'actionsThisGeneration': ['Water Import From Europa'], 'availableBlueCardActionCount': 0, 'cardCost': 3, 'cardDiscount': 0, 'cardsInHandNbr': 1, 'citiesCount': 3, 'coloniesCount': 0, 'color': 'yellow', 'energy': 2, 'energyProduction': 2, 'fleetSize': 1, 'heat': 0, 'heatProduction': 3, 'influence': 0, 'isActive': True, 'lastCardPlayed': 'Asteroid Mining', 'megaCredits': 0, 'megaCreditProduction': 7, 'name': 'Yellow', 'needsToResearch': True, 'noTagsCount': 0, 'plants': 2, 'plantProduction': 0, 'protectedResources': {'megacredits': 'off', 'steel': 'off', 'titanium': 'off', 'plants': 'off', 'energy': 'off', 'heat': 'off'}, 'protectedProduction': {'megacredits': 'off', 'steel': 'off', 'titanium': 'off', 'plants': 'off', 'energy': 'off', 'heat': 'off'}, 'tableau': [{'resources': 0, 'name': 'Helion', 'calculatedCost': 0}, {'resources': 0, 'name': 'Steelworks', 'calculatedCost': 15}, {'resources': 0, 'name': 'Viral Enhancers', 'calculatedCost': 9}, {'resources': 0, 'name': 'Vesta Shipyard', 'calculatedCost': 15}, {'resources': 0, 'name': 'Mars University', 'calculatedCost': 8}, {'resources': 0, 'name': 'Immigrant City', 'calculatedCost': 13}, {'resources': 0, 'name': 'Water Import From Europa', 'calculatedCost': 25}, {'resources': 0, 'name': 'Asteroid Mining', 'calculatedCost': 30}], 'selfReplicatingRobotsCards': [], 'steel': 2, 'steelProduction': 0, 'steelValue': 2, 'tags': [{'tag': 'building', 'count': 3}, {'tag': 'space', 'count': 4}, {'tag': 'science', 'count': 2}, {'tag': 'jovian', 'count': 3}, {'tag': 'microbe', 'count': 1}, {'tag': 'city', 'count': 1}, {'tag': 'event', 'count': 0}], 'terraformRating': 31, 'timer': {'sumElapsed': 739, 'startedAt': 1737143413945, 'running': True, 'afterFirstAction': True, 'lastStoppedAt': 1737143413945}, 'titanium': 13, 'titaniumProduction': 3, 'titaniumValue': 3, 'tradesThisGeneration': 0, 'victoryPointsBreakdown': {'terraformRating': 31, 'milestones': 10, 'awards': 12, 'greenery': 3, 'city': 6, 'escapeVelocity': 0, 'moonHabitats': 0, 'moonMines': 0, 'moonRoads': 0, 'planetaryTracks': 0, 'victoryPoints': 7, 'total': 69, 'detailsCards': [{'cardName': 'Vesta Shipyard', 'victoryPoint': 1}, {'cardName': 'Mars University', 'victoryPoint': 1}, {'cardName': 'Water Import From Europa', 'victoryPoint': 3}, {'cardName': 'Asteroid Mining', 'victoryPoint': 2}], 'detailsMilestones': [{'message': 'Claimed ${0} milestone', 'victoryPoint': 5, 'messageArgs': ['Mayor']}, {'message': 'Claimed ${0} milestone', 'victoryPoint': 5, 'messageArgs': ['Gardener']}], 'detailsAwards': [{'message': '${0} place for ${1} award (funded by ${2})', 'victoryPoint': 5, 'messageArgs': ['1st', 'Banker', 'Yellow']}, {'message': '${0} place for ${1} award (funded by ${2})', 'victoryPoint': 5, 'messageArgs': ['1st', 'Scientist', 'ki']}, {'message': '${0} place for ${1} award (funded by ${2})', 'victoryPoint': 2, 'messageArgs': ['2nd', 'Miner', 'Green']}], 'detailsPlanetaryTracks': []}, 'victoryPointsByGeneration': [32, 32, 32, 33, 36, 35, 35, 39, 40, 40, 43, 43, 43, 51, 54, 61], 'corruption': 0, 'excavations': 0}, 'waitingFor': {'title': 'Select how to pay for action', 'buttonLabel': 'Pay', 'type': 'payment', 'amount': 12, 'paymentOptions': {'heat': True, 'lunaTradeFederationTitanium': False, 'steel': False, 'titanium': True, 'seeds': False, 'auroraiData': False, 'spireScience': False, 'kuiperAsteroids': False}, 'seeds': 0, 'auroraiData': 0, 'kuiperAsteroids': 0, 'spireScience': 0}, 'players': [{'actionsTakenThisRound': 0, 'actionsTakenThisGame': 61, 'actionsThisGeneration': [], 'availableBlueCardActionCount': 2, 'cardCost': 3, 'cardDiscount': 0, 'cardsInHandNbr': 2, 'citiesCount': 2, 'coloniesCount': 0, 'color': 'red', 'energy': 8, 'energyProduction': 8, 'fleetSize': 1, 'heat': 10, 'heatProduction': 0, 'influence': 0, 'isActive': False, 'megaCredits': 112, 'megaCreditProduction': -1, 'name': 'ki', 'needsToResearch': True, 'noTagsCount': 1, 'plants': 5, 'plantProduction': 3, 'protectedResources': {'megacredits': 'off', 'steel': 'off', 'titanium': 'off', 'plants': 'off', 'energy': 'off', 'heat': 'off'}, 'protectedProduction': {'megacredits': 'off', 'steel': 'off', 'titanium': 'off', 'plants': 'off', 'energy': 'off', 'heat': 'off'}, 'tableau': [{'resources': 0, 'name': 'United Nations Mars Initiative', 'calculatedCost': 0}, {'resources': 0, 'name': 'Flooding', 'calculatedCost': 7}, {'resources': 0, 'name': 'Nuclear Power', 'calculatedCost': 10}, {'resources': 0, 'name': 'Rad-Suits', 'calculatedCost': 6}, {'resources': 0, 'name': 'Ore Processor', 'calculatedCost': 13}, {'resources': 4, 'name': 'Pets', 'calculatedCost': 10}, {'resources': 0, 'name': 'Trees', 'calculatedCost': 13}, {'resources': 0, 'name': 'Power Infrastructure', 'calculatedCost': 4}, {'resources': 0, 'name': 'Robotic Workforce', 'calculatedCost': 9}], 'selfReplicatingRobotsCards': [], 'steel': 0, 'steelProduction': 0, 'steelValue': 2, 'tags': [{'tag': 'building', 'count': 3}, {'tag': 'science', 'count': 1}, {'tag': 'power', 'count': 2}, {'tag': 'earth', 'count': 2}, {'tag': 'plant', 'count': 1}, {'tag': 'animal', 'count': 1}, {'tag': 'event', 'count': 1}], 'terraformRating': 35, 'timer': {'sumElapsed': 1130, 'startedAt': 1737143413923, 'running': False, 'afterFirstAction': True, 'lastStoppedAt': 1737143413945}, 'titanium': 4, 'titaniumProduction': 0, 'titaniumValue': 3, 'tradesThisGeneration': 0, 'victoryPointsBreakdown': {'terraformRating': 35, 'milestones': 5, 'awards': 2, 'greenery': 2, 'city': 2, 'escapeVelocity': 0, 'moonHabitats': 0, 'moonMines': 0, 'moonRoads': 0, 'planetaryTracks': 0, 'victoryPoints': 3, 'total': 49, 'detailsCards': [{'cardName': 'Flooding', 'victoryPoint': -1}, {'cardName': 'Rad-Suits', 'victoryPoint': 1}, {'cardName': 'Pets', 'victoryPoint': 2}, {'cardName': 'Trees', 'victoryPoint': 1}], 'detailsMilestones': [{'message': 'Claimed ${0} milestone', 'victoryPoint': 5, 'messageArgs': ['Terraformer']}], 'detailsAwards': [{'message': '${0} place for ${1} award (funded by ${2})', 'victoryPoint': 2, 'messageArgs': ['2nd', 'Scientist', 'ki']}], 'detailsPlanetaryTracks': []}, 'victoryPointsByGeneration': [33, 31, 32, 30, 30, 33, 34, 31, 31, 32, 32, 35, 36, 35, 37, 44], 'corruption': 0, 'excavations': 0}, {'actionsTakenThisRound': 0, 'actionsTakenThisGame': 59, 'actionsThisGeneration': [], 'availableBlueCardActionCount': 2, 'cardCost': 3, 'cardDiscount': 0, 'cardsInHandNbr': 7, 'citiesCount': 2, 'coloniesCount': 0, 'color': 'green', 'energy': 4, 'energyProduction': 4, 'fleetSize': 1, 'heat': 110, 'heatProduction': 14, 'influence': 0, 'isActive': False, 'megaCredits': 92, 'megaCreditProduction': 1, 'name': 'Green', 'needsToResearch': True, 'noTagsCount': 0, 'plants': 2, 'plantProduction': 0, 'protectedResources': {'megacredits': 'off', 'steel': 'off', 'titanium': 'off', 'plants': 'off', 'energy': 'off', 'heat': 'off'}, 'protectedProduction': {'megacredits': 'off', 'steel': 'off', 'titanium': 'off', 'plants': 'off', 'energy': 'off', 'heat': 'off'}, 'tableau': [{'resources': 0, 'name': 'Mining Guild', 'calculatedCost': 0}, {'resources': 0, 'name': 'Underground Detonations', 'calculatedCost': 6}, {'resources': 0, 'name': 'Business Network', 'calculatedCost': 4}, {'resources': 0, 'name': 'Giant Space Mirror', 'calculatedCost': 17}, {'resources': 0, 'name': 'Land Claim', 'calculatedCost': 1}], 'selfReplicatingRobotsCards': [], 'steel': 25, 'steelProduction': 2, 'steelValue': 2, 'tags': [{'tag': 'building', 'count': 3}, {'tag': 'space', 'count': 1}, {'tag': 'power', 'count': 1}, {'tag': 'earth', 'count': 1}, {'tag': 'event', 'count': 1}], 'terraformRating': 31, 'timer': {'sumElapsed': 1697, 'startedAt': 1737143413929, 'running': False, 'afterFirstAction': True, 'lastStoppedAt': 1737143413945}, 'titanium': 0, 'titaniumProduction': 0, 'titaniumValue': 3, 'tradesThisGeneration': 0, 'victoryPointsBreakdown': {'terraformRating': 31, 'milestones': 0, 'awards': 7, 'greenery': 0, 'city': 0, 'escapeVelocity': 0, 'moonHabitats': 0, 'moonMines': 0, 'moonRoads': 0, 'planetaryTracks': 0, 'victoryPoints': 0, 'total': 38, 'detailsCards': [], 'detailsMilestones': [], 'detailsAwards': [{'message': '${0} place for ${1} award (funded by ${2})', 'victoryPoint': 2, 'messageArgs': ['2nd', 'Banker', 'Yellow']}, {'message': '${0} place for ${1} award (funded by ${2})', 'victoryPoint': 5, 'messageArgs': ['1st', 'Miner', 'Green']}], 'detailsPlanetaryTracks': []}, 'victoryPointsByGeneration': [35, 32, 32, 33, 33, 31, 32, 32, 32, 33, 33, 35, 35, 39, 39, 37], 'corruption': 0, 'excavations': 0}, {'actionsTakenThisRound': 4, 'actionsTakenThisGame': 63, 'actionsThisGeneration': ['Water Import From Europa'], 'availableBlueCardActionCount': 0, 'cardCost': 3, 'cardDiscount': 0, 'cardsInHandNbr': 1, 'citiesCount': 3, 'coloniesCount': 0, 'color': 'yellow', 'energy': 2, 'energyProduction': 2, 'fleetSize': 1, 'heat': 0, 'heatProduction': 3, 'influence': 0, 'isActive': True, 'lastCardPlayed': 'Asteroid Mining', 'megaCredits': 0, 'megaCreditProduction': 7, 'name': 'Yellow', 'needsToResearch': True, 'noTagsCount': 0, 'plants': 2, 'plantProduction': 0, 'protectedResources': {'megacredits': 'off', 'steel': 'off', 'titanium': 'off', 'plants': 'off', 'energy': 'off', 'heat': 'off'}, 'protectedProduction': {'megacredits': 'off', 'steel': 'off', 'titanium': 'off', 'plants': 'off', 'energy': 'off', 'heat': 'off'}, 'tableau': [{'resources': 0, 'name': 'Helion', 'calculatedCost': 0}, {'resources': 0, 'name': 'Steelworks', 'calculatedCost': 15}, {'resources': 0, 'name': 'Viral Enhancers', 'calculatedCost': 9}, {'resources': 0, 'name': 'Vesta Shipyard', 'calculatedCost': 15}, {'resources': 0, 'name': 'Mars University', 'calculatedCost': 8}, {'resources': 0, 'name': 'Immigrant City', 'calculatedCost': 13}, {'resources': 0, 'name': 'Water Import From Europa', 'calculatedCost': 25}, {'resources': 0, 'name': 'Asteroid Mining', 'calculatedCost': 30}], 'selfReplicatingRobotsCards': [], 'steel': 2, 'steelProduction': 0, 'steelValue': 2, 'tags': [{'tag': 'building', 'count': 3}, {'tag': 'space', 'count': 4}, {'tag': 'science', 'count': 2}, {'tag': 'jovian', 'count': 3}, {'tag': 'microbe', 'count': 1}, {'tag': 'city', 'count': 1}, {'tag': 'event', 'count': 0}], 'terraformRating': 31, 'timer': {'sumElapsed': 739, 'startedAt': 1737143413945, 'running': True, 'afterFirstAction': True, 'lastStoppedAt': 1737143413945}, 'titanium': 13, 'titaniumProduction': 3, 'titaniumValue': 3, 'tradesThisGeneration': 0, 'victoryPointsBreakdown': {'terraformRating': 31, 'milestones': 10, 'awards': 12, 'greenery': 3, 'city': 6, 'escapeVelocity': 0, 'moonHabitats': 0, 'moonMines': 0, 'moonRoads': 0, 'planetaryTracks': 0, 'victoryPoints': 7, 'total': 69, 'detailsCards': [{'cardName': 'Vesta Shipyard', 'victoryPoint': 1}, {'cardName': 'Mars University', 'victoryPoint': 1}, {'cardName': 'Water Import From Europa', 'victoryPoint': 3}, {'cardName': 'Asteroid Mining', 'victoryPoint': 2}], 'detailsMilestones': [{'message': 'Claimed ${0} milestone', 'victoryPoint': 5, 'messageArgs': ['Mayor']}, {'message': 'Claimed ${0} milestone', 'victoryPoint': 5, 'messageArgs': ['Gardener']}], 'detailsAwards': [{'message': '${0} place for ${1} award (funded by ${2})', 'victoryPoint': 5, 'messageArgs': ['1st', 'Banker', 'Yellow']}, {'message': '${0} place for ${1} award (funded by ${2})', 'victoryPoint': 5, 'messageArgs': ['1st', 'Scientist', 'ki']}, {'message': '${0} place for ${1} award (funded by ${2})', 'victoryPoint': 2, 'messageArgs': ['2nd', 'Miner', 'Green']}], 'detailsPlanetaryTracks': []}, 'victoryPointsByGeneration': [32, 32, 32, 33, 36, 35, 35, 39, 40, 40, 43, 43, 43, 51, 54, 61], 'corruption': 0, 'excavations': 0}], 'autopass': False}, indent=2))