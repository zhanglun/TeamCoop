from teamcoop import app

@app.route('/mvc/')
def mvc():
    return "MVC Test!"