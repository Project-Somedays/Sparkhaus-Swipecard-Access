"""
Author: Pete Newman
Date Started: 2023-07-03

Authenticate
"""
# TODO: Refactor so that it's always just working with local json files
# TODO: Refector to split google sheet stuff from data wrangling stuff

from google_sheet_wrangling import save_to_json, authenticate, convert_records_to_induction_attendances, convert_records_to_induction_sessions, construct_list_from_column, construct_induction_register_by_equipment

# from pprint import pprint
from decouple import config
import sys
from pprint import pprint
import logging
import schedule

sys.path.append("C:/Users/proje/OneDrive/Documents/PiicoDev")
# from PiicoDev_RFID import PiicoDev_RFID

logger = logging.getLogger("test")
logger.setLevel(level=logging.DEBUG)

logFileFormatter = logging.Formatter(
    fmt="%(levelname)s %(asctime)s \t %(funcName)s L%(lineno)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
fileHandler = logging.FileHandler(filename="test.log", mode="w")
fileHandler.setFormatter(logFileFormatter)
fileHandler.setLevel(level=logging.INFO)

logger.addHandler(fileHandler)

SPREADSHEET_ID = config("SPREADSHEET_ID")
SN_CHECKIN = "Checkins"
SN_MEMBERS = "Members"
SN_INDUCTION_ATTENDANCE = "Induction Attendance"
SN_INDUCTION_SESSIONS = "Induction Sessions"
SN_EQUIPMENT = "Equipment"
TESTCASE = "peter.newman.22@gmail.com"
DATETIMEFORMAT = "%d/%m/%Y %H:%M:%S" 
 
def save_all_to_json(to_save: dict[str, dict]) -> None:
    for fn, data in to_save.items():
        save_to_json(data_dict=data, fn=fn)

def main():
    # Authenticating
    gc = authenticate("auth.json")

    # Open spreadsheet
    logger.info("Opening worksheet")
    sparkhaus_ss = gc.open_by_key(SPREADSHEET_ID)
    logger.info("Successfully opened spreadsheet!")

    # Open checkin worksheet
    # logger.info("Opening checkin worksheet...")
    # sheet_checkins = sparkhaus_ss.worksheet(CHECKIN_SHEET_NAME)
    # logger.info("Successfully opened checkin worksheet!")
    
    # Open member worksheet
    logger.info("Opening member worksheet...")
    sheet_members = sparkhaus_ss.worksheet(SN_MEMBERS).get_all_records()
    logger.info("Successfully opened member worksheet!")

    logger.info("Opening equipment worksheet...")
    sheet_equipment = sparkhaus_ss.worksheet(SN_EQUIPMENT)
    logger.info("Successfully opened equipment worksheet!")

    logger.info("Opening Inductions worksheet...")
    sheet_inductions_attendance_records = sparkhaus_ss.worksheet(SN_INDUCTION_ATTENDANCE).get_all_records()
    # pprint(sheet_inductions_attendance_records)
    logger.info("Successfully opened Induction Attendance")

    logger.info("Opening Induction Sessions worksheet...")
    sheet_induction_session_records = sparkhaus_ss.worksheet(SN_INDUCTION_SESSIONS).get_all_records()
    # pprint(sheet_induction_session_records)
    logger.info("Successfully opened Induction Attendance")

    equipment_list = construct_list_from_column(sheet_equipment.get_all_records(), "Equipment")
    pprint(equipment_list)
    
    induction_attendances = convert_records_to_induction_attendances(sheet_inductions_attendance_records)
    pprint(induction_attendances)
    
    induction_sessions = convert_records_to_induction_sessions(sheet_induction_session_records)
    pprint(induction_sessions)

    induction_register_by_equipment = construct_induction_register_by_equipment(equipment_list=equipment_list,attendance_records=induction_attendances)
    pprint(induction_register_by_equipment)

    base_data = {
        "Equipment" : equipment_list,
        "Members" : construct_list_from_column(sheet_members, "Email")
    }

    to_save: dict[str, dict] = {
        "base_data.json" : base_data,
        "induction_register.json" : sheet_induction_session_records,
        "induction_attendances.json" : sheet_inductions_attendance_records,
        "induction_register_by_equipment" : induction_register_by_equipment
    }

    # Note: doesn't currently update all the things on this schedule
    while True:
        schedule.every().hour.do(
            save_all_to_json(to_save)
        )

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



if __name__ == "__main__":
    main()
