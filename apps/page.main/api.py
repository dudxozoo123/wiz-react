def status():
    data = wiz.request.query()
    wiz.response.status(200, {
        'qwe': 'uio',
        'asd': 2,
    })