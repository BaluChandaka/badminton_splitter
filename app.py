import streamlit as st

# 1. Page Configuration & Styling
st.set_page_config(
    page_title="Badminton Splitter", 
    page_icon="🏸", 
    layout="centered"
)

st.title("🏸 Badminton Expense Splitting Agent")
st.write("Enter your group details below to calculate a payment plan with the fewest transactions.")

# 2. Dynamic Input for Names
names_str = st.text_input(
    "1. Enter everyone's names (separated by commas):", 
    value="Person 1, Person 2, Person 3"
)

# Convert the string into a clean list of unique names
participants = [name.strip() for name in names_str.split(",") if name.strip()]
# Remove duplicates while preserving order
participants = list(dict.fromkeys(participants))
num_people = len(participants)

if num_people < 2:
    st.warning("Please enter at least 2 participants to split expenses.")
else:
    st.markdown("---")
    st.write("### 💰 2. Enter what each person paid:")
    
    # Create dynamic input fields using columns for a cleaner layout
    expenses = {}
    cols = st.columns(2)
    
    for index, name in enumerate(participants):
        # Even indexes go to column 1, odd indexes go to column 2
        with cols[index % 2]:
            expenses[name] = st.number_input(
                f"Total amount paid by {name}:", 
                min_value=0.0, 
                value=0.0, 
                step=1.0, 
                key=f"pay_{name}"
            )

    # 3. Calculation Trigger Button
    if st.button("Calculate Splits", type="primary"):
        total_expense = sum(expenses.values())
        share_per_person = round(total_expense / num_people, 2)
        
        st.markdown("---")
        st.subheader("📊 Results Summary")
        
        # Display summary boxes
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric("Total Session Cost", f"${total_expense:.2f}")
        with metric_col2:
            st.metric("Individual Share", f"${share_per_person:.2f}")
            
        # Calculate net balances (paid amount minus what they actually owe)
        balances = {name: round(paid - share_per_person, 2) for name, paid in expenses.items()}
        
        # Filter into who gets money back (creditors) and who owes money (debtors)
        creditors = [[name, bal] for name, bal in balances.items() if bal > 0]
        debtors = [[name, -bal] for name, bal in balances.items() if bal < 0]
        
        st.subheader("💸 Optimized Payment Plan")
        
        has_transactions = False
        plan = []
        
        # Greedy algorithm: Match the largest debtor with the largest creditor
        for debtor in debtors:
            d_name, d_amount = debtor
            while d_amount > 0.01:
                for creditor in creditors:
                    c_name, c_amount = creditor
                    if c_amount > 0.01:
                        transfer = min(d_amount, c_amount)
                        transfer = round(transfer, 2)
                        
                        if transfer > 0:
                            plan.append(f"**{d_name}** pays **${transfer:.2f}** to **{c_name}**")
                            has_transactions = True
                            
                        d_amount -= transfer
                        creditor[1] -= transfer
                        break
                else:
                    break
                    
        # Output the step-by-step settlement plan
        if has_transactions:
            for step in plan:
                st.write(f"👉 {step}")
        else:
            st.success("Everyone spent the exact same amount! No transfers needed.")