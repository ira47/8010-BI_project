import csv

class ttl_preprocessor:
    ttl_addr = '../data/mappingbased_objects_en.ttl'
    relationship_output_addr = '../data/relationship.csv'
    entity_output_addr = '../data/entity.csv'
    line_start = 1 # 第一行是干扰信息
    line_end = 1000000 # 最大值18785001，是LTF Viewer显示的最后一行-1，因为它从1开始
    entity_set = set()
    print_interval = 10000

    def get_entity_and_relationship(self,line):
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
        a = websites[0][1:-1].split('/')[-1]
        to = websites[1][1:-1].split('/')[-1]
        b = websites[2][1:-1].split('/')[-1]
        return a,to,b

    def __init__(self):
        with open(self.ttl_addr,'r',encoding='utf8') as r:
            with open(self.relationship_output_addr,'w',newline='',encoding='utf8') as w:
                writer = csv.writer(w)
                for i in range(self.line_start):
                    r.readline()
                for line_index in range(self.line_end-self.line_start):
                    line = r.readline()
                    a,to,b = self.get_entity_and_relationship(line)
                    if a not in self.entity_set:
                        self.entity_set.add(a)
                    if b not in self.entity_set:
                        self.entity_set.add(b)
                    writer.writerow([a,to,b])
                    if line_index % self.print_interval == 0:
                        print(line_index)
        with open(self.entity_output_addr,'w',newline='',encoding='utf8') as w:
            writer = csv.writer(w)
            for entity in self.entity_set:
                writer.writerow([entity])




ttl_preprocessor()