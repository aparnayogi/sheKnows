import psycopg2
import json
import psycopg2.extras
from datetime import datetime

def connection():
    conn = psycopg2.connect(
            database="sheknows_db", user='she_user', password='12345678', host='127.0.0.1', port= '5432'
    )
    print("connection successfull")
    return conn

def user_signup(request_data):
    conn = connection()
    cursor = conn.cursor()
    try:
        QUERY1 = '''
                 SELECT MAX(user_id) FROM sheknows_schema.user_registration;
                 '''
        
        reg_result = cursor.execute(QUERY1)
        reg_records = cursor.fetchall()

        for row in reg_records:
           no_of_users = row[0]

        users_no=''
        if (no_of_users < 9):
            users_no = '00' + str(no_of_users+1)
        elif (no_of_users < 99):
            users_no =  '0' + str(no_of_users+1)
        else:
            users_no =  str(no_of_users+1)

        print(users_no)
            

        #User Registration Section Start
    
        INSERT_QUERY = '''
                INSERT INTO sheknows_schema.user_registration (
                user_id,
                first_name,
                last_name,  
                email,
                mobile_no,
                password,
                city
                ) 
                VALUES('{}','{}', '{}','{}','{}','{}','{}')'''.format(
                    users_no,
                    request_data['first_name'],
                    request_data['last_name'],
                    request_data['email'],
                    request_data['mobile_no'],
                    request_data['password'],
                    request_data['city']

                )
        print(INSERT_QUERY)
        cursor.execute(INSERT_QUERY)
        conn.commit()

        QUERY3 = '''
                 SELECT MAX(login_id) FROM sheknows_schema.user_login;
                 '''

        result = cursor.execute(QUERY3)
        records = cursor.fetchall()

        if records and records[0][0] is not None:
            next_login_id = records[0][0] + 1
        else:
            next_login_id = 1

        print("Next Login ID:", next_login_id)
        INSERT_QUERY1 = '''
                INSERT INTO sheknows_schema.user_login(
                login_id,
                user_id,
                email,
                password) 
                VALUES('{}','{}','{}','{}')'''.format(
                    next_login_id,
                    users_no,
                    request_data['email'],
                    request_data['password'],
                )
        
        cursor.execute(INSERT_QUERY1)
        conn.commit()

        #User Login Section End

        
    # except Exception as e:
    #     print("Error", str(e), "Occured")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return "Success"

# def validate_login_details(login_data):
#     conn = connection()
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
#     valid_user = False
#     email_user = login_data['user_email'].strip()
#     print("login data at db",login_data['user_email'])
#     print(email_user)
#     try:
#         QUERY = ''' 
#                 SELECT email,password FROM sheknows_schema.user_login
#                 WHERE email ILIKE  %s 
#                 '''

#         cursor.execute(QUERY, (email_user,))
#         reg_records = cursor.fetchall()
#         print("regi record" , reg_records)

#         for row in reg_records:
#            password = row['password']
#            email = row['email']
#            print(password,email)
#            if(login_data['user_email'] == email and login_data['password'] == password):
#                 valid_user = True

#     except Exception as e:
#         print("Error", str(e), "Occured")

#     finally:
#         if conn:
#             cursor.close()
#             conn.close()
#     return valid_user
# def validate_login_details(login_data):
#     conn = connection()
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
#     valid_user = False
#     email_user = login_data.get('user_email') or login_data.get('email', '').strip()
#     try:
#         QUERY = '''
#             SELECT email, password FROM sheknows_schema.user_login
#             WHERE email ILIKE %s
#         '''
#         cursor.execute(QUERY, (email_user,))
#         reg_records = cursor.fetchall()
#         for row in reg_records:
#             if login_data['password'] == row['password']:
#                 valid_user = True
#                 break
#     except Exception as e:
#         print("Error:", str(e))
#     finally:
#         if conn:
#             cursor.close()
#             conn.close()
#     return valid_user

def validate_login_details(login_data):
    conn = connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    valid_user = False

    # Safely get the user email from login_data
    email_user = login_data.get('user_email', '').strip()
    if not email_user:
        print("Error: Missing 'user_email' in login_data")
        return valid_user

    print("Login data at DB:", login_data)

    try:
        # Query to find the user in the database
        QUERY = ''' 
            SELECT email, password FROM sheknows_schema.user_login
            WHERE email ILIKE %s
        '''
        cursor.execute(QUERY, (email_user,))
        reg_records = cursor.fetchall()

        # Debugging output
        print("Fetched records:", reg_records)

        if not reg_records:
            print(f"No user found with email: {email_user}")
            return valid_user

        # Validate password
        for row in reg_records:
            email = row['email']
            password = row['password']
            print("Checking email and password:", email, password)
            if email_user.lower() == email.lower() and login_data['password'] == password:
                valid_user = True
                break

    except Exception as e:
        print("Error:", str(e), "Occurred")

    finally:
        if conn:
            cursor.close()
            conn.close()

    return valid_user
