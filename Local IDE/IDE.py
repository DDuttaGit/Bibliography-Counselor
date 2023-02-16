import os
from PySide2.QtCore import Qt, QRect, QSize
from PySide2.QtWidgets import QWidget, QPlainTextEdit, QTextEdit, QShortcut, QFileDialog, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout
from PySide2.QtGui import QColor, QPainter, QTextFormat, QFont, QKeySequence, QIcon
from Bkend import SearchandRank




class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


class QCodeEditor(QPlainTextEdit):
    def __init__(self, app):
        super().__init__(app)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)
        # self.setGeometry(QRect(30, 20, app.width/2-10, app.height-30))
        # self.height, self.width = (app.height()/2, app.width()/2)
        # self.setGeometry(QRect(0, 0, 92, 40))

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)

        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1


class QTerminal(QWidget):
    def __init__(self, app):
        super().__init__(app)
        # self.left = 50
        # self.top = 1000
        # self.width, self.height = (180, 90)
        # self.setGeometry(QRect(950, 450, 920, 520))
        self.height, self.width = (app.height(), app.width())
        self.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
                       "border-color: rgb(252, 233, 79);")
        self.init_text = '/bin/bash$ '
        self.initUI()

    def initUI(self):
        self.terminaltext = QPlainTextEdit(self)
        self.terminaltext.setObjectName(u"Terminal")
        self.terminaltext.setStyleSheet(u"background-color: rgb(74, 38, 51);\n"
                                   "color: rgb(255, 255, 255);")
        self.terminaltext.setGeometry(QRect(10, 10, 920, 400))
        font = QFont()
        font.setFamily(u"Nimbus Mono L")
        font.setPointSize(12)
        font.setBold(True)
        self.terminaltext.setFont(font)
        self.terminaltext.setReadOnly(True)
        self.terminaltext.setPlainText(self.init_text)

    def setText(self, text):
        oldText = str(self.terminaltext.toPlainText())
        self.terminaltext.setPlainText(oldText + '\n'+ self.init_text + text)


class QBackEnd(QWidget):
    def __init__(self, app):
            super().__init__(app)
            # self.left = 50
            # self.top = 1000
            self.width, self.height = (180, 90)
            # self.setGeometry(QRect(950, 20, 950, 430))
            self.setStyleSheet(u"background-color: rgb(250, 250, 250);\n"
                               "border-color: rgb(252, 233, 79);")
            self.iniText = 'Your Cite Suggestions will be appeared here\n=========================\n'
            self.height, self.width = (app.height(), app.width())
            self.initUI()

    def initUI(self):
        self.cite_result = QPlainTextEdit(self)
        self.cite_result.setObjectName(u"Terminal")
        self.cite_result.setStyleSheet(u"background-color: rgb(94, 110, 125);\n"
                                        "color: rgb(255, 255, 255);")
        self.cite_result.setGeometry(QRect(10, 10, 920, 400))
        # self.cite_result.height, self.cite_result = (app.height(), app.width())
        font = QFont()
        font.setFamily(u"Nimbus Mono L")
        font.setPointSize(12)
        font.setBold(True)
        self.cite_result.setFont(font)
        self.cite_result.setReadOnly(True)
        self.cite_result.setPlainText(self.iniText)

    def setText(self, text):
        oldText = str(self.cite_result.toPlainText())
        self.cite_result.setPlainText(oldText + '\n'+ self.iniText + text)

    def print_(self, text):
        oldText = str(self.cite_result.toPlainText())
        self.cite_result.setPlainText(oldText + '\n' + text)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Local LaTeX Editor'
        self.setWindowIcon(QIcon('./Icon/256_2.png'))
        self.saved = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        # layout1 = QHBoxLayout()
        # layout2 = QVBoxLayout()
        self.codeEditor = QCodeEditor(self)
        self.terminal = QTerminal(self)
        self.backend = QBackEnd(self)
        # layout2.addWidget(self.terminal)
        # layout2.addWidget(self.backend)
        # layout1.addWidget(self.codeEditor)
        # layout1.addLayout(layout2)
        layout = QGridLayout()
        layout.addWidget(self.codeEditor, 0, 0, 100, 10)
        layout.addWidget(self.backend, 0,500,60,10)
        layout.addWidget(self.terminal,50,500,50,10)
        self.run = QPushButton('', self)
        self.run.setToolTip('Compile using pdflatex\nCtrl+Shift+C')
        self.run.move(900, 950)
        self.run.setIcon(QIcon('Icon/circled-play_black.png'))
        self.run.setIconSize(QSize(30, 30))
        self.run.setStyleSheet(u"background-color: rgb(255, 203, 199);\n"
                          "border-style: outset;\n"
                          "border-width: 2px;\n"
                          "border-radius: 15px;\n"
                          "border-color: white;\n"
                          "padding: 7px;")
        self.run.clicked.connect(self.compileButton)
        self.suggest = QPushButton('', self)
        self.suggest.setToolTip('Get Suggesion\nCtrl+Space')
        self.suggest.move(900, 950)
        self.suggest.setIcon(QIcon('Icon/suugest_black.png'))
        self.suggest.setIconSize(QSize(30, 30))
        self.suggest.setStyleSheet(u"background-color: rgb(255, 203, 199);\n"
                               "border-style: outset;\n"
                               "border-width: 2px;\n"
                               "border-radius: 15px;\n"
                               "border-color: white;\n"
                               "padding: 7px;")
        self.suggest.clicked.connect(self.suggestButton)
        self.open = QPushButton('', self)
        self.open.setToolTip('Open a File\nCtrl+O')
        self.open.move(900, 950)
        self.open.setIcon(QIcon('Icon/opened-folder_black.png'))
        self.open.setIconSize(QSize(30, 30))
        self.open.setStyleSheet(u"background-color: rgb(255, 203, 199);\n"
                                   "border-style: outset;\n"
                                   "border-width: 2px;\n"
                                   "border-radius: 15px;\n"
                                   "border-color: white;\n"
                                   "padding: 7px;")
        self.open.clicked.connect(self.openButton)
        self.save = QPushButton('', self)
        self.save.setToolTip('Save a File\nCtrl+S')
        self.save.move(900, 950)
        self.save.setIcon(QIcon('Icon/save_black.png'))
        self.save.setIconSize(QSize(30, 30))
        self.save.setStyleSheet(u"background-color: rgb(255, 203, 199);\n"
                                "border-style: outset;\n"
                                "border-width: 2px;\n"
                                "border-radius: 15px;\n"
                                "border-color: white;\n"
                                "padding: 7px;")
        self.save.clicked.connect(self.saveButton)
        layout.addWidget(self.open)
        layout.addWidget(self.save)
        layout.addWidget(self.suggest)
        layout.addWidget(self.run)
        self.setLayout(layout)
        self.showMaximized()
        self.connectMe()

    def connectMe(self):
        self.codeEditor.shortcut = QShortcut(QKeySequence('Ctrl+ '), self)
        self.codeEditor.shortcut.activated.connect(
            lambda shortcut_key=self.codeEditor.shortcut.key().toString():
            self.suggestButton())

        self.codeEditor.shortcut_save = QShortcut(QKeySequence('Ctrl+S'), self)
        self.codeEditor.shortcut_save.activated.connect(
            lambda shortcut_key=self.codeEditor.shortcut_save.key().toString():
            self.saveButton())

        self.compile_shortcut = QShortcut(QKeySequence('Ctrl+Shift+C'), self)
        self.compile_shortcut.activated.connect(
            lambda shortcut_key=self.compile_shortcut.key().toString():
            self.compileButton())

        self.codeEditor.shortcut_open = QShortcut(QKeySequence('Ctrl+O'), self)
        self.codeEditor.shortcut_open.activated.connect(
            lambda shortcut_key=self.codeEditor.shortcut_open.key().toString():
            self.openButton())

    def suggestButton(self):
        self.suggest.setIcon(QIcon('Icon/suugest_white.png'))
        self.suggest.setIconSize(QSize(30, 30))
        cursor = self.codeEditor.textCursor()
        st, end = cursor.selectionStart(), cursor.selectionEnd()
        self.terminal.setText(self.codeEditor.toPlainText()[st:end])
        cursor = self.codeEditor.textCursor()
        st, end = cursor.selectionStart(), cursor.selectionEnd()
        query=self.codeEditor.toPlainText()[st:end]
        if st == end:
            self.backend.setText('You have selected no query to search! Sorry\n')
        else:
            sourceURLs = (('ACM-DL', 'IEEEXplore', 'Cross Ref', 'DBLP', 'Semantic Scholar'))
            top = 5
            # self.QForm = test.Form(self)
            # self.QForm.show()
            # sourceURLs = self.QForm.ret
            # acm,ieee, cref, dblp, ss, top = sourceURLs
            SearchandRank.run(query, sourceURLs, top, self.backend)
        self.suggest.setIcon(QIcon('Icon/suugest_black.png'))
        self.suggest.setIconSize(QSize(30, 30))

    def saveButton(self):
        self.save.setIcon(QIcon('Icon/save_white.png'))
        self.save.setIconSize(QSize(30, 30))
        if not self.saved:
            # Fname, done = QInputDialog.getText(self, 'Input Dialog', 'Save the File as: ')
            Fname, done = QFileDialog.getSaveFileName(self, 'Save the TeX', '~/')
            if str(done) == "All Files (*)":
                if not Fname.endswith('.tex'):
                    Fname = Fname+'.tex'
                with open(Fname, 'w') as f:
                    f.write(str(self.codeEditor.toPlainText()))
                    self.filename = Fname
                    self.title += ' - ' + self.filename.split('/')[-1]
                    self.setWindowTitle(self.title)
                self.terminal.setText(self.filename + ' saved successfully!')
                self.saved = True
            else:
                self.terminal.setText('Save Aborted!!')

        if self.saved:
            self.title += ' - ' + self.filename.split('/')[-1]
            with open(self.filename, 'w') as f:
                f.write(str(self.codeEditor.toPlainText()))
            self.terminal.setText(self.filename + ' saved successfully!')
        self.save.setIcon(QIcon('Icon/save_black.png'))
        self.save.setIconSize(QSize(30, 30))

    def compileButton(self):
        self.run.setIcon(QIcon('Icon/circled-play_white.png'))
        self.run.setIconSize(QSize(30, 30))
        if not self.saved:
            self.saveButton()
        if self.saved:
            self.saveButton()
            result = os.system("pdflatex " + self.filename + ' > ./.app_compile.log')
            with open('./.app_compile.log') as f:
                op = ''.join(f.readlines())
                print(op)
                self.terminal.setText(op)
            os.remove('./.app_compile.log')
            if result == 0:
                self.terminal.setText('Your Project has been compiled Succesfully')
            else:
                self.terminal.setText('Bad Resuest. No PDF Generated')
        else:
            self.terminal.setText('No file to Compile')
        self.run.setIcon(QIcon('Icon/circled-play_black.png'))
        self.run.setIconSize(QSize(30, 30))

    def openButton(self):
        self.open.setIcon(QIcon('Icon/opened-folder_white.png'))
        self.open.setIconSize(QSize(30, 30))
        fname, done = QFileDialog.getOpenFileName(self, 'Open a Tex file', '~/', 'TeX Files (*.tex);; Bib Files(*.bib)')
        if done:
            self.filename = fname
            self.saved = True
            self.title += ' - '+ self.filename.split('/')[-1]
            self.setWindowTitle(self.title)
            with open(fname) as f:
                text = ''.join(f.readlines())
                self.codeEditor.setPlainText(text)
        else:
            self.terminal.setText('No File Chosen')
        self.open.setIcon(QIcon('Icon/opened-folder_black.png'))
        self.open.setIconSize(QSize(30, 30))



if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication

    app = QApplication(sys.argv)
    Ide = App()
    sys.exit(app.exec_())
