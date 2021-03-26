from bottle import route, run, template, static_file




@route("/styles/<file:path>")
def serve_style(file):
    return static_file(file, root = "./styles")



@route("/images/<file:path>")
def serve_image(file):
    return static_file(file, root = "./images")


@route("/files/<file:path>")
def serve_satic_files(file):
    return static_file(file, root = "./files")



# web pages:
@route('/')
@route('/home')
def hello():
    return static_file("index.html", root = "./templates")


@route('/resume')
def resume():
    return template("./templates/resume")



run(host='localhost', port= 8080, debug = True)