"""Contains methods for communicating with google sheets"""
import json
import gspread


def authenticate(fn: str) -> gspread.Client:
    with open(file=fn, mode="r", encoding="utf-8") as file:
        # Load the JSON data into a dictionary
        credentials = json.load(file)
    gc = gspread.service_account_from_dict(credentials)
    return gc


# user_id = TESTCASE  # rfid.readText()

# if not id_to_email_map.get(user_id):
#     continue

# member_email = id_to_email_map[user_id]

# # Open previous 100 entries
# logger.info("Loading the previous 100 entries")
# last_row: int = sheet_checkins.row_count
# first_row: int = max(last_row - 100, 2)
# logger.info(f"First row: {first_row}, Last row: {last_row}")
# last_hundred_rows: list[list[str | datetime | bool]] = sheet_checkins.get(
#     f"A{first_row}:D{last_row}"
# )

# # just filter for the current member
# relevant_rows = [
#     r
#     for r in last_hundred_rows
#     if r[1] == member_email
#     and datetime.strptime(r[0], DATETIMEFORMAT).date()
#     == datetime.today().date()
# ]

# # if the user hasn't signed in during the last 48 hours i.e. empty list or if the last time they signed in, they were headed out...
# sign_in_or_out = (
#     "In"
#     if (len(relevant_rows) == 0 or relevant_rows[-1][2] == "Out")
#     else "Out"
# )

# sheet_checkins.append_row(
#     [
#         datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S"),
#         member_email,
#         sign_in_or_out,
#         False,
#     ]
# )
