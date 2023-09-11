"""
Author: Pete Newman
Date Started: 2023-07-03

Authenticate
"""
# TODO: Refactor so that it's always just working with local json files
# TODO: Refector to split google sheet stuff from data wrangling stuff

import google_sheet_wrangling
import data_wrangling

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


def main():
    # Authenticating
    gc = google_sheet_wrangling.authenticate("auth.json")

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
    sheet_inductions_attendance_records = sparkhaus_ss.worksheet(
        SN_INDUCTION_ATTENDANCE
    ).get_all_records()
    # pprint(sheet_inductions_attendance_records)
    logger.info("Successfully opened Induction Attendance")

    logger.info("Opening Induction Sessions worksheet...")
    sheet_induction_session_records = sparkhaus_ss.worksheet(
        SN_INDUCTION_SESSIONS
    ).get_all_records()
    # pprint(sheet_induction_session_records)
    logger.info("Successfully opened Induction Attendance")

    equipment_list = data_wrangling.construct_list_from_column(
        sheet_equipment.get_all_records(), "Equipment"
    )
    pprint(equipment_list)

    induction_attendances = data_wrangling.convert_records_to_induction_attendances(
        sheet_inductions_attendance_records
    )
    pprint(induction_attendances)

    induction_sessions = data_wrangling.convert_records_to_induction_sessions(
        sheet_induction_session_records
    )
    pprint(induction_sessions)

    induction_register_by_equipment = (
        data_wrangling.construct_induction_register_by_equipment(
            equipment_list=equipment_list, attendance_records=induction_attendances
        )
    )
    pprint(induction_register_by_equipment)

    base_data = {
        "Equipment": equipment_list,
        "Members": data_wrangling.construct_list_from_column(sheet_members, "Email"),
    }

    to_save: dict[str, dict] = {
        "base_data.json": base_data,
        "induction_register.json": sheet_induction_session_records,
        "induction_attendances.json": sheet_inductions_attendance_records,
        "induction_register_by_equipment": induction_register_by_equipment,
    }

    # Note: doesn't currently update all the things on this schedule
    while True:
        schedule.every().hour.do(data_wrangling.save_all_to_json(to_save))


if __name__ == "__main__":
    main()
