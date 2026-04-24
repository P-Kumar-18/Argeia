from flask import current_app, render_template
from . import main
from ...infrastructure import TransitionRepository

@main.route("/analysis")
def transition_analysis():
    transition_repo: TransitionRepository = current_app.transition_repo

    transitions = transition_repo.get_all()
    return render_template('transition_analysis.html', transitions=transitions)