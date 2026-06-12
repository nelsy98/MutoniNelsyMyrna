users = {
    "alice": {"id": 1, "name": "Alice", "password": "alice123", "role": "Customer", "shipping_location": "CA"},
    "bob":   {"id": 2, "name": "Bob",   "password": "bob123",   "role": "Cashier",  "store_location_id": "NY"},
    "carol": {"id": 3, "name": "Carol", "password": "carol123", "role": "Admin",    "shipping_location": "INTL"},
}

coupons = {
    "SAVE10": {"type": "percentage", "value": 0.10, "start": "2025-01-01", "end": "2026-12-31", "min_order": 50},
    "FLAT20": {"type": "flat_rate",  "value": 20,   "start": "2025-01-01", "end": "2026-12-31", "min_order": 100},
}

tax_rates = {"CA": 0.0825, "NY": 0.08875}  

attempts = 0
logged_in = False

while attempts < 3:
    username = input("Username: ")
    password_attempt = input("Password: ")

    if username in users and users[username]["password"] == password_attempt:
        logged_in = True
        break
    else:
        attempts = attempts + 1
        print(f"Invalid Credentials. Attempts remaining: {3 - attempts}")

if not logged_in:
    print("401 Unauthorized: Access Denied.")
else:
    stored_user = users[username]
    name = stored_user["name"]
    role = stored_user["role"]
    print(f"\nLogin successful. Welcome {name} (Role: {role})\n")

    cart = [
        {"item_price": 25.00, "quantity": 2},   
        {"item_price": 150.00, "quantity": 2},  
        {"item_price": 5.00, "quantity": 4},    
    ]

    coupon_code = input("Enter coupon code (or leave blank): ")
    checkout_date = "2026-06-12"
    manual_override_subtotal = None

    gross_subtotal = 0
    for item in cart:
        gross_subtotal = gross_subtotal + (item["item_price"] * item["quantity"])

    if manual_override_subtotal is not None:
        if role == "Cashier" or role == "Admin":
            gross_subtotal = manual_override_subtotal
        else:
            print("Unauthorized: cannot override subtotal")

    if gross_subtotal >= 500:
        tier_rate = 0.15
    elif gross_subtotal >= 200:
        tier_rate = 0.10
    elif gross_subtotal >= 100:
        tier_rate = 0.05
    else:
        tier_rate = 0.0

    tier_discount = gross_subtotal * tier_rate
    subtotal_after_tier = gross_subtotal - tier_discount

    coupon_discount = 0
    coupon_message = "No coupon applied."

    if coupon_code in coupons:
        c = coupons[coupon_code]

        if checkout_date < c["start"] or checkout_date > c["end"]:
            coupon_message = "Invalid Coupon: expired."
        else:
            if subtotal_after_tier < c["min_order"]:
                coupon_message = f"Invalid Coupon: minimum order of ${c['min_order']} not met."
            else:
                if c["type"] == "percentage":
                    coupon_discount = subtotal_after_tier * c["value"]
                elif c["type"] == "flat_rate":
                    coupon_discount = c["value"]

                if coupon_discount > subtotal_after_tier:
                    coupon_discount = subtotal_after_tier

                coupon_message = f"Coupon '{coupon_code}' applied successfully."
    else:
        if coupon_code:
            coupon_message = "Invalid Coupon: does not exist."

    subtotal_after_coupon = subtotal_after_tier - coupon_discount

    if role == "Cashier":
        location = stored_user.get("store_location_id", "DEFAULT")
    else:
        location = stored_user.get("shipping_location", "DEFAULT")

    if location in tax_rates:
        tax_rate = tax_rates[location]
    else:
        tax_rate = 0.0

    total_tax = subtotal_after_coupon * tax_rate

    final_total = subtotal_after_coupon + total_tax
    if final_total < 0:
        final_total = 0

    print("\n")
    print(f"{'CHECKOUT RECEIPT'}")
    print("\n")
    print(f"Customer: {name} ({role})")
    print("\n")
    print(f"{'Gross Subtotal: '}${gross_subtotal:,}")
    print(f"Tier Discount ({tier_rate*100:.0f}%): -${tier_discount:,.2f}")
    print(f"{'Subtotal after Tier: '}${subtotal_after_tier:,}")
    print(f"{'Coupon Discount: '}-${coupon_discount:,}")
    print(f"  -> {coupon_message}")
    print(f"{'Subtotal after Coupon: '}${subtotal_after_coupon:,}")
    print(f"Tax ({location} @ {tax_rate*100:.3f}%): '+${total_tax:,}")
    print("\n")
    print(f"{'FINAL TOTAL: '}${final_total:,}")
    print("\n")