import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Coorg Tyre Shop Billing", layout="wide")

st.title("🛞 Coorg Tyre Puncher Shop")
st.write("ടയർ സ്റ്റോക്ക് & ബില്ലിംഗ് മാനേജുമെന്റ് സിസ്റ്റം")

# മെനു ഓപ്ഷനുകൾ
menu = st.sidebar.selectbox("메നു (Menu)", ["ബില്ലിംഗ് (Billing)", "സ്റ്റോക്ക് ആഡ് ചെയ്യുക (Add Stock)", "റിപ്പോർട്ട് (Reports)"])

# ഡാറ്റ സേവ് ചെയ്യാൻ ലളിതമായി സെഷൻ സ്റ്റേറ്റ് ഉപയോഗിക്കുന്നു
if 'stock' not in st.session_state:
    st.session_state['stock'] = pd.DataFrame(columns=["Item Name", "Category", "Buy Price", "Sell Price", "Quantity"])

if 'sales' not in st.session_state:
    st.session_state['sales'] = []

# 1. സ്റ്റോക്ക് ആഡ് ചെയ്യുന്ന ഭാഗം
if menu == "സ്റ്റോക്ക് ആഡ് ചെയ്യുക (Add Stock)":
    st.header("പുതിയ സ്റ്റോക്ക് ചേർക്കുക")
    with st.form("stock_form"):
        item_name = st.text_input("ഐറ്റത്തിന്റെ പേര് (ഉദാ: MRF Tyre 100/90)")
        category = st.selectbox("വിഭാഗം", ["Tyre", "Tube", "Puncture Material", "Other"])
        buy_price = st.number_input("വാങ്ങിയ വില (Buying Price)", min_value=0.0)
        sell_price = st.number_input("വിൽപ്പന വില (Selling Price)", min_value=0.0)
        quantity = st.number_input("അളവ് (Quantity)", min_value=1, step=1)
        
        submit = st.form_submit_button("സ്റ്റോക്ക് സേവ് ചെയ്യുക")
        if submit:
            new_row = pd.DataFrame([[item_name, category, buy_price, sell_price, quantity]], 
                                   columns=["Item Name", "Category", "Buy Price", "Sell Price", "Quantity"])
            st.session_state['stock'] = pd.concat([st.session_state['stock'], new_row], ignore_index=True)
            st.success(f" સફળതയോടെ സേവ് ചെയ്തു: {item_name}")

    st.subheader("നിലവിലുള്ള സ്റ്റോക്ക്")
    st.dataframe(st.session_state['stock'])

# 2. ബില്ലിംഗ് ഭാഗം
elif menu == "ബില്ലിംഗ് (Billing)":
    st.header("കസ്റ്റമർ ബില്ലിംഗ്")
    if st.session_state['stock'].empty:
        st.warning("ആദ്യം 'Add Stock' വഴി സാധനങ്ങൾ ചേർക്കുക!")
    else:
        customer_name = st.text_input("കസ്റ്റമറുടെ പേര്")
        phone_number = st.text_input("ഫോൺ നമ്പർ")
        payment_mode = st.selectbox("പേയ്മെന്റ് രീതി", ["Cash", "UPI (GPay/PhonePe)", "Pending"])
        
        selected_item = st.selectbox("സാധനം തിരഞ്ഞെടുക്കുക", st.session_state['stock']['ItemName'].tolist())
        qty = st.number_input("എണ്ണം", min_value=1, value=1)
        
        if st.button("ബില്ലിൽ ചേർക്കുക"):
            item_details = st.session_state['stock'][st.session_state['stock']['ItemName'] == selected_item].iloc[0]
            total_price = item_details['Sell Price'] * qty
            
            st.write(f"**ആകെ തുക:** Rs. {total_price}")
            if st.button("ബിൽ പൂർത്തിയാക്കുക"):
                sale_record = {
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Customer": customer_name,
                    "Phone": phone_number,
                    "Item": selected_item,
                    "Qty": qty,
                    "Total": total_price,
                    "Mode": payment_mode
                }
                st.session_state['sales'].append(sale_record)
                st.success("ബിൽ വിജയകരമായി ജനറേറ്റ് ചെയ്തു!")

# 3. റിപ്പോർട്ട് ഭാഗം
elif menu == "റിപ്പോർട്ട് (Reports)":
    st.header("വിൽപ്പന വിവരങ്ങൾ")
    if len(st.session_state['sales']) > 0:
        sales_df = pd.DataFrame(st.session_state['sales'])
        st.dataframe(sales_df)
        total_revenue = sales_df['Total'].sum()
        st.metric(label="ആകെ വിൽപ്പന (Total Revenue)", value=f"Rs. {total_revenue}")
    else:
        st.info("ഇതുവരെ വിൽപ്പനകൾ ഒന്നും രേഖപ്പെടുത്തിയിട്ടില്ല.")
