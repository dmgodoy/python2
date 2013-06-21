#!/usr/bin/python

from lxml import etree

source = """
<root>
<parent>
    <ID>1</ID>
    <child1>Value1</child1>
    <child2>value11</child2>
    <child3>
       <subchild>value111</subchild>
    </child3>
</parent>
<parent>
    <ID>2</ID>
    <child1>value2</child1>
    <child2>value22</child2>
    <child2>value333</child2>
</parent>
<parent>
    <ID>3</ID>
    <child1>value3</child1>
    <child2>value33</child2>
</parent>
<parent>
    <ID>4</ID>
    <child1>value4</child1>
    <child2>value44</child2>
</parent>
</root>
"""

document = etree.fromstring(source)
inserts = []

id_number = 3

for parent in document.findall('parent'):
    insert = {}
    cont = 0
    for element in parent.iterdescendants():
        if element.tag == 'ID':
            if element.text == str(id_number):
                cont = 1
        if element.getchildren() == []:
            insert[element.tag] = element.text
    if cont:
        inserts.append(insert)

print inserts

