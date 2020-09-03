import os
import logging
import nx.nxfile as nxfile
from nx.nxfileset import NXFileSet


class MapNx:

    """ Helper class to get values from a map nx file. """

    def __init__(self):
        self.file = NXFileSet()

    def open(self, file):
        # Check if file exists
        if not os.path.exists(file):
            logging.warning(f'{file} does not exist')
            return
        try:
            # Open nx file
            self.file.load(file)
        except:
            logging.exception(f'Unable to open {file}')

    def get_map_nodes(self):
        map_nodes = {}
        for i in range(0, 9):
            map_digit = self.file.resolve(f'Map/Map{i}')
            if not map_digit:
                continue
            for child in map_digit.getChildren():
                map_nodes[child.name] = child.value
        return map_nodes

    def get_map_node(self, map_id):
        img = f'Map/Map{map_id[0:1]}/{map_id}.img'
        return self.file.resolve(img)

    def get_info_data(self, map_id):
        info = {}
        img = f'Map/Map{map_id[0:1]}/{map_id}.img'
        # Get map node
        map_node = self.file.resolve(img)
        if not map_node:
            return None
        info_node = map_node.getChild('info')
        for child in info_node.getChildren():
            info[child.name] = child.value
        return info

    def get_minimap_data(self, map_id):
        minimap = {}
        img = f'Map/Map{map_id[0:1]}/{map_id}.img'
        # Get map node
        map_node = self.file.resolve(img)
        if not map_node:
            return None
        # Get the current minimap node
        minimap_node = map_node.getChild('miniMap')
        if not minimap_node:
            return None
        for child in minimap_node.getChildren():
            if child.name == 'canvas':
                minimap[child.name] = (child.width, child.height)
            else:
                minimap[child.name] = child.value
        return minimap

    def get_background_data(self, map_id):
        back = []
        img = f'Map/Map{map_id[0:1]}/{map_id}.img'
        # Get map node
        map_node = self.file.resolve(img)
        if not map_node:
            return None
        # Get the current back node
        back_node = map_node.getChild('back')
        if not back_node:
            return None
        # Get values
        for array_node in back_node.getChildren():
            data = {'name': array_node.name}
            for child in array_node.getChildren():
                data[child.name] = child.value
            back.append(data)
        return back

    def get_layer_data(self, map_id, index):
        layer = {}
        img = f'Map/Map{map_id[0:1]}/{map_id}.img'
        # Get map node
        map_node = self.file.resolve(img)
        if not map_node:
            return None
        # Get the current layer
        layer_node = map_node.getChild(str(index))
        if not layer_node:
            return None
        # Get info for this layer
        info = {}
        info_node = layer_node.getChild('info')
        for child in info_node.getChildren():
            info[child.name] = child.value
        # Get tiles for this layer
        tiles = []
        tile_node = layer_node.getChild('tile')
        for array_node in tile_node.getChildren():
            data = {'name': array_node.name}
            for child in array_node.getChildren():
                data[child.name] = child.value
            tiles.append(data)
        # Get objects for this layer
        objects = []
        object_node = layer_node.getChild('obj')
        for array_node in object_node.getChildren():
            data = {'name': array_node.name}
            for child in array_node.getChildren():
                data[child.name] = child.value
            objects.append(data)
        # Add layer
        layer = {'info': info, 'tile': tiles, 'obj': objects}
        return layer

    def get_portal_data(self, map_id):
        portal = []
        img = f'Map/Map{map_id[0:1]}/{map_id}.img'
        # Get map node
        map_node = self.file.resolve(img)
        if not map_node:
            return None
        # Get the current back node
        portal_node = map_node.getChild('portal')
        if not portal_node:
            return None
        # Get values
        for array_node in portal_node.getChildren():
            data = {'name': array_node.name}
            for child in array_node.getChildren():
                data[child.name] = child.value
            portal.append(data)
        return portal

    def get_values(self, node):
        values = {}
        for child in node.getChildren():
            values[child.name] = child.value
        return values
