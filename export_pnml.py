import uuid
import xml.dom.minidom


class PNML():
    def __init__(self, net_id, net_name):
        self.net_id = net_id
        self.net_name = net_name

        self.place = []
        self.transition_list = []
        self.transition = []
        self.transition_dict = {}  # the transition could occur just one time in pn
        self.arc = []

        self.get_pnml_base()

    def get_pnml_base(self):

        self.doc = xml.dom.minidom.Document()
        self.pnml = self.doc.createElement('pnml')
        self.net = self.doc.createElement('net')

        self.net.setAttribute('id', self.net_id)
        self.net.setAttribute('type', "http://www.yasper.org/specs/epnml-1.1")

        name = self.doc.createElement('name')
        text = self.doc.createElement('text')
        text.appendChild(self.doc.createTextNode(self.net_name))
        name.appendChild(text)

        self.net.appendChild(name)
        self.pnml.appendChild(self.net)
        self.doc.appendChild(self.pnml)

    def get_pnml_refresh(self):
        self.pnml.appendChild(self.net)
        self.doc.appendChild(self.pnml)

    def add_place(self, input_transition, output_transition):
        place_id = str(uuid.uuid4())
        inter_place = self.doc.createElement('place')
        inter_place.setAttribute('id', place_id)

        name = self.doc.createElement('name')
        text = self.doc.createElement('text')

        inter = ''
        for i in input_transition:
            inter = inter + ',' + str(i)
        inter = inter[1:]
        input_transition_str = '[%s]' % inter

        inter = ''
        for i in output_transition:
            inter = inter + ',' + str(i)
        inter = inter[1:]
        output_transition_str = '[%s]' % inter

        text_node = '(%s,%s)' % (input_transition_str, output_transition_str)
        text.appendChild(self.doc.createTextNode(text_node))
        name.appendChild(text)
        inter_place.appendChild(name)

        self.net.appendChild(inter_place)

        inter = {'inp': input_transition, 'outp': output_transition, 'id': place_id, 'inp_len': len(input_transition),
                 'outp_len': len(output_transition), 'name': text_node}

        self.place.append(inter)
        inter = list(set(self.transition_list + input_transition + output_transition))
        self.transition_list = inter

    def get_transition(self):
        self.transition = []
        self.transition_dict = {}

        for i in self.transition_list:
            transition_id = str(uuid.uuid4())
            inter = {}
            inter['id'] = transition_id
            inter['name'] = i

            inter_transition = self.doc.createElement('transition')
            inter_transition.setAttribute('id', transition_id)

            name = self.doc.createElement('name')
            text = self.doc.createElement('text')

            text.appendChild(self.doc.createTextNode(i))
            name.appendChild(text)
            inter_transition.appendChild(name)
            self.net.appendChild(inter_transition)

            self.transition.append(inter)
            self.transition_dict[i] = transition_id

    def get_arc_xml(self):
        for i in self.arc:
            arc = self.doc.createElement('arc')
            arc.setAttribute('id', i['id'])
            arc.setAttribute('source', i['source'])
            arc.setAttribute('target', i['target'])

            name = self.doc.createElement('name')
            text = self.doc.createElement('text')
            text.appendChild(self.doc.createTextNode('1'))
            name.appendChild(text)
            arc.appendChild(name)

            arctype = self.doc.createElement('arctype')
            text = self.doc.createElement('text')
            text.appendChild(self.doc.createTextNode('normal'))
            arctype.appendChild(text)
            arc.appendChild(arctype)

            self.net.appendChild(arc)

    def get_arc(self):
        self.arc = []
        for i in self.place:
            # for input transition -> place
            for j in i['inp']:
                inter = {}
                inter['source'] = self.transition_dict[j]
                inter['target'] = i['id']
                inter['id'] = str(uuid.uuid4())
                self.arc.append(inter)

            # for output   place -> transition
            for j in i['outp']:
                inter = {}
                inter['source'] = i['id']
                inter['target'] = self.transition_dict[j]
                inter['id'] = str(uuid.uuid4())
                self.arc.append(inter)
        self.get_arc_xml()

    def get_np_info(self):
        self.get_transition()
        self.get_arc()
        return self.place, self.transition, self.arc

    def get_xml_string(self):
        self.get_transition()
        self.get_arc()
        self.get_pnml_refresh()
        xml_string = self.doc.toprettyxml(indent='\t', encoding='ISO-8859-1')
        return xml_string.decode()


def gain_pnml(name,places):
    pnml = PNML(str(uuid.uuid4()),name)

    for i in places:
        pnml.add_place(i['input'], i['output'])

    pnml.get_pnml_refresh()
    pnml_string = pnml.get_xml_string()

    return pnml_string


# usage example
places = [{'input': ['a'], 'output': ['b']}, {'input': ['a','b'], 'output': ['c']}, {'input': ['c'], 'output': ['d']},
         {'input': ['b'], 'output': ['d']}]

pnml_string = gain_pnml('example',places)
pnml_file = open('example.pnml', 'w')
pnml_file.write(pnml_string)
