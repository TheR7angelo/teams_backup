from PySide6.QtWidgets import QMessageBox


def message(self, text: str, title: str, icon: str):
    """
    :param text:
    Message à afficher
    :param title:
    Titre de la fenetre
    :param icon:
    Question, Information, Attention, Critique, None
    :return:
    None
    """

    self.msgPrint = QMessageBox()

    dictio = {'Question': QMessageBox.Question,
              'Information': QMessageBox.Information,
              'Attention': QMessageBox.Warning,
              'Critique': QMessageBox.Critical,
              # 'Validation': QtGui.QPixmap(os.getcwd() + "\\Ressources\\Parametres\\check.png"),
              # 'Erreur': QtGui.QPixmap(os.getcwd() + "\\Ressources\\Parametres\\cancel.png"),
              None: QMessageBox.NoIcon
              }
    try:
        self.msgPrint.setIcon(dictio[icon])
    except KeyError:
        print("L'icone utiliser n'est pas reconue")
        self.msgPrint.setIcon(QMessageBox.NoIcon)

    self.msgPrint.setWindowTitle(title)
    self.msgPrint.setText(text)
    self.msgPrint.exec_()
