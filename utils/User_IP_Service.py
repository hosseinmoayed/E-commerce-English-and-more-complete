def Get_Client_IP(request):
    http_x = request.META.get("HTTP_X_FORWARDED_FOR")
    remote = request.META.get("REMOTE_ADDR")
    if http_x is not None:
        user_ip = http_x
    else:
        user_ip = remote
    return user_ip