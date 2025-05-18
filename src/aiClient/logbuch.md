# Logbuch

## Phase 1
Zuerst habe ich ein Programm geschrieben, dass ein Spiel für drei Spieler automatisch erstellt und dann mit
zufälligen Zügen von Anfang bis Ende spielt. Um herauszufinden, wie der Server mit den Clients kommuniziert,
habe ich in erster Linie mit der Netzwerkanalyse der Browser Dev-Tools die Requests der Clients und die
Antworten der Server untersucht. Zusätzlich habe ich den Quellcode des Servers hinzugezogen. Mit den so gewonnenen
Informationen konnte ich einen Python-Client entwickeln, der drei Spieler simuliert und den Server steuert.
Dazu gehörte alle möglichen Szenarien herauszufinden und abzudecken, sodass der Client in jeder Spielsituation
"antwortfähig" ist.

## Phase 2
Als nächstes habe ich ein Custom Gymnasium Environment entwickelt, das im nächsten Schritt für das Training
eines neuronalen Netzes mit Reinforcement Learning zum Einsatz kommen sollte. Der Code des zuvor entwickelten
Clients konnte für die step-Funktion des Environments in weiten Teilen recycled werden. Zusätzlich habe ich
einen Beobachtungs- und Aktionsraum definiert. Diese wurden jeweils als Dict-Space angelegt, da sie sowohl
diskrete (Discrete, MultiBinary) als auch kontinuierliche (Box) Teile enthalten.

## Phase 3
In der letzten Phase wollte ich das zuvor entwickelte Custom Environment nutzen, um ein neuronales Netz zu trainieren.
Dabei sind verschiedene Probleme aufgetreten.

Z.B. ist das Framework Stable Baselines 3, das ich für das
Reinforcement Learning nutzen wollte, nicht auf heterogene Aktionsräume ausgelegt. Um dieses Problem zu umgehen,
habe ich mit der Hilfe von ChatGPT einen ActionWrapper und einen FeatureExtractor implementiert. Leider blieb
es erfolglos, diese korrekt in das Projekt zu integrieren.

Außerdem musste sichergestellt werden, dass keine invaliden Spielzüge an den Server gesendet werden. Dafür habe ich
eine Custom ActorCriticPolicy implementiert, in der eine Zuordnung zwischen Elementen aus dem Beobachtungsraum und dem
Aktionsraum erstellt wurde, mit der dynamisch eine Maskierung der Aktionen vorgenommen werden konnte. So wurde
sichergestellt, dass verbotene Aktionen unmöglich gewählt werden können.

## Fazit
Letztendlich ist die Entwicklung des Projekts leider nicht so weit fortgeschritten, wie ursprünglich geplant und es
wurde kein neuronales Netz tatsächlich trainiert. Stattdessen wurde nur auf Basis des Custom Environments ein
Gerüst implementiert, mit dem ein Spieler durch zufällige Züge simuliert werden kann. Da das Custom Enviroment
alle relevanten Parameter des Spiels berücksichtigt, kann dies in einer zukünftigen Arbeit dazu genutzt werden,
um ein neuronales Netz mit Reinforcement Learning zu trainieren.