"""Generate scrubbed demo data: one entity, USD, income statement, Aug-Sep 2026.
Planted cases: clean tie (6120, 4010), tie-out mismatch (6200), backwards balance (6350), no detail (6400)."""
import csv, json
ACCTS = {  # code: (name, natural)
 "4010":("Service revenue","credit"),"5010":("Salaries","debit"),"6120":("Software subscriptions","debit"),
 "6200":("Professional fees","debit"),"6350":("Meals","debit"),"6400":("Contract labor","debit"),
 "6500":("Rent","debit"),"6600":("Utilities","debit")}
V=[]  # (voucher, date, acct, amount, desc, counterparty, layer)
def add(v,d,a,amt,desc,cp,layer="Current"): V.append((v,d,a,amt,desc,cp,layer))
# 4010 revenue (credit = negative)
add("INV0001","2026-08-15","4010",-300000,"Monthly service fee","Customer P")
add("INV0002","2026-08-20","4010",-220000,"Monthly service fee","Customer Q")
add("INV0101","2026-09-15","4010",-300000,"Monthly service fee","Customer P")
add("INV0102","2026-09-20","4010",-233000,"Monthly service fee incl. added seats","Customer Q")
add("INV0103","2026-09-25","4010",-15000,"New customer onboarding fee","Customer R")
# 5010 salaries
add("PAY0801","2026-08-31","5010",310000,"Payroll","Payroll provider")
add("PAY0901","2026-09-30","5010",312400,"Payroll","Payroll provider")
# 6120 software
add("AP0801","2026-08-10","6120",30000,"Core platform subscription","Vendor C")
add("AP0802","2026-08-12","6120",12000,"Usage charges","Vendor B")
add("AP0901","2026-09-10","6120",30000,"Core platform subscription","Vendor C")
add("AP0902","2026-09-12","6120",17500,"Usage charges","Vendor B")
add("AP0903","2026-09-14","6120",24000,"Annual license","Vendor A")
add("FC0901","2026-09-30","6120",9999,"Forecast accrual (not actuals)","Vendor A","Forecast")
# 6200 professional fees (statement will show 61,000; detail sums 58,000)
add("AP0803","2026-08-18","6200",18000,"Advisory services","Firm L")
add("AP0904","2026-09-08","6200",18000,"Advisory services","Firm L")
add("AP0905","2026-09-22","6200",40000,"Project services","Firm M")
# 6350 meals (backwards in Sep)
add("EX0801","2026-08-28","6350",4000,"Team meals","Employee expenses")
add("EX0901","2026-09-12","6350",2300,"Team meals","Employee expenses")
add("EX0902","2026-09-27","6350",-3500,"Refund of event deposit","Caterer")
# 6500 rent, 6600 utilities
for m,d in (("08","2026-08-01"),("09","2026-09-01")): add("AP%s10"%m,d,"6500",25000,"Office rent","Landlord")
add("AP0820","2026-08-20","6600",3100,"Utilities","Utility co"); add("AP0920","2026-09-20","6600",3350,"Utilities","Utility co")
# 6400 contract labor: statement only, no voucher rows (planted no-detail case)
cur=lambda a,m:sum(x[3] for x in V if x[2]==a and x[1][5:7]==m and x[6]=="Current")
stmt=[]
for a,(n,nat) in ACCTS.items():
    p,c=cur(a,"08"),cur(a,"09")
    if a=="6200": c=61000      # planted mismatch (statement vs detail)
    if a=="6400": p,c=12000,40000  # planted no-detail
    stmt.append((a,n,p,c,c-p))
with open("demo_statement.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["Account","Name","Prior Month","Current Month","Change"]); w.writerows(stmt)
with open("demo_vouchers.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["Voucher","Date","Account display value","Account name","Currency","Amount","Posting layer","Description","Name2","Company accounts ID"])
    for v,d,a,amt,desc,cp,l in V: w.writerow([v,d,a,ACCTS[a][0],"USD",amt,l,desc,cp,"DEMO"])
NOTES={"6120":"Name each counterparty behind the change and say whether the movement is a new charge or a change in an existing counterparty's amount.",
 "6350":"A credit on this account is usually a refund or reversal; describe it from the entry description, not as spending.",
 "6400":"If no transaction detail exists, say so plainly; do not guess at contractors or reasons."}
json.dump({"threshold":25000,"naturals":{a:x[1] for a,x in ACCTS.items()},"notes":NOTES},open("demo_config.json","w"),indent=1)
print(open("demo_statement.csv").read())
