from wand.image import Images


import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        f.required_methods = ['OPTIONS']
        return update_wrapper(wrapped_function, f)
    return decorator


UPLOAD_FOLDER = '/home/nmz787/public_html/pdf'
ALLOWED_EXTENSIONS = set(['pdf'])

originalPdf = None
originalPdfObjList = []
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# useful debugging tricks
app.config["TRAP_BAD_REQUEST_KEY_ERRORS"] = True
app.config["TRAP_HTTP_EXCEPTIONS"] = True
app.config["DEBUG"] = True

@app.route('/~nmz787/removePdfWatermark', methods=['POST', 'PUT', 'OPTIONS'])
@crossdomain(origin='*', headers='crossDomain, Content-Type')
def upload_file():
    if request.method == 'POST':
        # original url of the document
        #url = request.form["url"]
    if request.form.get["yesNoResponse"]:
        yesNoResponse = request.form.get["yesNoResponse"]
        numberOfObjsRemoved = request.form.get["objsRemoved"]
        #if the watermark was gone
        if yesNoResponse == "yes"
        #remove
        currentNumObjsRemoved = 0
        return ("""<html>"""
                    """<b>Is the visible watermark gone?</b>"""
                    """<\br>"""
                    """<button name="yes" onclick="buttonFunction(this)" value="""" + currentNumObjsRemoved + """">Yes</button>"""
                    """<button name="no" onclick="buttonFunction(this) value="""" + currentNumObjsRemoved + """">No</button>"""
                    """<\br>"""
                    """<img src='http://diyhpl.us/~nmz787/pdf/current_pdf_image0.png'>"""
                    """<script>"""
                        """function buttonFunction(this1) {"""
                            """var xhr=new XMLHttpRequest();"""
                            """xhr.onload=function(e){"""
                                """if(this.status==200){"""
                                    """document.getElementsByTagName("html")[0].innerHTML = (xhr.responseText);"""
                                """}"""
                                """else if(xhr.status!=200){"""
                                    """alert('upload failure, status code '+xhr.status);"""
                                """}"""
                                """break;"""
                            """}"""
                            """xhr.open('POST','http://diyhpl.us:5000/~nmz787/removePdfWatermark',true);"""
                            """xhr.setRequestHeader('crossDomain','true');"""
                            """var formData=new FormData();"""
                            """formData.append('yesNoResponse',this1.name);"""
                            """xhr.send(formData);"""
                        """}"""
                    """</script>"""
                """</html>""")
	print 'request:\n'
    print request
	print '***********'
	print request.files["file"]
    # what sort of content type did the server claim for that file?
    content_type = request.form["contentType"]
	print 'content type is: ' + content_type

    # actual file content
    content = request.files["file"]
	print 'content is:\n'
	print content
	filename = request.form["filename"]

	print 'filename: ' + filename
	file = content
	print allowed_file(filename)
    if file and allowed_file(filename):
        filename = secure_filename(filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], str("WATERMARK_" + filename))
        print 'saving to filepath: ' + filepath
        file = open(filepath, "wb")
        file.write(content.read())
        file.close()
        originalPdf = open_pdf(filepath)
        originalPdfObjList = enumerate_objects(originalPdf)
        objectsRemoved = []
        for index, objid in enumerate(originalPdfObjList):
            remove_object(originalPdf, objid)
            objectsRemoved.append(objid)
            if index>=len(originalPdfObjList):
                break
        #return 'http://diyhpl.us/~nmz787/pdf/'+filename
        return ("""<html>"""
                    """<b>Is the visible watermark gone?</b>"""
                    """<\br>"""
                    """<button name="yes" onclick="buttonFunction(this)" value="""" + currentNumObjsRemoved + """">Yes</button>"""
                    """<button name="no" onclick="buttonFunction(this) value="""" + currentNumObjsRemoved + """">No</button>"""
                    """<\br>"""
                    """<img src='http://diyhpl.us/~nmz787/pdf/current_pdf_image0.png'>"""
                    """<script>"""
                        """function buttonFunction(this1) {"""
                            """var xhr=new XMLHttpRequest();"""
                            """xhr.onload=function(e){"""
                                """if(this.status==200){"""
                                    """document.getElementsByTagName("html")[0].innerHTML = (xhr.responseText);"""
                                """}"""
                                """else if(xhr.status!=200){"""
                                    """alert('upload failure, status code '+xhr.status);"""
                                """}"""
                                """break;"""
                            """}"""
                            """xhr.open('POST','http://diyhpl.us:5000/~nmz787/removePdfWatermark',true);"""
                            """xhr.setRequestHeader('crossDomain','true');"""
                            """var formData=new FormData();"""
                            """formData.append('yesNoResponse',this1.name);"""
                            """xhr.send(formData);"""
                        """}"""
                    """</script>"""
                """</html>""")
    else:
        return "dunno what to do with your request"

if __name__ == "__main__":
    app.run(host='0.0.0.0')

















def enumerate_objects(content):
    outlines = []
    content = content.replace("\r\n", "\n")
    lines = content.split("\n")
    skip_mode = False
    for line in lines:
        if not skip_mode:
            if line[-3:] == "obj" or line[-4:] == "obj " or " obj <<" in line[0:50] or " obj<<" in line[0:50]:
                stripped = line.strip()
                if not stripped == "endobj":
                    outlines.append(stripped)
                    skip_mode=True
                    continue
        elif skip_mode:
            if line == "endobj" or line == "endobj ":
                skip_mode = False
                continue
    return outlines

def remove_object(content, objid):
    outlines = []
    content = content.replace("\r\n", "\n")
    lines = content.split("\n")
    skip_mode = False
    for line in lines:
        if line == "":
            outlines.append("")
            continue
        if not skip_mode:
            if line[-3:] == "obj" or line[-4:] == "obj " or " obj <<" in line[0:50] or " obj<<" in line[0:50]:
                #if line.startswith(str(objid) + " "):
                stripped = line.strip()
                if stripped == objid:
                    skip_mode = True
                    #last_line = line
                    #callback(outlines, *args)
                    print 'line: ' + str(line)
                    #print 'outline: ' + str(outlines)
                    continue
            outlines.append(line)
        elif skip_mode:
            if line == "endobj" or line == "endobj ":
                skip_mode = False
        #last_line = line
    return "\n".join(outlines)

def get_object(content, objid):
    outlines = []
    content = content.replace("\r\n", "\n")
    lines = content.split("\n")
    copy_mode = False
    for line in lines:
        if not copy_mode:
            if line[-3:] == "obj" or line[-4:] == "obj " or " obj <<" in line[0:50] or " obj<<" in line[0:50]:
                #if line.startswith(str(objid) + " "):
                stripped = line.strip()
                if stripped == objid:
                    copy_mode = True
                    #last_line = line
                    #callback(outlines, *args)
                    print 'line: ' + str(line)
                    #print 'outline: ' + str(outlines)
                    continue
        elif copy_mode:
            if line == "endobj" or line == "endobj ":
                copy_mode = False
                continue
            outlines.append(line)
        #last_line = line
    return "\n".join(outlines)

def open_pdf(obj, verbose=False):
    """
    Opens a pdf and returns the resulting pdf as a string.
    """
    # reset the file handler
    if hasattr(obj, "seek"):
        obj.seek(0)
    else:
        obj = open(obj, "rb")
    # load up the raw bytes
    content = obj.read()
    return content

def save_pdf_page_as_png(content, pagenum=0, filename=None, outfilepath="/home/nmz787/public_html/pdf/"):
    if filename:
        with Image(filename=filename + "[" + str(pagenum) + "]", resolution=200) as img:
            img.save(filename=outfilepath + "current_pdf_image.png")
    elif content:
        with Image(blob=content, resolution=200) as img:
            status=0
            for currentpagenum in range(len(img.sequence)):
                if currentpagenum==pagenum:
                    status=1
                    continue
                if status==0:
                    del img.sequence[0]
                elif status==1:
                    del img.sequence[1]
                print currentpagenum
            img.save(filename=outfilepath + "current_pdf_image" + str(pagenum) + ".png")


save_pdf_page_as_png(content = None, filename="/home/nmz787/public_html/pdf/J.pdf")