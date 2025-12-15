import cairo

# --- Constantes du Projet ---

WIDTH, HEIGHT = 1366, 137
TEXT_TO_DISPLAY = "Angers"
# Taille de police augmentée pour étirer le mot sur la largeur
FONT_SIZE = HEIGHT * 0.9 


# --- Classe de Dessin des Segments (Dégradé de Fond) ---

class Segment:
    """
    Représente un segment horizontal (une ligne) de l'image.
    Utilisé pour générer un dégradé de noir (en haut) à blanc (en bas).
    """
    def __init__(self, h, total_height):
        """
        Initialise le segment à la hauteur 'h' (coordonnée Y).
        """
        # Dégradé de gris (Noir à Blanc) pour le fond
        gray_level = h / (total_height - 1)
        self.couleur = (gray_level, gray_level, gray_level)
        self.A = (0, h)
        self.B = (WIDTH, h)
        
    def trace(self, ctx):
        """
        Trace le segment coloré sur le contexte cairo.
        """
        ctx.save()
        ctx.set_source_rgb(*self.couleur)
        ctx.move_to(self.A[0], self.A[1])
        ctx.line_to(self.B[0], self.B[1])
        ctx.stroke()
        ctx.restore()


# --- Fonction de Dessin du Texte Étiré avec Dégradé Noir/Jaune ---

def draw_text_with_sco_gradient(ctx, text, width, height, font_size):
    """
    Dessine le texte "Angers" étiré avec un dégradé du SCO (Noir en haut, Jaune en bas).
    """
    # 1. Configuration de la police
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(font_size) 

    # 2. Mesure du texte pour le centrage
    extents = ctx.text_extents(text)
    
    # Coordonnée X de départ ajustée pour l'effet étiré (commence très à gauche)
    x_start = width * 0.02 
    # Coordonnée Y de départ pour le centrage vertical
    y_start = (height - extents[3]) / 2 - extents[1]

    # 3. Création du dégradé linéaire pour le texte (Noir en haut, Jaune en bas)
    
    # Les coordonnées Y sont basées sur la hauteur du texte pour que le dégradé soit centré sur le mot
    gradient = cairo.LinearGradient(0, y_start - extents[1], 0, y_start - extents[1] + extents[3])

    # Noir (couleur SCO) en haut (Y=0.0)
    gradient.add_color_stop_rgb(0.0, 0.0, 0.0, 0.0) 
    # Jaune (couleur SCO) en bas (Y=1.0)
    # Le jaune du SCO est souvent un jaune-doré, proche de (1.0, 0.84, 0.0)
    gradient.add_color_stop_rgb(1.0, 1.0, 0.84, 0.0)
    
    ctx.set_source(gradient)

    # 4. Dessin du texte
    ctx.move_to(x_start, y_start)
    ctx.show_text(text)


# --- Programme Principal (Génération de l'image) ---

# 1. Création de la surface et du contexte de dessin
img = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(img)

# 2. Application du dégradé de fond
for i in range(HEIGHT):
    Segment(i, HEIGHT).trace(ctx)

# 3. Ajout du texte "Angers" étiré avec dégradé Noir/Jaune
draw_text_with_sco_gradient(ctx, TEXT_TO_DISPLAY, WIDTH, HEIGHT, FONT_SIZE)

# 4. Sauvegarder l'image finale
img.write_to_png("tram_sco_angers.png")

print(f"Image 'tram_sco_angers.png' générée et sauvegardée avec
