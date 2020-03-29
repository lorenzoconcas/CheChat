# contiene funzioni utili per le view e per il db


def json_element(dataora, contenuto, sent, mittente):
    # trasforma i dati del messaggio in una linea json da spedire al client
    return '{"dataora":"' + dataora.strftime("%Y-%m-%d %H:%M:%S") + '", "contenuto":"' \
           + contenuto + '", "inviato":"' + str(sent) + '", "mittente":"' + mittente + '"}'