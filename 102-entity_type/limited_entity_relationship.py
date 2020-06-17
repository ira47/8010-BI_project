import csv
class limited_entity_relationship:
    entity_info_addr = '../data/entity_info.csv'
    entity_type_addr = '../data/entity.csv'
    relationship_addr= '../data/relationship.csv'

    normal_addr = '../data/new/normal.csv'
    company_addr = '../data/new/company.csv'
    normal_normal_addr = '../data/new/normal_normal.csv'
    normal_company_addr = '../data/new/normal_company.csv'
    company_normal_addr = '../data/new/company_normal.csv'
    company_company_addr = '../data/new/company_company.csv'

    entity_to_type = {}
    entity_to_info = {}

    def __init__(self):
        self.output_entity()
        self.output_relationship()

    def output_entity(self):
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
                self.entity_to_type[entity] = type_
        print(len(self.entity_to_type.keys()))
        with open(self.company_addr, 'w', newline='', encoding='utf8') as w1:
            with open(self.normal_addr, 'w', newline='', encoding='utf8') as w2:
                company_writer = csv.writer(w1)
                normal_writer = csv.writer(w2)
                for entity,type_ in self.entity_to_type.items():
                    if entity in self.entity_to_info.keys():
                        info = self.entity_to_info[entity]
                        line = [entity,type_] + info
                        company_writer.writerow(line)
                    else:
                        line = [entity,type_]
                        normal_writer.writerow(line)
        print('finish 1')


    def output_relationship(self):
        with open(self.relationship_addr, encoding='utf-8') as f:
            with open(self.normal_normal_addr, 'w', newline='', encoding='utf8') as w1:
                with open(self.normal_company_addr, 'w', newline='', encoding='utf8') as w2:
                    with open(self.company_normal_addr, 'w', newline='', encoding='utf8') as w3:
                        with open(self.company_company_addr, 'w', newline='', encoding='utf8') as w4:
                            normal_normal_writer = csv.writer(w1)
                            normal_company_writer = csv.writer(w2)
                            company_normal_writer = csv.writer(w3)
                            company_company_writer = csv.writer(w4)
                            lines = csv.reader(f)
                            for index,line in enumerate(lines):
                                a = line[0]
                                b = line[2]
                                if a in self.entity_to_info.keys():
                                    if b in self.entity_to_info.keys():
                                        company_company_writer.writerow(line)
                                    else:
                                        company_normal_writer.writerow(line)
                                else:
                                    if b in self.entity_to_info.keys():
                                        normal_company_writer.writerow(line)
                                    else:
                                        normal_normal_writer.writerow(line)
                                if index % 100000 == 0:
                                    print(index)

limited_entity_relationship()