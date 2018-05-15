 # -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 09:00:14 2018

@author: yuzy
"""

import pymysql
sim = []
simid=[]
def readsql(sqlword):
    # 打开数据库连接
    db = pymysql.connect("localhost","root","123456","recommander" )
 
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # SQL 查询语句
    try:
        # 执行SQL语句
        cursor.execute(sqlword)
        # 获取所有记录列表
        results = cursor.fetchall()
        return results
    except:
        print ("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()

def isexisted(mid,movies):
    for row in movies:
        if(mid = row[1]):
            return row[2]
    return 0

#分词
def read_from_file(file_name):
    with open(file_name,"r") as fp:
        words = fp.read()
    return words
def stop_words(stop_word_file):
    words = read_from_file(stop_word_file)
    result = jieba.cut(words)
    new_words = []
    for r in result:
        new_words.append(r)
    return set(new_words)
def del_stop_words(words,stop_words_set):
#   words是已经切词但是没有去除停用词的文档。
#   返回的会是去除停用词后的文档
    result = jieba.cut(words)
    new_words = []
    for r in result:
        if r not in stop_words_set:
            new_words.append(r)
    return new_words
def get_all_vector(file_path,stop_words_set):
    names = [ os.path.join(file_path,f) for f in os.listdir(file_path) ]
    posts = [ open(name).read() for name in names ]
    docs = []
    word_set = set()
    for post in posts:
        doc = del_stop_words(post,stop_words_set)
        docs.append(doc)
        word_set |= set(doc)
        #print len(doc),len(word_set)

    word_set = list(word_set)
    docs_vsm = []
    #for word in word_set[:30]:
        #print word.encode("utf-8"),
    for doc in docs:
        temp_vector = []
        for word in word_set:
            temp_vector.append(doc.count(word) * 1.0)
        #print temp_vector[-30:-1]
        docs_vsm.append(temp_vector)

    docs_matrix = np.array(docs_vsm)
column_sum = [ float(len(np.nonzero(docs_matrix[:,i])[0])) for i in range(docs_matrix.shape[1]) ]
column_sum = np.array(column_sum)
column_sum = docs_matrix.shape[0] / column_sum
idf =  np.log(column_sum)
idf =  np.diag(idf)
# 请仔细想想，根绝IDF的定义，计算词的IDF并不依赖于某个文档，所以我们提前计算好。
# 注意一下计算都是矩阵运算，不是单个变量的运算。
for doc_v in docs_matrix:
    if doc_v.sum() == 0:
        doc_v = doc_v / 1
    else:
        doc_v = doc_v / (doc_v.sum())
    tfidf = np.dot(docs_matrix,idf)
    return names,tfidf

#聚类，可用K-means
    
"""know user 288's rating matrixs"""
sqlword = "SELECT * FROM ratings WHERE id = 288 "
results = readsql(sqlword)
for row in results:
    mid=row[1]
    score=row[2]
    print(mid,score)

"""select every user"""
sqlword_1 = "SELECT DISTINCT id FROM ratings" 
users=readsql(sqlword_1)
for row in users:
    tgtmovie = []
    tgtscore_test = []
    tgtscore_main = []
    id=row[0]
    sqlword_x = "SELECT * FROM ratings WHERE id =" + id
    movies = readsql(sqlword)
    for row in movies:
        sc = isexisted(row[1],results)
        if(sc!=0):
            tgtmovie.append(row[1])
            tgtscore_test.append(row[2])
            tgtscore_main.append(sc)
    #计算相似度
