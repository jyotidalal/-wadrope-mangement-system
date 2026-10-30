import csv
import os
from datetime import datetime

# File paths for storing records
ITEMS_FILE = 'Wardrobe_Items.csv'
CARE_FILE = 'Care_Tasks.csv'
OUTFITS_FILE = 'Outfit_Logs.csv'


def setup_files():
    # Create empty files with headers if they don't exist
    if not os.path.exists(ITEMS_FILE):
        with open(ITEMS_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Item_Name', 'Category', 'Price', 'Wears_Since_Wash', 'Total_Wears'])

    if not os.path.exists(CARE_FILE):
        with open(CARE_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Item_Name', 'Task_Type', 'Due_Date', 'Status'])

    if not os.path.exists(OUTFITS_FILE):
        with open(OUTFITS_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Item_Name', 'Occasion', 'Comfort_Rating', 'Style_Rating'])


def read_csv_rows(filename):
    # Reads rows skipping the first header row and empty rows
    if not os.path.exists(filename):
        return []
    with open(filename, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = []
        is_header = True
        for row in reader:
            if not row or not any(field.strip() for field in row):
                continue
            if is_header:
                is_header = False
                continue
            rows.append(row)
        return rows


def write_csv_rows(filename, header, rows):
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def get_all_item_names():
    rows = read_csv_rows(ITEMS_FILE)
    return [row[0] for row in rows]


# ---------------- INVENTORY & WEAR FUNCTIONS ---------------- #

def add_new_item():
    print("\n--- Add Wardrobe Item ---")
    item_name = input("Enter Item Name (e.g. Blue Denim Jacket): ").strip()
    if not item_name:
        print("Item name cannot be empty.")
        return

    existing = [i.lower() for i in get_all_item_names()]
    if item_name.lower() in existing:
        print(f"'{item_name}' already exists in your wardrobe.")
        return

    print("Categories: 1. Top  2. Bottom  3. Outerwear  4. Footwear  5. Accessory")
    cat_map = {'1': 'Top', '2': 'Bottom', '3': 'Outerwear', '4': 'Footwear', '5': 'Accessory'}
    cat_choice = input("Select Category (1-5): ").strip()
    category = cat_map.get(cat_choice, 'Other')

    try:
        price = float(input("Enter Purchase Price: ").strip())
        if price < 0:
            print("Price cannot be negative.")
            return
    except ValueError:
        print("Please enter a valid number for price.")
        return

    with open(ITEMS_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([item_name, category, f"{price:.2f}", 0, 0])

    print(f"Added '{item_name}' ({category}) priced at {price:.2f}.")


def update_wear_or_wash():
    items = read_csv_rows(ITEMS_FILE)
    if not items:
        print("\nNo items found. Please add an item first.")
        return

    print("\nSelect Wardrobe Item:")
    for idx, row in enumerate(items, 1):
        print(f"{idx}. {row[0]} [{row[1]}] (Wears since wash: {row[3]}, Total wears: {row[4]})")

    try:
        choice = int(input(f"Choice (1-{len(items)}): ").strip())
        if not (1 <= choice <= len(items)):
            print("Invalid choice.")
            return
    except ValueError:
        print("Invalid number.")
        return

    selected = items[choice - 1]
    wears_since_wash = int(selected[3])
    total_wears = int(selected[4])

    print("\n1. Wore item today")
    print("2. Washed / Dry-cleaned item (Reset wash counter)")
    action = input("Enter choice (1 or 2): ").strip()

    if action == '1':
        wears_since_wash += 1
        total_wears += 1
        print(f"Updated: Logged wear for '{selected[0]}'.")
    elif action == '2':
        wears_since_wash = 0
        print(f"Updated: '{selected[0]}' marked as fresh and clean.")
    else:
        print("Invalid choice. Nothing updated.")
        return

    selected[3] = str(wears_since_wash)
    selected[4] = str(total_wears)
    write_csv_rows(ITEMS_FILE, ['Item_Name', 'Category', 'Price', 'Wears_Since_Wash', 'Total_Wears'], items)


def calculate_wash_status(category, wears_since_wash):
    # Threshold simulation based on garment category
    thresholds = {
        'Top': 2,
        'Bottom': 5,
        'Outerwear': 10,
        'Footwear': 15,
        'Accessory': 20
    }
    max_wears = thresholds.get(category, 3)
    remaining = max_wears - wears_since_wash

    if wears_since_wash == 0:
        return remaining, "Fresh / Clean"
    elif remaining > 0:
        return remaining, f"Can wear {remaining} more time(s) before wash"
    elif remaining == 0:
        return 0, "At wash threshold (Wash after next use)"
    else:
        overdue = abs(remaining)
        return -overdue, f"Needs wash! ({overdue} wear(s) overdue)"


def show_wardrobe_report():
    items = read_csv_rows(ITEMS_FILE)
    if not items:
        print("\nNo wardrobe items found.")
        return

    print("\n" + "-" * 88)
    print(f"{'Item Name':<22} | {'Category':<10} | {'Total Wears':<11} | {'CPW':<8} | {'Status'}")
    print("-" * 88)

    for row in items:
        name = row[0]
        cat = row[1]
        price = float(row[2])
        since_wash = int(row[3])
        total_w = int(row[4])

        _, status = calculate_wash_status(cat, since_wash)
        cpw_str = f"{price / total_w:.2f}" if total_w > 0 else "N/A"
        print(f"{name:<22} | {cat:<10} | {total_w:<11} | {cpw_str:<8} | {status}")

    print("-" * 88)


# ---------------- CARE & MAINTENANCE FUNCTIONS ---------------- #

def add_care_task():
    items = get_all_item_names()
    if not items:
        print("\nPlease add at least one wardrobe item first.")
        return

    print("\nSelect Item:")
    for idx, item in enumerate(items, 1):
        print(f"{idx}. {item}")

    try:
        choice = int(input(f"Choice (1-{len(items)}): ").strip())
        if not (1 <= choice <= len(items)):
            print("Invalid choice.")
            return
        item_name = items[choice - 1]
    except ValueError:
        print("Invalid number.")
        return

    task_type = input("Maintenance Task (e.g. Dry Clean, Tailor Hem, Shoe Polish): ").strip()
    if not task_type:
        print("Task description cannot be empty.")
        return

    due_date = input("Target Completion Date (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid format. Please use YYYY-MM-DD.")
        return

    with open(CARE_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([item_name, task_type, due_date, 'Pending'])

    print(f"Scheduled '{task_type}' for {item_name}.")


def complete_care_task():
    tasks = read_csv_rows(CARE_FILE)
    pending = [(idx, row) for idx, row in enumerate(tasks) if row[3].strip().lower() == 'pending']

    if not pending:
        print("\nNo pending maintenance tasks found.")
        return

    print("\nPending Maintenance & Care Tasks:")
    for display_idx, (real_idx, row) in enumerate(pending, 1):
        print(f"{display_idx}. [{row[0]}] {row[1]} (Due: {row[2]})")

    try:
        choice = int(input(f"Select completed task (1-{len(pending)}): ").strip())
        if not (1 <= choice <= len(pending)):
            print("Invalid choice.")
            return
    except ValueError:
        print("Invalid number.")
        return

    target_idx = pending[choice - 1][0]
    tasks[target_idx][3] = 'Completed'

    write_csv_rows(CARE_FILE, ['Item_Name', 'Task_Type', 'Due_Date', 'Status'], tasks)
    print(f"Marked '{tasks[target_idx][1]}' for {tasks[target_idx][0]} as Completed.")


def show_pending_care_tasks():
    tasks = read_csv_rows(CARE_FILE)
    pending = [row for row in tasks if row[3].strip().lower() == 'pending']

    if not pending:
        print("\nNo pending maintenance tasks right now.")
        return

    def parse_due_date(row):
        try:
            return datetime.strptime(row[2], "%Y-%m-%d")
        except ValueError:
            return datetime.max

    pending.sort(key=parse_due_date)

    print("\n" + "-" * 65)
    print(f"{'Item Name':<22} | {'Care Task':<24} | {'Target Date':<12}")
    print("-" * 65)
    for row in pending:
        print(f"{row[0]:<22} | {row[1]:<24} | {row[2]:<12}")
    print("-" * 65)


# ---------------- OUTFIT RATING & VALUE FUNCTIONS ---------------- #

def log_outfit_rating():
    items = get_all_item_names()
    if not items:
        print("\nPlease add at least one wardrobe item first.")
        return

    print("\nSelect Item Worn:")
    for idx, item in enumerate(items, 1):
        print(f"{idx}. {item}")

    try:
        choice = int(input(f"Choice (1-{len(items)}): ").strip())
        if not (1 <= choice <= len(items)):
            print("Invalid choice.")
            return
        item_name = items[choice - 1]
    except ValueError:
        print("Invalid number.")
        return

    occasion = input("Occasion / Event (e.g. Office, Casual Outing, Wedding): ").strip()
    if not occasion:
        print("Occasion cannot be empty.")
        return

    try:
        comfort = float(input("Comfort Rating (1 to 10): ").strip())
        style = float(input("Style Rating (1 to 10): ").strip())
        if not (1.0 <= comfort <= 10.0) or not (1.0 <= style <= 10.0):
            print("Ratings must be between 1 and 10.")
            return
    except ValueError:
        print("Invalid numeric rating entered.")
        return

    with open(OUTFITS_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([item_name, occasion, comfort, style])

    print(f"Recorded ratings (Comfort: {comfort}/10, Style: {style}/10) for {item_name}.")


def show_all_outfit_logs():
    logs = read_csv_rows(OUTFITS_FILE)
    if not logs:
        print("\nNo outfit ratings logged yet.")
        return

    grouped = {}
    for row in logs:
        item, occ, comf, sty = row[0], row[1], float(row[2]), float(row[3])
        if item not in grouped:
            grouped[item] = []
        grouped[item].append((occ, comf, sty))

    print("\n--- ALL RECORDED OUTFIT RATINGS ---")
    for item, entries in grouped.items():
        print(f"\n{item}:")
        for occ, comf, sty in entries:
            avg = (comf + sty) / 2.0
            print(f"  - {occ}: Comfort {comf:.1f}/10, Style {sty:.1f}/10 (Overall: {avg:.1f}/10)")


def calculate_wardrobe_index():
    items = read_csv_rows(ITEMS_FILE)
    logs = read_csv_rows(OUTFITS_FILE)
    if not items or not logs:
        return None

    item_scores = {}
    for row in logs:
        item = row[0]
        comf = float(row[2])
        sty = float(row[3])
        if item not in item_scores:
            item_scores[item] = [0.0, 0]
        item_scores[item][0] += (comf + sty) / 2.0
        item_scores[item][1] += 1

    total_weighted_score = 0.0
    total_evaluated_wears = 0

    for row in items:
        item = row[0]
        wears = int(row[4])
        weight = max(1, wears)
        if item in item_scores and item_scores[item][1] > 0:
            avg_item_score = item_scores[item][0] / item_scores[item][1]
            total_weighted_score += (avg_item_score * weight)
            total_evaluated_wears += weight

    if total_evaluated_wears == 0:
        return None

    return total_weighted_score / total_evaluated_wears, len(item_scores)


def show_wardrobe_index():
    stats = calculate_wardrobe_index()
    if stats is None:
        print("\nNot enough outfit ratings logged to calculate Wardrobe Satisfaction Index.")
        return

    index_score, rated_count = stats
    print("\n--- WARDROBE SATISFACTION INDEX ---")
    print(f"Total Rated Items           : {rated_count}")
    print(f"Overall Satisfaction (10-pt): {index_score:.2f} / 10.00")


# ---------------- DASHBOARD & DEEP DIVE ---------------- #

def item_deep_dive():
    items = read_csv_rows(ITEMS_FILE)
    if not items:
        print("\nNo wardrobe items found.")
        return

    print("\nSelect Item:")
    for idx, row in enumerate(items, 1):
        print(f"{idx}. {row[0]}")

    try:
        choice = int(input(f"Choice (1-{len(items)}): ").strip())
        if not (1 <= choice <= len(items)):
            print("Invalid choice.")
            return
    except ValueError:
        print("Invalid number.")
        return

    selected = items[choice - 1]
    item_name = selected[0]
    category = selected[1]
    price = float(selected[2])
    since_wash = int(selected[3])
    total_wears = int(selected[4])

    print("\n" + "=" * 55)
    print(f"ITEM SUMMARY: {item_name.upper()} ({category})")
    print("=" * 55)

    # Wear & Cost Stats
    _, status = calculate_wash_status(category, since_wash)
    cpw_str = f"{price / total_wears:.2f}" if total_wears > 0 else "N/A"
    print(f"\nPurchase Price   : {price:.2f}")
    print(f"Total Wears      : {total_wears} (Cost Per Wear: {cpw_str})")
    print(f"Wears Since Wash : {since_wash}")
    print(f"Hygiene Status   : {status}")

    # Care Tasks
    tasks = read_csv_rows(CARE_FILE)
    item_tasks = [r for r in tasks if r[0].lower() == item_name.lower()]
    print("\nMaintenance & Care Logs:")
    if not item_tasks:
        print("  None scheduled.")
    else:
        for t in item_tasks:
            print(f"  - {t[1]} (Target: {t[2]}) [{t[3]}]")

    # Outfit Ratings
    logs = read_csv_rows(OUTFITS_FILE)
    item_logs = [r for r in logs if r[0].lower() == item_name.lower()]
    print("\nOutfit Ratings:")
    if not item_logs:
        print("  None logged.")
    else:
        tot_comf, tot_sty = 0.0, 0.0
        for l in item_logs:
            c, s = float(l[2]), float(l[3])
            tot_comf += c
            tot_sty += s
            print(f"  - {l[1]}: Comfort {c:.1f}/10, Style {s:.1f}/10")
        count = len(item_logs)
        print(f"  Average: Comfort {tot_comf/count:.1f}/10 | Style {tot_sty/count:.1f}/10")


def show_daily_style_dashboard():
    items = read_csv_rows(ITEMS_FILE)
    tasks = read_csv_rows(CARE_FILE)

    print("\n" + "=" * 55)
    print("               DAILY WARDROBE DASHBOARD")
    print("=" * 55)

    # 1. Laundry Alerts
    print("\n1. LAUNDRY & WASH ALERTS:")
    alert_count = 0
    for row in items:
        try:
            name, cat = row[0], row[1]
            since_wash = int(row[3])
        except (ValueError, IndexError):
            continue

        rem, status = calculate_wash_status(cat, since_wash)
        if rem <= 0:
            alert_count += 1
            print(f"   ! {name} ({cat}): {since_wash} wears -> {status}")
    if alert_count == 0:
        print("   All wardrobe items are clean and ready to wear.")

    # 2. Upcoming Care Tasks
    print("\n2. UPCOMING MAINTENANCE TASKS:")
    pending = [r for r in tasks if len(r) >= 4 and r[3].strip().lower() == 'pending']

    def parse_due_date(row):
        try:
            return datetime.strptime(row[2], "%Y-%m-%d")
        except ValueError:
            return datetime.max

    pending.sort(key=parse_due_date)
    top_3 = pending[:3]
    if not top_3:
        print("   No pending care or repair tasks.")
    else:
        for idx, task in enumerate(top_3, 1):
            print(f"   {idx}. {task[1]} ({task[0]}) - Target: {task[2]}")

    # 3. Wardrobe Satisfaction Index
    print("\n3. WARDROBE SATISFACTION INDEX:")
    stats = calculate_wardrobe_index()
    if stats:
        idx_score, _ = stats
        print(f"   Current Style & Comfort Rating: {idx_score:.2f} / 10.00")
    else:
        print("   No outfit ratings logged yet.")
    print("=" * 55)


# ---------------- MAIN APPLICATION LOOP ---------------- #

def print_menu():
    print("\n--- Wardrobe Management System ---")
    print("1.  Daily Style Dashboard")
    print("2.  Add New Wardrobe Item")
    print("3.  Log Outfit Wear / Wash")
    print("4.  Wardrobe Usage & Laundry Report")
    print("5.  Schedule Care / Repair Task")
    print("6.  View Pending Care Tasks")
    print("7.  Mark Care Task as Completed")
    print("8.  Log Outfit Comfort & Style Rating")
    print("9.  View All Outfit Ratings")
    print("10. View Wardrobe Satisfaction Index")
    print("11. Item Deep Dive")
    print("0.  Exit")


def main():
    setup_files()

    while True:
        print_menu()
        choice = input("Enter choice (0-11): ").strip()

        if choice == '1':
            show_daily_style_dashboard()
        elif choice == '2':
            add_new_item()
        elif choice == '3':
            update_wear_or_wash()
        elif choice == '4':
            show_wardrobe_report()
        elif choice == '5':
            add_care_task()
        elif choice == '6':
            show_pending_care_tasks()
        elif choice == '7':
            complete_care_task()
        elif choice == '8':
            log_outfit_rating()
        elif choice == '9':
            show_all_outfit_logs()
        elif choice == '10':
            show_wardrobe_index()
        elif choice == '11':
            item_deep_dive()
        elif choice == '0':
            print("\nExiting. Wardrobe records saved.\n")
            break
        else:
            print("Invalid choice. Please select 0 to 11.")


if __name__ == "__main__":
    main()
