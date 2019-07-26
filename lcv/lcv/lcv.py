from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import date

@frappe.whitelist(allow_guest=True)
def updateJV(doc,method):
	account_list=[]
	account_json={}
	account_json["account"]="Expenses Included In Valuation - BABJI"
	account_json["debit"]=doc.total_taxes_and_charges
	account_json["debit_in_account_currency"]=doc.total_taxes_and_charges
	account_json["cost_center"]=doc.cost_center
	account_list.append(account_json)
	for row in doc.taxes:
		account_json={}
		account_json["party_type"]="Supplier"
                account_json["party"]=row.supplier
		account_json["account"]=row.account
		account_json["credit"]=row.amount
		account_json["credit_in_account_currency"]=row.amount
		account_json["cost_center"]=row.cost_center
		account_list.append(account_json)

        jv = frappe.get_doc({
        "doctype": "Journal Entry",
        "posting_date": doc.invoice_date,
        "naming_series":"OP-JV-.YY.-",
        "voucher_type":"Journal Entry",
	"voucher_number":doc.name,
        "accounts":account_list
	})
        jv.insert(ignore_permissions=True)
        jv.submit()

@frappe.whitelist(allow_guest=True)
def UpdateLCV(doc,method):
	doc_jv = frappe.get_doc("Landed Cost Voucher", doc.voucher_number)
	doc_jv.jv = doc.name
	doc_jv.save()

@frappe.whitelist(allow_guest=True)
def cancelJV(doc,method):
        doc_jv = frappe.get_doc("Journal Entry", doc.jv)
        doc_jv.cancel()
