import datetime as dt
import pandas as pd

shop_name = "WALMART"
address = "Shop no. 8, Wazirpura Road"
city = "Agra"
pincode = "282004"
gst_no = "768259477Z0"

def process_items(items):
    try:
        df = pd.read_csv("items.csv")
    except FileNotFoundError:
        print('''*******************
items.csv not found, it contains the item information and is required for the code to function.
Download sample from here: https://pastebin.com/hs5Awyam
*******************''')
        return []

    item_table = []
    for item_code, quantity in items:
        item_row = df[df['item_code'] == item_code]
        if item_row.empty:
            print(f"Item with code {item_code} not found.")
        else:
            item_data = item_row.iloc[0].to_dict()
            item_data['quantity'] = quantity
            item_data['amount'] = item_data['price'] * quantity
            item_table.append(item_data)

    return  pd.DataFrame(item_table)



def generate_invoice_number():
  try:
    with open("invoice_number.txt","r") as f:
      invoice_number = f.read()
    invoice_number = int(invoice_number)
    invoice_number += 1
  except FileNotFoundError:
    invoice_number = 1
  with open("invoice_number.txt","w") as f:
    f.write(str(invoice_number))
  return invoice_number

def display(cust_name,cust_no,invoice_id,items,payment_method):
  global shop_name,address,city,pincode,gst_no
  print("\n\n\n")
  print(f"******{shop_name}******")
  print(f'{address}\n{city}-{pincode}')
  print(f"GST-IN: {gst_no}")
  print(f'\nTo {cust_name.upper()}\nMobile No. {cust_no}\n\nInvoice No.{invoice_id}\n')
  print(f"\tDate: {dt.datetime.now().strftime('%d-%m-%Y')}")
  print(f"\tTime: {dt.datetime.now().strftime('%H:%M:%S')}\n")

  item_table = process_items(items)
  print(item_table[['item_name', 'quantity', 'price', 'tax', 'amount']].to_string(index=False))

  total_amount = item_table['amount'].sum()
  total_taxes = (round(0.01*item_table['tax']*item_table['amount'],2)).sum()

  print(f"\nSub Total: {total_amount}")
  print(f"Total Taxes: {total_taxes}")
  print(f"Grand Total: {total_amount + total_taxes}")

  print(f"Total Items: {len(item_table)} \tTotal Quantity: {item_table['quantity'].sum()}")
  print(f"Payment Method: {payment_method.upper()}\n")

  print("**THANK YOU VISIT AGAIN!**")

  print("Terms and conditions apply.")


def get_input():
  items = []
  ch = 1
  while(ch!=0):
    i = input("Scan Item code(0 to exit): ")
    if i=="0" or i=="":
      break
    else:
      i = int(i)
    q = input("Quantity(default 1): ")
    if q=="":
      q=1
    else:
      q=int(q)
    items.append((i,q))
  cn = input("Enter customer name: ")
  cp = input("Enter customer phone no.: ")
  pay = input("Enter payment method: ")
  invoice_number = generate_invoice_number()
  display(cn,cp,invoice_number,items,pay)

get_input() 