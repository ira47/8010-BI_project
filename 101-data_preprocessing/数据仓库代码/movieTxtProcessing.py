# import pymssql
import csv
import datetime

startLine = 0
endLine = 10000000

file = open("d://movies.txt", "r", encoding = 'ISO-8859-1', errors = 'ignore')
count = 0
data = []
line = file.readline()
v_productId = " "
v_userId = " "
v_profileName = " "
v_comment_num = ''
v_helpfulness = " "
v_score = 0
v_time = " "
v_summary = " "
v_text = " "

start = datetime.datetime.now()
total_write = 0
userCsv = open('userCsv.csv','w',encoding = 'ISO-8859-1',newline='')
productCsv = open('productCsv.csv','w',encoding = 'ISO-8859-1',newline='')
reviewCsv = open('reviewCsv.csv','w',encoding = 'ISO-8859-1',newline='')
commentCsv = open('commentCsv.csv','w',encoding = 'ISO-8859-1',newline='')
hasCommentCsv = open('hasCommentCsv.csv','w',encoding = 'ISO-8859-1',newline='')
user = csv.writer(userCsv)
product = csv.writer(productCsv)
review = csv.writer(reviewCsv)
comment = csv.writer(commentCsv)
hasComment = csv.writer(hasCommentCsv)

userSet = set()
productSet = set()


print("start")

while line:
    if line =="\n" and count == 8:
        count = 0               #下一条数据记录
        total_write += 1
        if total_write > startLine:
        
            if v_userId not in userSet:
                userSet.add(v_userId)
                user.writerow([v_userId,v_profileName])
            if v_productId not in productSet:
                productSet.add(v_productId)
                product.writerow([v_productId])
            review.writerow([str(total_write),v_productId,v_userId,v_time,v_score,v_helpfulness,v_comment_num,v_summary,v_text])
            comment.writerow([v_userId,str(total_write)])
            hasComment.writerow([v_productId,str(total_write)])

            if total_write % 10000 == 0:
                print(total_write)
            if total_write == endLine:
                end = datetime.datetime.now()
                print(end-start)
                break
    elif total_write < startLine:
        count += 1
    else:
        line = line.strip('\n')
        if count == 0:
            if line[:19] == 'product/productId: ':
                v_productId = line[19:].lstrip('0')
            else:
                print("**********", count, "error", line)
                count = count - 1
        elif count == 1:
            if line[:15] == 'review/userId: ':
                v_userId = line[15:]
            else:
                v_productId = v_productId + line.lstrip('0')
                count = count - 1
        elif count == 2:
            if line[:20] == 'review/profileName: ':
                v_profileName = line[20:]
            else:
                v_userId = v_userId + line
                count = count - 1
        elif count == 3:
            if line[:20] == 'review/helpfulness: ':
                raw_helpfulness = line[20:]
                helpList = raw_helpfulness.split("/", 1)
                v_comment_num = helpList[1]
                v_helpfulness = helpList[0]
            else:
                v_profileName = v_profileName + line
                count = count - 1
        elif count == 4:
            if line[:14] == 'review/score: ':
                v_score = line[14:]
            else:
                v_helpfulness = v_helpfulness + line
                count = count -1
        elif count == 5:
            if line[:13] == 'review/time: ':
                v_time = line[13:]
            else:
                v_score = v_score + line
                count = count - 1
        elif count == 6:
            if line[:16] == 'review/summary: ':
                v_summary = line[16:]
            else:
                v_time = v_time + line
                count = count - 1
        elif count == 7:
            if line[:13] == 'review/text: ':
                v_text = line[13:]
            else:
                v_summary = v_summary + line
                count = count - 1
        else:
            v_text = v_text + line
            count = count - 1
        count = count + 1
    line = file.readline()
file.close()
userCsv.close()
productCsv.close()
reviewCsv.close()


# output2 = open("./productErrorOutput.txt", "w", encoding = "utf-8", errors = 'ignore')

# csvFile = open("product.csv", "r", encoding = "utf-8", errors = 'ignore')
# reader = csv.reader(csvFile)

# for row in reader:
#     line = []
#     for index, data in enumerate(row):
#         if index == 4 or index == 10:
#             if data == '':
#                 data = "NULL"
#             line.append(data)
#         else:
#             if data == '':
#                 data = "NULL"
#             else:
#                 data = "'" + transferContent(data) + "'"
#             line.append(data)
#     sql = "INSERT INTO product VALUES(%s, \n%s, \n%s, \n%s, \n%s, \n%s, \n%s, \n%s, \n%s, \n%s, \n%s, \n%s, \n%s                    )"\
#         %(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10], line[11], line[12])
#     try:
#         cursor.execute(sql)
#         connection.commit()
#     except:
#         # print(sql)
#         output2.write(sql)
#         output2.write('\n\n')
# csvFile.close()

