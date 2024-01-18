import sys
from PySide6 import QtCore, QtWidgets, QtGui
from ebayScraper import EbayScraper
class ScraperGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.text = QtWidgets.QLabel("Welcome! Please enter what you'd like to sell below.",
                                    alignment=QtCore.Qt.AlignCenter)
        self.searchTerm = QtWidgets.QLineEdit("Ex. \"iPhone X\"",
                                    alignment=QtCore.Qt.AlignCenter)
        self.includeShippingCosts = QtWidgets.QCheckBox("Include Shipping Costs")                            
        self.button = QtWidgets.QPushButton("Show Recommended Price")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.includeShippingCosts)
        self.layout.addWidget(self.searchTerm)
        self.layout.addWidget(self.button)
        self.setWindowTitle("Ebay Price Finder")

        self.button.clicked.connect(self.searchFor)
        self.searchTerm.returnPressed.connect(self.searchFor)

    def searchFor(self):
        try:
            shippingIncluded = self.includeShippingCosts.isChecked()
            scrape = EbayScraper(f"{self.searchTerm.text()}", shipping=shippingIncluded)
            self.text.setText(scrape.finalAvg)
        except:
            self.text.setText("No sold listings found.")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = ScraperGUI()
    widget.resize(300, 100)
    widget.show()

    sys.exit(app.exec())