from shiftCalc import Calendar

test = Calendar(start_date= "2024-05-24", end_date= "2025-01-27")
test.calculate_shift()

test.calc_working_days("2024-05-24")

test.show_dates()

test.show_shift_on_date("2025-01-27")