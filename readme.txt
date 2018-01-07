; Es können und es ist wahrscheinlich dass Fehler vorhanden sind im Code. Auf Ergebnisse und alles dazugehörige keine Gewähr.
; --- use at own risk

; starten mit ins Verzeichnis navigieren und dann
; ..\PortfolioOptimization>python main.py
; ausführen. legt eine Datei im Verzeichnis an "efficientFrontier.xls".

; es müssen Pakete nachinstalliert werden:
; mit pip install "packet". Also pip install pandas, pip install scipy, pip install matplotlib (vllt auch pip install numpy)

; Da sind die Gewichte angegeben die die Portfoliooptimierung ermittelt hat als Funktion vom Return. Bei höheren Returns wird das sinnlos da dann nur noch das übrig ist was im Zeitraum den höchsten Return
; erzielt hat. Ergibt sich einfach daraus, dass dann nichts anderes beigemischt werden kann um auf diesen Return zu kommen. Wenn man das plottet in Excel bekommt man typische Effizienzlinien (volatilität auf die x-achse und 
; return auf die y-achse (diese sind btw. auf 1 jahr bezogen.)) (siehe z.B. https://en.wikipedia.org/wiki/Efficient_frontier).
; Grundsätzliche Annahme:
; 	-Unabhängige Schwankungen der Kurse (wichtig, die Kurse sollten in Euro lauten! Da ist nicht eingebaut dass man noch die Umrechnung von Dollar in Euro macht, das müsste anders modelliert werden dann!)
; 	-Durch die Verwendung von Euro-Kursen ist der Wechselkurs und dessen Schwankung schon inklusive.
;	-Geometrische Brownsche Bewegung (= keine negativen Kurse, die beobachtete Volatilität wird um Niveaueffekte korrigiert. Idee ist, dass ein Kurs bei 1000€ "stärker" schwankt als einer bei 1€. Um das trotzdem zu vergleichen,
; 		nimmt man den Effekt mit. Siehe auch: http://www.math.ucsd.edu/~msharpe/stockgrowth.pdf oder https://en.wikipedia.org/wiki/Geometric_Brownian_motion )
;	-Die Optimierung nutzt die klassische Portfoliotheorie (siehe https://en.wikipedia.org/wiki/Modern_portfolio_theory ). Im Grunde bestimmt man die Covariance-Matrix (nicht zu verwechseln mit der Korrelationsmatrix).
		Die Korrelationsmatrix wird auch ausgegeben, aber ist im Grunde in der Covariance-Matrix enthalten. Ist aber ganz interessant, da man direkt sieht wie die Korrelationskoeffizienten sind um ein Gefühl dafür zu bekommen.

; Das ganze taugt nur zu einer groben Abschätzung dessen was möglicherweise sinnvolle Gewichte sind.

; hinzufügen von weiteren ETFs kann man in der main.py machen. Die einfach im Editor öffnen. Glaube die Logik ist offensichtlich. Den neuen ETF laden, addsecurity und fertig.
; Daten bekommt man von yahoo. https://de.finance.yahoo.com/quote/DBXE.F/history?period1=1350252000&period2=1508018400&interval=1d&filter=history&frequency=1d

; teilweise ist es komisch die Sachen zu finden. Man sollte darauf achten, einen deutschen Handelsplatz zu wählen. .F ist frankfurt, .DE ist Xetra etc. Das Einlesen
; der Sachen ist umständlich, da man das als CSV im englischen Format nur kriegt, und direkt im Editor alle , durch ; und . durch , ersetzen muss (in dieser Reihenfolge) um das mal in Excel zu sehen..
; Das Ding dann als xls abspeichern. Hier auch mal schauen wie oft da "null" drin steht im Zeitraum. Wenn das sehr oft vorkommt dann einen anderen Handelsplatz wählen!
