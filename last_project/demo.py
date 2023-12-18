import pymysql.cursors

# Establish a connection to the MySQL server
connection = pymysql.connect(host='localhost',
                            user='root',
                            password='',
                            db='Quiz',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

answer = 'your_answer'  # Set your answer

try:
    with connection.cursor() as cursor:
        # Insert a new record
        sql = f"INSERT INTO `moning` (`Quiz_ans`) VALUES ('{answer}')"
        cursor.execute(sql)

    # The connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

finally:
    connection.close()

# ALTER TABLE moning
# MODIFY Quiz_ans MEDIUMTEXT;

# ALTER TABLE moning
# ADD Quiz_ans MEDIUMTEXT;

# CREATE TABLE moning (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     Quiz_qust MEDIUMTEXT,
#     Quiz_ans MEDIUMTEXT,
#     Quiz_text MEDIUMTEXT,
#     Quiz_trans MEDIUMTEXT
# );