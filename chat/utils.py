# contiene funzioni utili per le view


def json_element(dataora, contenuto, sent, mittente):
    # trasforma i dati del messaggio in una linea json da spedire al client
    return '{"dataora":"' + dataora.strftime("%Y-%m-%d %H:%M:%S") + '", "contenuto":"' \
           + contenuto + '", "inviato":"' + str(sent) + '", "mittente":"' + mittente + '"}'


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
