import csv


class company_website_pair:
    line_start = 1  # 默认为1，因为第一行是干扰信息
    line_end = 31254270  # 最大值31254270
    entity_output_addr = '../data/company_to_websites.csv'

    entity_input_addr = '../data/entity.csv'
    ttl_addr = '../data/instance_types_transitive_en.ttl'
    company_to_websites = {}
    print_interval = 100000
    line_index = 0

    def __init__(self):
        self.input_entity()
        self.input()
        self.output()

    def is_company(self, entity, type_):
        if 'Company' in entity or 'Company' in type_:
            return True
        elif 'company' in entity or 'company' in type_:
            return True
        return False

    def input_entity(self):
        with open(self.entity_input_addr, encoding='utf-8') as f:
            lines = csv.reader(f)
            for line in lines:
                entity = line[0]
                type_ = line[1]
                if self.is_company(entity, type_):
                    self.company_to_websites[entity] = []
        print(len(self.company_to_websites.keys()))
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
        return entity, entity_website

    def input(self):
        with open(self.ttl_addr, 'r', encoding='utf8') as r:
            for self.line_index in range(self.line_start):
                r.readline()
            for self.line_index in range(self.line_start,self.line_end):
                line = r.readline()
                entity, entity_website = self.process_line(line)
                if entity in self.company_to_websites.keys() and \
                    entity_website not in self.company_to_websites[entity]:
                    self.company_to_websites[entity].append(entity_website)
                if self.line_index % self.print_interval == 0:
                    print(self.line_index)

    def output(self):
        with open(self.entity_output_addr, 'w', newline='', encoding='utf8') as w:
            writer = csv.writer(w)
            for company, websites in self.company_to_websites.items():
                if len(websites) >= 1:
                    if len(websites) >= 2:
                        print(company,websites)
                    writer.writerow([company, websites[0]])


company_website_pair()