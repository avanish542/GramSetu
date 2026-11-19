def gramsetu_globals(request):
    """
    Global context processor injecting general app settings, current user unread notifications count,
    and demo village details.
    """
    unread_notifications_count = 0
    if request.user.is_authenticated:
        try:
            unread_notifications_count = request.user.notifications.filter(is_read=False).count()
        except AttributeError:
            unread_notifications_count = 0

    return {
        'APP_NAME': 'GramSetu V2',
        'TAGLINE': 'A Digital Bridge Between Panchayat & People',
        'UNREAD_NOTIFICATIONS_COUNT': unread_notifications_count,
        'DEMO_VILLAGE_NAME': 'Tenuhari (Shukla)',
        'DEMO_PANCHAYAT_NAME': 'Tenuhari (Shukla) Gram Panchayat',
        'DEMO_BLOCK': 'Sahjanwa',
        'DEMO_DISTRICT': 'Gorakhpur',
        'DEMO_STATE': 'Uttar Pradesh',
        'DEMO_PINCODE': '273209',
        'DEMO_SARPANCH': 'MOHANLAL',
    }

