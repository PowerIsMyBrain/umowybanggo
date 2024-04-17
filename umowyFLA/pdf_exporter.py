from fpdf import FPDF, XPos, YPos

def generate_contract_pdf(data):
    pdf = FPDF()
    pdf.add_page()

    path_to_font = "static/fonts/DejaVuSans.ttf"
    pdf.add_font("DejaVu", "", path_to_font)
    pdf.set_font("DejaVu", size=12)

    # Nagłówek dokumentu - wyrównany do środka
    pdf.cell(200, 10, text="Umowa", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    # Standardowe dane - wyrównane do lewej
    pdf.cell(200, 10, text=f"Data umowy: {data['data_umowy']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(200, 10, text=f"Miejsce zawarcia umowy: {data['miejsce_umowy']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Paragrafy - zdefiniowana szerokość i wyrównanie do lewej
    for paragraf in data['paragrafy']:
        pdf.set_xy(10, pdf.get_y())  # Resetowanie pozycji x do lewego marginesu
        pdf.cell(200, 10, text=paragraf['tytul'], new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        pdf.multi_cell(190, 10, text=paragraf['tresc'])  # Ustaw szerokość na 190, aby zapewnić margines

    # Zapisanie do pliku
    pdf.output("umowa.pdf")




if  __name__ == "__main__":
    # Przykładowe dane
    data = {
        'data_umowy': '2024-04-17',
        'miejsce_umowy': 'Warszawa',
        'paragrafy': [
            {'tytul': '§1 Warunki ogólne', 'tresc': 'Treść paragrafu 1 dotycząca warunków ogólnych umowy.'},
            {'tytul': '§2 Prawa i obowiązki', 'tresc': 'Treść paragrafu 2 dotycząca praw i obowiązków stron.'},
            {'tytul': '§3 Prawa i obowiązki', 'tresc': 'Treść paragrafu 3 dotycząca praw i obowiązków stron.'},
            {'tytul': '§4 Prawa i obowiązki', 'tresc': 'Treść paragrafu 4 dotycząca praw i obowiązków stron.'}
        ]
    }
    generate_contract_pdf(data)
