import fitz
doc = fitz.open(r'C:\Users\ToniF\Documents\Proyectos\proyectos-vscode\cv-raquel-orfila\data\otros\SobacirR2.pdf')
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=200)
    pix.save(rf'C:\Users\ToniF\Documents\Proyectos\proyectos-vscode\cv-raquel-orfila\data\otros\sobacirr2_page{i}.png')
    print(f'Saved page {i}')
