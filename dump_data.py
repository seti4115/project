import codecs

with codecs.open("data.json", "r", "utf-16") as f:
    data = f.read()

with codecs.open("data_utf8.json", "w", "utf-8") as f:
    f.write(data)
