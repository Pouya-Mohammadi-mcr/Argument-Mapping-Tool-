from flask import (
    Blueprint, g, redirect, render_template, request, url_for, session, jsonify
)

from AMT.Auth import loginRequired
from AMT.Database import Database


bp = Blueprint('Arguments', __name__)

@bp.route('/')
def index():
    error = None
    issues = Database().findIssues()
    if issues=="SERROR":
        error="Service Unavaibale"
    elif issues=="ERROR":
        error="No topics found"
    return render_template('Arguments/Home.html', issues=issues, error=error)

@bp.route("/createArgument", methods=('GET', 'POST'))
@loginRequired
def createArgument():
    error = None   
    success = None
    argumentID = None

    rel = request.args.get('rel', None)
    element = request.args.get('element', None)
    if element:
        element = int(element)

    if request.method == 'POST':

        argument = request.form['argument']
        elementID = request.form['elementID']
        relation = request.form['relation']
        anonymous = request.form.get('anonymous')

        if not argument:
            error = "Your argument cannot be empty"
    
        if error == None:
            if elementID and relation:
                if anonymous:
                    result = Database().createArgumentAndRelationAnonymous(g.user['username'],argument, elementID, relation)
                    if result == "ERROR":
                        error= "The element you are referring to does not exist"
                    else:
                        success = "Your argument and its relation are succesfully created"
                        argumentID = result[0]['a']
                else:
                    result = Database().createArgumentAndRelation(g.user['username'],argument, elementID, relation)
                    if result == "ERROR":
                        error= "The element you are referring to does not exist"
                    else:
                        success = "Your argument and its relation are succesfully created" 
                        argumentID = result[0]['a']
                   
            else:
                if anonymous:
                    result = Database().createArgumentAnonymous(g.user['username'],argument)
                    success = "Your argument is succesfully created without any relations"
                    argumentID = result.id
                else:
                    result = Database().createArgument(g.user['username'],argument)
                    success = "Your argument is succesfully created without any relations"
                    argumentID = result.id

    return render_template('Arguments/CreateArgument.html', error=error, success=success, element=element, rel=rel, argumentID=argumentID)

@bp.route("/createIssue", methods=('GET', 'POST'))
@loginRequired
def createIssue():
    error = None   
    success = None
    issueID = None

    if request.method == 'POST':

        issue = request.form['issue']
        anonymous = request.form.get('anonymous')

        if not issue:
            error = "Your topic cannot be empty"
    
        if error == None:
            if anonymous:
                result = Database().createIssueAnonymous(g.user['username'],issue)
            else:
                result = Database().createIssue(g.user['username'],issue)
            success = "Your topic is succesfully created"
            issueID = result.id

    
    return render_template('Arguments/CreateIssue.html', error=error, success=success, issueID=issueID)

@bp.route("/createPosition", methods=('GET', 'POST'))
@loginRequired
def createPosition():
    error = None   
    success = None
    positionID = None


    issue = request.args.get('issue', None)
    if issue:
        issue = int(issue)

    if request.method == 'POST':

        position = request.form['position']
        issueID = request.form['issueID']
        anonymous = request.form.get('anonymous')


        if not position:
            error = "Your position cannot be empty"
        elif not issueID:
            error = "You should specify the topic you are taking a position on"
    
        if error == None:
            if anonymous:
                result = Database().createPositionAnonymous(g.user['username'],position, issueID)
                if result == "ERROR":
                    error= "The topic you are referring to does not exist"
                else:
                    success = "Your position is succesfully created"
                    positionID= result[0]['p']
            else:
                result = Database().createPosition(g.user['username'],position, issueID)
                if result == "ERROR":
                    error= "The topic you are referring to does not exist"
                else:
                    success = "Your position is succesfully created"
                    positionID= result[0]['p']

    
    return render_template('Arguments/CreatePosition.html', error=error, success=success, issue=issue, positionID=positionID)

@bp.route("/createRelation", methods=('GET', 'POST'))
@loginRequired
def createRelation():
    error = None   
    success = None
    relationID = None


    if request.method == 'POST':

        relation = request.form['relation']
        node1 = request.form['node1']
        node2 = request.form['node2']

        if not relation:
            error = "You must specify relation's title"
        elif not node1 or not node2:
            error = "Elements' IDs cannot be empty"
    
        if error == None:
            result = Database().createRelation(g.user['username'],node1,node2,relation)
            if result == "ERROR":
                error= "One or both the elements you are referring to do not exist"
            else:
                success = "The relation is succesfully created"
                relationID = result[0]['r']
    
    return render_template('Arguments/CreateRelation.html', error=error, success=success, relationID=relationID)

@bp.route("/findElement", methods=('GET', 'POST'))
def findElement():
    error = None  

    if request.method == 'POST':

        elementID = int(request.form['elementID'])

        if elementID == None:
            error = "You must specify the element ID"
        else:
            element = Database().getSingleElement(elementID)
            if element == "ERROR":
                error = "Element not found"
            elif list(element.labels)[0] == "Issue":
                return redirect(url_for('Arguments.showPositions',issueID = elementID))
            elif list(element.labels)[0] == "Position":
                return redirect(url_for('Arguments.showArguments',elementID = elementID, isPosition = 'Yes'))
            elif list(element.labels)[0] == "Argument":
                return redirect(url_for('Arguments.showArguments',elementID = elementID, isArgument = 'Yes'))
            elif list(element.labels)[0] == "Relation":
                return redirect(url_for('Arguments.showArguments',elementID = elementID, isRelation ='Yes'))
            else:
                error = "Element not found"

    return render_template('Arguments/Find.html', error=error)
 

@bp.route("/showPositions/<int:issueID>")
def showPositions(issueID):
    userRate= None
    username = session.get('username')
    if username:
        result = Database().getUserRate(username, issueID)
        if result != "ERROR":
            userRate = int(result['rate'])
    session['url'] = url_for('Arguments.showPositions', issueID = issueID)
    error = None
    positions = Database().getPositions(issueID)
    if positions == "ERROR":
        error = "No positions have been taken on this issue"
    issue = Database().getSingleElement(issueID)
    return render_template('Arguments/ShowPositions.html', positions=positions, issue=issue, error=error, userRate=userRate)

@bp.route("/showArguments/<int:elementID>")
def showArguments(elementID):
    #When its a position page
    isPosition = request.args.get('isPosition', None)
    parentTopic = None
    if isPosition  == 'Yes':
        parentTopic = Database().getParentTopic(int(elementID))

    #When its an argument page
    isArgument = request.args.get('isArgument', None)
    outgoingArgs = None
    if isArgument  == 'Yes':
        outgoingArgsTemp = Database().getOutgoingArguments(int(elementID))
        if outgoingArgsTemp != 'ERROR':
            outgoingArgs = outgoingArgsTemp

    #When its a relation page     
    isRelation = request.args.get('isRelation', None)
    relFrom = None
    relTo = None
    if isRelation == 'Yes':
        relFrom = Database().getRelFrom(int(elementID))
        relTo = Database().getRelTo(int(elementID))

    userRate= None
    username = session.get('username')
    if username:
        result = Database().getUserRate(username, elementID)
        if result != "ERROR":
            userRate = int(result['rate'])
    session['url'] = url_for('Arguments.showArguments', elementID = elementID)
    error = None
    arguments = Database().getArguments(elementID)
    if arguments == "ERROR":
        error = "No arguments have been made on this element"
    element = Database().getSingleElement(elementID)
    return render_template('Arguments/ShowArguments.html', arguments=arguments, element=element, error=error, userRate=userRate, parentTopic=parentTopic, outgoingArgs=outgoingArgs, relFrom=relFrom, relTo=relTo)

@bp.route("/rate", methods=('GET', 'POST'))
@loginRequired
def rate():

    if request.method == 'POST':

        elementID = int(request.form['elementID'])    
        rate = request.form.get('rate')
        if rate:
            rate = int(rate)
            result = Database().rate(g.user['username'], elementID, rate)

    if 'url' in session:
        return redirect(session['url'])
    return render_template('Arguments/StarRating.html')


@bp.route('/search',  methods=('GET', 'POST'))
def search():
    error = None
    searchResults = None

    if request.method == 'POST':
        searchPhrase = request.form['searchPhrase']

        if not searchPhrase:
            error = 'Search phrase is required'
        else:
            searchResults = Database().search(searchPhrase)
            if searchResults == "ERROR":
                error = "No matches found"

    return render_template('Arguments/Search.html', error=error, searchResults=searchResults)

@bp.route('/getReputation')
def getReputation():
    username = request.args.get('username')
    if username:
        if username=="Anonymous":
            return jsonify(reputation="Reputation cannot be shown for anonymous users")
        reputation = Database().getUserReputation(username)
        return jsonify(reputation=reputation)
    return jsonify(reputation="Not found")