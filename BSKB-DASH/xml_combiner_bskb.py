from time import sleep
import xml.etree.ElementTree as ET

PARENT_1_FILE = "BSKBLive.xml"
PARENT_2_FILE = "dashboard_data.xml"
CHILD_FILE = "scorebug.xml"


#append parent files to child file repeatedly
def xmlCombine():
    list1 = ['title', 'goal', 'period', 'reverse', 'hBonus', 'vBonus']
    list2 = ['clock', 'clockmin', 'clocksec', 'playclock', 'Hscore', 'Vscore', 'quarter', 'qtrtext']
    while True:
        try:
            #read parent 1 file
            with open(PARENT_1_FILE, "r") as parent1:
                xml1 = parent1.read()
            
            #read parent 2 file
            with open(PARENT_2_FILE, "r") as parent2:
                xml2 = parent2.read()

            #parsse parent files
            root1 = ET.fromstring(xml1)
            root2 = ET.fromstring(xml2)

            #create root element for child
            childRoot = ET.Element("info")

            reverse_element = root2.find('.//reverse')
            reverse_flag = reverse_element is not None and reverse_element.text and reverse_element.text.strip() == '1'



            for element in list2:
                childElement = root1.find(f".//{element}")
                if childElement is not None:
                    if reverse_flag and element in ("Hscore", "Vscore"):
                        # Swap Hscore and Vscore
                        swapped_element_name = "Vscore" if element == "Hscore" else "Hscore"
                        swapped_element = root1.find(f".//{swapped_element_name}")
                        if swapped_element is not None:
                            swapped_element_copy = ET.Element(element)
                            swapped_element_copy.text = swapped_element.text
                            childRoot.append(swapped_element_copy)
                    else:
                        childRoot.append(childElement)

            for element in list1:
                if element is not None:
                    childElement = root2.find(element)
                    childRoot.append(childElement)

            childTree = ET.ElementTree(childRoot)

            childTree.write(CHILD_FILE)

            sleep(0.1)
        except Exception as e:
            print(f"Error {e}")
            sleep(0.1)

xmlCombine()
