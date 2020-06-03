import xlrd
import random
from binary_expression_tree import *
from fractions import Fraction
from interval import Interval
import datetime


def get_integers(vType, num_in_total, vMin, vMax, vInterval):
    numbers = []

    if vInterval > 0:
        start = vMax
        vInterval = int(vInterval)
        while start + num_in_total * vInterval > vMax:
            start = random.randint(int(vMin), int(vMax))

        for i in range(num_in_total):
            numbers.append(start + i * vInterval)
    else:
        for i in range(num_in_total):
            x = 0
            while x == 0 or x in numbers:
                x = random.randint(int(vMin), int(vMax))
            numbers.append(x)

    numbers.sort()
    return numbers


def get_decimals(vType, num_in_total, vMin, vMax, vInterval):
    numbers = []
    places = random.choice([1, 2, 3, 4, 5])
    if 'two' in vType:
        places = 2
    if 'three' in vType:
        places = 3
    if vInterval>0:
        start = vMax
        while start + num_in_total * vInterval > vMax:
            start = round(random.uniform(float(vMin), float(vMax)), places)

        for i in range(num_in_total):
            numbers.append(round(start + i * vInterval, places))
    else:
        for i in range(num_in_total):
            x = 0
            while x == 0 or x in numbers:
                x = round(random.uniform(float(vMin), float(vMax)), places)
            numbers.append(x)
    numbers.sort()
    return numbers


def get_fractions(vType, num_in_total, vMin, vMax, vInterval):
    numbers = []
    n1, n2 = 1, 1
    if vInterval.isdigit():
        vInterval = int(vInterval)
        while n1 >= n2 or Fraction(n1, n2) < vMin or Fraction(n1, n2) > vMax or Fraction(n1, n2) in numbers:
            n1 = random.randint(1, 10)
            n2 = random.randint(1, 10)
        numbers.append(Fraction(n1, n2))
        for i in range(num_in_total-1):
            numbers.append(numbers[0] + Fraction((i+1)*vInterval))

    elif vInterval == '1/n':
        while n1 >= n2 or Fraction(n1, n2) < vMin or Fraction(n1, n2) > vMax or Fraction(n1, n2) in numbers:
            n1 = 1
            n2 = random.randint(5, 20)
        numbers.append(Fraction(n1, n2))
        for i in range(num_in_total-1):
            numbers.append(Fraction(n1+1+i, n2))

    else:
        for i in range(num_in_total):
            while Fraction(n1, n2) < vMin or Fraction(n1, n2) > vMax or Fraction(n1, n2) in numbers:
                n1 = random.randint(1, 10)
                n2 = random.randint(1, 10)

            numbers.append(Fraction(n1, n2))

    numbers.sort()
    return numbers


def get_time(vType, num_in_total, vMin, vMax, vInterval):

    timeList = []
    intervalList = []
    # the structure of time
    strf = '%H:%M:%S.%f'
    if 'ms' in vType:
        strf = '%M:%S.%f'
    elif 'second' in vType:
        strf = '%H:%M:%S'
    elif 'minute' in vType:
        strf = '%H:%M'


    year, month, day, hour, minute, second, microsecond = 2020, 1, 1, 0, 0, 0, 0
    if 'hour' in vType:
        hour = random.randint(0, 23)
    if 'half' in vType:
        minute = 30
    if 'quarter' in vType:
        minute = random.choice([15, 30, 45])
    if 'minute' in vType:
        minute = random.randint(0, 59)
    if 'second' in vType:
        second = random.randint(0, 59)
    if 'ms' in vType:
        microsecond = random.randint(100, 1000) * 1000

    start = datetime.datetime(year, month, day, hour, minute, second, microsecond)

    timeList.append(start.strftime(strf))

    end = datetime.datetime(year, month, day+1, hour, minute, second, microsecond)
    interval = interval_microsecond = interval_second = interval_minute = interval_hour = datetime.timedelta()
    for i in range(num_in_total-1):
        while start.__getattribute__('day') != end.__getattribute__('day'):
            if 'hour' in vInterval:
                interval_hour = datetime.timedelta(hours=random.randint(1, 23))
            if 'half' in vInterval:
                interval_minute = datetime.timedelta(minutes=random.choice([0, 30]))
            if 'minute' in vInterval:
                interval_minute = datetime.timedelta(minutes=random.randint(1, 59))
            if 'second' in vInterval:
                interval_second = datetime.timedelta(seconds=random.randint(1, 59))
            if 'ms' in vInterval:
                interval_microsecond = datetime.timedelta(microseconds=random.randint(1, 1000)*1000)
            interval = interval_microsecond + interval_second + interval_minute + interval_hour
            end = start + interval
        timeList.append(end.strftime(strf))
        intervalList.append(interval)
    return timeList, intervalList


def get_date(vType, num_in_total, vMin, vMax, vInterval):
    dateList = []
    intervalList = []
    year, month, day = 2020, 1, 1
    if 'year' in vType:
        year = random.randint(2000, 2020)
    if 'month' in vType:
        month = random.randint(1, 12)
    if 'day' in vType:
        if month == 2:
            day = random.randint(1, 28)
        elif month in [1, 3, 5, 7, 8, 10, 12]:
            day = random.randint(1, 31)
        else:
            day = random.randint(1, 30)
    start = datetime.datetime(year, month, day)
    dateList.append(start.date())
    if 'week' in vType:
        dateList.append(str('Week No. ' + str(start.weekday())))
    end = datetime.datetime(year+10, month, day)
    interval = interval_week = interval_day = datetime.timedelta()

    for i in range(num_in_total-1):
        while abs(start.__getattribute__('year') - end.__getattribute__('year')) > 1:
            if 'day' in vInterval:
                interval_day = datetime.timedelta(days=random.randint(1, 365))
            if 'week' in vInterval:
                interval_week = datetime.timedelta(weeks=random.randint(1, 50))
            interval = interval_day + interval_week
            end = start + interval
        dateList.append(end.date())
        intervalList.append(interval)
    return dateList, intervalList


def get_money(vType, num_in_total, vMin, vMax, vInterval):
    moneylist = []
    unit = ''
    is_decimal = False
    if ('euro' in vType) and ('cent' in vType):
        is_decimal = True
        unit = random.choice(['euro', 'cents'])
    elif 'euro' in vType:
        unit = 'euro'
    elif 'cent' in vType:
        unit = 'cents'
    for i in range(num_in_total):
        val = 0
        if unit == 'euro':
            val += random.randint(int(float(vMin)), int(float(vMax)))
            if is_decimal == True:
                val += 0.05 * random.randint(1, 20)
        if unit == 'cents':
            val += 5 * random.randint(1, 20)
        moneylist.append(val)
    return moneylist, unit


def get_content(vType, num_in_total, vMin, vMax, vInterval):
    contentlist = []
    unit = ''
    is_decimal = False
    unitlist = []
    val = 0
    if 'L' in vType:
        unitlist.append('L')
    if 'dL' in vType:
        unitlist.append('dL')
    if 'cL' in vType:
        unitlist.append('cL')
    if 'mL' in vType:
        unitlist.append('mL')
    unit = random.choice(unitlist)
    for i in range(num_in_total):
        if unit == 'L':
            val = round(random.uniform(int(float(vMin)), int(float(vMax))), 1)
        else:
            val = random.randint(1, 10)
        contentlist.append(val)
    return contentlist, unit


def get_weight(vType, num_in_total, vMin, vMax, vInterval):
    weightlist = []
    unit = ''
    is_decimal = False
    val = 0
    if 'kg' in vType:
        unit = 'kg'
    else:
        unit = 'g'
    for i in range(num_in_total):
        if unit == 'kg':
            if ',' in vType:
                val = round(random.uniform(int(float(vMin)), int(float(vMax))), 1)
            else:
                val = random.randint(int(float(vMin)), int(float(vMax)))

        else:
            val = random.randint(10, 1000)
        weightlist.append(val)
    return weightlist, unit


def get_temperature(vType, num_in_total, vMin, vMax, vInterval):
    tem_list = []
    for i in range(num_in_total):
        val = random.randint(int(float(vMin)), int(float(vMax)))
        tem_list.append(val)
    tem_list.sort()
    return tem_list


def template_number_sequence(data, index):
    table = data.sheets()[1]
    # number of rows and cols
    cols_num = table.ncols
    first_row_values = table.row_values(0)
    kc_col_no = dc_col_no = vType_col_no = tol_col_no = range_col_no = inv_col_no = tp_col_no = 0
    for col_no in range(cols_num):
        if 'Knowledge component' in first_row_values[col_no]:
            kc_col_no = col_no
        if 'Discription' in first_row_values[col_no]:
            dc_col_no = col_no
        if 'Type' in first_row_values[col_no]:
            vType_col_no = col_no
        if 'Total' in first_row_values[col_no]:
            tol_col_no = col_no
        if 'range' in first_row_values[col_no]:
            range_col_no = col_no
        if 'Interval' in first_row_values[col_no]:
            inv_col_no = col_no
    row_no = int(index)
    kc_row_value = table.row_values(row_no)
    value_type = str(kc_row_value[vType_col_no])
    num_in_total = int(float(kc_row_value[tol_col_no]))
    min_value = str(kc_row_value[range_col_no])
    max_value = str(kc_row_value[range_col_no + 1])
    interval = str(kc_row_value[inv_col_no])
    output = []
    if 'decimal' in value_type:
        if ('random' in interval) or ('/' in interval):
            value_interval = -1
        else:
            value_interval = float(random.choice(eval(kc_row_value[inv_col_no])))
        numbers = get_decimals(value_type, num_in_total, float(min_value), float(max_value), value_interval)
        for i in range(len(numbers)):
            output.append(str(numbers[i]))
    elif 'fraction' in value_type:
        if '[' in interval:
            value_interval = str(random.choice(eval(kc_row_value[inv_col_no])))
        else:
            value_interval = interval
        numbers = get_fractions(value_type, num_in_total, float(min_value), float(max_value), value_interval)
        for i in range(len(numbers)):
            output.append(str(numbers[i]))
    elif ('int' in value_type) or ('object' in value_type):
        if ('random' in interval) or ('/' in interval):
            value_interval = -1
        else:
            value_interval = float(random.choice(eval(kc_row_value[inv_col_no])))
        numbers = get_integers(value_type, num_in_total, int(float(min_value)), int(float(max_value)), value_interval)
        for i in range(len(numbers)):
            output.append(str(numbers[i]))
    elif 'time' in value_type:
        time_list, interval_list = get_time(value_type, num_in_total, min_value, max_value, interval)
        for i in range(num_in_total):
            output.append(str('time: ' + str(time_list[i])))
        for i in range(num_in_total-1):
            output.append(str('time interval: ' + str(interval_list[i])))
    elif 'date' in value_type:
        date_list, interval_list = get_date(value_type, num_in_total, min_value, max_value, interval)
        for i in range(num_in_total):
            output.append(str('date: ' + str(date_list[i])))
        for i in range(num_in_total-1):
            output.append(str('date interval: ' + str(interval_list[i])))
    elif 'money' in value_type:
        if ('random' in interval) or ('/' in interval):
            value_interval = -1
        else:
            value_interval = float(random.choice(eval(kc_row_value[inv_col_no])))
        moneylist, unit = get_money(value_type, num_in_total, min_value, max_value, interval)
        for i in range(num_in_total):
            output.append(str(str(moneylist[i]) + str(unit)))
    elif 'content' in value_type:
        if ('random' in interval) or ('/' in interval):
            value_interval = -1
        else:
            value_interval = float(random.choice(eval(kc_row_value[inv_col_no])))
        contentlist, unit = get_content(value_type, num_in_total, min_value, max_value, interval)
        for i in range(num_in_total):
            output.append(str(str(contentlist[i]) + str(unit)))
    elif 'weight' in value_type:
        if ('random' in interval) or ('/' in interval):
            value_interval = -1
        else:
            value_interval = float(random.choice(eval(kc_row_value[inv_col_no])))
        weightlist, unit = get_weight(value_type, num_in_total, min_value, max_value, interval)
        for i in range(num_in_total):
            output.append(str(str(weightlist[i]) + str(unit)))
    elif 'temperature' in value_type:
        if ('random' in interval) or ('/' in interval):
            value_interval = -1
        else:
            value_interval = float(random.choice(eval(kc_row_value[inv_col_no])))
        tem_list = get_temperature(value_type, num_in_total, min_value, max_value, interval)
        for i in range(num_in_total):
            output.append(str(str(tem_list[i]) + 'degree'))
    return output
    # if 'object' in vType:
    #     object = random.choice(['bin', 'mountain', 'pancake'])
    #     print("object: ", object)


