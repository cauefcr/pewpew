class Score:
    def setScore(self, name, score, filen):
        """Defines a new score based on input and appends it on filen so
that it may replace any of the highscores"""
        with open(filen, "a") as file:
            file.write(name + "-" + str(score)+"\n")
        scores = Score().getScore(filen)
        cont = 0
        with open(filen, "w") as file:
            for i in scores:
                for j in i:
                    file.write(i[j] + "-" + str(j) +"\n")
                cont += 1
                if cont > 4:
                    break

    def getScore(self, filen):
        """Reads the score from the filen file located inside
the game's directory, sorts it along with the new score and replaces accordingly"""
        #values = []
        names = []
        score1 = ""
        with open(filen) as file:
            for line in file:
                (name, score) = line.split('-', 1)
                for i in score:
                    if i == '\n':
                        break
                    score1 += i
                #values.append(score1)
                aux = {int(score1):name}
                names.append(aux)
                score1 = ""
                
            names.sort()
            names.reverse()
            #values.sort()
        return names
