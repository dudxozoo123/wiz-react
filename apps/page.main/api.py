def status():
    data = wiz.request.query()
    print(data)
    print("qweqwe")
    wiz.response.status(200, {
        'qwe': 'uio',
        'asd': 2,
    })