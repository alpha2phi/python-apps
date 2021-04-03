from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi

from . import appbuilder, db
from .models import Accounts
"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""
"""
    Application wide 404 error handler
"""


class AccountsModelApi(ModelRestApi):
    resource_name = 'accounts'
    datamodel = SQLAInterface(Accounts)


appbuilder.add_api(AccountsModelApi)


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template("404.html",
                        base_template=appbuilder.base_template,
                        appbuilder=appbuilder),
        404,
    )


db.create_all()
