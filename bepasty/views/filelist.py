# Copyright: 2014 Thomas Waldmann <tw@waldmann-edv.de>
# License: BSD 2-clause, see LICENSE for details.

import errno

from flask import current_app, render_template
from flask.views import MethodView

from . import blueprint
from .upload import check_upload_permission


def file_infos(names=None):
    """
    iterates over storage files metadata.
    note: we put the storage name into the metadata as 'id'

    :param names: None means "all items"
                  otherwise give a list of storage item names
    """
    storage = current_app.storage
    if names is None:
        names = list(storage)
    for name in names:
        with storage.open(name) as item:
            meta = dict(item.meta)
            meta['id'] = name
            yield meta


class FileListView(MethodView):
    def get(self):
        check_upload_permission()
        return render_template('filelist.html', files=file_infos())


blueprint.add_url_rule('/+list', view_func=FileListView.as_view('filelist'))
