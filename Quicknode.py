from Katana import UI4
from PySide6 import QtWidgets, QtCore, QtGui
import pickle
from Katana import NodegraphAPI
from Katana import RenderingAPI
from Katana import RenderManager # Import RenderManager for preview rendering

class MyCustomTab(UI4.Tabs.BaseTab):
    def __init__(self, parent):
        super(MyCustomTab, self).__init__(parent)
        self.setAcceptDrops(True)  # Enable accepting drops

        # Create a Widget to display dragged nodes
        self.node_list_widget = QtWidgets.QListWidget()
        self.node_list_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        # Connect the double-click signal to a function
        self.node_list_widget.itemDoubleClicked.connect(self.focus_on_node)


        self.node_list_widget.itemClicked.connect(self.select_node_on_click)
        
        
        # Set up the layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel('Drag nodes here:'))
        layout.addWidget(self.node_list_widget)
        
        # Create a horizontal layout for the buttons
        button_layout = QtWidgets.QHBoxLayout()

        # Create the "Sort" button
        self.sort_button = QtWidgets.QPushButton("Sort")
        button_layout.addWidget(self.sort_button)

        # Create the "Clear" button
        self.clear_button = QtWidgets.QPushButton("Clear")
        button_layout.addWidget(self.clear_button)

        # Add the button layout to the main vertical layout
        layout.addLayout(button_layout)

        # Connect the button signals to their respective functions
        self.sort_button.clicked.connect(self.sort_nodes)
        self.clear_button.clicked.connect(self.clear_node_list)

        self.setLayout(layout)
                
                
        self.node_list_widget.installEventFilter(self)

    def eventFilter(self, watched, event):
            if watched == self.node_list_widget and event.type() == QtCore.QEvent.KeyPress:
                key = event.key()

                if key == QtCore.Qt.Key_V:
                    selected_items = self.node_list_widget.selectedItems()
                    if selected_items:
                        for item in selected_items:
                            node_name = item.text()
                            node = NodegraphAPI.GetNode(node_name)
                            if node:
                                NodegraphAPI.SetNodeViewed(node, viewed=True, exclusive=True)
                        return True  # Event handled
                    return False  # No selected items; event not handled

                elif key == QtCore.Qt.Key_F:
                    UI4.App.Tabs.FindTopTab('Node Graph').frameSelection()
                    return True  # Event handled

                elif key == QtCore.Qt.Key_E:
                    selected_items = self.node_list_widget.selectedItems()
                    if selected_items:
                        for item in selected_items:
                            node_name = item.text()
                            node = NodegraphAPI.GetNode(node_name)
                            if node:
                                NodegraphAPI.SetNodeEdited(node, edited=True, exclusive=False)
                        return True  # Event handled
                    return False

                elif key == QtCore.Qt.Key_Delete:
                    selected_items = self.node_list_widget.selectedItems()
                    if selected_items:
                        # Remove items in reverse order to avoid shifting indices
                        for item in reversed(selected_items):
                            row = self.node_list_widget.row(item)
                            self.node_list_widget.takeItem(row)
                        return True  # Event handled
                    return False
                    
                elif key == QtCore.Qt.Key_P:
                    selected_items = self.node_list_widget.selectedItems()
                    if selected_items:
                        for item in reversed(selected_items):
                            node_name = item.text()
                            node = NodegraphAPI.GetNode(node_name)
                            if node:
                                # --- Best Practice: Clear existing view flags ---
                                # Get all nodes in the current node graph
                                all_nodes = NodegraphAPI.GetAllNodes()                              
                                # Use RenderManager to start the 'preview' render process
                                print(node_name)
                                NodegraphAPI.SetNodeViewed(node, viewed=True, exclusive=True)
                                RenderManager.StartRender('previewRender', node)
                                print("Preview render initiated via RenderManager.")

                        
                        return True  # Event handled
                    return False
                    
                elif key == QtCore.Qt.Key_I:
                    selected_items = self.node_list_widget.selectedItems()
                    if selected_items:
                        for item in reversed(selected_items):
                            node_name = item.text()
                            node = NodegraphAPI.GetNode(node_name)
                            if node:
                                # --- Best Practice: Clear existing view flags ---
                                # Get all nodes in the current node graph
                                all_nodes = NodegraphAPI.GetAllNodes()                              
                                # Use RenderManager to start the 'preview' render process
                                print(node_name)
                                RenderManager.StartRender('liveRender', node)
                                print("Live render initiated via RenderManager.")

                    
                        return True  # Event handled
                    return False

                else:
                    return False  # Unhandled key
            # Let other events pass to the base implementation
            return super(MyCustomTab, self).eventFilter(watched, event)
                            
    def sort_nodes(self):
        # This function will be called when the "Sort" button is clicked
        print("Sort button clicked!")
        # Sorting logic here
        items = []
        for i in range(self.node_list_widget.count()):
            items.append(self.node_list_widget.item(i).text())
        items.sort()
        self.node_list_widget.clear()
        self.node_list_widget.addItems(items)

    def clear_node_list(self):
        # This function will be called when the "Clear" button is clicked
        print("Clear button clicked!")
        # Clear the node list
        self.node_list_widget.clear()
                        
    def dragEnterEvent(self, event):
        # Accept the drag event if it contains node data
        mime_data = event.mimeData()
        formats = mime_data.formats()
        print(f"Available MIME formats: {formats}") # Print all available formats
        if 'nodegraph/nodes' in formats:
            print("Drag entered with correct format ('nodegraph/nodes')")
            event.acceptProposedAction()
        else:
            print("Drag entered with incorrect format")
            event.ignore()

    def dropEvent(self, event):
        # Handle the drop event
        mime_data = event.mimeData()
        if mime_data.hasFormat('nodegraph/nodes'):
            print("Drop occurred with correct format ('nodegraph/nodes')")
            # Extract node data from the event
            node_data_raw = mime_data.data('nodegraph/nodes')
            print(f"Raw node data ('nodegraph/nodes'): {node_data_raw}")  # Debugging print

            # Try to unpickle the data
            try:
                node_info = pickle.loads(node_data_raw)
                print(f"Unpickled node info: {node_info}")
                if isinstance(node_info, list):
                    for item in node_info:
                        if isinstance(item, tuple) and len(item) > 1:
                            node_name = item[0]
                            self.node_list_widget.addItem(node_name)
                            print(f"Added item to list: {node_name}") # Debugging print
                elif isinstance(node_info, dict) and 'nodeNames' in node_info:
                    node_names = node_info['nodeNames']
                    for node_name in node_names:
                        self.node_list_widget.addItem(node_name)
                        print(f"Added item to list: {node_name}") # Debugging print
                else:
                    print("Unexpected format of unpickled data")

            except Exception as e:
                print(f"Error unpickling node data: {e}")
                # If unpickling fails, try decoding as UTF-8 directly
                try:
                    node_data_bytes = bytearray(node_data_raw) # Convert QByteArray to bytearray
                    node_name = node_data_bytes.decode('utf-8')
                    self.node_list_widget.addItem(node_name)
                    print(f"Added item to list (decoded): {node_name}")
                except UnicodeDecodeError as decode_e:
                    print(f"Error decoding as UTF-8: {decode_e}")

            event.acceptProposedAction()
        else:
            print("Drop occurred with incorrect format")
            event.ignore()

    def process_node_data(self, node_data):
        # Not needed
        return []
        
    def select_node_on_click(self, item):
     
        
        for other_node in NodegraphAPI.GetAllNodes():
                    NodegraphAPI.SetNodeSelected(other_node, False)
        
        node_name = item.text()
        node = NodegraphAPI.GetNode(node_name)
        NodegraphAPI.SetNodeSelected(node, True)
        

    def focus_on_node(self, item):
        """
        When a node name in the list is double-clicked, this function
        attempts to find the corresponding node in the current Node Graph
        and sets the view focus to it.
        """
        node_name = item.text()
        node = NodegraphAPI.GetNode(node_name)
        NodegraphAPI.SetNodeSelected(node, True)

        all_tabs = UI4.App.Tabs.GetAllTabs()
        node_graph_tab = None
        
        UI4.App.Tabs.FindTopTab('Node Graph').frameSelection()
        

PluginRegistry = [
    ('KatanaPanel', 2.0, 'QuickNode', MyCustomTab),
    ('KatanaPanel', 2.0, 'Custom/QuickNode', MyCustomTab),
]
