# examples.md
Natural Language → Blue Prism Mapping + XML Skeleton (Few-Shot Examples)

Rule:
- INPUT = Natural language description
- OUTPUT = Blue Prism stage mapping
- XML Skeleton = minimal, demo-safe (no secrets)

---

## EXAMPLE 1 — Password Reset Automation (Email + AD + ServiceNow)

INPUT
Reset user password based on an email request. Read email from Outlook queue, extract User ID and Ticket ID. Login to Active Directory, search user, reset password, send confirmation email, and update ServiceNow ticket. If user not found or login fails, update ticket as Failed.

OUTPUT
Process Name: Password_Reset_Automation

Stages:
Start → Read_Email → Login_AD → Check_Login → Search_User → User_Exists
User_Exists(True) → Reset_Password → Send_Email → Update_SN_Success → End
User_Exists(False) → Update_SN_Failed → End
Check_Login(False) → Exception_Handler → End

XML Skeleton:
```xml
<process name="Password_Reset_Automation">
  <stage name="Start" type="Start"/>
  <stage name="Read_Email" type="Action"/>
  <stage name="Login_AD" type="Action"/>
  <stage name="Check_Login" type="Decision"/>
  <stage name="Search_User" type="Action"/>
  <stage name="User_Exists" type="Decision"/>
  <stage name="Reset_Password" type="Action"/>
  <stage name="Send_Email" type="Action"/>
  <stage name="Update_SN_Success" type="Action"/>
  <stage name="Update_SN_Failed" type="Action"/>
  <stage name="Exception_Handler" type="Exception"/>
  <stage name="End" type="End"/>
</process>
```

---

## EXAMPLE 2 — CrowdStrike Asset Decommission

INPUT
Get Helix ticket details, login to CrowdStrike, search asset by hostname. If found, decommission and close ticket. If not found, update worklog and keep ticket pending.

OUTPUT
Process Name: CrowdStrike_Asset_Decommission

Stages:
Start → Get_Helix_Ticket → Login_CrowdStrike → Check_Login → Search_Asset → Asset_Found
Asset_Found(True) → Decommission_Asset → Update_Helix_Success → End
Asset_Found(False) → Update_Helix_Not_Found → End
Check_Login(False) → Exception_Handler → End

XML Skeleton:
```xml
<process name="CrowdStrike_Asset_Decommission">
  <stage name="Start" type="Start"/>
  <stage name="Get_Helix_Ticket" type="Action"/>
  <stage name="Login_CrowdStrike" type="Action"/>
  <stage name="Check_Login" type="Decision"/>
  <stage name="Search_Asset" type="Action"/>
  <stage name="Asset_Found" type="Decision"/>
  <stage name="Decommission_Asset" type="Action"/>
  <stage name="Update_Helix_Success" type="Action"/>
  <stage name="Update_Helix_Not_Found" type="Action"/>
  <stage name="Exception_Handler" type="Exception"/>
  <stage name="End" type="End"/>
</process>
```

---

## EXAMPLE 3 — Helix DLP Whitelisting Search

INPUT
Search Helix for Endpoint Security tickets related to DLP Whitelisting. If no work orders are found, end process.

OUTPUT
Process Name: Helix_DLP_Whitelisting_Search

Stages:
Start → Build_Query → HTTP_Get → Validate_Response → Parse_Result → WO_Found
WO_Found(True) → End_With_Data
WO_Found(False) → End_No_Data

XML Skeleton:
```xml
<process name="Helix_DLP_Whitelisting_Search">
  <stage name="Start" type="Start"/>
  <stage name="Build_Query" type="Calculation"/>
  <stage name="HTTP_Get" type="Action"/>
  <stage name="Validate_Response" type="Decision"/>
  <stage name="Parse_Result" type="Action"/>
  <stage name="WO_Found" type="Decision"/>
  <stage name="End_With_Data" type="End"/>
  <stage name="End_No_Data" type="End"/>
</process>
```

---

## EXAMPLE 4 — Qualys Tag Create and Update

INPUT
Read tag details from Excel. Create tags in Qualys via API. Verify creation and update tag name.

OUTPUT
Process Name: Qualys_Tag_Create_Update

Stages:
Start → Read_Excel → Loop_Tags → Create_Tag → Verify_Tag → Update_Tag → End

XML Skeleton:
```xml
<process name="Qualys_Tag_Create_Update">
  <stage name="Start" type="Start"/>
  <stage name="Read_Excel" type="Action"/>
  <stage name="Loop_Tags" type="LoopStart"/>
  <stage name="Create_Tag" type="Action"/>
  <stage name="Verify_Tag" type="Decision"/>
  <stage name="Update_Tag" type="Action"/>
  <stage name="End" type="End"/>
</process>
```

---

## EXAMPLE 5 — McAfee Policy Exception

INPUT
Fetch Helix ticket, login to McAfee ePO, add policy exception, update Helix ticket.

OUTPUT
Process Name: McAfee_Policy_Exception

Stages:
Start → Get_Helix_Ticket → Login_McAfee → Search_Policy → Add_Exception → Update_Helix → End

XML Skeleton:
```xml
<process name="McAfee_Policy_Exception">
  <stage name="Start" type="Start"/>
  <stage name="Get_Helix_Ticket" type="Action"/>
  <stage name="Login_McAfee" type="Action"/>
  <stage name="Search_Policy" type="Action"/>
  <stage name="Add_Exception" type="Action"/>
  <stage name="Update_Helix" type="Action"/>
  <stage name="End" type="End"/>
</process>
```

---

## EXAMPLE 6 — Remedy Ticket Lookup

INPUT
Search Remedy for DLP Whitelisting tickets and return Work Order IDs.

OUTPUT
Process Name: Remedy_Ticket_Search

Stages:
Start → Search_Tickets → WO_Found → End

XML Skeleton:
```xml
<process name="Remedy_Ticket_Search">
  <stage name="Start" type="Start"/>
  <stage name="Search_Tickets" type="Action"/>
  <stage name="WO_Found" type="Decision"/>
  <stage name="End" type="End"/>
</process>
```

---

## EXAMPLE 7 — HTTP Retry Pattern

INPUT
Retry HTTP API calls up to 3 times with backoff if API fails.

OUTPUT
Process Name: HTTP_Retry_Pattern

Stages:
Start → HTTP_Call → Success?
Success(True) → End
Success(False) → Retry → HTTP_Call

XML Skeleton:
```xml
<process name="HTTP_Retry_Pattern">
  <stage name="Start" type="Start"/>
  <stage name="HTTP_Call" type="Action"/>
  <stage name="Success" type="Decision"/>
  <stage name="Retry" type="Action"/>
  <stage name="End" type="End"/>
</process>
```

---

## EXAMPLE 8 — Bulk CrowdStrike Tagging

INPUT
Read hostnames from Excel and tag assets in CrowdStrike.

OUTPUT
Process Name: Bulk_CrowdStrike_Tagging

Stages:
Start → Read_Excel → Login → Loop_Hosts → Search_Asset → Apply_Tag → End

XML Skeleton:
```xml
<process name="Bulk_CrowdStrike_Tagging">
  <stage name="Start" type="Start"/>
  <stage name="Read_Excel" type="Action"/>
  <stage name="Login" type="Action"/>
  <stage name="Loop_Hosts" type="LoopStart"/>
  <stage name="Search_Asset" type="Action"/>
  <stage name="Apply_Tag" type="Action"/>
  <stage name="End" type="End"/>
</process>
```

---

## EXAMPLE 9 — Helix Assignment Automation

INPUT
Assign Helix tickets to BOT and update worklog.

OUTPUT
Process Name: Helix_Assign_To_Bot

Stages:
Start → Search_Tickets → Loop_Tickets → Update_Assignee → Add_Worklog → End

XML Skeleton:
```xml
<process name="Helix_Assign_To_Bot">
  <stage name="Start" type="Start"/>
  <stage name="Search_Tickets" type="Action"/>
  <stage name="Loop_Tickets" type="LoopStart"/>
  <stage name="Update_Assignee" type="Action"/>
  <stage name="Add_Worklog" type="Action"/>
  <stage name="End" type="End"/>
</process>
```

---

## EXAMPLE 10 — Endpoint Decommission via Ticket

INPUT
Process endpoint decommission request from ticket and update endpoint tool.

OUTPUT
Process Name: Endpoint_Decommission

Stages:
Start → Get_Ticket → Login_Tool → Decommission → Update_Ticket → End

XML Skeleton:
```xml
<process name="Endpoint_Decommission">
  <stage name="Start" type="Start"/>
  <stage name="Get_Ticket" type="Action"/>
  <stage name="Login_Tool" type="Action"/>
  <stage name="Decommission" type="Action"/>
  <stage name="Update_Ticket" type="Action"/>
  <stage name="End" type="End"/>
</process>
```
