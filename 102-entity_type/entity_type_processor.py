import csv


class entity_type_processor:
    line_start = 1  # 默认为1，因为第一行是干扰信息
    line_end = 31254270  # 最大值31254270
    entity_output_addr = '../data/entity.csv'
    entity_input_addr = '../data/entity_backup.csv'

    ttl_addr = '../data/instance_types_transitive_en.ttl'
    entity_to_types = {}
    print_interval = 100000
    line_index = 0

    def __init__(self):
        self.input_entity()
        self.input(create_entity=False)
        self.output()

    def input_entity(self):
        with open(self.entity_input_addr, encoding='utf-8') as f:
            lines = csv.reader(f)
            for line in lines:
                entity = line[0]
                self.entity_to_types[entity] = []
        # print(len(self.entity_to_types.keys()))
        # print('Aquarius (constellation)' in self.entity_to_types.keys())

    def website_to_keyword(self, website):
        division = website[1:-1].split('/')
        keyword = division[-1]
        if keyword == '':
            keyword = division[-2]
        keyword = keyword.replace('"', '')
        keyword = keyword.replace(',', '')
        keyword = keyword.replace('_', ' ')
        old_keywords = keyword.split(' ')
        new_keywords = []
        for key in old_keywords:
            if key != '' and not key.isdigit():
                new_keywords.append(key)
        keyword = ' '.join(new_keywords)
        return keyword

    def get_clear_type(self, raw_type):
        if raw_type == '':
            return ''
        if 'Q' in raw_type:
            division = raw_type.split('Q')
            if len(division) == 2 and division[1].isdigit():
                return ''
        if '#' in raw_type:
            division = raw_type.split('#')
            if len(division) == 2:
                raw_type = division[1]
        if raw_type == 'Thing' or raw_type == 'Agent':
            return ''
        return raw_type


    def process_line(self, line):
        PREFIX = 'http://dbpedia.org/resource/'
        websites = line.strip().split(' ')
        if len(websites) != 4:  # 最后还有一个 .，所以不是3
            print('文件行不符合三元组格式要求')
            print(self.line_index)
            print(line)
            print(len(websites))
            exit(1)
        for website in websites[:3]:
            if website[0] != '<' or website[-1] != '>':
                print('网址不符合格式规范')
                print(websites)
                print(website)
                exit(2)
        entity_website = websites[0].replace('"', '')[1:-1]
        entity = ''
        if len(entity_website) > len(PREFIX) and \
                entity_website[:len(PREFIX)] == PREFIX:
            entity = self.website_to_keyword(websites[0])
        raw_type = self.website_to_keyword(websites[2])
        type_ = self.get_clear_type(raw_type)
        return entity, type_

    def input(self, create_entity=True):
        with open(self.ttl_addr, 'r', encoding='utf8') as r:
            for i in range(self.line_start):
                r.readline()
            for self.line_index in range(self.line_start,self.line_end):
                line = r.readline()
                entity, type_ = self.process_line(line)
                if create_entity and entity != '' and entity not in self.entity_to_types.keys():
                    self.entity_to_types[entity] = []
                if entity != '' and type_ != '' and entity in self.entity_to_types.keys() \
                        and type_ not in self.entity_to_types[entity]:
                        self.entity_to_types[entity].append(type_)
                if self.line_index % self.print_interval == 0:
                    print(self.line_index)

    def output(self):
        with open(self.entity_output_addr, 'w', newline='', encoding='utf8') as w:
            writer = csv.writer(w)
            # writer = csv.writer(w, delimiter='/')
            for entity, types in self.entity_to_types.items():
                if len(types) == 0:
                    writer.writerow([entity, 'None'])
                else:
                    writer.writerow([entity,'|'.join(types)])


entity_type_processor()