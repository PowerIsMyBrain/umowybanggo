from fpdf import FPDF
def generate_contract_pdf(data):
    pdf = FPDF()
    pdf.add_page()

    path_to_font = "static/fonts/DejaVuSans.ttf"
    pdf.add_font("DejaVu", "", path_to_font, uni=True)
    pdf.set_font("DejaVu", size=12)

    # Nagłówek dokumentu - wyrównany do środka
    pdf.set_xy(100, 10)  # Ustawienie pozycji na środku strony (przy założeniu szerokości strony 200)
    pdf.cell(100, 10, "Umowa", align='C')

    # Standardowe dane - wyrównane do lewej
    pdf.ln(20)  # Przesunięcie w dół o 20 jednostek
    pdf.cell(200, 10, f"Data umowy: {data['data_umowy']}")
    pdf.cell(200, 10, f"Miejsce zawarcia umowy: {data['miejsce_umowy']}")

    # Paragrafy - zdefiniowana szerokość i wyrównanie do lewej
    for paragraf in data['paragrafy']:
        pdf.set_xy(10, pdf.get_y() + 10)  # Resetowanie pozycji x do lewego marginesu i przesunięcie w dół
        pdf.cell(200, 10, paragraf['tytul'], align='C')
        pdf.cell(190, 10, paragraf['tresc'], align='L')  # Ustaw szerokość na 190, aby zapewnić margines

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
