
from PyQt5.QtWidgets import QApplication
import sys
from msale import MSale
if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = MSale()
    m.show()
    sys.exit(app.exec_())



