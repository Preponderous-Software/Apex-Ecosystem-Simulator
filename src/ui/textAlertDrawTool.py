# This class is responsible for drawing text alerts on the screen.

class TextAlertDrawTool():

    def drawTextAlert(self, textAlert, graphik):
        numLines = len(textAlert.text)        
        backgroundColor = (255, 255, 255)
        backgroundX = textAlert.x - textAlert.size * 6
        backgroundY = textAlert.y - textAlert.size
        backgroundWidth = 250
        backgroundHeight = 20*numLines + 20
        graphik.drawRectangle(backgroundX, backgroundY, backgroundWidth, backgroundHeight, backgroundColor)
        for i in range(0, numLines):
            graphik.drawText(textAlert.text[i], textAlert.x, textAlert.y + 20*i, textAlert.size, textAlert.color)