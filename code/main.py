from bottle import run, template, static_file, route, get

@get("public/css/<filename:re:.*\.css")
def css(filename):
    return static_file(filename, root = "public/css")


@get("public/js/<filename:re:.*\.js")
def css(filename):
    return static_file(filename, root = "public/js")
