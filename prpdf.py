import os
import glob
import random
import json
import logging
from datetime import datetime, date
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, render_template, request, redirect, jsonify
import settings
import autoscan
import merge
import splitpages
import status
import shutil
from vars import *

app = Flask(__name__)

# Homepage - List PDFs and show preview
@app.route('/')
def index():
    pdf = loadFiles()
    if pdf:
        search = pdf[0]
    else:
        search = {"name": ""}
    return render_template(
        'explorer.html', 
        liste=pdf, 
        preview=search['name'], 
        subdirhtml=subdirhtml, 
        folders=loadArchivFolder(),
        iterator=0
    )


# Form submission on homepage (file rename/move)
@app.route('/', methods=['POST'])
def my_form_post():
    newid = request.form['pdf']
    oldid = request.form['oldpdf']
    folder = request.form['folder']
    iterator = request.form['inputiterator']

    sortCol = request.form.get("sortCol", type=int, default=2)
    sortDir = request.form.get("sortDir", default="desc")
    searchTerm = request.form.get("searchTerm", default="")

    append_date = config.get("append_date", True)
    append_random = config.get("append_random", True)

    fileneu = newid
    if append_date:
        filedatum = date.fromtimestamp(os.path.getmtime(os.path.join(unknown_dir, oldid))).strftime('%d_%m_%Y')
        fileneu += "_" + filedatum
    if append_random:
        fileneu += "_" + str(random.randint(1111, 9999))
    fileneu += ".pdf"

    message = ""
    file_moved = False

    if newid != "":
        if folder != "unknown":
            shutil.move(os.path.join(unknown_dir, oldid), os.path.join(folder, fileneu))
            message = "Success: File moved"
            file_moved = True
        else:
            shutil.move(os.path.join(unknown_dir, oldid), os.path.join(unknown_dir, fileneu))
            message = "Success: Title changed"

    pdf = loadFiles()

    if file_moved:
        def sort_key(item):
            if sortCol == 0:
                return item['name']
            elif sortCol == 1:
                return item['size']
            else:
                return item['date']

        pdf_sorted = sorted(pdf, key=sort_key, reverse=(sortDir == "desc"))
        new_preview = pdf_sorted[0]['name'] if pdf_sorted else ""
        iterator = 0
    else:
        new_preview = fileneu

    return render_template(
        'explorer.html',
        message=message,
        liste=pdf,
        preview=new_preview,
        subdirhtml=subdirhtml,
        folders=loadArchivFolder(),
        iterator=iterator,
        sort_column=sortCol,
        sort_direction=sortDir,
        search_term=searchTerm
    )


# Merge PDF page(s) selection page
@app.route('/merge')
def domerge():
    pdf = loadFiles()
    return render_template('merge.html', files=pdf)

@app.route('/merge', methods=['POST'])
def domergepost():
    file1 = request.form['file1']
    file2 = request.form['file2']
    option = request.form['option']
    filename = request.form['pdf']

    if "merge" in option:
        message = merge.pdf_merge_file(os.path.join(unknown_dir, file1), os.path.join(unknown_dir, file2), filename)
    else:
        message = merge.pdf_adf(os.path.join(unknown_dir, file1), os.path.join(unknown_dir, file2), filename)

    pdf = loadFiles()
    return render_template('explorer.html', liste=pdf, message=message, subdirhtml=subdirhtml, folders=loadArchivFolder(), iterator=0)


# Split PDF page(s) selection page
@app.route('/split')
def dosplit():
    pdf = loadFiles()
    return render_template('split.html', files=pdf)

@app.route('/split', methods=['POST'])
def dosplitpost():
    file1 = request.form['file1']
    page = int(request.form['page'])
    logging.info(f"Split Page after: {page}")

    splitpages.split_pdf(os.path.join(unknown_dir, file1), page)

    pdf = loadFiles()
    return render_template('explorer.html', liste=pdf, message="", subdirhtml=subdirhtml, folders=loadArchivFolder(), iterator=0)


# Trigger autoscan manually
@app.route('/autoscan')
def doautoscan():
    try:
        autoscan.run()
        global subdirhtml
        subdirhtml = ""
        listdirs(archiv_dir)
    except Exception as e:
        logging.error(f"An exception occurred {e}")

    pdf = loadFiles()
    search = pdf[0] if pdf else {"name": ""}
    return render_template('explorer.html', liste=pdf, preview=search['name'], subdirhtml=subdirhtml, folders=loadArchivFolder(), iterator=0)


# Delete file
@app.route('/delete/<string:id>')
def dodelete(id):
    os.remove(os.path.join(unknown_dir, id))
    return redirect('/')


# Rotate PDF pages
@app.route('/rotate/<string:id>')
def dorotate(id):
    splitpages.rotate_pages(os.path.join(unknown_dir, id))

    rotated_name = id.replace(".pdf", "_rotated.pdf")

    sortCol = 2
    sortDir = "desc"
    searchTerm = ""

    message = f"File '{rotated_name}' successfully rotated."

    pdf = loadFiles()

    def sort_key(item):
        if sortCol == 0:
            return item['name']
        elif sortCol == 1:
            return item['size']
        else:
            return item['date']

    pdf_sorted = sorted(pdf, key=sort_key, reverse=(sortDir == "desc"))

    iterator = 0
    for i, item in enumerate(pdf_sorted):
        if item['name'] == rotated_name:
            iterator = i
            break

    return render_template(
        'explorer.html',
        message=message,
        liste=pdf_sorted,
        preview=rotated_name,
        subdirhtml=subdirhtml,
        folders=loadArchivFolder(),
        iterator=iterator,
        sort_column=sortCol,
        sort_direction=sortDir,
        search_term=searchTerm
    )


# OCR page display
@app.route('/<string:id>')
def doocr(id):
    return render_template('magic.html', preview=id, subdirhtml=subdirhtml, folders=loadArchivFolder(), pdf=id)


# Autoscan rule save
@app.route('/magic', methods=['POST'])
def autoscan_rule():
    newid = request.form['pdf']
    folder = request.form['folder']
    keywords = request.form['keywords']

    keyw_array = [k.strip() for k in keywords.split(",")]
    key = folder + ";" + newid

    config = settings.loadConfig()
    config["index"].update({key: keyw_array})
    settings.writeJsonConfig(config)

    pdf = loadFiles()
    return render_template('explorer.html', liste=pdf, subdirhtml=subdirhtml, folders=loadArchivFolder(), iterator=0, message="Autoscan rule saved")


# Settings view
@app.route('/settings')
def setting():
    config_raw = settings.getConfigRaw()
    return render_template('settings.html', config=settings.loadConfig(), config_raw=config_raw.read())


# Save settings
@app.route('/settings', methods=['POST'])
def setting_save():
    config_raw = request.form['hiddenconfig']
    global config
    logging.info(f"Config: {config_raw}")

    if not config_raw:
        config_raw = settings.getConfigRaw()
        return render_template('settings.html', config=config, config_raw=config_raw.read())

    try:
        json.loads(config_raw)
        settings.writeConfig(config_raw)
        config = settings.loadConfig()
        return render_template('settings.html', config=config, config_raw=config_raw, message="Config saved")
    except Exception as e:
        logging.error(e)
        return render_template('settings.html', config=config, config_raw=config_raw, message="JSON error")


# Check if update is needed (for front-end polling)
@app.route("/check_update")
def check_update():
    logging.info(f"Checking for new files... Update needed? Result: {status.update_needed}")
    return jsonify({"update": status.update_needed})


# Reset the update flag
@app.route("/reset_update_flag")
def reset_update_flag():
    status.update_needed = False
    return '', 204


# Subdirectories list & HTML generation for folder tree
subdirs = [archiv_dir]
subdirhtml = ""

def listdirs(rootdir):
    global subdirhtml
    for it in os.scandir(rootdir):
        if it.is_dir():
            subdirs.append(it.path)
            subdirhtml += f"""
            <li><i class="fas fa-angle-right rotate"></i>
            <span><i class="far fa-folder-open ic-w mx-1"></i><a href="javascript:void(0)" onClick="selectfolder('{it.path}');">{it.name}</a></span>
            <ul class="nested">
            """
            listdirs(it.path)
            subdirhtml += "</ul></li>"

print('Creating Directory Map... that can take some time')
listdirs(archiv_dir)


# Load list of archive folders
def loadArchivFolder():
    return subdirs


# Load list of PDFs from unknown_dir with metadata
def loadFiles():
    res = []
    if os.path.exists(unknown_dir):
        files = glob.glob(os.path.join(unknown_dir, "*.pdf"))
        for file in files:
            filer = {
                "name": os.path.basename(file),
                "size": f"{os.path.getsize(file) / 1_000_000:.2f} MB",
                "date": datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S')
            }
            res.append(filer)
    return res


if __name__ == '__main__':
    work_dir = os.environ.get('WORKDIR', '.')

    logfile_path = os.path.join(work_dir, 'config', 'server.log')

    file_handler = TimedRotatingFileHandler(
        logfile_path,
        when='midnight',
        interval=1,
        backupCount=7,
        encoding='utf-8'
    )
    file_handler.suffix = "%Y-%m-%d"
    file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))

    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, stream_handler],
        force=True
    )

    config = settings.loadConfig()

    logging.info(f"Start PR PDF Server from {work_dir}...")
    print(f"Start PR PDF Server from {work_dir}...")
    print("""
     (\__/)  .-  -.)
     /0 0 `./    .'
    (O__,   \   (
      / .  . )  .
      |-| '-' \  )
      (   _(   ).'
    °....~....$

      PR PDF
    """)

    app.run(host='0.0.0.0', port=config["port"], debug=True)
