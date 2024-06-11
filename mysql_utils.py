import pymysql

db = pymysql.connect(host='localhost',
                user='root',
                password='test_root',
                database='academicworld',
                charset='utf8mb4',
                port=3306,
                cursorclass=pymysql.cursors.DictCursor)


# R10: adding constraint
def r10_constraint():
    with db.cursor() as cursor:
        # making faculty not null.
        try:
 #           cursor.execute('alter table faculty drop constraint faculty_chk_5')
            cursor.execute('ALTER TABLE faculty add constraint name_with_at_violation check ( name not like "%@%" )')
        except Exception as e: print('error constraint:', e); return
        db.commit()

        print('successfully added constraint for Faculty on name column.')

r10_constraint()

# R11: creating_view
def r11_view():
    with db.cursor() as cursor:
        try:
            sql = 'DROP VIEW AI_Professors_by_publication'
            cursor.execute(sql)
            db.commit()
        except:
            print('Mysql table AI_Professors_by_publication do not exist. Nothing to drop;')
            pass
        sql ='CREATE VIEW AI_Professors_by_publication as SELECT f.name as faculty, u.name as university, count(*) as publication_count FROM ' + \
	'faculty f left join faculty_publication p on f.id = p.faculty_id left join university u ' + \
	'on f.university_id = u.id where f.research_interest like "%deep learning%" group by f.name, u.name order by publication_count desc'
        cursor.execute(sql)
        db.commit()
        print('Mysql view AI_Professors_by_publication has created!')
r11_view()

def get_AI_faculty():
    with db.cursor() as cursor:
        cursor.execute('select * from AI_Professors_by_publication limit 10')
        return cursor.fetchall()
        
# R12: creating index
def r12_create_index():
    with db.cursor() as cursor:
        try:
            sql = 'DROP INDEX faculty_name_index ON faculty'
            cursor.execute(sql)
            db.commit()
        except:
            print('Mysql: the index do not exist yet. Nothing to clean')
            pass

        sql = 'CREATE INDEX faculty_name_index ON faculty (email)'
        cursor.execute(sql)
        print('Mysql: successfully added index on (email) for faculty table')
r12_create_index()

def get_university(input_value):
    with db.cursor() as cursor:
        sql = 'select id, name from university where name like "%' + input_value + '%";'
        cursor.execute(sql)
        result = cursor.fetchall()
        return result


def get_keyword_by_year(input_value):
    with db.cursor() as cursor:
        
        sql = 'Select name, count ' \
              'From (Select keyword_id, count(publication_id) as count ' \
              'from publication_keyword, publication where publication.year = ' \
              + input_value + ' and publication.id = publication_keyword.publication_id ' \
                'group by keyword_id order by count desc limit 15)  k, keyword where keyword.id = k.keyword_id;';
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

def get_keyword_trend(input_value):
    with db.cursor() as cursor:
        sql = 'select p.year AS year, COUNT(p.id) AS count ' \
             'FROM publication p JOIN publication_keyword pk ' \
             'ON p.id = pk.publication_id JOIN keyword k ' \
             'ON pk.keyword_id = k.id WHERE k.name like "%' + input_value + \
             '%" GROUP BY p.year ORDER BY year ASC;'

        cursor.execute(sql)
        result = cursor.fetchall()
        return result

#r6_insert
def insert_professor(inp, debug=False):
    with db.cursor() as cursor:
        name, position, ri, email = inp.split(',')
        cursor.execute('SELECT * FROM faculty WHERE email = "' + email +'"')
        r = cursor.fetchall()
        if len(r) > 0:
            return 'Faculty already exists. Abort Insertion.'
        cursor.execute('select max(id) from faculty')
        r = cursor.fetchall()
        try:
            sql = 'INSERT INTO faculty (id, name, position, research_interest, email) VALUES ("{}", "{}", "{}", "{}", "{}")'.format(r[0]['max(id)']+1, name, position,ri, email)
            result = cursor.execute(sql)
            db.commit()
            print('result is', result)
            return 'faculty added!' if result == 1 else 'failed'
        except Exception as e:
            return str(e) + ' (name may contain @, or name is None)'
#r6_delete
def delete_professor_by_email(email):
    with db.cursor() as cursor:
        sql = 'select * from faculty where email = "' + email + '"'
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            return 'There is no record found. Abort deletion.'
        
        sql = 'DELETE FROM faculty WHERE email = "' + email + '"'
        cursor.execute(sql)
        db.commit()
        print('Found records!')
        for r in result:
             print(r)
        return 'Records are found and deletion succeeded.'

if __name__ == '__main__':
    print(get_keyword_Trend('users'))
