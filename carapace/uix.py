# import qute
#
# from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
#
#
# class W(qute.QWidget):
#
#     def __init__(self, parent=None):
#         super(W, self).__init__(parent=parent or qute.utilities.windows.mainWindow())
#
#         self.setLayout(
#             qute.utilities.layouts.slimify(
#                 qute.QVBoxLayout(),
#             ),
#         )
#
#         self.w = qute.QLabel('fooooooooooooooooooo barrrrrrrrrrrrrr')
#         self.layout().addWidget(self.w)
#
#
# def get_parent_layout():
#
#     for child in qute.utilities.windows.mainWindow().findChildren(qute.QWidget):
#         if child.objectName():
#             #if 'Item' in child.objectName() or 'Menu' in child.objectName() or 'scrollarea' in child.objectName() or 'formLayout' in child.objectName() or 'ScrollFieldExecuter' in child.objectName() or 'label' in child.objectName():
#             #    continue
#
#             if 'toolbox' in child.objectName().lower():
#                 print(child.objectName(), type(child))
#
#             if child.objectName() == 'animBotWorkspaceControl':
#                 print('Laout : {}'.format(child.layout()))
#                 return child.layout()
#
#
# def launch():
#     w = W()
#     w.show()
#
#     parent_layout = get_parent_layout().parent().layout()
#     parent_layout.addWidget(w)
#
#
#
