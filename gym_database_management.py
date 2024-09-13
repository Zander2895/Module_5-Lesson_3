import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='1Y6%11]5?16f',
            database='fitness_center'
        )
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to add a new member to the Members table
def add_member(name, age):
    conn = create_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()

        cursor.execute("INSERT INTO Members (name, age) VALUES (%s, %s)", (name, age))
    
        conn.commit()
        print(f"Member {name} added successfully!")
        
    except Error as e:
        print(f"Error: {e}. Member ID already exists or violates other constraints.")
        
    finally:
        cursor.close()
        conn.close()

# Function to add a new workout session for a specific member
def add_workout_session(member_id, date, duration_minutes, calories_burned):
    conn = create_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Members WHERE id = %s", (member_id,))
        if cursor.fetchone() is None:
            raise ValueError("Invalid member ID")
        
        cursor.execute(
            "INSERT INTO WorkoutSessions (member_id, session_date, session_time, activity) VALUES (%s, %s, %s, %s)",
            (member_id, date, duration_minutes, calories_burned)
        )

        conn.commit()
        print(f"Workout session for member ID {member_id} added successfully!")
        
    except ValueError as e:
        print(f"Error: {e}")
        
    finally:
        cursor.close()
        conn.close()

# Function to update the age of a specific member
def update_member_age(member_id, new_age):
    conn = create_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Members WHERE id = %s", (member_id,))
        if cursor.fetchone() is None:
            raise ValueError("Member not found")
        
        cursor.execute("UPDATE Members SET age = %s WHERE id = %s", (new_age, member_id))
    
        conn.commit()
        print(f"Member ID {member_id} updated with new age {new_age}!")
        
    except ValueError as e:
        print(f"Error: {e}")
        
    finally:
        cursor.close()
        conn.close()

# Function to delete a workout session based on its session ID
def delete_workout_session(session_id):
    conn = create_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM WorkoutSessions WHERE id = %s", (session_id,))
        if cursor.fetchone() is None:
            raise ValueError("Workout session not found")
        
        cursor.execute("DELETE FROM WorkoutSessions WHERE id = %s", (session_id,))
        
        conn.commit()
        print(f"Workout session ID {session_id} deleted successfully!")
        
    except ValueError as e:
        print(f"Error: {e}")
        
    finally:
        cursor.close()
        conn.close()

# Function to retrieve members whose ages are within a specified range using SQL BETWEEN
def get_members_in_age_range(start_age, end_age):
    conn = create_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Members WHERE age BETWEEN %s AND %s", (start_age, end_age))
        
        members = cursor.fetchall()
        if members:
            print(f"Members between ages {start_age} and {end_age}:")
            for member in members:
                print(member)
        else:
            print(f"No members found between ages {start_age} and {end_age}")
        
    finally:
        cursor.close()
        conn.close()

# Main script to test all the functions
if __name__ == "__main__":

    print("Testing Add Member:")
    add_member('John Doe', 25)
    add_member('Jane Doe', 28)

    print("\nTesting Add Workout Session:")
    add_workout_session(1, '2024-09-11', 60, 500)
    add_workout_session(2, '2024-09-12', 45, 300)

    print("\nTesting Update Member Age:")
    update_member_age(1, 26)

    print("\nTesting Delete Workout Session:")
    delete_workout_session(2)

    print("\nTesting Get Members in Age Range:")
    get_members_in_age_range(25, 30)