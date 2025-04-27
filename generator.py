import csv
import random
import datetime
from faker import Faker  # Library to generate fake data
import os


def gen_book_records():
    # Initialize Faker to generate realistic fake data
    fake = Faker()

    # --- Configuration ---
    NUM_RECORDS = 500000
    FILENAME = 'book_records.csv'
    START_DATE = datetime.date(2015, 1, 1) # Start date for purchase dates
    END_DATE = datetime.date.today()      # End date for purchase dates
    # --- End Configuration ---

    def generate_random_date(start, end):
        """Generates a random date between start and end (inclusive)."""
        time_between_dates = end - start
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates + 1)
        random_date = start + datetime.timedelta(days=random_number_of_days)
        return random_date

    print(f"Starting generation of {NUM_RECORDS} book records...")

    # Prepare the header row based on your variable names
    # Combining DD, MM, YY into a single 'purchase_date' column for standard CSV practice
    header = ['bno', 'bname', 'Auth', 'price', 'publ', 'qty', 'purchase_date']

    try:
        with open(FILENAME, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write the header row
            writer.writerow(header)

            # Generate and write the data rows
            for i in range(1, NUM_RECORDS + 1):
                bno = i

                # Generate Book Name (using fake sentences)
                bname = fake.sentence(nb_words=random.randint(3, 8)).replace('.', '') # Remove trailing period

                # Generate Author Name
                Auth = fake.name()

                # Generate Price (integer as per your input example)
                price = random.randint(5, 150) # Random price between 5 and 150

                # Generate Publisher Name
                publ = fake.company()

                # Generate Quantity
                qty = random.randint(1, 50) # Random quantity between 1 and 50

                # Generate Purchase Date
                purchase_date_obj = generate_random_date(START_DATE, END_DATE)
                purchase_date_str = purchase_date_obj.strftime('%Y-%m-%d') # Format as YYYY-MM-DD

                # Create the data row
                data_row = [bno, bname, Auth, price, publ, qty, purchase_date_str]

                # Write the row to the CSV
                writer.writerow(data_row)

                # Optional: Print progress every 5000 records
                if i % 50000 == 0:
                    print(f"Generated {i}/{NUM_RECORDS} records...")

        print("-" * 30)
        print(f"Successfully generated {NUM_RECORDS} records.")
        print(f"Data saved to: {os.path.abspath(FILENAME)}")
        print("-" * 30)

    except IOError as e:
        print(f"Error writing to file {FILENAME}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return FILENAME

def gen_member_records():
    # Initialize Faker to generate realistic fake data
    fake = Faker()

    # --- Configuration ---
    NUM_MEMBER_RECORDS = 500000  # Define number of member records to generate
    MEMBER_FILENAME = 'member_records.csv' # Define the output filename
    START_DATE = datetime.date(2018, 1, 1) # Start date for membership dates
    END_DATE = datetime.date.today()      # End date for membership dates
    # --- End Configuration ---

    def generate_random_date(start, end):
        """Generates a random date between start and end (inclusive)."""
        time_between_dates = end - start
        days_between_dates = time_between_dates.days
        # Ensure days_between_dates is not negative if start == end
        random_number_of_days = random.randrange(max(0, days_between_dates) + 1)
        random_date = start + datetime.timedelta(days=random_number_of_days)
        return random_date

    def generate_random_mobile():
        """Generates a random 10-digit mobile number as a string."""
        return f"{random.randint(6, 9)}{''.join([str(random.randint(0, 9)) for _ in range(9)])}"


    print(f"Starting generation of {NUM_MEMBER_RECORDS} member records...")

    # Prepare the header row for the member table
    # Based on fields in Member.py: mno, mname, Date_of_Membership, addr, mob
    member_header = ['mno', 'mname', 'Date_of_Membership', 'addr', 'mob']

    try:
        with open(MEMBER_FILENAME, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write the header row
            writer.writerow(member_header)

            # Generate and write the data rows
            for i in range(1, NUM_MEMBER_RECORDS + 1):
                mno = i

                # Generate Member Name
                mname = fake.name()

                # Generate Date of Membership
                membership_date_obj = generate_random_date(START_DATE, END_DATE)
                # Format as YYYY-MM-DD for standard CSV practice
                membership_date_str = membership_date_obj.strftime('%Y-%m-%d')

                # Generate Member Address
                # Replace newlines with spaces for cleaner CSV output
                addr = fake.address().replace('\n', ', ')

                # Generate Member Mobile Number (as a string of digits)
                # Member.py expects an int, but CSV best practice might be string
                # Using a simple random 10-digit generator here
                mob = generate_random_mobile()

                # Create the data row
                member_data_row = [mno, mname, membership_date_str, addr, mob]

                # Write the row to the CSV
                writer.writerow(member_data_row)

                # Optional: Print progress
                if i % 50000 == 0:
                    print(f"Generated {i}/{NUM_MEMBER_RECORDS} member records...")

        print("-" * 30)
        print(f"Successfully generated {NUM_MEMBER_RECORDS} member records.")
        # Use os.path.abspath to show the full path where the file is saved
        print(f"Data saved to: {os.path.abspath(MEMBER_FILENAME)}")
        print("-" * 30)

    except IOError as e:
        print(f"Error writing to file {MEMBER_FILENAME}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return MEMBER_FILENAME
        
def gen_issue_records():
    # Initialize Faker (though not strictly needed for this table, kept for consistency)
    fake = Faker()

    # --- Configuration ---
    # Assuming previous generation counts for realistic IDs
    NUM_BOOK_RECORDS_PREV = 500000 # Number of book records generated previously
    NUM_MEMBER_RECORDS_PREV = 500000 # Number of member records generated previously

    NUM_ISSUE_RECORDS = 500000  # Define number of issue/transaction records
    ISSUE_FILENAME = 'issue_records.csv' # Define the output filename
    # Issue dates should logically start after memberships might have started
    START_DATE_ISSUE = datetime.date(2018, 6, 1)
    END_DATE_ISSUE = datetime.date.today()      # End date for issue/return dates
    RETURN_PROBABILITY = 0.85 # Probability that a book has been returned
    MAX_LOAN_DAYS = 90 # Maximum number of days a book might be loaned out
    # --- End Configuration ---

    def generate_random_date(start, end):
        """Generates a random date between start and end (inclusive)."""
        # Ensure start is not after end
        if start > end:
            start = end
        time_between_dates = end - start
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(max(0, days_between_dates) + 1)
        random_date = start + datetime.timedelta(days=random_number_of_days)
        return random_date

    def format_date(date_obj):
        """Formats a date object to YYYY-MM-DD string."""
        return date_obj.strftime('%Y-%m-%d')

    # --- Main Generation Logic ---
    print(f"Starting generation of {NUM_ISSUE_RECORDS} issue records...")

    # Header based on fields in Issue.py: Bno, Mno, d_o_issue, d_o_ret
    issue_header = ['bno', 'mno', 'd_o_issue', 'd_o_ret']

    # Calculate padding length based on previous record counts
    book_padding = len(str(NUM_BOOK_RECORDS_PREV))
    member_padding = len(str(NUM_MEMBER_RECORDS_PREV))

    try:
        with open(ISSUE_FILENAME, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write the header row
            writer.writerow(issue_header)

            # Generate and write the data rows
            for i in range(1, NUM_ISSUE_RECORDS + 1):
                # Generate random Book Code (referencing assumed existing books)
                random_book_id = random.randint(1, NUM_BOOK_RECORDS_PREV)
                bno = random_book_id

                # Generate random Member Code (referencing assumed existing members)
                random_member_id = random.randint(1, NUM_MEMBER_RECORDS_PREV)
                mno = random_member_id

                # Generate Date of Issue
                d_o_issue_obj = generate_random_date(START_DATE_ISSUE, END_DATE_ISSUE)
                d_o_issue_str = format_date(d_o_issue_obj)

                # Generate Date of Return (conditionally)
                d_o_ret_str = "" # Default to empty (not returned)
                # Check if the book *could* have been returned by END_DATE_ISSUE
                potential_return_date = d_o_issue_obj + datetime.timedelta(days=random.randint(1, MAX_LOAN_DAYS))

                # Only set a return date if it's before or on the simulation end date
                # AND based on random probability
                if potential_return_date <= END_DATE_ISSUE:
                    if random.random() < RETURN_PROBABILITY:
                        d_o_ret_str = format_date(potential_return_date)
                # If the potential return date is in the future relative to END_DATE_ISSUE,
                # it definitely hasn't been returned within our data period.

                # Create the data row
                issue_data_row = [bno, mno, d_o_issue_str, d_o_ret_str]

                # Write the row to the CSV
                writer.writerow(issue_data_row)

                # Optional: Print progress
                if i % 50000 == 0:
                    print(f"Generated {i}/{NUM_ISSUE_RECORDS} issue records...")

        print("-" * 30)
        print(f"Successfully generated {NUM_ISSUE_RECORDS} issue records.")
        print(f"Data saved to: {os.path.abspath(ISSUE_FILENAME)}")
        print("-" * 30)

    except IOError as e:
        print(f"Error writing to file {ISSUE_FILENAME}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return ISSUE_FILENAME