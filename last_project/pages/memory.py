# 必要なライブラリをインポートします
import streamlit as st
import pymysql.cursors

def fetch_data():
    # データベースに接続します
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='Quiz',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # すべてのレコードを選択します
            sql = "SELECT * FROM `moning` ORDER BY `id`"
            cursor.execute(sql)

            # すべてのレコードをフェッチします
            result = cursor.fetchall()

            return result
    finally:
        connection.close()

def reset_data():
    # データベースに接続します
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='Quiz',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # すべてのレコードを削除します
            sql = "DELETE FROM `moning`"
            cursor.execute(sql)

        # 変更をコミットします
        connection.commit()
    finally:
        connection.close()

def main():
    st.title("문제 기록")
    # リセットボタンを作成します
    if st.button('데이터베이스 리셋'):
        # ボタンがクリックされた場合、データベースをリセットします
        reset_data()
        st.success("데이터베이스가 리셋되었습니다.")
        
    # データベースからデータをフェッチします
    data = fetch_data()

    # データを表示します
    for record in data:
        st.write(f"문제 번호: {record['id']}")
        st.write(f"📖원본 문장📖: {record['Quiz_text']}")
        st.write(f"📖번역 문장📖: {record['Quiz_trans']}")
        st.write(f"문제: {record['Quiz_qust']}")
        st.write(f"답: {record['Quiz_ans']}")
        st.write("---")



# main 関数を呼び出します
if __name__ == "__main__":
    main()
