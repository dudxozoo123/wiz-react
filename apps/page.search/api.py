def status():
    data = wiz.request.query()
    wiz.response.status(200, {
        'qwe': 'search',
        'asd': 2,
    })