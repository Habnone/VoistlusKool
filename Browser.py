import sqlite3
import tkinter as tk
from tkinter import messagebox

# Connect to the database
conn = sqlite3.connect('cars.db')
cursor = conn.cursor()

def search_car(brand=None, model=None, year=None, max_price=None):
    # Construct the SQL query based on the provided parameters
    query = "SELECT * FROM cars WHERE 1=1"
    params = []

    if brand:
        query += " AND brand=?"
        params.append(brand)
    if model:
        query += " AND model=?"
        params.append(model)
    if year:
        query += " AND year=?"
        params.append(year)
    if max_price:
        query += " AND price <= ?"
        params.append(max_price)

    # Execute the query
    cursor.execute(query, tuple(params))
    cars = cursor.fetchall()
    
    return cars

def show_results():
    brand = brand_entry.get()
    model = model_entry.get()
    year = year_entry.get()
    max_price = max_price_entry.get()

    cars = search_car(brand=brand, model=model, year=year, max_price=max_price)

    if cars:
        result_text.delete('1.0', tk.END)
        for car in cars:
            # Display the car details in the results text box
            result_text.insert(tk.END, f"Brand: {car[2]}\n")
            result_text.insert(tk.END, f"Engine: {car[3]}\n")
            result_text.insert(tk.END, f"Mileage: {car[4]}\n")
            result_text.insert(tk.END, f"Fuel: {car[5]}\n")
            result_text.insert(tk.END, f"Model: {car[6]}\n")
            result_text.insert(tk.END, f"Transmission: {car[8]}\n")
            result_text.insert(tk.END, f"Year: {car[9]}\n")
            result_text.insert(tk.END, f"Bodytype: {car[10]}\n")
            result_text.insert(tk.END, f"Drive: {car[11]}\n")
            result_text.insert(tk.END, f"Price: {car[12]}\n\n")
    else:
        messagebox.showinfo("No Results", "No cars found matching the criteria.")

# Create the main window
root = tk.Tk()
root.title("Car Search")

# Create labels and entry fields for search parameters
brand_label = tk.Label(root, text="Brand:")
brand_label.grid(row=0, column=0, sticky="w")
brand_entry = tk.Entry(root)
brand_entry.grid(row=0, column=1)

model_label = tk.Label(root, text="Model:")
model_label.grid(row=1, column=0, sticky="w")
model_entry = tk.Entry(root)
model_entry.grid(row=1, column=1)

year_label = tk.Label(root, text="Year:")
year_label.grid(row=2, column=0, sticky="w")
year_entry = tk.Entry(root)
year_entry.grid(row=2, column=1)

max_price_label = tk.Label(root, text="Max Price:")
max_price_label.grid(row=3, column=0, sticky="w")
max_price_entry = tk.Entry(root)
max_price_entry.grid(row=3, column=1)

# Create a button to trigger the search
search_button = tk.Button(root, text="Search", command=show_results)
search_button.grid(row=4, columnspan=2)

# Create a text box to display search results
result_text = tk.Text(root, height=20, width=80)
result_text.grid(row=5, columnspan=2, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()

# Close the database connection
conn.close()
