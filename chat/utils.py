# contiene funzioni utili per le view e per il db


def json_element(dataora, contenuto, sent, mittente):
    # trasforma i dati del messaggio in una linea json da spedire al client
    return '{"time":"' + dataora.strftime("%Y-%m-%d %H:%M:%S") + '", "content":"' \
           + contenuto + '", "sent":"' + str(sent) + '", "sender":"' + mittente + '"}'
