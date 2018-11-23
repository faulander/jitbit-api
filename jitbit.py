import json
import logging

import requests
from requests.auth import HTTPBasicAuth

logger = logging.getLogger("jitbit")

"""
Forked      from tclancy
Github:     https://github.com/faulander/jitbit-api for the latest version
License:    MIT License


General Methods:
Authorization (POST)        Done via Requests/HHTPBasicAuth

Ticket methods:
Tickets                     get_tickets
Ticket                      get_ticket_by_id
Ticket (POST)               create_ticket
UpdateTicket (POST)         update_ticket
SetCustomField (POST)       set_custom_field_by_id
Stats                       get_stats
TicketCustomFields          get_ticket_custom_fields_by_id
Attachment              
AttachFile (POST)
AddSubscriber (POST)        add_subscriber_by_id
Categories                  get_categories
TechsForCategory            get_techs_for_category
CustomFieldsForCategory     get_custom_fields_for_category
MergeTickets                merge_tickets

Comment methods:
Comment (POST)
Comments
CommentTemplates

User methods:
CreateUser (POST)           create_user
UpdateUser (POST)           update_user_by_id
UserByEmail                 get_user_by_email
Users                       get_users
Companies                   get_companies
Company (POST)

Knowledgebase methods:
Articles                    get_articles
Article                     get_article_by_id

Asset methods:
Assets (GET)                get_assets
Asset (GET)
Asset (POST)
UpdateAsset (POST)
AssignAssetToUser (POST)
AddAssetToTicket (POST)
"""



class JitBitAPI(object):
    def __init__(self, api_url, username, password):
        self.api_url = api_url
        self.authentication = HTTPBasicAuth(username, password)

        if not self.test_credentials():
            logger.error("Authorization failed for JitBit API")
            raise ValueError("Authorization failed, please check your credentials")

    def _make_request(self, method, data=None):
        """
        :param method:  string  API method listed above
        :param data:    dict    Dictionary with POST-Data
        :return:
        """
        url = "%s/api/%s" % (self.api_url, method)
        if data:
            return requests.post(url, data=data, auth=self.authentication)
        return requests.get(url, auth=self.authentication)

    def test_credentials(self):
        response = self._make_request("Authorization")
        return response.status_code == 200

    def get_tickets(self, *args, **kwargs):
        """
        :param args:    ---
        :param kwargs:
                    mode	        string	            (optional) Allows you to choose, what tickets to show:
                                    “all”(default)      – all tickets, including closed
                                    “unanswered”        – shows new or updated by customer or for tech tickets
                                    “unclosed”          – all active tickets
                                    “handledbyme”       – shows tickets assigned to the user
                    categoryid	    int	                (optional) Filter by a category
                    sectionId	    int	                (optional) Filter by a section
                    statusId	    int[]	            (optional) Filter by status(es), you can pass an array like
                                                        this: ?statusId=1&statusId=2
                    fromUserId	    int	                (optional) Filter by a ticket creator
                    fromCompanyId	int	                (optional) Filter by a company
                    handledByUserID	int	                (optional) Filter by a ticket performer
                    tagName	        string	            (optional) Filter by ticket a tag
                    dateFrom	    string	            (optional) Filter by creation date (date format should
                                                        be YYYY-MM-DD, for example 2016-11-24)
                    dateTo	        string	            (optional) Filter by creation date (date format should
                                                        be YYYY-MM-DD, for example 2016-11-24)
                    updatedFrom	    string	            (optional) Filter by “last updated” date (date format should
                                                        be YYYY-MM-DD, for example 2016-11-24)
                    updatedTo	    string	            (optional) Filter by “last updated” date (date format should
                                                        be YYYY-MM-DD, for example 2016-11-24)
                    count	        int	                (optional) How many tickets to return. Default: 10. Max: 100.
                    offset	        int	                (optional) Use this to create paging. For example
                                                        “offset=20&count=20” will return the next 20 tickets after
                                                        the first 20. Defalut: 0.
        :return: JSON with found tickets
        """
        data = {}
        data["mode"] = kwargs.get('mode', 'all')
        data["categoryid"] = kwargs.get('categoryId', '')
        data["sectionid"] = kwargs.get('sectionId', '')
        data["statusid"] = kwargs.get('statusId', '1')
        data["fromuserid"] = kwargs.get('fromuserId', '')
        data["fromcompanyid"] = kwargs.get('fromcompanyId', '')
        data["handledbyuserid"] = kwargs.get('handledbyuserId', '')
        data["tagname"] = kwargs.get('tagname', '')
        data["datefrom"] = kwargs.get('datefrom', '')
        data["dateto"] = kwargs.get('dateto', '')
        data["updatedfrom"] = kwargs.get('updatedfrom', '')
        data["updatedto"] = kwargs.get('updatedto', '')
        data["count"] = kwargs.get('count', '')
        data["offset"] = kwargs.get('offset', '1')
        modes = ["all", "unanswered", "unclosed", "handledbyme"]
        assert data["mode"] in modes, "mode must be one of %s" % modes
        assert int(data['offset']) > 0, "Offset count is 1-based"

        url = (f"Tickets?mode={data['mode']}&"
               f"categoryid={data['categoryid']}&"
               f"sectionId={data['sectionid']}&"
               f"statusId={data['statusid']}&"
               f"fromUserId={data['fromuserid']}&"
               f"fromCompanyId={data['fromcompanyid']}&"
               f"handledByUserID={data['handledbyuserid']}&"
               f"tagName={data['tagname']}&"
               f"dateFrom={data['datefrom']}&"
               f"dateTo={data['dateto']}&"
               f"updatedFrom={data['updatedfrom']}&"
               f"updatedTo={data['updatedto']}&"
               f"count={data['count']}&"
               f"offset={data['offset']}")
        response = self._make_request(url)
        return json.loads(response.content)

    def get_ticket_by_id(self, id):
        response = self._make_request("Ticket?id=%s" % id)
        if response.status_code == 200:
            try:
                return json.loads(response.content)
            except ValueError:
                pass
        logger.critical('Failure for get_ticket, status: %d, content: %s', response.status_code, response.content)

    def create_ticket(self, categoryId, body, subject, priorityId, userId, tags):
        """
        :param categoryId:      int                     Category ID
        :param body:            string                  Ticket body
        :param subject:         string                  Ticket subject
        :param priorityId:      int                     Ticket priority. Values:
                                                            -1  – Low
                                                            0   – Normal
                                                            1   – High
                                                            2   – Critical
        :param userId:          int                     User-ID to create a ticket “on-behalf” of this user
                                                        (requires technician permissions)
        :param tags:            string                  A string of tags separated by comma.
                                                        Example: tags=tag1,tag2,tag3
        :return:                The created ticket ID
        """
        assert all([categoryId, body, subject, priorityId]), "Must provide values for categoryId, body, subject and priorityId"
        data = {
            "categoryId": categoryId,
            "body": body,
            "subject": subject,
            "priorityId": priorityId,
        }
        if userId:
            data["userId"] = userId
        if tags:
            data["tags"] = tags
        response = self._make_request("Ticket", data=data)
        if response.status_code == 200:
            # there's no good way to differentiate between success and failure with this API
            try:
                jitbit_ticket_id = int(response.content)
                logger.info("Ticket created: %d", jitbit_ticket_id)
                return jitbit_ticket_id
            except TypeError:
              pass
            except ValueError:
                pass
        else:
            logger.critical("JitBit ticket creation failed, response was %s %d", response.content, response.status_code)
        return None

    def get_users(self, count=500, page=1, list_mode="all"):
        """

        :param count:       int                 (optional) number of users to return. Default: 500
        :param page:        int                 (optional) used to get the next set of users after the first one.
                                                So ?count=50 returns the first 50 users and ?count=50&page=2
                                                returns the following 50 users.
        :param list_mode:   string              (optional)
                                                    “all” (default) - all users
                                                    “techs”         - techs including admins
                                                    “admins”        - admins only
                                                    “regular”       - only regular users
        :return:            JSON with Users
        """
        assert page > 0, "Page count is 1-based"
        modes = ["all", "techs", "admins", "regular"]
        assert list_mode in modes, "list_mode must be one of %s" % modes
        url = "Users?count=%d&page=%d&listMode=%s" % (count, page, list_mode)
        response = self._make_request(url)
        return json.loads(response.content)

    def get_user_by_email(self, email):
        response = self._make_request("UserByEmail?email=%s" % email)
        if response.status_code == 200:
            try:
                return json.loads(response.content)
            except ValueError:
                pass
        logger.critical('Failure for get_user_by_email, status: %d, content: %s', response.status_code, response.content)

    def create_user(self, username, password, email, first_name, last_name, company, department, phone="", location="", send_welcome_email=False):
        """
        :param username:            string  username, should not be taken by another user
        :param password:            string  user’s password
        :param email:               string  user’s email
        :param first_name:          string  user's firstname
        :param last_name:           string  user's lastname
        :param company:             string  Set user’s company. If the company doesn’t exist, it will be created.
        :param department:          string  Set user’s department. If the department doesn’t exist, it will be created.
        :param phone:               string  user's phone
        :param location:            string  user's location
        :param send_welcome_email:  bool    Send a “welcome” to the user
        :return:                    created userId
        """
        assert all([username, password, email]), "Must provide values for username, password and email"
        data = {
            "username": username,
            "password": password,
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
            "phone": phone,
            "location": location,
            "company": company,
            "department": department,
            "sendWelcomeEmail": send_welcome_email
        }
        response = self._make_request("CreateUser", data=data)
        if response.status_code == 200:
            # there's no good way to differentiate between success and failure with this API
            try:
                jitbit_user_id = int(response.content)
                logger.info("JitBit user created for %s %s", first_name, last_name)
                return jitbit_user_id
            except TypeError:

                pass
            except ValueError:
                pass
        elif response.status_code == 500:
            logger.critical("500 error at JitBit for %s %s, it may be the user already exists", first_name, last_name)
        else:
            logger.critical("JitBit user creation failed for %s %s, response was %s %d", first_name, last_name,
                        response.content, response.status_code)
        return None

    def update_user_by_id(self, user_id, username="", email="", first_name="", last_name="", company="", phone="", location="", password=None, notes="", department="", disabled=False):
        """
        :param user_id:         int     edited user’s ID
        :param username:        string  username, should not be taken by another user
        :param email:           string  user’s email
        :param first_name:      string  firstname
        :param last_name:       string  lastname
        :param company:         string  company name
        :param phone:           string  phone
        :param location:        string  location
        :param password:        string  password
        :param notes:           string  optional administrator’s notes
        :param department:      string  user’s department name
        :param disabled:        bool    enable/disable the user
        :return:                ???
        """
        data = {
            "userId": user_id,
            "username": username,
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
            "phone": phone,
            "location": location,
            "company": company,
            "department": department,
            "disabled": disabled
        }
        if password:
            data["password"] = password
        if notes:
            data["notes"] = notes
        response = self._make_request("UpdateUser", data=data)
        if response.status_code == 200:
            logger.info("JitBit user updated for id %s, user %s, email %s", user_id, username, email)
            return True
        logger.critical("JitBit user update failed for id %s, response code was %d, %s", user_id, response.status_code,
                    response.content)
        return False

    def get_companies(self):
        response = self._make_request("Companies")
        return json.loads(response.content)

    def get_categories(self):
        response = self._make_request("categories")
        return json.loads(response.content)

    def get_articles(self):
        response = self._make_request("Articles")
        return json.loads(response.content)

    def get_article_by_id(self, article_id):
        response = self._make_request("Article/%s" % article_id)
        return json.loads(response.content)

    def get_assets(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
                        page	                optional	page number to return assets from. If you need assets from 51 to 101 - pass “2”, etc.
                        assignedToUserId	    optional	filter by assigned user ID
                        assignedToCompanyId	    optional	filter by assigned company ID
                        assignedToDepartmentId	optional	filter by assigned company ID
        :return: JSON
        """
        data = {}
        data["page"] = kwargs.get('page', '')
        data["assignedtouserid"] = kwargs.get('assignedtouserid', '')
        data["assignedtocompany"] = kwargs.get('assignedtocompany', '')
        data["assignedtodepartmentid"] = kwargs.get('assignedtodepartmentid', '')
        url = ("Assets?page={data['page']}&"
               "assignedToUserId={data['assignedtouserid']}&"
               "assignedToCompanyId={data['assignedtocompany']}&"
               "assignedToDepartmentId={data['assignedtodepartmentid']}"
               )
        response = self._make_request(url)
        if response.status_code == 200:
            return json.loads(response.content)
        return False

    def update_ticket(self, *args, **kwargs):
        """
        :param args: ---
        :param kwargs:
                        categoryId (optional)           int	Ticket category
                        priority (optional)	            int	Ticket priority. Values:
                            -1  – Low
                            0   – Normal
                            1   – High
                            2   – Critical
                        date (optional)	                DateTime	Ticket creation date
                        userId (optional)	            int	        Ticket submitter’s user ID
                        dueDate (optional)	            DateTime	Due date
                        assignedUserId (optional)	    int	        Assigned technician’s ID. Set to 0 (zero) to remove the currently assigned user.
                        timeSpentInSeconds (optional)	int	        Time spent on the ticket
                        statusId (optional)	            int	        Ticket status ID. “Closed” id 3, “New” is 1, “In process” is 2. Check your custom status IDs in the admin area
                        tags (optional)	                int	        A comma-separated list of tags to apply to the ticket. Like tags=tag1,tag2,tag3. All existing tags will be removed
        :return: 200 OK if there were no errors. Returns an error message otherwise.
        """
        data["categoryId"] = kwargs.get('categoryId', '')
        data["priority"] = kwargs.get('priority', '')
        data["date"] = kwargs.get('date', '')
        data["userId"] = kwargs.get('userId', '')
        data["dueDate"] = kwargs.get('dueDate', '')
        data["assignedUserId"] = kwargs.get('assignedUserId', '')
        data["timeSpentInSeconds"] = kwargs.get('timeSpentInSeconds', '')
        data["statusId"] = kwargs.get('statusId', '')
        data["tags"] = kwargs.get('tags', '')

        url = ("UpdateTicket=categoryId={data['categoryId']}&"
               "priority={data['priority']}&"
               "date={data['date']}&"
               "userId={data['userId']}&"
               "dueDate={data['dueDate']}&"
               "assignedUserId={data['assignedUserId']}&"
               "timeSpentInSeconds={data['timeSpentInSeconds']}&"
               "statusId={data['statusId']}&"
               "tags={data['tags']}"
                )
        if response.status_code == 200:
            return json.loads(response.content)
        return False

    def set_custom_field_by_id(self, ticketId, fieldId, value):
        """
        :param ticketId: int
        :param fieldId: int
        :param value: Value as a string. For checkboxes pass true or false. For dropdowns pass the option ID. For dates pass date as a string in any format.
        :return: 200 OK if there were no errors. Returns an error message otherwise.
        """
        assert all([ticketId, fieldId, value]), "Must provide values for ticketId, fieldId and value"

        data["ticketId"] = ticketId
        data["fieldId"] = fieldId
        data["value"] = value

        response = self._make_request("SetCustomField", data=data)
        return response.status_code

    def get_stats(self):
        """
        :return: JSON
        """
        response = self._make_request("Stats")
        return json.loads(response.content)

    def get_ticket_custom_fields_by_id(self, id):
        url = "TicketCustomFields?id=%s" % id
        response = self._make_request(url)
        return json.loads(response.content)

    def add_subscriber_by_id(self, ticketId, userId):
        """

        :param ticketId:    int
        :param userId:      int
        :return:            200 if ok, errorcode otherwise?
        """
        assert all([ticketId, userId]), "Must provide values for ticketId and userId"
        url = "AddSubscriber?id=%d&userId=%d" % (ticketId, userId)
        response = self._make_request(url)
        return response.status_code

    def  get_techs_for_category(self, categoryId):
        """
        :param categoryId:  int
        :return:            JSON with all possible assignees for a category
        """
        url = "TechsForCategory?id=%d" % categoryId
        response = self._make_request(url)
        return json.loads(response.content)

    def get_custom_fields_for_category(self, categoryId):
        """
        :param categoryId:  int
        :return:            JSON with all possible assignees for a category
        """
        url = "CustomFieldsForCategory?id=%d" % categoryId
        response = self._make_request(url)
        return json.loads(response.content)

    def merge_tickets(self, id, id2):
        """
        :param id:      int     first to be merged ticket ids
        :param id2:     int     second to be merged ticket id
        :return:        ???
        """
        assert all([id, id2]), "two tickets need to be provided"
        url = "MergeTickets?id=%d&id2=%d" % (id,id2)
        response = self._make_request(url)
        return json.loads(response.content)
