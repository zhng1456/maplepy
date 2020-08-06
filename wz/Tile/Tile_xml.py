import os
import xml.etree.ElementTree as ET


class Tile_xml:

    def __init__(self):
        self.root = None
        self.name = None
        self.info = None
        self.objects = None

    def open(self, file):
        if self.root:
            print('{} already opened.'.format(file))
            return
        if not os.path.isfile(file):
            print('{} does not exist.'.format(file))
            return
        self.root = ET.parse(file).getroot()

    def parse_root(self):
        if not self.root:
            print('No file opened.')
            return
        try:
            info = {}
            objects = {}
            # Parse xml
            for child in self.root:
                if child.attrib.get('name') == 'info':
                    info = self.parse_info(child)
                else:
                    object_data = self.parse_canvas_array(child)
                    objects[child.attrib.get('name')] = object_data
            # Set variables
            self.name = self.root.get('name')
            self.info = info
            self.objects = objects
        except:
            print('Error while parsing.')

    def parse_info(self, info):
        item = {}
        value_tags = ['int', 'string']
        for value in info:
            if value.tag in value_tags:
                item[value.get('name')] = value.get('value')
        return item

    def parse_tags(self, tags):
        items = {}
        for child in tags:
            items[child.get('name')] = self.parse_item_array(child)
        return items

    def parse_item_array(self, array):
        items = []
        for child in array:
            items.append(self.parse_canvas_array(child))
        return items

    def parse_canvas_array(self, canvases):
        items = []
        for child in canvases:
            items.append(self.parse_canvas(child))
        return items

    def parse_canvas(self, canvas):
        item = {}
        vector_tags = ['vector']
        value_tags = ['int', 'string']
        # Canvas values
        item['name'] = canvas.get('name')
        item['width'] = canvas.get('width')
        item['height'] = canvas.get('height')
        # Inner items
        for value in canvas:
            if value.tag in vector_tags:
                item['x'] = value.get('x')
                item['y'] = value.get('y')
            if value.tag in value_tags:
                item[value.get('name')] = value.get('value')
        return item
