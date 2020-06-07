# import pymssql
import csv
import datetime

file = open("d://product.csv", "r", newline='',encoding='gb18030')
source = csv.reader(file,delimiter=',', quotechar='"')

start = datetime.datetime.now()
total_write = 0

productId = ''
title = ''
actors = ''
directors = ''
actor = []
director = []
price = 0.0
genre = []
language = []
format_ = ''
studio = ''
classification = ''
running_time = 0
publication_date_send = ''
release_date_send = ''
p_year = ''
p_month = ''
p_season = ''
p_weekday = ''
r_year = ''
r_month = ''
r_season = ''
r_weekday = ''

productCsv = open('productsCsv.csv','w',newline='',encoding='gb18030')
staffCsv = open('staffCsv.csv','w',newline='',encoding='gb18030')
actCsv = open('actCsv.csv','w',newline='',encoding='gb18030')
directCsv = open('directCsv.csv','w',newline='',encoding='gb18030')
product = csv.writer(productCsv)
staff = csv.writer(staffCsv)
act = csv.writer(actCsv)
direct = csv.writer(directCsv)

actorSet = set()
directorSet = set()


print("start")

for line in source:
    # 处理行
    productId = line[0].lstrip('0') # 790747324
    title = ''.join(line[1].split('\n'))
    actors = line[2]
    directors = line[3]

    # actor 和 director
    actor = line[2].split(',')
    if len(actor) == 1:
        actor = line[2].split('\n') # B000HWXRPQ
    else:
        for i in range(len(actor)): # B000HWY64M
            actor[i] = ''.join(actor[i].split('\n'))
    for i in range(len(actor)):
        actor[i] = actor[i].strip()

    director = line[3].split(',')
    if len(director) == 1:
        director = line[3].split('\n')
    else:
        for i in range(len(director)): # B001AQU7X8
            director[i] = ''.join(director[i].split('\n'))
    for i in range(len(director)): # B000Y0VU2S:修改方法：用excel去除错误
        director[i] = director[i].strip()

    if len(director) == 1:
        director = line[3].split('\n')
    if line[4] == '':
        price = ''
    else:
        price = (float)(line[4])
    
    genre = line[5]
    language = line[6]
    format_ = line[7]
    studio = line[8]
    classification = line[9]
    if line[10] == '':
        running_time = ''
    else:
        running_time = (int)(line[10])

    # 日期计算
    if line[11] == '':
        public_date = ''
        p_year = ''
        p_month = ''
        p_day = ''
        p_season = ''
        p_weekday = ''
    else:
        public_date = line[11]
        d = line[11].split('/')
        if len(d) == 1:
            d = line[11].split('-')
        p_year = d[0]
        p_month = d[1]
        p_day = d[2]
        publication_date = datetime.date(int(p_year),int(p_month),int(p_day))
        if p_month == 1 or p_month == 2 or p_month == 3:
            p_season = '1'
        if p_month == 4 or p_month == 5 or p_month == 6:
            p_season = '2'
        if p_month == 7 or p_month == 8 or p_month == 9:
            p_season = '3'
        else:
            p_season = '4'
        p_weekday = str(publication_date.weekday())

    if line[12] == '':
        release_date = ''
        r_year = ''
        r_month = ''
        r_day = ''
        r_season = ''
        r_weekday = ''
    else:
        release_date = line[12]
        d = line[12].split('/')
        if len(d) == 1:
            d = line[12].split('-')
        r_year = d[0]
        r_month = d[1]
        r_day = d[2]
        release_date = datetime.date(int(r_year),int(r_month),int(r_day))
        if r_month == 1 or r_month == 2 or r_month == 3:
            r_season = '1'
        if r_month == 4 or r_month == 5 or r_month == 6:
            r_season = '2'
        if r_month == 7 or r_month == 8 or r_month == 9:
            r_season = '3'
        else:
            r_season = '4'
        r_weekday = str(release_date.weekday())

    # actor和director
    if actor[0] != '':
        for a in actor:
            if a not in actorSet:
                actorSet.add(a)
            act.writerow([a,productId])
    if director[0] != '':
        for a in director:
            if a not in directorSet:
                directorSet.add(a)
            direct.writerow([a,productId])
    
    # 插入
    product.writerow([productId,title,price,format_,studio,classification,running_time,
        # actors,directors,public_date,release_date,
        public_date,release_date,
        p_year,p_month,p_day,p_season,p_weekday,r_year,r_month,r_day,r_season,r_weekday,
        language,genre])
    
    total_write += 1
    if total_write % 10000 == 0:
        print(total_write)

for a in actorSet:
    if a not in directorSet:
        staff.writerow([a])
for a in directorSet:
    staff.writerow([a])

end = datetime.datetime.now()
print(end-start)

file.close()
productCsv.close()
staffCsv.close()
actCsv.close()
directCsv.close()

