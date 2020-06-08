import csv

class entity_website_pair:
    line_start = 1 # 默认为1，因为第一行是干扰信息
    line_end = 10000 # 最大值18746175
    entity_output_addr = '../data/entity_website_pair_1w.csv'

    ttl_addr = '../data/mappingbased_objects_en.ttl'
    entity_set = {}
    print_interval = 100000

    def __init__(self):
        self.input()
        self.output()
    
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
        PREFIX = 'http://dbpedia.org/resource/'
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
        a_website = websites[0].replace('"','')[1:-1]
        b_website = websites[2].replace('"','')[1:-1]
        a = ''
        b = ''
        if len(a_website) > len(PREFIX) and \
            a_website[:len(PREFIX)] == PREFIX:
            a = self.website_to_keyword(websites[0])
        if len(b_website) > len(PREFIX) and \
            b_website[:len(PREFIX)] == PREFIX:
            b = self.website_to_keyword(websites[2])
        return a,b,a_website,b_website

    def input(self):
        with open(self.ttl_addr,'r',encoding='utf8') as r:
            for i in range(self.line_start):
                r.readline()
            for line_index in range(self.line_end-self.line_start):
                line = r.readline()
                a,b,a_website,b_website = self.process_line(line)
                if a != '' and a_website != '':
                    if a not in self.entity_set.keys():
                        self.entity_set[a] = [a_website]
                    elif a_website not in self.entity_set[a]:
                        self.entity_set[a].append(a_website)
                if b != '' and b_website != '':
                    if b not in self.entity_set.keys():
                        self.entity_set[b] = [b_website]
                    elif b_website not in self.entity_set[b]:
                        self.entity_set[b].append(b_website)
                if line_index % self.print_interval == 0:
                    print(line_index)


    def output(self):
        with open(self.entity_output_addr, 'w',newline='', encoding='utf8') as w:
            writer = csv.writer(w,delimiter='|')
            for entity,websites in self.entity_set.items():
                # writer.writerow([entity,len(websites),websites])
                writer.writerow([websites[0]])

entity_website_pair()