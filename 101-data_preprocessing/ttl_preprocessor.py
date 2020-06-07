import csv

class ttl_preprocessor:
    line_start = 1 # 默认为1，因为第一行是干扰信息
    line_end = 18746175 # 最大值18746175
    relationship_output_addr = '../data/relationship.csv'
    entity_output_addr = '../data/entity.csv'

    ttl_addr = '../data/mappingbased_objects_en.ttl'
    entity_input_addr = '../data/entity_old.csv'
    entity_set = set()
    print_interval = 100000

    def __init__(self):
        # self.entity_set = self.get_entity_info()
        self.output_relationship()
        self.output_entity(only_need_new=False)
    
    def website_to_keyword(self,website):
        division = website[1:-1].split('/')
        keyword = division[-1]
        if keyword == '':
            keyword = division[-2]
        keyword = keyword.replace('"','')
        keyword = keyword.replace(',','')
        keyword = keyword.replace('_', ' ')
        old_keywords = keyword.split(' ')
        new_keywords = []
        for key in old_keywords:
            if key != '' and not key.isdigit():
                new_keywords.append(key)
        keyword = ' '.join(new_keywords)
        return keyword
        
    def process_line(self,line):
        websites = line.strip().split(' ')
        if len(websites) != 4: # 最后还有一个 .，所以不是3
            print('文件行不符合三元组格式要求')
            print(line)
            print(len(websites))
            exit(1)
        for website in websites[:3]:
            if website[0] != '<' or website[-1] != '>':
                print('网址不符合格式规范')
                print(websites)
                print(website)
                exit(2)
        a = self.website_to_keyword(websites[0])
        to = self.website_to_keyword(websites[1])
        b = self.website_to_keyword(websites[2])
        return a,to,b

    def output_relationship(self):
        with open(self.ttl_addr,'r',encoding='utf8') as r:
            with open(self.relationship_output_addr,'w',newline='',encoding='utf8') as w:
                writer = csv.writer(w)
                for i in range(self.line_start):
                    r.readline()
                for line_index in range(self.line_end-self.line_start):
                    line = r.readline()
                    a,to,b = self.process_line(line)
                    if a != '' and a not in self.entity_set:
                        self.entity_set.add(a)
                    if b != '' and b not in self.entity_set:
                        self.entity_set.add(b)
                    if a!='' and to!='' and b!='' and a!=b:
                        writer.writerow([a,to,b])
                    if line_index % self.print_interval == 0:
                        print(line_index)


    def get_entity_info(self,read_old=False):
        entity_set = set()
        if read_old:
            addr = self.entity_input_addr
        else:
            addr = self.entity_output_addr
        with open(addr, 'r', encoding='utf8') as r:
            for line in r.readlines():
                entity = line.strip()
                # if entity[0] == '"' and entity[-1] == '"':
                #     entity = entity[1:-1]
                entity_set.add(entity)
        # print('Sandyford,_Newcastle_upon_Tyne' in self.entity_set)
        return entity_set

    def output_entity(self,only_need_new=False):
        old_entity = set()
        if only_need_new:
            old_entity = self.get_entity_info(read_old=True)
        with open(self.entity_output_addr, 'w', newline='', encoding='utf8') as w:
            writer = csv.writer(w)
            for entity in self.entity_set:
                if only_need_new and entity in old_entity:
                    continue
                writer.writerow([entity])

ttl_preprocessor()