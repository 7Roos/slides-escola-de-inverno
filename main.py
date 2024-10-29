from manim import *  # or: from manimlib import *
from manim_slides import Slide
from pathlib import Path
import os
from manim import AS2700  # Padrão australiano de cores
from manim import X11

# Create animations
# manim presentation.py
# Flags:
# -q  quality: low(l), medium(m) and high(h),e.g, ql low quality

# Convert to html
# manim-slides convert BasicExample slides.html

# --flush_cache                  Remove cached partial movie files

FLAGS = f"-qh"
SCENE = "Cover"
CLEAN = "--flush_cache "

########### Change background ###########
# config.background_color = X11.BEIGE


class Cover(Slide):
    def update_canvas(self):
        self.counter += 1
        old_slide_number = self.canvas["slide_number"]
        new_slide_number = Text(
            f"{self.counter}/{self.TOTAL_SLIDES}",
            font_size=25,
            color=AS2700.R64_DEEP_INDIAN_RED,
        ).move_to(old_slide_number)
        self.play(Transform(old_slide_number, new_slide_number))

    def caption(self, figure, label):
        self.counter_fig += 1
        fig_name = Text(
            f"Fig. {self.counter_fig}{label}.",
            font_size=25,
            font="Open Sans",
            color=AS2700.N61_BLACK,
        ).next_to(figure, DOWN)
        # self.add(fig_name)
        return fig_name

    def number_of_eq(self, eq, shift=1):
        # Com o parâmetro aligned_edge=LEFT. a borda esquerda do número
        # ficará alinhada com a borda esquerda da equação.
        # Além disso, podemos ajustar a distância entre a equação e o
        # número utilizando o parâmetro buff, se não for informado pelo
        # usuário, assumirá o padrão, um.
        self.counter_eq += 1
        eq_name = Text(
            f"({self.counter_eq})",
            font_size=25,
            font="Latin Modern Math",
            color=AS2700.N61_BLACK,
        ).next_to(eq, RIGHT, buff=shift, aligned_edge=LEFT)
        return eq_name
        # self.add(eq_name)

    def cite(self, obj, author, title, year):
        """Adds a citation to the slide's reference dictionary."""
        self.counter_ref += 1
        self.references[self.counter_ref] = {
            "author": author,
            "title": title,
            "year": year,
            "object": obj,
        }

    def create_ref_group(self):
        """Creates a VGroup of footnotes for all references in the slide."""
        ref_group = VGroup()
        footnote_number_group = VGroup()
        for ref_num, ref_data in self.references.items():
            # Há alguns problemas ainda com a numeração.
            # Para o BulletedList não está funcionando de forma adequada
            # o número não está superescrito.
            footnote_number = (
                (
                    Text(
                        f"{ref_num}",
                        font_size=20,
                        font="Latin Modern Math",
                        color=BLACK,
                    )
                )
                .next_to(ref_data["object"], RIGHT)
                .shift(0.36 * LEFT + 0.12 * UP)
            )
            footnote_text = f"{ref_num}. {ref_data['author']} ({ref_data['year']})."
            footnote = Text(
                footnote_text,
                font_size=18,
                font="Latin Modern Mono",
                color=AS2700.N64_DARK_GREY,
            )
            footnote_number_group.add(VGroup(footnote_number))
            ref_group.add(VGroup(footnote).arrange(RIGHT))
        ref_group.arrange(DOWN, aligned_edge=LEFT).to_corner(DOWN + LEFT)
        return ref_group

    def add_reference(self, ref_text, index):
        """A função add_reference recebe o VGroup e um índice,
        e adiciona o elemento correspondente à cena"""
        self.add(ref_text[index])

    def initialize_counters(self):
        self.counter = 0
        self.counter_fig = 0
        self.counter_eq = 0
        self.counter_ref = 0
        self.references = {}
        self.fig_group = VGroup()
        self.TOTAL_SLIDES = 9

    def construct(self):
        ########### Change background ###########
        background = ImageMobject("background.png")  # instantiate the background image
        background.scale(1)  # scale it to fill the scene
        self.add(background)
        self.wait()

        self.initialize_counters()

        ########### Cover ###########
        title = VGroup(
            Text(
                "MODELO DE ISING NA REDE QUADRADA",
                color=AS2700.B11_RICH_BLUE,
                font="GFS Complutum",
                weight=BOLD,
                font_size=45,
            ),
            Text(
                "BICAMADA COM INTERAÇÃO ENTRE ",
                color=AS2700.B11_RICH_BLUE,
                font="GFS Complutum",
                weight=BOLD,
                font_size=45,
            ),
            Text(
                "PLANOS FRUSTRADA",
                color=AS2700.B11_RICH_BLUE,
                font="GFS Complutum",
                weight=BOLD,
                font_size=45,
            ),
        ).arrange(DOWN)

        logo = SVGMobject("./media/images/LogoFull_color.svg")

        author = Text(
            "Matheus Roos",
            color=AS2700.B11_RICH_BLUE,
            slant=ITALIC,
            font="Gentium",
            font_size=60,
        )
        orientador = Text(
            "Prof. Dr. Mateus Schmidt",
            color=AS2700.B11_RICH_BLUE,
            slant=ITALIC,
            font="Gentium",
            font_size=60,
        )
        advisor = VGroup(author, orientador).arrange(direction=DOWN).scale(0.5)

        cover = VGroup(title, logo, advisor).arrange(direction=DOWN, buff=1)
        self.add(cover)
        self.wait()

        ########### Contents ###########
        outiline_title = Text(
            "Visão geral",
            font="GFS Complutum",
            weight=BOLD,
            font_size=48,
            color=AS2700.B11_RICH_BLUE,
        )
        outiline_title.to_edge(UP)
        self.add(title)

        outiline = (
            BulletedList(
                "Introdução",
                "Metodologia",
                "Resultados",
                "Conclusão",
                buff=0.25,
                dot_scale_factor=2,
                font_size=50,
            )
            .set_color(X11.DARKORANGE4)
            .to_corner(UL)
            .shift(DOWN)
        )

        self.next_slide()
        self.counter = 2
        slide_number = (
            Text(
                f"2/{self.TOTAL_SLIDES}", font_size=25, color=AS2700.R64_DEEP_INDIAN_RED
            )
            .to_corner(DR)
            .shift(0.3 * DR)
        )
        self.add_to_canvas(slide_number=slide_number)
        self.add(slide_number)

        self.wipe(VGroup(title, logo, advisor), VGroup(outiline_title, outiline))
        self.wait(2)

        ########### Intro ###########
        title = Text(
            "INTRODUÇÃO",
            color=AS2700.B11_RICH_BLUE,
            font="GFS Complutum",
            weight=BOLD,
        ).to_edge(UL)
        intro = (
            BulletedList(
                "Dispositivos magnéticos [1];",  # memória magnética
                "Fases magnéticas e frustração;",  # geometrias de redes
                "Transições de fase [2];",  # água
                "Assinaturas de criticalidade quântica [3];",  # QAC
                "Modelo de Ising com campo transverso.",  # simples c/insights valiosos
                buff=0.25,
                dot_scale_factor=2,
                font_size=40,
            )
            .set_color(AS2700.G12_HOLLY)
            .to_corner(LEFT)
            .shift(0.1 * LEFT)
        )

        self.next_slide()
        self.wipe(Group(outiline_title, outiline), title)

        self.cite(
            intro[0],
            "T. Kaneyoshi",
            "A transverse Ising bilayer film with an antiferromagnetic...",
            "2015",
        )

        self.cite(intro[2], "M. Vojta", "Quantum phase transitions", "2003")

        self.cite(
            intro[3],
            "N. Kellermann, M. Schmidt",
            "Quantum Ising model on the frustrated...",
            "2019",
        )
        foot_text = self.create_ref_group()

        self.add_reference(foot_text, 0)

        chip = ImageMobject("./media/images/chip").scale(0.14).to_edge(RIGHT)
        caption_chip = self.caption(chip, "")
        self.add(
            intro[0],
            chip,
            caption_chip,
        )

        self.update_canvas()
        self.wait()

        self.next_slide()
        composto = ImageMobject("./media/images/FePS3.png").scale(1.5).to_corner(RIGHT)
        caption_composto = self.caption(composto, ": (Jae-Ung Lee et.al., 2016)")
        self.add(intro[1])
        self.wipe(
            Group(chip, caption_chip),
            Group(composto, caption_composto),
            direction=UP,
        )
        poly_2 = (
            RegularPolygon(n=6, start_angle=30 * DEGREES, color=RED)
            .scale(0.69)
            .move_to(composto)
            .shift(1.4 * LEFT + 0.7 * UP)
        )
        self.add(poly_2)
        self.wait()
        poly_2.set_fill(color=RED, opacity=0.4)
        self.wait()

        self.next_slide()

        # Caption subfigures
        label_hex = Text(
            "(c) Hexagonal.",
            font="Latin Modern Math",
            font_size=25,
            color=AS2700.N61_BLACK,
        )
        label_triangle = Text(
            "(b) Triangular.",
            font="Latin Modern Math",
            font_size=25,
            color=AS2700.N61_BLACK,
        )
        label_square = Text(
            "(a) Quadrada.",
            font="Latin Modern Math",
            font_size=25,
            color=AS2700.N61_BLACK,
        )

        # Organiza os captions das subfiguras em grid 2x2
        lattices_line1 = VGroup(label_square, label_triangle).arrange(RIGHT, buff=1)
        label_hex.next_to(lattices_line1[0], 9 * DOWN)

        # Cria a legenda dos spins
        legend = VGroup()
        spin_up = Circle(radius=0.15, color=BLACK, fill_opacity=1)
        spin_down = Circle(radius=0.15, color=AS2700.X13_MARIGOLD, fill_opacity=1)
        spins = VGroup(spin_up, spin_down).arrange(DOWN, buff=0.5)
        label_up = MathTex("+1/2", font_size=25, color=AS2700.N61_BLACK).next_to(
            spins[0], RIGHT
        )
        label_down = MathTex("-1/2", font_size=25, color=AS2700.N61_BLACK).next_to(
            spins[1], RIGHT
        )
        legend.add(spins, label_up, label_down).next_to(lattices_line1[1], 2.8 * DOWN)

        lattice = VGroup(lattices_line1, label_hex, legend)
        lattice.to_edge(RIGHT).shift(UP)
        caption_lattice = self.caption(lattice, ": Algumas geometrias")

        # Create hexagon
        hexagon = (
            RegularPolygon(n=6, start_angle=30 * DEGREES, color=AS2700.G13_EMERALD)
            .scale(0.8)
            .next_to(lattice[1], UP)
        )

        # Cria uma lista para armazenar os spins (círculos)
        spins_hex = VGroup()

        # Itera sobre os vértices do hexágono e cria um círculo em cada um
        for vertex in hexagon.get_vertices():
            spin = Circle(radius=0.15, color=BLACK, fill_opacity=1)
            spin.move_to(vertex)
            spins_hex.add(spin)

        # Faz o procedimento análogo para a estrutura triangular
        triangle = (
            RegularPolygon(n=3, color=AS2700.G13_EMERALD)
            .scale(0.8)
            .next_to(lattices_line1[1], UP)
        )
        spins_triangle = VGroup()
        # Itera sobre os vértices do triângulo e cria um círculo em cada um
        for vertex in triangle.get_vertices():
            spin = Circle(radius=0.15, color=BLACK, fill_opacity=1)
            spin.move_to(vertex)
            spins_triangle.add(spin)

        # E por fim, cria a última estrutura, a geometria quadrada.
        square = (
            RegularPolygon(n=4, start_angle=45 * DEGREES, color=AS2700.G13_EMERALD)
            .scale(0.8)
            .next_to(lattices_line1[0], UP)
        )
        spins_square = VGroup()
        # Itera sobre os vértices do quadrado e cria um círculo em cada um
        for vertex in square.get_vertices():
            spin = Circle(radius=0.15, color=BLACK, fill_opacity=1)
            spin.move_to(vertex)
            spins_square.add(spin)

        # Adiciona geometrias de rede à cena.
        self.wipe(
            Group(composto, poly_2, caption_composto),
            Group(
                square,
                spins_square,
                triangle,
                spins_triangle,
                hexagon,
                spins_hex,
                lattice[0:2],
            ),
            direction=UP,
        )
        self.wait()

        # Fase FE, todos os spins estão alinhados.
        ferromagnetic = Text(
            "Ferromagnética (FE)",
            font="Liberation Sans",
            weight=BOLD,
            font_size=25,
            color=AS2700.G13_EMERALD,
        ).shift(2 * DL + UP)
        self.play(FadeIn(ferromagnetic), FadeIn(caption_lattice), run_time=0.5)
        self.wait()

        # Fase AF, os spins serão alternados.
        self.next_slide()
        antiferromagnetic = Text(
            "Antiferromagnética (AF)",
            font="Liberation Sans",
            weight=BOLD,
            font_size=30,
            color=AS2700.G13_EMERALD,
        ).move_to(ferromagnetic)
        self.play(Transform(ferromagnetic, antiferromagnetic))

        self.add(legend, label_up, label_down)

        # Animação de mudança de cor
        for i in range(0, len(spins_hex), 2):
            if i < 4:
                self.play(
                    spins_hex[i].animate.set_color(AS2700.X13_MARIGOLD),
                    spins_square[i].animate.set_color(AS2700.X13_MARIGOLD),
                    spins_triangle[i].animate.set_color(AS2700.X13_MARIGOLD),
                    run_time=0.5,
                    rate_func=smooth,
                )
            else:
                self.play(spins_hex[i].animate.set_color(AS2700.X13_MARIGOLD))
        self.wait()

        self.remove(ferromagnetic)

        
        ### Transição de fase
        phaseTransitionClassification = (
            ImageMobject("./media/images/phaseTransitionClassification")
            .scale(0.3)
            .to_corner(RIGHT)
        )
        caption_phaseTransitionClassification = self.caption(
            phaseTransitionClassification, ": (M. Roos, 2023)"
        )

        self.next_slide()

        self.add(intro[2])
        self.wipe(
            Group(
                lattice,
                square,
                spins_square,
                triangle,
                spins_triangle,
                hexagon,
                spins_hex,
                legend,
                caption_lattice,
            ),
            Group(phaseTransitionClassification, caption_phaseTransitionClassification),
            direction=UP,
        )
        self.add_reference(foot_text, 1)
        self.wait()
        
        self.next_slide()
        gapOrderParameters = (
            ImageMobject("./media/images/SaltoParametroDeOrdem_Black")
            .scale(0.3)
            .to_corner(RIGHT)
        )
        caption_gapOrderParameters = self.caption(
            gapOrderParameters, ": (M. Roos, 2023)"
        )
        self.wipe(
            Group(phaseTransitionClassification, caption_phaseTransitionClassification),
            Group(gapOrderParameters, caption_gapOrderParameters),
            direction=UP,
        )
        self.wait()
        ######

        

        quantumTransition = (
            ImageMobject("./media/images/QuantumTransition.png")
            .scale(0.17)
            .to_edge(RIGHT)
        )
        caption_quantumTransition = self.caption(quantumTransition, ": (M. Roos, 2023)")
        self.next_slide()
        self.add(intro[3])
        self.wipe(
            Group(gapOrderParameters, caption_gapOrderParameters),
            Group(quantumTransition, caption_quantumTransition),
            direction=UP,
        )
        self.add_reference(foot_text, 2)
        self.wait()

        self.next_slide()
        self.add(intro[4])
        self.play(
            quantumTransition.animate.shift(8 * RIGHT),
            caption_quantumTransition.animate.shift(8 * RIGHT),
        )
        self.wait()

        ########### Metodologia: modelo ###########
        title2 = Text(
            "METODOLOGIA",
            color=AS2700.B11_RICH_BLUE,
            font="GFS Complutum",
            weight=BOLD,
            font_size=40,
        ).to_corner(UL)

        self.next_slide()
        self.remove(foot_text[0], foot_text[1], foot_text[2])
        self.wipe(Group(title, intro), title2, direction=LEFT)
        self.update_canvas()

        model = Text(
            "Modelo",
            color=AS2700.B11_RICH_BLUE,
            font="GFS Complutum",
            weight=BOLD,
            font_size=35,
        ).to_corner(UL)
        title2.to_corner(UL)
        self.play(Transform(title2, model))

        hamilton = MathTex(
            "\\mathcal{H} &= \\sum_{(ij)}J_{ij}\\sigma_{i}^{z}\\sigma_{j}^{z} - \\Gamma\\sum_{i}\\sigma_{i}^{x} \\\\",
            "\\sum_{(ij)}J_{ij}\\sigma_{i}^{z}\\sigma_{j}^{z} &= ",
            "J_{1}\\sum_{\\langle ij \\rangle}\\sigma_{i}^{z}\\sigma_{j}^{z} +",
            "J_{x}\\sum_{\\langle\\langle ij \\rangle\\rangle}\\sigma_{i}^{z}\\sigma_{j}^{z} +",
            "J_{p}\\sum_{( ij )'}\\sigma_{i}^{z}\\sigma_{j}^{z}.",
            font_size=25,
            color=AS2700.N61_BLACK,
        )
        partition_func = MathTex(
            "Z = \\mathrm{Tr} \\ e^{-\\beta \\mathcal{H}} \\hspace{1cm} \\text{e} \\hspace{1cm} f = -k_{B}T \\ln Z.",
            color=AS2700.N61_BLACK,
            font_size=25,
        )
        mag = MathTex(
            "m_{i}^{\\alpha} = \\langle \\sigma^{\\alpha}_{i} \\rangle =",
            "\\mathrm{Tr} \\ \\sigma_{i}^{\\alpha} e^{-\\beta \\mathcal{H}} / Z.",
            color=AS2700.N61_BLACK,
            font_size=25,
        )

        eqs = (
            VGroup(hamilton, partition_func, mag)
            .arrange(DOWN, buff=0.5)
            .to_edge(LEFT)
            .shift(1 * UP)
        )

        labels = VGroup()
        for i in range(len(eqs)):
            label = self.number_of_eq(eqs[i], 4)
            labels.add(label)

        lattice = SVGMobject("./media/images/lattice.svg")
        lattice.scale(1.15).to_edge(DL).shift(0.2 * UP)
        caption_lattice = self.caption(lattice, ": Configurações de spins")

        self.play(Write(eqs[0]), FadeIn(labels[0]))
        self.wait()
        self.play(Write(lattice), FadeIn(caption_lattice))
        self.wait()

        for i in (1, 2):
            self.next_slide()
            self.play(Write(eqs[i]), FadeIn(labels[i]))
            self.wait()

        groundStateDiagram = SVGMobject("./media/images/GroundState.svg")
        groundStateDiagram.scale(1.6).to_edge(RIGHT).shift(0.5 * UP)
        caption_groundStateDiagram = self.caption(groundStateDiagram, ": T=0")

        self.next_slide()
        self.play(Write(groundStateDiagram), FadeIn(caption_groundStateDiagram))
        self.wait()

        ########### Metodologia: método ###########
        method = (
            Text(
                "MÉTODO:",
                color=AS2700.B11_RICH_BLUE,
                font="GFS Complutum",
                weight=BOLD,
                font_size=35,
            )
            .to_corner(UL)
            .shift(0.2 * UP)
        )
        cmf = (
            Text(
                "cluster mean field (CMF)",
                color=AS2700.B11_RICH_BLUE,
                font="Liberation Sans",
                weight=BOLD,
                font_size=30,
            )
            .next_to(method, RIGHT)
            .shift(0.1 * DOWN)
        )

        self.next_slide()
        self.wipe(
            VGroup(
                title2,
                eqs,
                labels,
                lattice,
                caption_lattice,
                groundStateDiagram,
                caption_groundStateDiagram,
            ),
            VGroup(method, cmf),
            direction=DOWN,
        )
        self.update_canvas()

        # Equations
        h_CMF = MathTex(
            "\\mathcal{H} = \\mathcal{H}^{\\textrm{CMF}} =",
            "\\mathcal{H}_{\\text{intra}}(\\sigma^{z}_{i}) +",
            "\\mathcal{H}_{\\text{inter}}(\\sigma^{z}_{i}, m^{z}_{i}) -",
            "\\Gamma\\sum_{i}^{n_{s}} \\sigma^{x}_{i} \\text{ .}",
            font_size=25,
            color=AS2700.N61_BLACK,
        )
        h_intra = MathTex(
            "\\mathcal{H}_{intra} &= J_{1} \\left[ \\left( \\sigma_{1}^{z} + \\sigma_{4}^{z} \\right) \\left( \\sigma_{2}^{z} + \\sigma_{3}^{z} \\right) + \\left( \\sigma_{5}^{z} + \\sigma_{8}^{z} \\right) \\left( \\sigma_{6}^{z} + \\sigma_{7}^{z} \\right) \\right] \\\\",
            "& + J_{x} \\left[ \\left(\\sigma_{1}^{z} + \\sigma_{4}^{z} \\right)\\left( \\sigma_{6}^{z} + \\sigma_{7}^{z} \\right) + \\left( \\sigma_{2}^{z} + \\sigma_{3}^{z} \\right)\\left( \\sigma_{5}^{z} + \\sigma_{8}^{z} \\right) \\right] \\\\",
            "& + J_{p} \\left(\\sigma_{1}^{z}\\sigma_{5}^{z} + \\sigma_{2}^{z}\\sigma_{6}^{z} + \\sigma_{3}^{z}\\sigma_{7}^{z} + \\sigma_{4}^{z}\\sigma_{8}^{z} \\right) \\text{ .}",
            font_size=25,
            color=AS2700.N61_BLACK,
        )
        h_inter = MathTex(
            "\\mathcal{H}_{inter}^{AF_{1}} &= \\left( -2J_{1} + 2J_{x} \\right) \\left(\\sigma_{1}^{z} - \\sigma_{2}^{z} - \\sigma_{3}^{z} + \\sigma_{4}^{z} - \\sigma_{5}^{z} + \\sigma_{6}^{z} + \\sigma_{7}^{z} - \\sigma_{8}^{z} - 4 m_{1}\\right) m_{1} \\\\",
            "\\mathcal{H}_{inter}^{AF_{2}} &= \\left( -2J_{1} -2J_{x}\\right) \\left( \\sigma_{1}^{z}  -\\sigma_{2}^{z} - \\sigma_{3}^{z} + \\sigma_{4}^{z} + \\sigma_{5}^{z} - \\sigma_{6}^{z} - \\sigma_{7}^{z} + \\sigma_{8}^{z} - 4m_{1} \\right) m_{1} \\\\",
            "\\mathcal{H}_{inter}^{AF_{3}} &= \\left( 2J_{1} -2J_{x} \\right) \\left( \\sigma_{1}^{z} + \\sigma_{2}^{z} + \\sigma_{3}^{z} + \\sigma_{4}^{z} -\\sigma_{5}^{z} -\\sigma_{6}^{z} - \\sigma_{7}^{z} - \\sigma_{8}^{z} - 4m_{1} \\right) m_{1} \\text{ .}",
            font_size=25,
            color=AS2700.N61_BLACK,
        )
        order_parameter_eq = MathTex(
            "m_{AF_{\\mathrm{I}}} &= \\left(m_{1}^{z} -m_{2}^{z} -m_{3}^{z} + m_{4}^{z} -m_{5}^{z} + m_{6}^{z} + m_{7}^{z} -m_{8}^{z} \\right) / n_{s} \\\\",
            "m_{AF_{\\mathrm{II}}} &= \\left(m_{1}^{z} -m_{2}^{z} -m_{3}^{z} + m_{4}^{z} + m_{5}^{z} -m_{6}^{z} -m_{7}^{z} + m_{8}^{z} \\right) / n_{s} \\\\",
            "m_{AF_{\\mathrm{III}}} &= \\left(m_{1}^{z} + m_{2}^{z} + m_{3}^{z} + m_{4}^{z} - m_{5}^{z} - m_{6}^{z} - m_{7}^{z} - m_{8}^{z} \\right) / n_{s} \\text{ .}",
            font_size=25,
            color=AS2700.N61_BLACK,
        )
        h_eqs = VGroup(h_CMF, h_intra, h_inter, order_parameter_eq).arrange(
            DOWN, buff=0.75
        )

        # Labels
        labels = VGroup()
        for i in range(len(h_eqs)):
            label = self.number_of_eq(h_eqs[i], 4.5)
            labels.add(label)

        # Bullets
        IDENT = 4.4 * LEFT  # Identação
        h_CMF_bullet = Dot(color=AS2700.N61_BLACK).shift(3.2 * UP + IDENT)
        h_intra_bullet = Dot(color=AS2700.N61_BLACK).shift(2 * UP + IDENT)
        h_inter_bullet = Dot(color=AS2700.N61_BLACK).shift(0.2 * UP + IDENT)
        order_param_bullet = Dot(color=AS2700.N61_BLACK).shift(1.7 * DOWN + IDENT)
        bullets = VGroup(
            h_CMF_bullet, h_intra_bullet, h_inter_bullet, order_param_bullet
        )

        # Texts
        h_CMF_text = (
            VGroup(
                Text(
                    "Cluster cúbico de ",
                    font="Latin Modern Math",
                    font_size=25,
                ),
                MathTex("n_{s} = 8", font_size=30),
                Text(" sítios:", font="Latin Modern Math", font_size=25),
            )
            .arrange(RIGHT, buff=0.1)
            .set_color_by_gradient(
                AS2700.R11_INTERNATIONAL_ORANGE, AS2700.G11_BOTTLE_GREEN
            )
        )
        h_intra_text = Text(
            "Interações computadas exatamente:",
            font="Latin Modern Math",
            font_size=25,
            gradient=(AS2700.R11_INTERNATIONAL_ORANGE, AS2700.G11_BOTTLE_GREEN),
        )
        h_inter_text = Text(
            "Incorporam campo médio:",
            font="Latin Modern Math",
            font_size=25,
            gradient=(AS2700.R11_INTERNATIONAL_ORANGE, AS2700.G11_BOTTLE_GREEN),
        )

        order_parameter_text = Text(
            "Parâmetro de ordem:",
            font_size=25,
            gradient=(AS2700.R11_INTERNATIONAL_ORANGE, AS2700.G11_BOTTLE_GREEN),
        )
        texts = VGroup(h_CMF_text, h_intra_text, h_inter_text, order_parameter_text)

        # Itens
        itens = VGroup()
        for i in range(len(bullets)):
            texts[i].next_to(bullets[i], RIGHT)
            itens.add(VGroup(bullets[i], texts[i]))

        mean_field = (
            MathTex(
                "\\sigma^{z}_{i} \\sigma^{z}_{j} \\approx",
                "\\sigma^{z}_{i}m^{z}_{j} + ",
                "\\sigma^{z}_{j}m^{z}_{i} -",
                "m^{z}_{i} m^{z}_{j}.",
                font_size=25,
                color=AS2700.G13_EMERALD,
            )
            .next_to(texts[2], RIGHT)
            .shift(0.02 * DOWN)
        )

        eqs = (
            VGroup(
                h_eqs,
                labels,
                itens,
                mean_field,
            )
            .to_edge(LEFT)
            .shift(0.4 * LEFT + 0.5 * DOWN)
        )

        cluster = ImageMobject("./media/images/cluster.png").scale(0.24).to_edge(RIGHT)
        caption_cluster = self.caption(cluster, ": Cluster")

        self.add(itens[0])
        self.play(Write(h_eqs[0]), FadeIn(labels[0]))
        self.add(cluster, caption_cluster)
        cluster.shift(5 * RIGHT)
        caption_cluster.shift(5 * RIGHT)
        self.play(
            cluster.animate.shift(5 * LEFT),
            caption_cluster.animate.shift(5 * LEFT),
            rate_func=rate_functions.ease_out_sine,
        )
        # self.play()
        self.wait()

        self.next_slide()
        self.add(itens[1])
        self.play(Write(h_eqs[1]), FadeIn(labels[1]))
        self.wait()

        self.next_slide()
        self.add(itens[2])
        self.play(Write(mean_field))
        framebox = SurroundingRectangle(
            mean_field,
            buff=0.1,
            color=[AS2700.R11_INTERNATIONAL_ORANGE, AS2700.G11_BOTTLE_GREEN],
        )
        self.play(Write(framebox), Write(h_eqs[2]), FadeIn(labels[2]))
        self.wait()

        self.next_slide()
        self.add(itens[3])
        self.play(Write(h_eqs[3]), FadeIn(labels[3]))
        self.wait()

        ########### Results ###########
        result_title = Text(
            "RESULTADOS",
            color=AS2700.B11_RICH_BLUE,
            font="GFS Complutum",
            weight=BOLD,
            font_size=40,
        ).to_edge(UP)

        self.next_slide()
        self.update_canvas()
        self.wipe(
            Group(method, cmf, eqs, framebox, cluster, caption_cluster),
            result_title,
            direction=DOWN,
        )

        subtitle_bullet = Dot(color=AS2700.N61_BLACK).to_corner(UL).shift(DOWN)
        subtitle_text = (
            Text(
                "Diagramas de fase clássico: rede quadrada e hexagonal bicamada;",
                font="Latin Modern Math",
                font_size=31,
            )
            .set_color_by_gradient(AS2700.B11_RICH_BLUE, AS2700.N61_BLACK)
            .next_to(subtitle_bullet, RIGHT)
        )
        subtitle = VGroup(subtitle_bullet, subtitle_text).shift(0.1 * UP)
        self.add(subtitle)
        rossato_text = (
            Text(
                "Diagramas de fase clássico e quântico;",
                font="Latin Modern Math",
                font_size=35,
            )
            .set_color_by_gradient(AS2700.B11_RICH_BLUE, AS2700.N61_BLACK)
            .next_to(subtitle_bullet, RIGHT)
        )
        bullet2 = Dot(color=AS2700.N61_BLACK).next_to(subtitle_bullet, 1.2 * DOWN)
        rangeQAC = (
            MathTex(
                "\\text{QAC:} g_{Q}^{*} < g < g_{C}^{*}, i.e., 0.32 < J_{x} / J_{1} < 0.43.",
                font_size=35,
            )
            .set_color_by_gradient(AS2700.B11_RICH_BLUE, AS2700.N61_BLACK)
            .next_to(bullet2, RIGHT)
        )
        fluctuations = (
            Text(
                "Flutuações clássicas e quânticas;",
                font="Latin Modern Math",
                font_size=35,
            )
            .set_color_by_gradient(AS2700.B11_RICH_BLUE, AS2700.N61_BLACK)
            .next_to(subtitle_bullet, RIGHT)
        )
        qac_name = (
            Text(
                "Quantum annealed criticality;",
                font="Latin Modern Math",
                font_size=35,
            )
            .set_color_by_gradient(AS2700.B11_RICH_BLUE, AS2700.N61_BLACK)
            .next_to(subtitle_bullet, RIGHT)
        )

        # Portal
        line = Line(3 * DOWN, 1.5 * UP, color=[BLACK, ORANGE, BLACK])

        whiteboard_right = (
            Square(color=WHITE, fill_opacity=1)
            .scale(3)
            .next_to(line, RIGHT)
            .shift(0.2 * LEFT)
        )
        classicalPhaseDiagram_img = (
            SVGMobject("./media/images/classicalPhaseDiagram.svg")
            .scale(2.2)
            .move_to(whiteboard_right)
        )

        whiteboard_left = (
            Rectangle(width=6.67, height=4.57, color=WHITE, fill_opacity=1)
            .next_to(line, LEFT)
            .shift(0.25 * RIGHT)
        )
        quantumPhaseDiagram_img = (
            ImageMobject("./media/images/QuantumPhaseDiagram")
            .scale(0.155)
            .move_to(whiteboard_left)
            .shift(0.1 * UP)
        )
        rossatoDiagram = (
            ImageMobject("./media/images/rossatoDiagram")
            .scale(0.12)
            .move_to(whiteboard_left)
        )
        diagramG1 = (
            ImageMobject("./media/images/diagram_J1(0.5)G(1)")
            .scale(0.14)
            .move_to(whiteboard_left)
        )
        diagramG2 = (
            ImageMobject("./media/images/diagram_J1(0.5)G(2)")
            .scale(0.14)
            .move_to(whiteboard_left)
        )
        qac_05 = (
            ImageMobject("./media/images/QAC_J1(0.5)Jx(0.35)")
            .scale(0.14)
            .move_to(whiteboard_left)
        )
        qac_05.shift(7 * LEFT)

        self.add(quantumPhaseDiagram_img)
        self.add(rossatoDiagram)
        self.add(diagramG1)
        self.add(diagramG2)
        self.add(qac_05)
        self.add(whiteboard_left)
        self.add(line)

        self.add(classicalPhaseDiagram_img)
        self.add(whiteboard_right)
        self.wait()
        self.play(classicalPhaseDiagram_img.animate.shift(6.5 * LEFT))
        classical_label = self.caption(classicalPhaseDiagram_img, ": Clássico")

        self.add(classical_label)
        self.wait()

        self.next_slide()
        self.remove(whiteboard_right)
        self.play(
            rossatoDiagram.animate.shift(7 * RIGHT + 0.75 * DOWN),
        )
        rossato_label = self.caption(rossatoDiagram, ": (L. Rossato, et al., 2023)")
        self.add(rossato_label)
        self.wait()

        self.next_slide()
        self.play(
            rossatoDiagram.animate.shift(8 * RIGHT),
            rossato_label.animate.shift(8 * RIGHT),
            quantumPhaseDiagram_img.animate.shift(7 * RIGHT),
            Transform(subtitle_text, rossato_text),
            FadeIn(bullet2),
            FadeIn(rangeQAC),
        )
        quantum_label = self.caption(quantumPhaseDiagram_img, ": Quântico")
        self.add(quantum_label)
        self.update_canvas()
        self.wait()

        self.next_slide()
        self.play(
            quantumPhaseDiagram_img.animate.shift(7 * RIGHT),
            quantum_label.animate.shift(7 * RIGHT),
            diagramG1.animate.shift(7 * RIGHT),
            Transform(subtitle_text, fluctuations),
        )
        diagramG1_label = self.caption(diagramG1, ": Diagrama de fase")
        self.add(diagramG1_label)
        self.wait()

        self.next_slide()
        self.play(
            diagramG1.animate.shift(7 * RIGHT),
            diagramG1_label.animate.shift(7 * RIGHT),
            diagramG2.animate.shift(7 * RIGHT),
        )
        diagramG2_label = self.caption(diagramG2, ": Pontos críticos quânticos")
        self.add(diagramG2_label)
        self.wait()

        self.next_slide()
        self.play(
            classicalPhaseDiagram_img.animate.shift(7 * LEFT),
            classical_label.animate.shift(7 * LEFT),
        )
        self.remove(whiteboard_left)
        self.play(qac_05.animate.shift(7 * RIGHT), Transform(subtitle_text, qac_name))
        qac_label = self.caption(qac_05, ": QAC")
        self.add(qac_label)
        self.update_canvas()
        self.wait()

        ########### Conclusão ###########
        conclusion_title = Text(
            "CONCLUSÃO",
            color=AS2700.B11_RICH_BLUE,
            font="GFS Complutum",
            weight=BOLD,
            font_size=40,
        ).to_edge(UP)

        self.next_slide()
        self.update_canvas()
        self.wipe(
            Group(
                result_title,
                qac_05,
                qac_label,
                subtitle_text,
                diagramG2,
                diagramG2_label,
                line,
                bullet2,
                subtitle_bullet,
                rangeQAC,
            ),
            conclusion_title,
            direction=UP + RIGHT,
        )

        conclusion_itens = (
            BulletedList(
                "Frustração e a interação entre planos ("
                r"$J_{x}$"
                ") e o seu papel;",
                "Presença de um ponto tricrítico na transição "
                r"$\textrm{AF}_{2}-\textrm{PM}$"
                ";",
                "Fenômeno QAC;",
                "Investigar o comportamento de outras quantidades termodinâmicas.",
                font_size=40,
            )
            .set_color(AS2700.G13_EMERALD)
            .to_edge(LEFT)
        )

        self.add(conclusion_itens[0])
        self.wait()

        for i in range(1, len(conclusion_itens)):
            self.next_slide()
            self.add(conclusion_itens[i])
            self.wait()


if __name__ == "__main__":
    script_name = f"{Path(__file__).resolve()}"
    os.system(f"manim {script_name} {FLAGS} {SCENE}")
    os.system(f"manim-slides convert {SCENE} index.html")
