from PyQt5 import QtGui, QtCore, QtWebKit
import sys
import urllib
import re
 
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
 
 
class programa(QtGui.QWidget):
 
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.msg = QtGui.QMessageBox(self)
		self.msg.setWindowTitle(_fromUtf8("Información"))
		self.setWindowTitle(_fromUtf8('Finder'))
		self.resize(529, 440)
		self.input_busqueda = QtGui.QLineEdit(self)
		self.input_busqueda.setGeometry(10, 20, 371, 20)
		self.boton_buscar = QtGui.QPushButton("Buscar", self)
		self.boton_buscar.setGeometry(390, 10, 61, 41)
		self.boton_guardar = QtGui.QPushButton("Guardar", self)
		self.boton_guardar.setGeometry(455, 10, 61, 41)
		self.connect(self.boton_guardar, QtCore.SIGNAL("clicked()"), self.guardar)
		#TABLA ORDENADORA DE RESULTADOS
		self.tabla = QtGui.QTreeWidget(self)
		self.tabla.setGeometry(0, 195, 530, 246)
		self.tabla.headerItem().setText(0, "#")
		self.tabla.headerItem().setText(1, "Id.")
		self.tabla.headerItem().setText(2, _fromUtf8("Tamaño"))
		self.tabla.headerItem().setText(3, "Url")
		#FIN TABLA
		self.grupo_options = QtGui.QGroupBox(self)
		self.grupo_options.setGeometry(10, 47, 291, 101)
		self.icon_perpage_label = QtGui.QLabel(self.grupo_options)
		self.icon_perpage_label.setGeometry(20, 30, 90, 16)
		self.icons_perpage_spin = QtGui.QSpinBox(self.grupo_options)
		self.icons_perpage_spin.setGeometry(113, 27, 47, 22)
		self.icons_perpage_spin.setProperty("value", 20)
		self.minimum_size_label = QtGui.QLabel(self.grupo_options)
		self.minimum_size_label.setGeometry(20, 70, 100, 13)
		self.minimum_size_spin = QtGui.QSpinBox(self.grupo_options)
		self.minimum_size_spin.setMaximum(190)
		self.minimum_size_spin.setGeometry(113, 65, 47, 22)
		self.minimum_size_spin.setProperty("value", 16)
		self.maximum_size_label = QtGui.QLabel(self.grupo_options)
		self.maximum_size_label.setGeometry(170, 70, 70, 13)
		self.maximum_size_spin = QtGui.QSpinBox(self.grupo_options)
		self.maximum_size_spin.setGeometry(241, 67, 42, 22)
		self.maximum_size_spin.setMaximum(190)
		self.maximum_size_spin.setProperty("value", 40)
		self.grupo_preview = QtGui.QGroupBox(self)
		self.grupo_preview.setGeometry(320, 47, 201, 141)
		self.total_results_label = QtGui.QLabel(self)
		self.total_results_label.setGeometry(20, 145, 81, 21)
		self.total_results_label.setStyleSheet("font-weight: bold;")
		self.numero_results_label = QtGui.QLabel(self)
		self.numero_results_label.setGeometry(100, 145, 31, 21)
		self.numero_results_label.setStyleSheet("font-weight: bold;")
		self.viewing_page_label = QtGui.QLabel(self)
		self.viewing_page_label.setGeometry(132, 145, 91, 21)
		self.viewing_page_label.setStyleSheet("font-weight: bold;")
		self.number_vpage_label = QtGui.QLabel(self)
		self.number_vpage_label.setGeometry(190, 145, 51, 21)
		self.number_vpage_label.setStyleSheet("font-weight: bold;")
		self.go_page_label = QtGui.QLabel(_fromUtf8("Ir a página:"), self)
		self.go_page_label.setGeometry(20, 170, 71, 16)
		self.go_page_label.setStyleSheet("font-weight: bold;")
		self.go_page_spin = QtGui.QSpinBox(self)
		self.go_page_spin.setGeometry(89, 168, 42, 22)
 
		self.grupo_options.setTitle("Opciones")
		self.icon_perpage_label.setText(_fromUtf8("Iconos por página:"))
		self.minimum_size_label.setText(_fromUtf8("Tamaño mínimo    :"))
		self.maximum_size_label.setText(_fromUtf8("Tam. máximo:"))
		self.grupo_preview.setTitle("Prevista")
		self.total_results_label.setText("Resultados:")
		self.numero_results_label.setText("0")
		self.viewing_page_label.setText(_fromUtf8("| Página:"))
		self.number_vpage_label.setText("0")
		self.connect(self.boton_buscar, QtCore.SIGNAL("clicked()"), self.buscar)
		self.connect(self.tabla, QtCore.SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.ver_link)
		self.preview = QtWebKit.QWebView(self.grupo_preview)
		self.preview.setGeometry(6, 16, 191, 115)

		self.connect(self, QtCore.SIGNAL("closeEvent()"), self.close)
 
	def guardar(self):
		archivo = QtGui.QFileDialog.getSaveFileName(self,
                self.tr("Guardar Archivo"), ".")
		try:
			loader = urllib.urlopen(str(self.url)).read()
			file = open(archivo, "wb")
			file.write(loader)
			file.close()
			self.msg.setText(_fromUtf8("Tu archivo se guardó con éxito"))
		except:
			self.msg.setText(_fromUtf8("¡Tu archivo no se pudo guardar!"))
			pass
		self.msg.exec_()
	def ver_link(self, item, i):
		self.url = item.text(3)
		self.preview.setStyleSheet("background-color: transparent; ")
		self.preview.setHtml("<center><img src='%s'></center>" % self.url)
 
	def buscar(self):
		self.tabla.clear()
		q = str(self.input_busqueda.text())
		icons_perpage = self.icons_perpage_spin.value()
		min_size = self.minimum_size_spin.value()
		max_size = self.maximum_size_spin.value()
		page = self.go_page_spin.value()
		url = urllib.urlopen("https://www.iconfinder.com/xml/search/?q=%s&c=%s&min=%s&max=%s&p=%s&api_key=4c5b276337af418894c87590412e4e39" % (q, icons_perpage, min_size, max_size, page)).read()
		x = url.split("<icon>")
		id = []
		size = []
		image = []
		for d in x:
			for idx in re.findall("<id>(.+?)<\/id>", d):
				id.append(idx)
			for sizex in re.findall("<size>(.+?)<\/size>", d):
				size.append(sizex)
			for imagex in re.findall("<image>(.+?)<\/image>", d):
				image.append(imagex)
		count = 1;
		for i, idx, sizex, imagex in zip(range(len(id)), id, size, image):
			exec("item_%s = QtGui.QTreeWidgetItem(self.tabla)"%i)
			self.tabla.topLevelItem(i).setText(0, str(count))
			self.tabla.topLevelItem(i).setText(1, str(idx))
			self.tabla.topLevelItem(i).setText(2, str(sizex))
			self.tabla.topLevelItem(i).setText(3, str(imagex))
			count += 1
		self.number_vpage_label.setText(str(page))
		self.numero_results_label.setText(str(count-1))
 
app = QtGui.QApplication(sys.argv)
form = programa()
form.show()
app.exec_()