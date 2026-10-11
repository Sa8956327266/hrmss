from fpdf import FPDF

def generate_offer_letter(user):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Offer Letter", ln=True)
    pdf.cell(200, 10, txt=f"Name: {user['name']}", ln=True)
    pdf.cell(200, 10, txt=f"Department: {user['department']}", ln=True)
    pdf.cell(200, 10, txt(f"Designation: {user['designation']}"), ln=True)
    return pdf.output(dest="S").encode("latin1")

def generate_salary_slip(user, month, amount):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Salary Slip", ln=True)
    pdf.cell(200, 10, txt=f"Name: {user['name']}", ln=True)
    pdf.cell(200, 10, txt=f"Month: {month}", ln=True)
    pdf.cell(200, 10, txt=f"Amount: {amount}", ln=True)
    return pdf.output(dest="S").encode("latin1")
