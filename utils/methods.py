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

def get_user_agent(request):
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    return user_agent


def date_filter(params, queryset, field):
    try:
        filter_kwargs = {}
        date_after = params.get("start_date")
        date_before = params.get("end_date")
        if date_after and date_before:
            date_after = jalali_to_gregorian(date_after)
            date_before = jalali_to_gregorian(date_before)
            filter_kwargs[f"{field}__gte"] = date_after
            filter_kwargs[f"{field}__lte"] = date_before
        elif date_after:
            date_after = jalali_to_gregorian(date_after)
            filter_kwargs[f"{field}__gte"] = date_after
        elif date_before:
            date_before = jalali_to_gregorian(date_before)
            filter_kwargs[f"{field}__lte"] = date_before
        queryset = queryset.filter(**filter_kwargs)
    except:
        pass
    return queryset


def ordering_filter(params, query):
    ordering = params.getlist("ordering")
    if ordering:
        for order in ordering:
            query = query.order_by(f"{order}")
    return query




