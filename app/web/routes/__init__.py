from flask import Blueprint


main = Blueprint("main", __name__)

from . import landing
from . import dashboard
from . import tasks
from . import schedule_task
from . import edit_task
from . import transition_analysis