from persiantools.jdatetime import JalaliDate


def ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def jalali_to_gregorian(date_str):
    y, m, d = map(int, date_str.replace("/", "-").split("-"))
    jdate = JalaliDate(y, m, d)
    return jdate.to_gregorian()