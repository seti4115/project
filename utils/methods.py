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


def filter_queryset(params, filters: list, query):
    filter_kwargs = {}

    for field in filters:
        values = params.getlist(field)

        if values:
            filter_kwargs[f"{field}__in"] = values

    if filter_kwargs:
        query = query.filter(**filter_kwargs)

    return query
