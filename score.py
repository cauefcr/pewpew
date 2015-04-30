class Score:
    def setScore(self, name, score):
        """Defines a new score based on input and appends it on Scores.txt so
that it may replace any of the highscores"""
        with open("Scores.txt", "a") as file:
            file.write(name + "-" + str(score)+"\n")
        scores = Score().getScore()
        cont = 0
        with open("Scores.txt", "w") as file:
            for i in scores:
                for j in i:
                    file.write(i[j] + "-" + str(j) +"\n")
                cont += 1
                if cont > 4:
                    break

    def getScore(self):
        """Reads the score from the Scores.txt file located inside
the game's directory, sorts it along with the new score and replaces accordingly"""
        #values = []
        names = []
        score1 = ""
        with open("Scores.txt") as file:
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
