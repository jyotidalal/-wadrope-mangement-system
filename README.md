# -wadrope-mangement-system
# 👗 Smart Wardrobe Organizer

**A Python-Based Wardrobe Management System**

Smart Wardrobe Organizer is a menu-driven Python application that helps users manage their clothing collection, track clothing usage, monitor washing requirements, schedule maintenance tasks, and evaluate outfit comfort and style ratings.

The application uses CSV files to store records permanently and provides a daily dashboard for monitoring wardrobe activities.

## ✨ Features

### 1. Wardrobe Management
- Add new clothing items.
- Categorize clothes into Top, Bottom, Outerwear, Footwear, and Accessory.
- Store purchase prices.
- Prevent duplicate clothing entries.

### 2. Wear & Wash Tracking
- Record when an item is worn.
- Track total wears and wears since the last wash.
- Reset the washing counter after washing or dry-cleaning.
- Calculate washing status using category-based thresholds.

### 3. Wardrobe Usage & Laundry Report
- Display clothing categories and total usage.
- Calculate Cost Per Wear (CPW).
- Display the current washing status of each item.

### 4. Care & Maintenance Management
- Schedule maintenance tasks for wardrobe items.
- Add tasks such as dry cleaning, tailoring, and shoe polishing.
- Set target completion dates.
- View pending tasks sorted by due date.
- Mark maintenance tasks as completed.

### 5. Outfit Comfort & Style Ratings
- Record the occasion for which an item was worn.
- Assign comfort ratings between 1 and 10.
- Assign style ratings between 1 and 10.
- View previously recorded outfit ratings.

### 6. Wardrobe Satisfaction Index
- Calculate average comfort and style ratings.
- Generate an overall wardrobe satisfaction score out of 10.
- Use clothing usage as a weighting factor in the calculation.

### 7. Daily Style Dashboard
Provides a combined overview of:
- Laundry and washing alerts.
- Upcoming maintenance tasks.
- Wardrobe Satisfaction Index.

### 8. Item Deep Dive
Displays detailed information about an individual clothing item, including:
- Purchase price.
- Total wears.
- Cost per wear.
- Washing status.
- Maintenance history.
- Average comfort and style ratings.

---

## 🛠️ Technologies Used

| Technology | Application |
|---|---|
| Python | Application development |
| CSV | Storing wardrobe records |
| OS | Checking and managing files |
| DateTime | Date validation and maintenance scheduling |

## 🧠 Python Concepts & Data Structures

The project demonstrates the following concepts:

- **Lists:** Storing and managing wardrobe records.
- **Dictionaries:** Grouping outfit ratings and defining washing thresholds.
- **List Comprehension:** Filtering clothing records and pending tasks.
- **Functions:** Organizing application operations into reusable functions.
- **File Handling:** Reading and writing CSV files.
- **Exception Handling:** Managing invalid inputs and date formats.
- **Sorting:** Arranging maintenance tasks according to due dates.
- **Lambda / Key-based Sorting:** The project uses a sorting key function for arranging pending tasks.
- **Conditional Statements:** Managing application operations and washing status.
- **Loops:** Displaying records and maintaining the main application menu.

## 📂 Project Structure

```text
Smart-Wardrobe-Organizer/
│
├── main.py
│
├── Wardrobe_Items.csv
│
├── Care_Tasks.csv
│
├── Outfit_Logs.csv
│
└── README.md
```

### CSV File Description

| File | Stored Information |
|---|---|
| Wardrobe_Items.csv | Item name, category, price, wears since wash, total wears |
| Care_Tasks.csv | Item name, task type, due date, task status |
| Outfit_Logs.csv | Item name, occasion, comfort rating, style rating |

The application automatically creates these CSV files with their respective headers when they do not already exist.

## ⚙️ Installation & Execution

**Prerequisites:**
- Python 3.x
- Any Python-supported code editor or terminal.

**Step 1: Clone the repository**

```bash
git clone YOUR_REPOSITORY_URL
```

**Step 2: Open the project directory**

```bash
cd Smart-Wardrobe-Organizer
```

**Step 3: Run the application**

```bash
python main.py
```

No external Python packages are required.

## 📋 Application Menu

The application provides the following operations:

| Option | Operation |
|---|---|
| 1 | Daily Style Dashboard |
| 2 | Add New Wardrobe Item |
| 3 | Log Outfit Wear / Wash |
| 4 | Wardrobe Usage & Laundry Report |
| 5 | Schedule Care / Repair Task |
| 6 | View Pending Care Tasks |
| 7 | Mark Care Task as Completed |
| 8 | Log Outfit Comfort & Style Rating |
| 9 | View All Outfit Ratings |
| 10 | View Wardrobe Satisfaction Index |
| 11 | Item Deep Dive |
| 0 | Exit Application |

## 🎯 Project Objective

The main objective of this project is to apply Python programming concepts and data structures to a practical wardrobe management problem. It provides a systematic approach to tracking clothing usage, washing schedules, maintenance activities, clothing expenses, and outfit satisfaction.

## 👩‍💻 Project Details

- **Project Name:** Smart Wardrobe Organizer
- **Programming Language:** Python
- **Project Domain:** Data Structures & Python Programming
- **Application Type:** Menu-Driven CLI Application
- **Data Storage:** CSV Files

---

**If you find this project useful, consider giving the repository a ⭐!**
