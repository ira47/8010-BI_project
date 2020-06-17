import csv
class limited_entity_relationship:
    entity_info_addr = '../data/entity_info.csv'
    entity_type_addr = '../data/entity.csv'
    relationship_addr = '../data/relationship.csv'

    output_entity_addr = '../data/company_entity.csv'
    output_relationship_addr = '../data/company_relationship.csv'

    entity_to_type = {}
    entity_to_info = {}

    def __init__(self):
        self.read_type_and_info()
        self.output_entity()
        self.output_relationship()

    def read_type_and_info(self):
        with open(self.entity_info_addr, encoding='utf-8') as f:
            lines = csv.reader(f)
            for line in lines:
                entity = line[0]
                info = line[1:]
                self.entity_to_info[entity] = info
        print(len(self.entity_to_info.keys()))
        with open(self.entity_type_addr, encoding='utf-8') as f:
            lines = csv.reader(f)
            for line in lines:
                entity = line[0]
                type_ = line[1]
                if entity in self.entity_to_info.keys():
                    self.entity_to_type[entity] = type_
        print(len(self.entity_to_type.keys()))

    def output_entity(self):
        with open(self.output_entity_addr, 'w', newline='', encoding='utf8') as w:
            writer = csv.writer(w)
            for entity,type_ in self.entity_to_type.items():
                info = self.entity_to_info[entity]
                line = [entity,type_] + info
                writer.writerow(line)

    def output_relationship(self):
        with open(self.relationship_addr, encoding='utf-8') as f:
            with open(self.output_relationship_addr, 'w', newline='', encoding='utf8') as w:
                writer = csv.writer(w)
                lines = csv.reader(f)
                for index,line in enumerate(lines):
                    a = line[0]
                    b = line[2]
                    if a in self.entity_to_type.keys() and \
                        b in self.entity_to_type.keys():
                        writer.writerow(line)
                    if index % 100000 == 0:
                        print(index)

limited_entity_relationship()