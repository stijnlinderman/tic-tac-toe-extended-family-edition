# IMPORTS
import random
import string as stringImport
import math

# VARIABLES
divider, emptyLine = "\n" + "-" * 30, ""
defaultError = "something went wrong"
maxFieldSize = 26
alphabetCapitals = stringImport.ascii_uppercase


# MAIN FUNCTION
def playTicTacToe():
    game = GameField()
    playing = True
    while playing:
        if not game.configurated:
            game.configure()
        game.runGame()
        rematch = game.proposeRematch()
        if rematch:
            continue
        newGame = game.proposeNewGame()
        if newGame:
            game.resetConfiguration()
            continue
        game.printGoodbyeMessage(True)
        game.printCredits()
        playing = False


# CLASSES
class GameField:
    def __init__(self):
        self.gameName = "Tic-Tac-Toe: Extended Family Edition"
        self.configurated = False
        self.introMessage()

    def introMessage(self):
        print(divider + "\nWelcome to " + self.gameName + "!")

    def configure(self):
        self.configureSize()
        self.configurePlayers()
        self.configurated = True

    def configureSize(self):
        print(divider)
        sizeString = askForInput("",
                                 "How big should the game field be?",
                                 "amount",
                                 "Please input an amount between 3 and " + str(
                                     maxFieldSize) + ".", 1, 4,
                                 [],
                                 rangeInStrings(3, maxFieldSize + 1))
        self.gameFieldSize = int(sizeString)
        self.configureFields()
        self.configureWinPatterns()
        print(
            "\nOK. Game field size was set to " + sizeString + "x" + sizeString + ".")

    def configureFields(self):
        self.columnIndexes = list(range(0, self.gameFieldSize))
        self.columnNames = list(alphabetCapitals[0:self.gameFieldSize])
        self.rowIndexes = list(range(0, self.gameFieldSize))
        self.rowNames = []
        self.fieldNames = []
        self.insertPossibleFields()
        self.amountFields = len(self.fieldNames)

    def insertPossibleFields(self):
        for rowIndex in self.rowIndexes:
            self.rowNames.insert(rowIndex, str(rowIndex + 1))
            for columnName in self.columnNames:
                self.fieldNames.append(
                    columnName + self.rowNames[rowIndex])

    def configureWinPatterns(self):
        self.winningPatterns = []
        self.winSequenceLength = self.gameFieldSize
        self.configureHorizontalWinPatterns(self.winSequenceLength)
        self.configureVerticalWinPatterns(self.winSequenceLength)
        self.configureDiagonalPatterns(self.winSequenceLength)

    def configureHorizontalWinPatterns(self, sqLength):
        for rowNumber in self.rowIndexes:
            patternStartIndex = rowNumber * sqLength
            newPattern = list(range(patternStartIndex,patternStartIndex + sqLength))
            self.winningPatterns.append(newPattern)

    def configureVerticalWinPatterns(self, sqLength):
        verticalPatterns = [[] for columns in self.columnIndexes]
        for rowNumber in self.rowIndexes:
            for columnNumber in self.columnIndexes:
                fieldNumber = rowNumber * sqLength + columnNumber
                verticalPatterns[columnNumber].append(fieldNumber)
        self.winningPatterns.extend(verticalPatterns)

    def configureDiagonalPatterns(self, sqLength):
        diagonalDown = {"start": 0, "step": sqLength + 1}
        diagonalUp = {"start": sqLength - 1, "step": sqLength - 1}
        for diagonal in [diagonalDown, diagonalUp]:
            pattern = []
            for columnIndex in self.columnIndexes:
                fieldIndex = diagonal["start"] + columnIndex * diagonal["step"]
                pattern.append(fieldIndex)
            self.winningPatterns.append(pattern)

    def configurePlayers(self):
        print(divider)
        self.players = []
        self.configureAmountOfPlayers()
        self.invitePlayers()

    def configureAmountOfPlayers(self):
        amountOptions = rangeInStrings(2, self.gameFieldSize + 1)
        self.amountString = askForInput("",
                                        "How many players do you want to add to the game?",
                                        "amount",
                                        "Please input an amount between 2 and " + str(
                                            self.gameFieldSize) + ".", 1,
                                        4, [], amountOptions)
        self.amountPlayers = int(self.amountString)
        print("\nOK. " + str(
            self.amountPlayers) + " players will be invited to the game.")

    def invitePlayers(self):
        self.callPlayerNamesString = ""
        for playerNumber in range(self.amountPlayers):
            print(divider)
            playerNamesInUse, playerCharsInUse = self.getPlayerDataInUse()
            newPlayer = Player(playerNumber, playerNamesInUse, playerCharsInUse)
            self.addPlayer(newPlayer)
            if playerNumber == self.amountPlayers - 1:
                self.callPlayerNamesString += " and "
            elif playerNumber > 0:
                self.callPlayerNamesString += ", "
            self.callPlayerNamesString += newPlayer.name
        print(divider + "\nWelcome " + self.callPlayerNamesString + "!\n")

    def getPlayerDataInUse(self):
        playerNamesInUse, playerCharsInUse = [], []
        for player in self.players:
            playerNamesInUse.append(player.name)
            playerCharsInUse.append(player.char)
        return playerNamesInUse, playerCharsInUse

    def addPlayer(self, player):
        self.players.append(player)

    def runGame(self):
        self.resetMoves()
        self.randomizePlayerOrder()
        self.runGameCycle()

    def resetMoves(self):
        self.amountFieldsInUse = 0
        for player in self.players:
            player.resetMoves()

    def randomizePlayerOrder(self):
        random.shuffle(self.players)

    def runGameCycle(self):
        self.welcomePlayers()
        while True:
            self.printGameField()
            playerOnTurn = self.getPlayerOnTurn()
            self.processMove(playerOnTurn)
            if self.hasPlayerWon(playerOnTurn):
                self.announceGameOutcome(playerOnTurn)
                break
            elif self.amountFieldsInUse == self.amountFields:
                self.announceGameOutcome()
                break
            self.rotateTurn()
            continue

    def welcomePlayers(self):
        print("A new round of " + self.gameName + " has started.",
              "You need " + str(
                  self.gameFieldSize) + " marks in a row to win the game.",
              "\n" + self.getPlayerOnTurn().name + " may take first turn. Good luck and have fun!",
              sep="\n")

    def printGameField(self):
        print(*[
            divider,
            "\n       " + self.gameFieldSize * "  " + "COLUMNS",
            self.getColumnNamesFormattedForPrint(),
            emptyLine,
            *self.getRowsFormattedForPrint(),
            emptyLine
        ], sep="\n")

    def getColumnNamesFormattedForPrint(self):
        columnNames = "         "
        for columnName in self.columnNames:
            columnNames += "   " + columnName
        return columnNames

    def getRowsFormattedForPrint(self):
        rowPrintLines = []
        fieldValuesForPrinting = self.getGameFieldValuesForPrint()
        for rowInt in self.rowIndexes:
            startInt = rowInt * self.gameFieldSize
            rowName = str(rowInt + 1)
            if int(rowName) < 10:
                rowName = " " + rowName
            rowLine1 = "      " + rowName + "    " + fieldValuesForPrinting[
                startInt]
            rowLine2 = "            -"
            for rowValue in fieldValuesForPrinting[
                            startInt + 1:startInt + self.gameFieldSize]:
                rowLine1 += " | " + rowValue
                rowLine2 += " + -"
            rowPrintLines.append(rowLine1)
            if rowInt < self.gameFieldSize - 1:
                rowPrintLines.append(rowLine2)
        floorDescriptionLineNumber = math.floor(len(rowPrintLines) / 2)
        rowPrintLines[floorDescriptionLineNumber] = "ROWS" + rowPrintLines[
                                                                 floorDescriptionLineNumber][
                                                             4:]
        return rowPrintLines

    def getGameFieldValuesForPrint(self):
        fieldValues = list(self.amountFields * " ")
        for player in self.players:
            for moveFieldIndex in player.moves:
                fieldValues[moveFieldIndex] = player.char
        return fieldValues

    def getPlayerOnTurn(self):
        return self.players[0]

    def processMove(self, player):
        playerMove = askForInput(player.name,
                                 "where do you want to place your mark? (example: B3)",
                                 "field",
                                 "Please input the name of an unused field.",
                                 2, 3, self.getGameFieldsInUseNames(),
                                 self.fieldNames)
        moveFieldIndex = self.fieldNames.index(playerMove)
        player.updateMoves(moveFieldIndex)
        self.amountFieldsInUse += 1

    def getGameFieldsInUseNames(self):
        fieldsInUseNames = []
        for player in self.players:
            for fieldIndex in player.moves:
                fieldsInUseNames.append(self.fieldNames[fieldIndex])
        return fieldsInUseNames

    def hasPlayerWon(self, player):
        for pattern in self.winningPatterns:
            if self.isPatternPartOfPattern(player.moves, pattern):
                return True

    def isPatternPartOfPattern(self, pattern1, pattern2):
        matchOnAllFields = all(element in pattern1 for element in pattern2)
        return matchOnAllFields

    def announceGameOutcome(self, winner=None):
        self.printGameField()
        if winner:
            print(winner.name + " WON!")
        else:
            print("The game was a draw. Nobody won.")

    def rotateTurn(self):
        playerListOldOrder = self.players
        self.players = []
        for i, player in enumerate(playerListOldOrder):
            if i > 0:
                self.players.append(player)
        self.players.append(playerListOldOrder[0])

    def proposeRematch(self):
        print(divider)
        restartAnswer = askForInput(self.callPlayerNamesString,
                                    "do you want a rematch?", "answer",
                                    "Please answer 'yes' or 'no'.", 2, 3, [],
                                    ['YES', 'NO'])
        if restartAnswer == "YES":
            print(
                "\nOK. Starting a new round for " + self.callPlayerNamesString + ".\n" + divider)
            return True

    def proposeNewGame(self):
        print(divider)
        newPlayersAnswer = askForInput("",
                                       "Do you want to start a new game with a new size and new players?",
                                       "answer",
                                       "Please answer 'yes' or 'no'.", 2, 3, [],
                                       ['YES', 'NO'])
        if newPlayersAnswer == "YES":
            print("\nOK.")
            return True

    def resetConfiguration(self):
        self.amountFieldsInUse = 0
        self.configurated = False

    def printGoodbyeMessage(self, extraEmptyLine=None):
        if extraEmptyLine:
            print(emptyLine)
        print(
            "OK. " + self.callPlayerNamesString + ", thank you for playing and goodbye!")

    def printCredits(self):
        print(divider + "\n" + self.gameName + " was coded by Stijn Linderman.")


# CLASSES
class Player:
    def __init__(self, playerNumber, namesInUse, charsInUse):
        self.name = askForInput("Player " + str(playerNumber + 1),
                                "what is your name?", "name",
                                "Please input a unique name that contains two to sixteen characters.",
                                2, 16,
                                namesInUse)
        print(emptyLine)
        self.char = askForInput("Hi " + self.name,
                                "what character do you want to use in the game?",
                                "character",
                                "Please input a unique, single, alphabetical character.",
                                1, 1, charsInUse,
                                alphabetCapitals)
        print(
            "\n" + self.name + ", thanks for your input. You moves in the game will be marked with the letter " + self.char + ".")
        self.resetMoves()

    def resetMoves(self):
        self.moves = []

    def updateMoves(self, field):
        self.moves.append(field)


# UTIL FUNCTIONS
def askForInput(name, question, inputType="input",
                explanation="Please try again.", inputMinLength=0,
                inputMaxLength=16, inputImpossibilities=[],
                inputPossibilities=[]):
    nameLength = len(name)
    if nameLength > 0:
        name += ", "
    while True:
        inputQuestion = question + "\n"
        inputAnswer = input(name + inputQuestion).upper()
        inputAccepted, error = isStringWithinBoundaries(inputAnswer,
                                                        inputMinLength,
                                                        inputMaxLength,
                                                        inputImpossibilities,
                                                        inputPossibilities)
        if inputAccepted:
            return inputAnswer
        else:
            print(
                "\nThe " + inputType + " that was entered " + error + ". " + explanation)
            continue


def isStringWithinBoundaries(input, minLength=0, maxLength=16,
                             impossibilities=[], possibilities=[]):
    impossibilitiesAmount = len(impossibilities)
    possibilitiesAmount = len(possibilities)
    stringLengthWithoutSpaces = getStringLengthWithoutSpaces(input)
    if (impossibilitiesAmount > 0 and input in impossibilities) or (
            possibilitiesAmount > 0 and input not in possibilities) or stringLengthWithoutSpaces < minLength or stringLengthWithoutSpaces > maxLength:
        return False, "was not accepted"
    elif stringLengthWithoutSpaces >= minLength and stringLengthWithoutSpaces <= maxLength:
        return True, None
    return False, defaultError


def rangeInStrings(min, max):
    return [str(i) for i in range(min, max)]


def getStringLengthWithoutSpaces(string):
    return len(string.replace(" ", ""))


playTicTacToe()