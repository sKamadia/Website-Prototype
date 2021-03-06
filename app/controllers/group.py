from flask import render_template, session, redirect, request
from app.models.User import User
from app.services.JsonService import JsonService
from app import db
import json
from app.models.DiscussionGroup import DiscussionGroup
from app import db


class GroupController:

    @staticmethod
    def createGroup():
        """
        Handles creating new groups

        :return: redirect
        """

        groupName = request.form['groupName']
        groupMembers = User.query.filter(User.id.in_(request.form.getlist('groupMembers'))).all()

        newGroup = DiscussionGroup(discussiontitle=groupName)
        newGroup.groupMemberships = groupMembers

        db.session.add(newGroup)
        db.session.commit()

        return redirect('/listview')

    @staticmethod
    def showCreateGroup():
        """
        Handles returning the view for creating a group, providing the list of users of the application to the template
        :return: jinjaTemplate
        """
        if session.get("logged_in"):
            users = User.query.order_by(User.username).all()
            dictUsers = [JsonService.prepareModel(user) for user in users]
            jsonUsers = json.dumps(dictUsers)
            return render_template("create_group.html", users=jsonUsers)
        else:
            return render_template("login.html")