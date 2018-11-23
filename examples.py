from jitbit import JitBitAPI as Jitbit

JITBIT_URL = ''
JITBIT_USERNAME = ''
JITBIT_PASSWORD = ''

tickets = Jitbit(JITBIT_URL, JITBIT_USERNAME, JITBIT_PASSWORD)

### get_tickets
### Response: JSON
### print (tickets.get_tickets(statusId=1))

### get_tickets_by_id
### Response: JSON
### print (tickets.get_ticket_by_id(1000))

### create_ticket
### Response: Ticket ID
### print (tickets.create_ticket(8, "(BODY)", "(SUBJECT)", 1, "", "info"))

### get_users
### Response: JSON
### print (tickets.get_users())

### create_user(self, username, password, email, first_name, last_name, company, department, phone="", location="", send_welcome_email=False)
### Response: User ID
### print (tickets.create_user("username", "password123", "dalai@lama.org", "Dalai", "Lama", "Company", "Department"))

### update_user_by_id(self, user_id, username, email, first_name, last_name, company, phone, location, password=None, notes="", department="", disabled=False)
### Response: True or False
### print (tickets.update_user_by_id(346, "username_new"))

### get_companies
### Response: JSON
### #print (tickets.get_companies())

### get_categories
### Response: JSON
#print (tickets.get_categories())

### get_articles
### Response: JSON
###print (tickets.get_articles())

### get_articles_by_id
### Response: JSON
### print (tickets.get_article_by_id(5632))

### get_assets
### Response: JSON
### print (tickets.get_assets())

### update_ticket ###