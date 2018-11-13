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
UpdateTicket (POST)
SetCustomField (POST)
Stats
TicketCustomFields
Attachment
AttachFile (POST)
AddSubscriber (POST)
Categories                  get_categories
TechsForCategory
CustomFieldsForCategory
MergeTickets

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
        url = "%s/api/%s" % (self.api_url, method)
        if data:
            return requests.post(url, data=data, auth=self.authentication)
        return requests.get(url, auth=self.authentication)
    def test_credentials(self):
        response = self._make_request("Authorization")
        return response.status_code == 200
    def get_tickets(self, *args, **kwargs):
        data[mode] = kwargs.get('mode', '')
        data[categoryid] = kwargs.get('categoryid', '')
        data[sectionid] = kwargs.get('sectionid', '')
        data[statusid] = kwargs.get('statusid', '')
        data[fromuserid] = kwargs.get('fromuserid', '')
        data[fromcompanyid] = kwargs.get('fromcompanyid', '')
        data[handledbyuserid] = kwargs.get('handledbyuserid', '')
        data[tagname] = kwargs.get('tagname', '')
        data[datefrom] = kwargs.get('datefrom', '')
        data[dateto] = kwargs.get('dateto', '')
        data[updatedfrom] = kwargs.get('updatedfrom', '')
        data[updatedto] = kwargs.get('updatedto', '')
        data[count] = kwargs.get('count', '')
        data[offset] = kwargs.get('offset', '')
        modes = ["all", "unanswered", "unclosed", "handledbyme"]
        assert date[mode] in modes, "mode must be one of %s" % modes
        assert offset > 0, "Offset count is 1-based"

        url = ("Tickets?mode={data[mode]}&"
               "categoryid={data[categoryid]}&"
               "sectionId={data[sectionid]}&"
               "statusId={data[statusid]}&"
               "fromUserId={data[fromuserid]}&"
               "fromCompanyId={data[fromcompanyid]}&"
               "handledByUserID={data[handledbyuserid]}&"
               "tagName={data[tagname]}&"
               "dateFrom={data[datefrom]}&"
               "dateTo={data[dateto]}&"
               "updatedFrom={data[updatedfrom]}&"
               "updatedTo={data[updatedto]}&"
               "count={data[count]}&"
               "offset={data[offset]}")
        response = self._make_request(url)
        return json.loads(response.content)
    def get_ticket_by_id(self, id):
        response = self._make_request("Ticket?id=%s" % id)
        if response.status_code == 200:
            try:
                return json.loads(response.content)
            except ValueError:
                pass
        logger.warn('Failure for get_ticket, status: %d, content: %s', response.status_code, response.content)
    def create_ticket(self,categoryId,body,subject,priorityId,userId,tags):
        assert all([categoryId, body, subject, priorityId]), "Must provide values for categoryId, body, subject and priorityId"
        data = {
            "categoryId": categoryId,
            "body": body,
            "subject": subject,
            "priorityId": priorityId,
        }
        if userId:
            data[userId] = userId
        if tags:
            data[tags] = tags
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
            logger.warn("JitBit ticket creation failed, response was %s %d", response.content, response.status_code)
        return None

    def get_users(self, count=500, page=1, list_mode="all"):
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
        logger.warn('Failure for get_user_by_email, status: %d, content: %s', response.status_code, response.content)
    def create_user(self, username, password, email, first_name, last_name, company, phone="", location="", send_welcome_email=False):
        """
        Add user per https://www.jitbit.com/helpdesk/helpdesk-api/#CreateUser
        If successful, returns JitBit userId
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
            logger.warn("500 error at JitBit for %s %s, it may be the user already exists", first_name, last_name)
        else:
            logger.warn("JitBit user creation failed for %s %s, response was %s %d", first_name, last_name,
                        response.content, response.status_code)
        return None
    def update_user_by_id(self, user_id, username, email, first_name, last_name, company, phone, location, password=None, notes="", department="", disabled=False):
        """
        Update list of available parameters at https://www.jitbit.com/helpdesk/helpdesk-api/#UpdateUser
        returns True/ False to indicate apparent success as JitBit's docs don't say they return any info
        Everything except notes is a required field
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
        logger.warn("JitBit user update failed for id %s, response code was %d, %s", user_id, response.status_code,
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
        data[page] = kwargs.get('page', '')
        data[assignedtouserid] = kwargs.get('assignedtouserid', '')
        data[assignedtocompany] = kwargs.get('assignedtocompany', '')
        data[assignedtodepartmentid] = kwargs.get('assignedtodepartmentid', '')
        url = ("Assets?page={data[page]}&"
               "assignedToUserId={data[assignedtouserid]}&"
               "assignedToCompanyId={data[assignedtocompany]}&"
               "assignedToDepartmentId={data[assignedtodepartmentid]}"
               )
        response = self._make_request(url)
        return json.loads(response.content)
