import csv
from io import StringIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_csv(expenses):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Category', 'Description', 'Amount', 'Currency'])
    
    for expense in expenses:
        writer.writerow([
            expense.date,
            expense.category.name if expense.category else 'Uncategorized',
            expense.description,
            expense.amount,
            expense.currency.code
        ])
    
    return output.getvalue()

def generate_pdf(expenses, user):
    buffer = StringIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Expense Report for {user.username}", styles['Heading1']))
    
    data = [['Date', 'Category', 'Description', 'Amount', 'Currency']]
    for expense in expenses:
        data.append([
            expense.date.strftime('%Y-%m-%d'),
            expense.category.name if expense.category else 'Uncategorized',
            expense.description,
            str(expense.amount),
            expense.currency.code
        ])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    return buffer.getvalue()
