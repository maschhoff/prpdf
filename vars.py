# Folder - !!! DO NOT CHANGE FOR DOCKER !!!!

import os

work_dir = os.environ['WORKDIR']
pdf_dir = work_dir + r"/static/pdf/"                # Source
temp_dir = r"/tmp/images/"                          # Temp
archiv_dir = "/Archiv/"                             # Oberordner Archiv -- darunter Ablage der Item Ordner
unknown_dir = work_dir + r"/static/pdf/unknown/"    # nicht erkannte PDFs
