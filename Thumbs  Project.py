from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

def adicionar_texto_na_imagem(imagem_caminho, texto, numero, fonte_caminho, tamanho_fonte_texto, tamanho_fonte_numero, cor_texto, cor_sombra, salvar_como):
    # abrir a imagem
    imagem = Image.open(imagem_caminho).convert('RGBA')
    largura_imagem, altura_imagem = imagem.size
    
    # criar uma imagem separada para a sombra
    sombra = Image.new('RGBA', imagem.size, (0, 0, 0, 0))
    desenho_sombra = ImageDraw.Draw(sombra)
    
    # carregar fontes
    fonte_texto = ImageFont.truetype(fonte_caminho, tamanho_fonte_texto)
    fonte_numero = ImageFont.truetype(fonte_caminho, tamanho_fonte_numero)
    
    # calcular a caixa delimitadora (bbox) do texto
    bbox_texto = desenho_sombra.textbbox((0, 0), texto, font=fonte_texto)
    largura_texto = bbox_texto[2] - bbox_texto[0]
    altura_texto = bbox_texto[3] - bbox_texto[1]
    
    # calcular a caixa delimitadora (bbox) do número
    bbox_numero = desenho_sombra.textbbox((0, 0), numero, font=fonte_numero)
    largura_numero = bbox_numero[2] - bbox_numero[0]
    altura_numero = bbox_numero[3] - bbox_numero[1]
    
    # calcular a posição centralizada para o texto
    posicao_texto = ((largura_imagem - largura_texto) / 2, (altura_imagem - (altura_texto + altura_numero)) / 2)
    posicao_numero = ((largura_imagem - largura_numero) / 2, posicao_texto[1] + altura_texto)
    
    # desenhar a sombra do texto
    deslocamento_sombra = 5
    posicao_sombra_texto = (posicao_texto[0] + deslocamento_sombra, posicao_texto[1] + deslocamento_sombra)
    posicao_sombra_numero = (posicao_numero[0] + deslocamento_sombra, posicao_numero[1] + deslocamento_sombra)
    
    desenho_sombra.text(posicao_sombra_texto, texto, font=fonte_texto, fill=cor_sombra)
    desenho_sombra.text(posicao_sombra_numero, numero, font=fonte_numero, fill=cor_sombra)
    
    # aplicar desfoque à sombra
    sombra = sombra.filter(ImageFilter.GaussianBlur(radius=5))
    
    # compor a sombra desfocada na imagem original
    imagem = Image.alpha_composite(imagem, sombra)
    
    # inicializar o ImageDraw para a imagem final
    desenho_final = ImageDraw.Draw(imagem)
    
    # adicionar texto principal
    desenho_final.text(posicao_texto, texto, font=fonte_texto, fill=cor_texto)
    
    # adicionar número principal
    desenho_final.text(posicao_numero, numero, font=fonte_numero, fill=cor_texto)
    
    # salvar a imagem com o texto adicionado
    imagem.save(salvar_como)
    print(f'Imagem salva como {salvar_como}')

# pegar o diretório do script atual
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# configurações
imagem_caminho = os.path.join(diretorio_atual, 'nome_da_img.png')  # Caminho da imagem a ser carregada
fonte_caminho = os.path.join(diretorio_atual, 'comic_sans.ttf')  # Caminho da fonte TrueType (.ttf)
tamanho_fonte_texto = 144  # Tamanho da fonte para o texto principal
tamanho_fonte_numero = 144  # Tamanho da fonte para o número
cor_texto = (255, 255, 255)  # Cor do texto (em RGB)
cor_sombra = (0, 0, 0, 255)  # Cor da sombra (em RGBA)

for i in range(1, 3):
    texto = 'Série'
    numero = f'#{i}'
    salvar_como = os.path.join(diretorio_atual, f'Thumb{i}.png')
    adicionar_texto_na_imagem(imagem_caminho, texto, numero, fonte_caminho, tamanho_fonte_texto, tamanho_fonte_numero, cor_texto, cor_sombra, salvar_como)
