import json

print(json.dumps({'cardsInHand': [{'name': 'Security Fleet', 'calculatedCost': 12}], 'ceoCardsInHand': [], 'dealtCorporationCards': [{'name': 'United Nations Mars Initiative', 'calculatedCost': 0}, {'name': 'EcoLine', 'calculatedCost': 0}], 'dealtPreludeCards': [], 'dealtCeoCards': [], 'dealtProjectCards': [{'name': 'Water Splitting Plant', 'calculatedCost': 12}, {'name': 'Heat Trappers', 'calculatedCost': 6}, {'name': 'Martian Rails', 'calculatedCost': 13}, {'name': 'Rover Construction', 'calculatedCost': 8}, {'name': 'Magnetic Field Generators', 'calculatedCost': 20}, {'name': 'Food Factory', 'calculatedCost': 12}, {'name': 'Investment Loan', 'calculatedCost': 3}, {'name': 'Asteroid Mining Consortium', 'calculatedCost': 13}, {'name': 'Dust Seals', 'calculatedCost': 2}, {'name': 'Power Grid', 'calculatedCost': 18}], 'draftedCards': [], 'game': {'awards': [{'playerName': 'ki', 'playerColor': 'red', 'name': 'Landlord', 'scores': [{'playerColor': 'yellow', 'playerScore': 1}, {'playerColor': 'red', 'playerScore': 3}, {'playerColor': 'green', 'playerScore': 1}]}, {'playerName': 'Yellow', 'playerColor': 'yellow', 'name': 'Scientist', 'scores': [{'playerColor': 'yellow', 'playerScore': 1}, {'playerColor': 'red', 'playerScore': 2}, {'playerColor': 'green', 'playerScore': 0}]}, {'playerName': '', 'playerColor': '', 'name': 'Banker', 'scores': []}, {'playerName': '', 'playerColor': '', 'name': 'Thermalist', 'scores': []}, {'playerName': 'Yellow', 'playerColor': 'yellow', 'name': 'Miner', 'scores': [{'playerColor': 'yellow', 'playerScore': 0}, {'playerColor': 'red', 'playerScore': 3}, {'playerColor': 'green', 'playerScore': 0}]}], 'colonies': [], 'deckSize': 103, 'discardedColonies': [], 'expectedPurgeTimeMs': 1737999406476, 'gameAge': 124, 'gameOptions': {'altVenusBoard': False, 'aresExtension': False, 'boardName': 'tharsis', 'bannedCards': [], 'includedCards': [], 'ceoExtension': False, 'coloniesExtension': False, 'communityCardsOption': False, 'corporateEra': True, 'draftVariant': True, 'escapeVelocityMode': False, 'escapeVelocityBonusSeconds': 2, 'fastModeOption': False, 'includeFanMA': False, 'includeVenusMA': True, 'initialDraftVariant': False, 'moonExpansion': False, 'pathfindersExpansion': False, 'preludeDraftVariant': True, 'preludeExtension': False, 'prelude2Expansion': False, 'promoCardsOption': False, 'politicalAgendasExtension': 'Standard', 'removeNegativeGlobalEvents': False, 'showOtherPlayersVP': False, 'showTimers': True, 'shuffleMapOption': False, 'solarPhaseOption': False, 'soloTR': False, 'randomMA': 'No randomization', 'requiresMoonTrackCompletion': False, 'requiresVenusTrackCompletion': False, 'turmoilExtension': False, 'twoCorpsVariant': False, 'venusNextExtension': False, 'undoOption': False, 'underworldExpansion': False}, 'generation': 7, 'globalsPerGeneration': [], 'isSoloModeWin': False, 'lastSoloGeneration': 14, 'milestones': [{'playerName': '', 'playerColor': '', 'name': 'Terraformer', 'scores': [{'playerColor': 'yellow', 'playerScore': 22}, {'playerColor': 'red', 'playerScore': 24}, {'playerColor': 'green', 'playerScore': 23}]}, {'playerName': '', 'playerColor': '', 'name': 'Mayor', 'scores': [{'playerColor': 'yellow', 'playerScore': 1}, {'playerColor': 'red', 'playerScore': 2}, {'playerColor': 'green', 'playerScore': 0}]}, {'playerName': '', 'playerColor': '', 'name': 'Gardener', 'scores': [{'playerColor': 'yellow', 'playerScore': 0}, {'playerColor': 'red', 'playerScore': 1}, {'playerColor': 'green', 'playerScore': 1}]}, {'playerName': '', 'playerColor': '', 'name': 'Builder', 'scores': [{'playerColor': 'yellow', 'playerScore': 0}, {'playerColor': 'red', 'playerScore': 0}, {'playerColor': 'green', 'playerScore': 0}]}, {'playerName': '', 'playerColor': '', 'name': 'Planner', 'scores': [{'playerColor': 'yellow', 'playerScore': 13}, {'playerColor': 'red', 'playerScore': 1}, {'playerColor': 'green', 'playerScore': 1}]}], 'oceans': 1, 'oxygenLevel': 2, 'passedPlayers': ['yellow'], 'phase': 'action', 'spaces': [{'x': -1, 'y': -1, 'id': '01', 'spaceType': 'colony', 'bonus': []}, {'x': -1, 'y': -1, 'id': '02', 'spaceType': 'colony', 'bonus': []}, {'x': 4, 'y': 0, 'id': '03', 'spaceType': 'land', 'bonus': [1, 1]}, {'x': 5, 'y': 0, 'id': '04', 'spaceType': 'ocean', 'bonus': [1, 1]}, {'x': 6, 'y': 0, 'id': '05', 'spaceType': 'land', 'bonus': [], 'tileType': 2, 'color': 'red'}, {'x': 7, 'y': 0, 'id': '06', 'spaceType': 'ocean', 'bonus': [3]}, {'x': 8, 'y': 0, 'id': '07', 'spaceType': 'ocean', 'bonus': []}, {'x': 3, 'y': 1, 'id': '08', 'spaceType': 'land', 'bonus': []}, {'x': 4, 'y': 1, 'id': '09', 'spaceType': 'land', 'bonus': [1]}, {'x': 5, 'y': 1, 'id': '10', 'spaceType': 'land', 'bonus': [], 'tileType': 0, 'color': 'red'}, {'x': 6, 'y': 1, 'id': '11', 'spaceType': 'land', 'bonus': []}, {'x': 7, 'y': 1, 'id': '12', 'spaceType': 'land', 'bonus': [], 'tileType': 0, 'color': 'green'}, {'x': 8, 'y': 1, 'id': '13', 'spaceType': 'ocean', 'bonus': [3, 3]}, {'x': 2, 'y': 2, 'id': '14', 'spaceType': 'land', 'bonus': [3]}, {'x': 3, 'y': 2, 'id': '15', 'spaceType': 'land', 'bonus': []}, {'x': 4, 'y': 2, 'id': '16', 'spaceType': 'land', 'bonus': []}, {'x': 5, 'y': 2, 'id': '17', 'spaceType': 'land', 'bonus': []}, {'x': 6, 'y': 2, 'id': '18', 'spaceType': 'land', 'bonus': [], 'tileType': 2, 'color': 'yellow'}, {'x': 7, 'y': 2, 'id': '19', 'spaceType': 'land', 'bonus': []}, {'x': 8, 'y': 2, 'id': '20', 'spaceType': 'land', 'bonus': [1]}, {'x': 1, 'y': 3, 'id': '21', 'spaceType': 'land', 'bonus': [2, 0]}, {'x': 2, 'y': 3, 'id': '22', 'spaceType': 'land', 'bonus': [2]}, {'x': 3, 'y': 3, 'id': '23', 'spaceType': 'land', 'bonus': [2]}, {'x': 4, 'y': 3, 'id': '24', 'spaceType': 'land', 'bonus': [2]}, {'x': 5, 'y': 3, 'id': '25', 'spaceType': 'land', 'bonus': [2, 2]}, {'x': 6, 'y': 3, 'id': '26', 'spaceType': 'land', 'bonus': [2]}, {'x': 7, 'y': 3, 'id': '27', 'spaceType': 'land', 'bonus': [2]}, {'x': 8, 'y': 3, 'id': '28', 'spaceType': 'ocean', 'bonus': [2, 2]}, {'x': 0, 'y': 4, 'id': '29', 'spaceType': 'land', 'bonus': [2, 2]}, {'x': 1, 'y': 4, 'id': '30', 'spaceType': 'land', 'bonus': [2, 2]}, {'x': 2, 'y': 4, 'id': '31', 'spaceType': 'land', 'bonus': [2, 2]}, {'x': 3, 'y': 4, 'id': '32', 'spaceType': 'ocean', 'bonus': [2, 2]}, {'x': 4, 'y': 4, 'id': '33', 'spaceType': 'ocean', 'bonus': [2, 2]}, {'x': 5, 'y': 4, 'id': '34', 'spaceType': 'ocean', 'bonus': [2, 2]}, {'x': 6, 'y': 4, 'id': '35', 'spaceType': 'land', 'bonus': [2, 2]}, {'x': 7, 'y': 4, 'id': '36', 'spaceType': 'land', 'bonus': [2, 2]}, {'x': 8, 'y': 4, 'id': '37', 'spaceType': 'land', 'bonus': [2, 2]}, {'x': 1, 'y': 5, 'id': '38', 'spaceType': 'land', 'bonus': [2]}, {'x': 2, 'y': 5, 'id': '39', 'spaceType': 'land', 'bonus': [2, 2]}, {'x': 3, 'y': 5, 'id': '40', 'spaceType': 'land', 'bonus': [2]}, {'x': 4, 'y': 5, 'id': '41', 'spaceType': 'land', 'bonus': [2]}, {'x': 5, 'y': 5, 'id': '42', 'spaceType': 'land', 'bonus': [2]}, {'x': 6, 'y': 5, 'id': '43', 'spaceType': 'ocean', 'bonus': [2]}, {'x': 7, 'y': 5, 'id': '44', 'spaceType': 'ocean', 'bonus': [2]}, {'x': 8, 'y': 5, 'id': '45', 'spaceType': 'ocean', 'bonus': [2], 'tileType': 1}, {'x': 2, 'y': 6, 'id': '46', 'spaceType': 'land', 'bonus': []}, {'x': 3, 'y': 6, 'id': '47', 'spaceType': 'land', 'bonus': []}, {'x': 4, 'y': 6, 'id': '48', 'spaceType': 'land', 'bonus': []}, {'x': 5, 'y': 6, 'id': '49', 'spaceType': 'land', 'bonus': []}, {'x': 6, 'y': 6, 'id': '50', 'spaceType': 'land', 'bonus': []}, {'x': 7, 'y': 6, 'id': '51', 'spaceType': 'land', 'bonus': [2]}, {'x': 8, 'y': 6, 'id': '52', 'spaceType': 'land', 'bonus': []}, {'x': 3, 'y': 7, 'id': '53', 'spaceType': 'land', 'bonus': [1, 1]}, {'x': 4, 'y': 7, 'id': '54', 'spaceType': 'land', 'bonus': []}, {'x': 5, 'y': 7, 'id': '55', 'spaceType': 'land', 'bonus': [3]}, {'x': 6, 'y': 7, 'id': '56', 'spaceType': 'land', 'bonus': [3]}, {'x': 7, 'y': 7, 'id': '57', 'spaceType': 'land', 'bonus': []}, {'x': 8, 'y': 7, 'id': '58', 'spaceType': 'land', 'bonus': [0], 'tileType': 2, 'color': 'red'}, {'x': 4, 'y': 8, 'id': '59', 'spaceType': 'land', 'bonus': [1]}, {'x': 5, 'y': 8, 'id': '60', 'spaceType': 'land', 'bonus': [1, 1]}, {'x': 6, 'y': 8, 'id': '61', 'spaceType': 'land', 'bonus': []}, {'x': 7, 'y': 8, 'id': '62', 'spaceType': 'land', 'bonus': []}, {'x': 8, 'y': 8, 'id': '63', 'spaceType': 'ocean', 'bonus': [0, 0]}, {'x': -1, 'y': -1, 'id': '69', 'spaceType': 'colony', 'bonus': []}], 'spectatorId': 's1d33f4a76497', 'temperature': -22, 'isTerraformed': False, 'undoCount': 0, 'venusScaleLevel': 0, 'step': 89}, 'id': 'pf77bab17562', 'runId': 'r6d46a1351d2a', 'pickedCorporationCard': [{'name': 'United Nations Mars Initiative', 'calculatedCost': 0}], 'preludeCardsInHand': [], 'thisPlayer': {'actionsTakenThisRound': 1, 'actionsTakenThisGame': 19, 'actionsThisGeneration': [], 'availableBlueCardActionCount': 0, 'cardCost': 3, 'cardDiscount': 0, 'cardsInHandNbr': 1, 'citiesCount': 2, 'coloniesCount': 0, 'color': 'red', 'energy': 2, 'energyProduction': 2, 'fleetSize': 1, 'heat': 4, 'heatProduction': 0, 'influence': 0, 'isActive': True, 'lastCardPlayed': 'Viral Enhancers', 'megaCredits': 8, 'megaCreditProduction': 2, 'name': 'ki', 'needsToResearch': True, 'noTagsCount': 0, 'plants': 1, 'plantProduction': 0, 'protectedResources': {'megacredits': 'off', 'steel': 'off', 'titanium': 'off', 'plants': 'off', 'energy': 'off', 'heat': 'off'}, 'protectedProduction': {'megacredits': 'off', 'steel': 'off', 'titanium': 'off', 'plants': 'off', 'energy': 'off', 'heat': 'off'}, 'tableau': [{'resources': 0, 'name': 'United Nations Mars Initiative', 'calculatedCost': 0}, {'resources': 0, 'name': 'Solar Wind Power', 'calculatedCost': 11}, {'resources': 0, 'name': 'Viral Enhancers', 'calculatedCost': 9}], 'selfReplicatingRobotsCards': [], 'steel': 0, 'steelProduction': 0, 'steelValue': 2, 'tags': [{'tag': 'space', 'count': 1}, {'tag': 'science', 'count': 2}, {'tag': 'power', 'count': 1}, {'tag': 'earth', 'count': 1}, {'tag': 'microbe', 'count': 1}, {'tag': 'event', 'count': 0}], 'terraformRating': 24, 'timer': {'sumElapsed': 509, 'startedAt': 1737135407416, 'running': True, 'afterFirstAction': True, 'lastStoppedAt': 1737135407416}, 'titanium': 3, 'titaniumProduction': 0, 'titaniumValue': 3, 'tradesThisGeneration': 0, 'victoryPointsBreakdown': {'terraformRating': 24, 'milestones': 0, 'awards': 15, 'greenery': 1, 'city': 1, 'escapeVelocity': 0, 'moonHabitats': 0, 'moonMines': 0, 'moonRoads': 0, 'planetaryTracks': 0, 'victoryPoints': 0, 'total': 41, 'detailsCards': [], 'detailsMilestones': [], 'detailsAwards': [{'message': '${0} place for ${1} award (funded by ${2})', 'victoryPoint': 5, 'messageArgs': ['1st', 'Scientist', 'Yellow']}, {'message': '${0} place for ${1} award (funded by ${2})', 'victoryPoint': 5, 'messageArgs': ['1st', 'Miner', 'Yellow']}, {'message': '${0} place for ${1} award (funded by ${2})', 'victoryPoint': 5, 'messageArgs': ['1st', 'Landlord', 'ki']}], 'detailsPlanetaryTracks': []}, 'victoryPointsByGeneration': [22, 22, 30, 30, 37, 41], 'corruption': 0, 'excavations': 0}, 'waitingFor': {'title': 'Take your next action', 'buttonLabel': 'Take action', 'type': 'or', 'options': [{'title': 'Play project card', 'buttonLabel': 'Play card', 'type': 'projectCard', 'cards': [{'name': 'Security Fleet', 'calculatedCost': 12, 'reserveUnits': {'megacredits': 0, 'steel': 0, 'titanium': 0, 'plants': 0, 'energy': 0, 'heat': 0}}], 'microbes': 0, 'floaters': 0, 'paymentOptions': {'heat': False, 'lunaTradeFederationTitanium': False, 'plants': False, 'corruption': False}, 'lunaArchivesScience': 0, 'seeds': 0, 'graphene': 0, 'kuiperAsteroids': 0, 'corruption': 0}, {'title': 'End Turn', 'buttonLabel': 'End', 'type': 'option'}, {'title': 'Standard projects', 'buttonLabel': 'Confirm', 'type': 'card', 'cards': [{'resources': 0, 'name': 'Power Plant:SP', 'calculatedCost': 11, 'isDisabled': True}, {'resources': 0, 'name': 'Asteroid:SP', 'calculatedCost': 14, 'isDisabled': True}, {'resources': 0, 'name': 'Aquifer', 'calculatedCost': 18, 'isDisabled': True}, {'resources': 0, 'name': 'Greenery', 'calculatedCost': 23, 'isDisabled': True}, {'resources': 0, 'name': 'City', 'calculatedCost': 25, 'isDisabled': True}], 'max': 1, 'min': 1, 'showOnlyInLearnerMode': True, 'selectBlueCardAction': False, 'showOwner': False}, {'title': 'Pass for this generation', 'buttonLabel': 'Pass', 'type': 'option'}, {'title': 'Sell patents', 'buttonLabel': 'Sell', 'type': 'card', 'cards': [{'name': 'Security Fleet', 'calculatedCost': 12}], 'max': 1, 'min': 1, 'showOnlyInLearnerMode': False, 'selectBlueCardAction': False, 'showOwner': False}], 'initialIdx': 0}, 'players': [{'actionsTakenThisRound': 0, 'actionsTakenThisGame': 17, 'actionsThisGeneration': [], 'availableBlueCardActionCount': 0, 'cardCost': 3, 'cardDiscount': 0, 'cardsInHandNbr': 13, 'citiesCount': 1, 'coloniesCount': 0, 'color': 'yellow', 'energy': 0, 'energyProduction': 0, 'fleetSize': 1, 'heat': 0, 'heatProduction': 0, 'influence': 0, 'isActive': False, 'megaCredits': 56, 'megaCreditProduction': 1, 'name': 'Yellow', 'needsToResearch': True, 'noTagsCount': 0, 'plants': 1, 'plantProduction': 0, 'protectedResources': {'megacredits': 'off', 'steel': 'off', 'titanium': 'off', 'plants': 'off', 'energy': 'off', 'heat': 'off'}, 'protectedProduction': {'megacredits': 'off', 'steel': 'off', 'titanium': 'off', 'plants': 'off', 'energy': 'off', 'heat': 'off'}, 'tableau': [{'resources': 0, 'name': 'Inventrix', 'calculatedCost': 0}], 'selfReplicatingRobotsCards': [], 'steel': 0, 'steelProduction': 0, 'steelValue': 2, 'tags': [{'tag': 'science', 'count': 1}, {'tag': 'event', 'count': 0}], 'terraformRating': 22, 'timer': {'sumElapsed': 303, 'startedAt': 1737135407363, 'running': False, 'afterFirstAction': True, 'lastStoppedAt': 1737135407416}, 'titanium': 0, 'titaniumProduction': 0, 'titaniumValue': 3, 'tradesThisGeneration': 0, 'victoryPointsBreakdown': {'terraformRating': 22, 'milestones': 0, 'awards': 6, 'greenery': 0, 'city': 1, 'escapeVelocity': 0, 'moonHabitats': 0, 'moonMines': 0, 'moonRoads': 0, 'planetaryTracks': 0, 'victoryPoints': 0, 'total': 29, 'detailsCards': [], 'detailsMilestones': [], 'detailsAwards': [{'message': '${0} place for ${1} award (funded by ${2})', 'victoryPoint': 2, 'messageArgs': ['2nd', 'Scientist', 'Yellow']}, {'message': '${0} place for ${1} award (funded by ${2})', 'victoryPoint': 2, 'messageArgs': ['2nd', 'Miner', 'Yellow']}, {'message': '${0} place for ${1} award (funded by ${2})', 'victoryPoint': 2, 'messageArgs': ['2nd', 'Landlord', 'ki']}], 'detailsPlanetaryTracks': []}, 'victoryPointsByGeneration': [25, 27, 29, 30, 32, 32], 'corruption': 0, 'excavations': 0}, {'actionsTakenThisRound': 1, 'actionsTakenThisGame': 19, 'actionsThisGeneration': [], 'availableBlueCardActionCount': 0, 'cardCost': 3, 'cardDiscount': 0, 'cardsInHandNbr': 1, 'citiesCount': 2, 'coloniesCount': 0, 'color': 'red', 'energy': 2, 'energyProduction': 2, 'fleetSize': 1, 'heat': 4, 'heatProduction': 0, 'influence': 0, 'isActive': True, 'lastCardPlayed': 'Viral Enhancers', 'megaCredits': 8, 'megaCreditProduction': 2, 'name': 'ki', 'needsToResearch': True, 'noTagsCount': 0, 'plants': 1, 'plantProduction': 0, 'protectedResources': {'megacredits': 'off', 'steel': 'off', 'titanium': 'off', 'plants': 'off', 'energy': 'off', 'heat': 'off'}, 'protectedProduction': {'megacredits': 'off', 'steel': 'off', 'titanium': 'off', 'plants': 'off', 'energy': 'off', 'heat': 'off'}, 'tableau': [{'resources': 0, 'name': 'United Nations Mars Initiative', 'calculatedCost': 0}, {'resources': 0, 'name': 'Solar Wind Power', 'calculatedCost': 11}, {'resources': 0, 'name': 'Viral Enhancers', 'calculatedCost': 9}], 'selfReplicatingRobotsCards': [], 'steel': 0, 'steelProduction': 0, 'steelValue': 2, 'tags': [{'tag': 'space', 'count': 1}, {'tag': 'science', 'count': 2}, {'tag': 'power', 'count': 1}, {'tag': 'earth', 'count': 1}, {'tag': 'microbe', 'count': 1}, {'tag': 'event', 'count': 0}], 'terraformRating': 24, 'timer': {'sumElapsed': 509, 'startedAt': 1737135407416, 'running': True, 'afterFirstAction': True, 'lastStoppedAt': 1737135407416}, 'titanium': 3, 'titaniumProduction': 0, 'titaniumValue': 3, 'tradesThisGeneration': 0, 'victoryPointsBreakdown': {'terraformRating': 24, 'milestones': 0, 'awards': 15, 'greenery': 1, 'city': 1, 'escapeVelocity': 0, 'moonHabitats': 0, 'moonMines': 0, 'moonRoads': 0, 'planetaryTracks': 0, 'victoryPoints': 0, 'total': 41, 'detailsCards': [], 'detailsMilestones': [], 'detailsAwards': [{'message': '${0} place for ${1} award (funded by ${2})', 'victoryPoint': 5, 'messageArgs': ['1st', 'Scientist', 'Yellow']}, {'message': '${0} place for ${1} award (funded by ${2})', 'victoryPoint': 5, 'messageArgs': ['1st', 'Miner', 'Yellow']}, {'message': '${0} place for ${1} award (funded by ${2})', 'victoryPoint': 5, 'messageArgs': ['1st', 'Landlord', 'ki']}], 'detailsPlanetaryTracks': []}, 'victoryPointsByGeneration': [22, 22, 30, 30, 37, 41], 'corruption': 0, 'excavations': 0}, {'actionsTakenThisRound': 0, 'actionsTakenThisGame': 14, 'actionsThisGeneration': [], 'availableBlueCardActionCount': 0, 'cardCost': 3, 'cardDiscount': 0, 'cardsInHandNbr': 1, 'citiesCount': 0, 'coloniesCount': 0, 'color': 'green', 'energy': 0, 'energyProduction': 1, 'fleetSize': 1, 'heat': 5, 'heatProduction': 1, 'influence': 0, 'isActive': False, 'megaCredits': 109, 'megaCreditProduction': 0, 'name': 'Green', 'needsToResearch': True, 'noTagsCount': 1, 'plants': 0, 'plantProduction': 0, 'protectedResources': {'megacredits': 'off', 'steel': 'off', 'titanium': 'off', 'plants': 'off', 'energy': 'off', 'heat': 'off'}, 'protectedProduction': {'megacredits': 'off', 'steel': 'off', 'titanium': 'off', 'plants': 'off', 'energy': 'off', 'heat': 'off'}, 'tableau': [{'resources': 0, 'name': 'CrediCor', 'calculatedCost': 0}], 'selfReplicatingRobotsCards': [], 'steel': 0, 'steelProduction': 0, 'steelValue': 2, 'tags': [{'tag': 'event', 'count': 0}], 'terraformRating': 23, 'timer': {'sumElapsed': 715, 'startedAt': 1737135407393, 'running': False, 'afterFirstAction': True, 'lastStoppedAt': 1737135407416}, 'titanium': 0, 'titaniumProduction': 0, 'titaniumValue': 3, 'tradesThisGeneration': 0, 'victoryPointsBreakdown': {'terraformRating': 23, 'milestones': 0, 'awards': 4, 'greenery': 1, 'city': 0, 'escapeVelocity': 0, 'moonHabitats': 0, 'moonMines': 0, 'moonRoads': 0, 'planetaryTracks': 0, 'victoryPoints': 0, 'total': 28, 'detailsCards': [], 'detailsMilestones': [], 'detailsAwards': [{'message': '${0} place for ${1} award (funded by ${2})', 'victoryPoint': 2, 'messageArgs': ['2nd', 'Miner', 'Yellow']}, {'message': '${0} place for ${1} award (funded by ${2})', 'victoryPoint': 2, 'messageArgs': ['2nd', 'Landlord', 'ki']}], 'detailsPlanetaryTracks': []}, 'victoryPointsByGeneration': [22, 26, 26, 26, 28, 28], 'corruption': 0, 'excavations': 0}], 'autopass': False}, indent=2))