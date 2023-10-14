from pypdf import PdfReader
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np

reader = PdfReader("resultado_klabin_2022.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()

conectivos = set(STOPWORDS)
conectivos.update(["da", "meu", "em", "e", "você", "de", "ao", "os", "na", "o", "4T21", "para", "milhões",
                  "resultado", "que", "nas", "dos", "n", "p", "4T22", "foi", "ano", "Klabin", "3T22", "resultados",
                  "trimestre"])

# Definindo cores mais vibrantes
def random_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return f"hsl({np.random.randint(0, 360)}, {np.random.randint(80, 100)}%, {np.random.randint(40, 70)}%)"

# Ajustando espaçamento e cores na WordCloud
nuvem_palavras = WordCloud(stopwords=conectivos, background_color="black", width=1920, height=1080,
                           contour_width=3, contour_color='white', color_func=random_color_func, margin=10).generate(text)

fig, ax = plt.subplots()

ax.imshow(nuvem_palavras, interpolation='bilinear')
ax.set_axis_off()
plt.show()