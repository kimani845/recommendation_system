import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pandas as pd
from datetime import datetime
import os
from cake_sales_analysis import CakeSalesTracker, CAKE_TYPES, REGIONS

class CakeSalesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cake Sales Tracker")
        self.root.geometry("800x600")
        
        self.tracker = CakeSalesTracker()
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.sales_tab = ttk.Frame(self.notebook)
        self.predict_tab = ttk.Frame(self.notebook)
        self.analysis_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.sales_tab, text="Record Sales")
        self.notebook.add(self.predict_tab, text="Predictions")
        self.notebook.add(self.analysis_tab, text="Analysis")
        
        # Set up each tab
        self.setup_sales_tab()
        self.setup_predict_tab()
        self.setup_analysis_tab()
    
    def setup_sales_tab(self):
        """Set up the sales recording tab"""
        # Date selection
        date_frame = ttk.LabelFrame(self.sales_tab, text="Date")
        date_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(date_frame, text="Select Date:").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = DateEntry(date_frame, width=12, background='darkblue',
                                   foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Region selection
        ttk.Label(date_frame, text="Select Region:").grid(row=0, column=2, padx=5, pady=5)
        self.region_var = tk.StringVar()
        self.region_combo = ttk.Combobox(date_frame, textvariable=self.region_var, values=REGIONS)
        self.region_combo.grid(row=0, column=3, padx=5, pady=5)
        self.region_combo.current(0)
        
        # Cake sales entry
        sales_frame = ttk.LabelFrame(self.sales_tab, text="Cake Sales")
        sales_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create entry fields for each cake type
        self.cake_entries = {}
        for i, cake_type in enumerate(CAKE_TYPES):
            row = i // 2
            col = (i % 2) * 2
            
            ttk.Label(sales_frame, text=f"{cake_type}:").grid(row=row, column=col, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(sales_frame, width=10)
            entry.grid(row=row, column=col+1, padx=5, pady=5, sticky='w')
            entry.insert(0, "0")
            self.cake_entries[cake_type] = entry
        
        # Submit button
        submit_btn = ttk.Button(self.sales_tab, text="Record Sales", command=self.record_sales)
        submit_btn.pack(pady=10)
    
    def setup_predict_tab(self):
        """Set up the prediction tab"""
        # Date selection
        date_frame = ttk.LabelFrame(self.predict_tab, text="Prediction Date")
        date_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(date_frame, text="Select Date:").grid(row=0, column=0, padx=5, pady=5)
        self.pred_date_entry = DateEntry(date_frame, width=12, background='darkblue',
                                        foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.pred_date_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Region selection
        ttk.Label(date_frame, text="Select Region:").grid(row=0, column=2, padx=5, pady=5)
        self.pred_region_var = tk.StringVar()
        self.pred_region_combo = ttk.Combobox(date_frame, textvariable=self.pred_region_var, values=REGIONS)
        self.pred_region_combo.grid(row=0, column=3, padx=5, pady=5)
        self.pred_region_combo.current(0)
        
        # Prediction results
        results_frame = ttk.LabelFrame(self.predict_tab, text="Predicted Sales")
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create labels for each cake type
        self.pred_labels = {}
        for i, cake_type in enumerate(CAKE_TYPES):
            row = i // 2
            col = (i % 2) * 2
            
            ttk.Label(results_frame, text=f"{cake_type}:").grid(row=row, column=col, padx=5, pady=5, sticky='e')
            label = ttk.Label(results_frame, text="0")
            label.grid(row=row, column=col+1, padx=5, pady=5, sticky='w')
            self.pred_labels[cake_type] = label
        
        # Predict button
        predict_btn = ttk.Button(self.predict_tab, text="Generate Prediction", command=self.generate_prediction)
        predict_btn.pack(pady=10)
        
        # Train model button
        train_btn = ttk.Button(self.predict_tab, text="Train Model", command=self.train_model)
        train_btn.pack(pady=10)
    
    def setup_analysis_tab(self):
        """Set up the analysis tab"""
        # Analysis options
        options_frame = ttk.Frame(self.analysis_tab)
        options_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(options_frame, text="Update Summaries", command=self.update_summaries).pack(side='left', padx=5)
        ttk.Button(options_frame, text="Update Dashboard", command=self.update_dashboard).pack(side='left', padx=5)
        ttk.Button(options_frame, text="Open Excel File", command=self.open_excel).pack(side='left', padx=5)
        
        # Summary display
        summary_frame = ttk.LabelFrame(self.analysis_tab, text="Key Insights")
        summary_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.summary_text = tk.Text(summary_frame, wrap='word', height=20)
        self.summary_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Load initial summary
        self.load_summary()
    
    def record_sales(self):
        """Record sales data"""
        try:
            date = self.date_entry.get_date()
            region = self.region_var.get()
            
            if not region:
                messagebox.showerror("Error", "Please select a region")
                return
            
            # Get sales data
            sales_dict = {}
            for cake_type, entry in self.cake_entries.items():
                try:
                    sales = int(entry.get())
                    if sales < 0:
                        messagebox.showerror("Error", f"Sales for {cake_type} cannot be negative")
                        return
                    sales_dict[cake_type] = sales
                except ValueError:
                    messagebox.showerror("Error", f"Invalid sales value for {cake_type}")
                    return
            
            # Add sales data
            self.tracker.add_daily_sales(date, region, sales_dict)
            messagebox.showinfo("Success", f"Sales data recorded for {date.strftime('%Y-%m-%d')}")
            
            # Clear entries
            for entry in self.cake_entries.values():
                entry.delete(0, tk.END)
                entry.insert(0, "0")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def generate_prediction(self):
        """Generate sales prediction"""
        try:
            date = self.pred_date_entry.get_date()
            region = self.pred_region_var.get()
            
            if not region:
                messagebox.showerror("Error", "Please select a region")
                return
            
            # Generate prediction
            predictions = self.tracker.predict_next_day(date, region)
            
            if predictions:
                # Update labels
                for cake_type, label in self.pred_labels.items():
                    label.config(text=str(predictions.get(cake_type, 0)))
                
                # Add to Excel
                self.tracker.add_prediction_to_excel(date, region, predictions)
                messagebox.showinfo("Success", f"Prediction generated for {date.strftime('%Y-%m-%d')}")
            else:
                messagebox.showerror("Error", "Failed to generate prediction. Please train the model first.")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def train_model(self):
        """Train the prediction model"""
        try:
            self.tracker.train_prediction_model()
            messagebox.showinfo("Success", "Model trained successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_summaries(self):
        """Update summary sheets"""
        try:
            self.tracker.update_summaries()
            messagebox.showinfo("Success", "Summaries updated successfully")
            self.load_summary()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_dashboard(self):
        """Update dashboard"""
        try:
            self.tracker.update_dashboard()
            messagebox.showinfo("Success", "Dashboard updated successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def open_excel(self):
        """Open the Excel file"""
        try:
            os.startfile(self.tracker.excel_file)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def load_summary(self):
        """Load summary data into the text widget"""
        try:
            if not os.path.exists(self.tracker.excel_file):
                return
            
            self.summary_text.delete(1.0, tk.END)
            
            # Load data
            try:
                daily_data = pd.read_excel(self.tracker.excel_file, sheet_name='Daily Sales')
                dow_data = pd.read_excel(self.tracker.excel_file, sheet_name='Day of Week Analysis')
                region_data = pd.read_excel(self.tracker.excel_file, sheet_name='Regional Analysis')
                
                # Total sales
                total_sales = daily_data['Total Sales'].sum() if 'Total Sales' in daily_data.columns else 0
                self.summary_text.insert(tk.END, f"Total Sales: {total_sales}\n\n")
                
                # Best selling cake
                if len(CAKE_TYPES) > 0 and all(cake in daily_data.columns for cake in CAKE_TYPES):
                    cake_sales = {cake: daily_data[cake].sum() for cake in CAKE_TYPES}
                    best_cake = max(cake_sales.items(), key=lambda x: x[1])
                    self.summary_text.insert(tk.END, f"Best Selling Cake: {best_cake[0]} ({best_cake[1]} units)\n\n")
                
                # Best sales day
                if 'Day of Week' in dow_data.columns and 'Total Sales' in dow_data.columns:
                    best_day = dow_data.loc[dow_data['Total Sales'].idxmax()]
                    self.summary_text.insert(tk.END, f"Best Sales Day: {best_day['Day of Week']} ({best_day['Total Sales']} units)\n\n")
                
                # Best region
                if 'Region' in region_data.columns and 'Total Sales' in region_data.columns:
                    best_region = region_data.loc[region_data['Total Sales'].idxmax()]
                    self.summary_text.insert(tk.END, f"Best Region: {best_region['Region']} ({best_region['Total Sales']} units)\n\n")
                
                # Regional preferences
                if 'Region' in region_data.columns and all(cake in region_data.columns for cake in CAKE_TYPES):
                    self.summary_text.insert(tk.END, "Regional Preferences:\n")
                    for _, row in region_data.iterrows():
                        region = row['Region']
                        cake_sales = {cake: row[cake] for cake in CAKE_TYPES}
                        best_cake = max(cake_sales.items(), key=lambda x: x[1])
                        self.summary_text.insert(tk.END, f"  {region}: {best_cake[0]} ({best_cake[1]} units)\n")
                
            except Exception as e:
                self.summary_text.insert(tk.END, f"Error loading summary data: {e}")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = CakeSalesApp(root)
    root.mainloop()