from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from AMT.Auth import loginRequired
from AMT.Database import Database


bp = Blueprint('Arguments', __name__)

@bp.route('/')
def index():
    issues = Database().findIssues()
    return render_template('Arguments/Home.html', issues=issues)

#@bp.route("/issue/<int:issueID>")
#def representIssue(issueID):
#    graph = getDB()
#    matcher = NodeMatcher(graph)
#    issue = matcher.get(issueID)

    # positions taken to this = query
#    pass


@bp.route("/createArgument", methods=('GET', 'POST'))
@loginRequired
def createArgument():
    error = None   
    success = None

    if request.method == 'POST':

        argument = request.form['argument']
        elementID = request.form['elementID']
        relation = request.form['relation']

        if not argument:
            error = "Your argument cannot be empty"
    
        if error == None:
            if elementID and relation:
                Database().createArgumentAndRelation(g.user['username'],argument, elementID, relation)
                success = "Your argument and its relation are succesfully created"
            else:
                Database().createArgument(g.user['username'],argument)
                success = "Your argument is succesfully created"
    
    return render_template('Arguments/CreateArgument.html', error=error, success=success)

@bp.route("/createIssue", methods=('GET', 'POST'))
@loginRequired
def createIssue():
    error = None   
    success = None

    if request.method == 'POST':

        issue = request.form['issue']

        if not issue:
            error = "Your issue cannot be empty"
    
        if error == None:
            Database().createIssue(g.user['username'],issue)
            success = "Your issue is succesfully created"
    
    return render_template('Arguments/CreateIssue.html', error=error, success=success)

@bp.route("/createPosition", methods=('GET', 'POST'))
@loginRequired
def createPosition():
    error = None   
    success = None

    if request.method == 'POST':

        position = request.form['position']
        issueID = request.form['issueID']

        if not position:
            error = "Your position cannot be empty"
        elif not issueID:
            error = "You should specify the issue you are taking a position on"
    
        if error == None:
            Database().createPosition(g.user['username'],position, issueID)
            success = "Your position is succesfully created"
    
    return render_template('Arguments/CreatePosition.html', error=error, success=success)

@bp.route("/createRelation", methods=('GET', 'POST'))
@loginRequired
def createRelation():
    error = None   
    success = None

    if request.method == 'POST':

        relation = request.form['relation']
        node1 = request.form['node1']
        node2 = request.form['node2']

        if not relation:
            error = "You must specify relation's title"
        elif not node1 or not node2:
            error = "Documents' IDs cannot be empty"
    
        if error == None:
            Database().createRelation(g.user['username'],node1,node2,relation)
            success = "The relation is succesfully created"
    
    return render_template('Arguments/CreateRelation.html', error=error, success=success)